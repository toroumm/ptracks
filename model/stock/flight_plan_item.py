#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
flight_plan_item.
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

# Python library
import logging

# < module data >----------------------------------------------------------------------------------

# logging level
# M_LOG_LVL = logging.DEBUG

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(# M_LOG_LVL)

# < class CFlightPlanItem >------------------------------------------------------------------------


class CFlightPlanItem(object):

    _EXACTLY = 0
    _OR_BELOW = 1
    _OR_ABOVE = 2

    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        # logger
        # M_LOG.info("__init__:>>")

        self.__s_name = None

        self._fInbound = -1.

        self._iAltConstraint = 0
        self._iAltConstraintType = 0
        self._iSpeedConstraint = 0

        self._vFlyOver = False
        self._vApproach = False

        # logger
        # M_LOG.info("__init__:<<")

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    
    @property
    def s_name(self):
        """
        get latitude
        """
        return self.__s_name
                                            
    @s_name.setter
    def s_name(self, f_val):
        """
        set latitude
        """
        self.__s_name = f_val

    # ---------------------------------------------------------------------------------------------
    
    @property
    def f_lng(self):
        """
        get longitude
        """
        return self.__f_lng
                                            
    @f_lng.setter
    def f_lng(self, f_val):
        """
        set longitude
        """
        self.__f_lng = f_val

# < the end >--------------------------------------------------------------------------------------
