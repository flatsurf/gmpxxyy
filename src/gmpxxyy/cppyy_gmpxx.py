# ********************************************************************
#  This file is part of gmpxxyy.
#
#        Copyright (C) 2019 Julian Rüth
#
#  gmpxxyy is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 2 of the License, or
#  (at your option) any later version.
#
#  gmpxxyy is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with gmpxxyy. If not, see <https://www.gnu.org/licenses/>.
# ********************************************************************

import cppyy

def is_primitive_gmp_type(name):
    r"""
    Return whether ``name`` is mpz_class, mpq_class, or mpf_class.

    EXAMPLES::

        >>> from gmpxxyy.cppyy_gmpxx import is_primitive_gmp_type
        >>> bool(is_primitive_gmp_type("__gmp_expr<__mpz_struct[1],__mpz_struct[1]>"))
        True
        >>> bool(is_primitive_gmp_type("__gmp_expr<__mpz_struct[1],__gmp_binary_expr<__gmp_expr<__mpz_struct[1],__mpz_struct[1]>,__gmp_expr<__mpz_struct[1],__mpz_struct[1]>,__gmp_binary_plus> >"))
        False

    """
    import re
    return re.match('__gmp_expr<__mp._struct\\[1\\],__mp._struct\\[1\\]>', name)

def enable_pretty_print(proxy, name):
    r"""
    Pretty print GMP types.

    EXAMPLES::

        >>> import gmpxxyy
        >>> import cppyy
        >>> cppyy.gbl.mpz_class(1)
        1

    """
    if is_primitive_gmp_type(name):
        proxy.__str__ = proxy.get_str
        proxy.__repr__ = proxy.get_str

cppyy.py.add_pythonization(enable_pretty_print)

def enable_pickling(proxy, name):
    r"""
    Pickle GMP types.

    EXAMPLES::

        >>> from pickle import dumps, loads
        >>> from gmpxxyy import mpz
        >>> a = mpz(1)
        >>> loads(dumps(a)) == a
        True

    """
    def reduce(self):
        return (type(self), (str(self),))

    if is_primitive_gmp_type(name):
        proxy.__reduce__ = reduce

cppyy.py.add_pythonization(enable_pickling)

def enable_arithmetic(proxy, name):
    r"""
    The C++ operators implemented by GMP do not return values but expressions
    that are then optimized away by the compiler.

    While this works in cppyy, it creates some trouble since these expressions
    do not explicitly keep their operands alive. So, we opt out of this and
    just evaluate everything immediately.

    EXAMPLES::

        >>> from gmpxxyy import mpz
        >>> mpz(1) - mpz(3)
        -2

    """
    if is_primitive_gmp_type(name):
        proxy.__add__ = lambda lhs, rhs: cppyy.gbl.gmpxxyy.add[proxy, type(rhs)](lhs, rhs)
        proxy.__radd__ = lambda rhs, lhs: cppyy.gbl.gmpxxyy.radd[type(rhs), proxy](lhs, rhs)
        proxy.__sub__ = lambda lhs, rhs: cppyy.gbl.gmpxxyy.sub[proxy, type(rhs)](lhs, rhs)
        proxy.__rsub__ = lambda rhs, lhs: cppyy.gbl.gmpxxyy.rsub[type(rhs), proxy](lhs, rhs)
        proxy.__mul__ = lambda lhs, rhs: cppyy.gbl.gmpxxyy.mul[proxy, type(rhs)](lhs, rhs)
        proxy.__rmul__ = lambda rhs, lhs: cppyy.gbl.gmpxxyy.rmul[type(rhs), proxy](lhs, rhs)
        proxy.__truediv__ = lambda lhs, rhs: cppyy.gbl.gmpxxyy.div[proxy, type(rhs)](lhs, rhs)
        proxy.__rtruediv__ = lambda rhs, lhs: cppyy.gbl.gmpxxyy.rdiv[type(rhs), proxy](lhs, rhs)
        proxy.__neg__ = cppyy.gbl.gmpxxyy.neg[proxy]

cppyy.py.add_pythonization(enable_arithmetic)

# We need the GMP headers (with C++) to be around. We could ship them with this
# Python library but then we would have to hope that the libgmpxx.so is
# compatible. Most likely it is but it doesn't feel right to me.
cppyy.load_library("gmp")
cppyy.load_library("gmpxx")
cppyy.include("gmpxx.h")
cppyy.cppdef("""
namespace gmpxxyy {
template <typename T, typename S> T add(const T& lhs, const S& rhs) { return lhs + rhs; }
template <typename T, typename S> S radd(const T& lhs, const S& rhs) { return lhs + rhs; }
template <typename T, typename S> T sub(const T& lhs, const S& rhs) { return lhs - rhs; }
template <typename T, typename S> S rsub(const T& lhs, const S& rhs) { return lhs - rhs; }
template <typename T, typename S> T mul(const T& lhs, const S& rhs) { return lhs * rhs; }
template <typename T, typename S> S rmul(const T& lhs, const S& rhs) { return lhs * rhs; }
template <typename T, typename S> T div(const T& lhs, const S& rhs) { return lhs / rhs; }
template <typename T, typename S> S rdiv(const T& lhs, const S& rhs) { return lhs / rhs; }
template <typename T> T neg(const T& lhs) { return static_cast<T>(-lhs); }
}
""")

mpz = cppyy.gbl.mpz_class
mpq = cppyy.gbl.mpq_class
mpf = cppyy.gbl.mpf_class
