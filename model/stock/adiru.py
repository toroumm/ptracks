#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
adiru

DOCUMENT ME!

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

revision 0.2  2015/dez  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2016/01"

# < imports >--------------------------------------------------------------------------------------

# python library
import copy

# libs
import libs.coords.pos_lat_lng as pll

# < class CADIRU >---------------------------------------------------------------------------------

class CADIRU(object):
    """
    represents air data inertial reference unit
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        # inicia a super classe
        super(CADIRU, self).__init__()

        # altitude
        self.__f_alt = 0.

        # instrument air speed
        self.__f_ias = 0.

        # proa em relação ao norte magnético
        self.__f_proa = 0.

        # proa em relação ao norte verdadeiro
        self.__f_true_heading = 0.

        # velocidade
        self.__f_vel = 0.

    # ---------------------------------------------------------------------------------------------
    def copy(self):
        """
        copy constructor
        """
        # return a copy
        return copy.deepcopy(self)

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def f_alt(self):
        """
        get altitude
        """
        return self.__f_alt

    @f_alt.setter
    def f_alt(self, f_val):
        """
        set altitude
        """
        self.__f_alt = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_ias(self):
        """
        get ias (instrument air speed)
        """
        return self.__f_ias

    @f_ias.setter
    def f_ias(self, f_val):
        """
        set ias (instrument air speed)
        """
        self.__f_ias = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_proa(self):
        """
        get proa
        """
        return self.__f_proa

    @f_proa.setter
    def f_proa(self, f_val):
        """
        set proa
        """
        # check input
        assert 0. <= f_val <= 360.

        # save proa
        self.__f_proa = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_true_heading(self):
        """
        get true heading
        """
        return self.__f_true_heading

    @f_true_heading.setter
    def f_true_heading(self, f_val):
        """
        set true heading
        """
        # check input
        assert 0. <= f_val <= 360.

        # save true heading
        self.__f_true_heading = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_vel(self):
        """
        get velocidade
        """
        return self.__f_vel

    @f_vel.setter
    def f_vel(self, f_val):
        """
        set velocidade
        """
        self.__f_vel = f_val

# < the end >--------------------------------------------------------------------------------------
