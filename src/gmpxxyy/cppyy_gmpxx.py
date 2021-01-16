r"""
Pythonizations for GMP types

TESTS:

Operators work between primitive GMP types::

    >>> from gmpxxyy import mpz
    >>> x = mpz(0)
    >>> x < x
    False
    >>> x < x + 1
    True

"""
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

from cppyythonizations.operators.order import enable_total_order
from cppyythonizations.operators.arithmetic import enable_arithmetic, enable_neg
from cppyythonizations.util import filtered

def is_primitive_gmp_type(proxy, name):
    r"""
    Return whether ``name`` is mpz_class, mpq_class, or mpf_class.

    EXAMPLES::

        >>> from gmpxxyy.cppyy_gmpxx import is_primitive_gmp_type
        >>> bool(is_primitive_gmp_type(None, "__gmp_expr<__mpz_struct[1],__mpz_struct[1]>"))
        True
        >>> bool(is_primitive_gmp_type(None, "__gmp_expr<__mpz_struct[1],__gmp_binary_expr<__gmp_expr<__mpz_struct[1],__mpz_struct[1]>,__gmp_expr<__mpz_struct[1],__mpz_struct[1]>,__gmp_binary_plus> >"))
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
    proxy.__str__ = lambda self: str(self.get_str())
    proxy.__repr__ = lambda self: str(self.get_str())

cppyy.py.add_pythonization(filtered(is_primitive_gmp_type)(enable_pretty_print))

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

    proxy.__reduce__ = reduce

cppyy.py.add_pythonization(filtered(is_primitive_gmp_type)(enable_pickling))

def enable_gmp_arithmetic(proxy, name):
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
        >>> 1 + mpz(1)
        2
        >>> mpz(1) + 1
        2

    TESTS:

    Check that we allow operators that do not return a GMP type::

        >>> import cppyy
        >>> cppyy.cppdef('''
        ... class X{};
        ... std::string operator+(const X&, const mpz_class&) { return "plus"; }
        ... std::string operator+(const mpz_class&, const X&) { return "plus"; }
        ... ''')
        True
        >>> mpz(1) + cppyy.gbl.X()
        'plus'
        >>> cppyy.gbl.X() + mpz(1)
        'plus'

    """
    unwrap = lambda value: cppyy.gbl.gmpxxyy.maybe[proxy.__cpp_name__].cast(value)

    enable_arithmetic(proxy, name, unwrap)
    enable_neg(proxy, name, unwrap)

cppyy.py.add_pythonization(filtered(is_primitive_gmp_type)(enable_gmp_arithmetic))

def enable_float(proxy, name):
    r"""
    The C++ types implemented by GMP do not expose cast operators to double,
    therefore we need to manually expose that operator here.

    EXAMPLES::

        >>> from gmpxxyy import mpq
        >>> float(mpq(1, 3))
        0.3333333333333333

    """
    proxy.__float__ = lambda self: self.get_d()

cppyy.py.add_pythonization(filtered(is_primitive_gmp_type)(enable_float))

# We need the GMP headers (with C++) to be around. We could ship them with this
# Python library but then we would have to hope that the libgmpxx.so is
# compatible. Most likely it is but it doesn't feel right to me.
cppyy.load_library("gmp")
cppyy.load_library("gmpxx")
cppyy.include("gmpxx.h")
cppyy.cppdef("""
namespace gmpxxyy {
template <typename T>
struct maybe {
  template <typename S>
  static auto cast(const S& s) {
    if constexpr(std::is_convertible_v<S, T>)
      return static_cast<T>(s);
    else
      return s;
  }
};
}
""")

cppyy.py.add_pythonization(filtered(is_primitive_gmp_type)(enable_total_order))

mpz = cppyy.gbl.mpz_class
mpq = cppyy.gbl.mpq_class
mpf = cppyy.gbl.mpf_class
