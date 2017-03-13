#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
runway

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

# model
import ptracks.model.common.fix as CFix

# < class CRunway >--------------------------------------------------------------------------------

class CRunway(CFix.CFix):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_rwy_name, ff_rwy_lat, ff_rwy_lng, ff_rwy_track, ff_rwy_gp):
        """
        define uma aerovia

        @param fs_rwy_name: nome
        @param ff_rwy_lat: latitude
        @param ff_rwy_lng: longitude
        @param ff_rwy_track: path
        @param ff_rwy_gp: glide path
        """
        # inicia a super classe
        super(CRunway, self).__init__(fs_rwy_name, ff_rwy_lat, ff_rwy_lng)

        # herdados de CFix
        # self.s_name      # nome
        # self.position    # posição

        self.__f_track = ff_rwy_track
        self.__f_app_angle = ff_rwy_gp

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def f_app_angle(self):
        """
        get glide path
        """
        return self.__f_app_angle
                                            
    @f_app_angle.setter
    def f_app_angle(self, f_val):
        """
        set glide path
        """
        self.__f_app_angle = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_track(self):
        """
        get track
        """
        return self.__f_track
                                            
    @f_track.setter
    def f_track(self, f_val):
        """
        set track
        """
        self.__f_track = f_val

# < the end >--------------------------------------------------------------------------------------
