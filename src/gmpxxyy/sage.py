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

from sage.all import Morphism, ZZ, QQ, Hom
from .cppyy_gmpxx import mpz, mpq

class ConversionZZMpz(Morphism):
    r"""
    Conversion from our mpz type to SageMath integers.

    EXAMPLES::

        sage: from gmpxxyy import mpz
        sage: ZZ(mpz(1))
        1

    """
    def __init__(self):
        Morphism.__init__(self, Hom(mpz, ZZ, ZZ.category(), check=False))

    def _call_(self, x):
        return ZZ(x.get_str())

mpz.is_exact = lambda: True
ZZ.register_conversion(ConversionZZMpz())

class ConversionQQMpq(Morphism):
    r"""
    Conversion from our mpq type to SageMath rationals.

    EXAMPLES::

        sage: from gmpxxyy import mpq
        sage: QQ(mpq(1, 2))
        1/2

    """
    def __init__(self):
        Morphism.__init__(self, Hom(mpq, QQ, QQ.category(), check=False))
    
    def _call_(self, x):
        return QQ(x.get_str())

mpq.is_exact = lambda: True
QQ.register_conversion(ConversionQQMpq())
