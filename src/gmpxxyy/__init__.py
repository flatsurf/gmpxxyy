r"""
Python and SageMath wrappers for GMP

EXAMPLES::

    >>> from gmpxxyy import mpq
    >>> a = mpq(2, 6)
    >>> a + a
    2/3

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

from .cppyy_gmpxx import mpz, mpq, mpf

try:
    import sage
    from .sage import mpz, mpq
except ModuleNotFoundError:
    pass

