#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
standard_route

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

# < class CStandardRoute >-------------------------------------------------------------------------

class CStandardRoute(object):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        DOCUMENT ME!
        """
        # inicia a super classe
        super(CStandardRoute, self).__init__()

        # route name
        self.__s_name = None

        self.__lst_items = []
        self.__lst_runways = []

    # ---------------------------------------------------------------------------------------------
    def addItem(self, f_item):
        """
        DOCUMENT ME!
        """
        self.__lst_items.append(f_item)

    # ---------------------------------------------------------------------------------------------
    def addRunway(self, fs_rwy):
        """
        DOCUMENT ME!
        """
        self.__lst_runways.append(fs_rwy)

    # ---------------------------------------------------------------------------------------------
    def belongsToRunway(self, fs_rwy):
        """
        DOCUMENT ME!
        """
        # return
        return fs_rwy in self.__lst_runways

    # ---------------------------------------------------------------------------------------------
    def getItem(self, fi_ndx):
        """
        DOCUMENT ME!
        """
        # check input
        if fi_ndx >= len(self.__lst_items):
            return None

        # verifica condições de execuçao
        if not self.__lst_items:
            return None

        # return
        return self.__lst_items[fi_ndx]

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def lst_items(self):
        """
        get list items
        """
        return self.__lst_items
                                            
    @lst_items.setter
    def lst_items(self, f_val):
        """
        set list items
        """
        self.__lst_items = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def s_name(self):
        """
        get name
        """
        return self.__s_name
                                            
    @s_name.setter
    def s_name(self, f_val):
        """
        set name
        """
        self.__s_name = f_val

# < the end >--------------------------------------------------------------------------------------
