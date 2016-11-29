#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
aircraft

mantém os detalhes de uma aeronave

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

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
import copy

# libs
import libs.coords.pos_lat_lng as pll

# model
import model.stock.adiru as cadi

# < class CAircraft >------------------------------------------------------------------------------

class CAircraft(object):
    """
    mantém as informações específicas sobre uma aeronave
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_id="ABCDEF"):
        """
        @param  fs_id: identificação da aeronave
        """
        # check input
        assert fs_id

        # air data inertial reference unit
        self.__adiru = cadi.CADIRU()
        assert self.__adiru

        # callsign
        self.__s_callsign = "NONAME"

        # icao address
        self.__s_icao_addr = fs_id

        # posição lat/lng
        self.__pos = pll.CPosLatLng()
        assert self.__pos is not None

    # ---------------------------------------------------------------------------------------------
    def copy(self):
        """
        copy constructor
        """
        # return a copy
        return copy.deepcopy(self)

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def adiru(self):
        """
        get air data inertial reference unit
        """
        return self.__adiru

    @adiru.setter
    def adiru(self, f_val):
        """
        set air data inertial reference unit
        """
        self.__adiru = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_alt(self):
        """
        get altitude
        """
        return self.__adiru.f_alt

    @f_alt.setter
    def f_alt(self, f_val):
        """
        set altitude
        """
        self.__adiru.f_alt = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def s_callsign(self):
        """
        get callsign
        """
        return self.__s_callsign  # .decode ( "utf-8" )

    @s_callsign.setter
    def s_callsign(self, f_val):
        """
        set callsign
        """
        self.__s_callsign = f_val.strip()  # .encode ( "utf-8" )

    # ---------------------------------------------------------------------------------------------
    @property
    def s_icao_addr(self):
        """
        get ICAO address
        """
        return self.__s_icao_addr

    @s_icao_addr.setter
    def s_icao_addr(self, f_val):
        """
        set ICAO address
        """
        self.__s_icao_addr = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_lat(self):
        """
        get latitude
        """
        return self.__pos.f_lat

    @f_lat.setter
    def f_lat(self, f_val):
        """
        set latitude
        """
        self.__pos.f_lat = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_lng(self):
        """
        get longitude
        """
        return self.__pos.f_lng

    @f_lng.setter
    def f_lng(self, f_val):
        """
        set longitude
        """
        self.__pos.f_lng = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def pos(self):
        """
        get position
        """
        return self.__pos

    @pos.setter
    def pos(self, f_val):
        """
        set position
        """
        self.__pos = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_proa(self):
        """
        get proa
        """
        return self.__adiru.f_proa

    @f_proa.setter
    def f_proa(self, f_val):
        """
        set proa
        """
        self.__adiru.f_proa = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_true_heading(self):
        """
        get true heading
        """
        return self.__adiru.f_true_heading

    @f_true_heading.setter
    def f_true_heading(self, f_val):
        """
        set true heading
        """
        self.__adiru.f_true_heading = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_vel(self):
        """
        get velocidade
        """
        return self.__adiru.f_vel

    @f_vel.setter
    def f_vel(self, f_val):
        """
        set velocidade
        """
        self.__adiru.f_vel = f_val

# < the end >--------------------------------------------------------------------------------------
