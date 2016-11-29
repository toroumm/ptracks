#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
fix

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

# libs
import libs.coords.pos_lat_lng as pll

# < class CFix >-----------------------------------------------------------------------------------

class CFix(object):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_fix_indc="NONAME", ff_fix_lat=0., ff_fix_lng=0.):
        """
        define um navaid
                
        @param fs_fix_indc: nome
        @param ff_fix_lat: latitude
        @param ff_fix_lng: longitude
        """
        # inicia a super classe
        super(CFix, self).__init__()

        self.__s_indc = fs_fix_indc

        self.__position = pll.CPosLatLng(ff_fix_lat, ff_fix_lng)
        assert self.__position

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def s_indc(self):
        """
        get indicativo
        """
        return self.__s_indc
                                            
    @s_indc.setter
    def s_indc(self, f_val):
        """
        set indicativo
        """
        self.__s_indc = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def position(self):
        """
        get posição
        """
        return self.__position
                                            
    @position.setter
    def position(self, f_val):
        """
        set posição
        """
        self.__position = f_val

# < the end >--------------------------------------------------------------------------------------
