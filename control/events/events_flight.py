#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
events_flight

generic event superclass. What follows is a list of all events. None of these classes should
perform any tasks, as that could introduce vulnerabilities

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
initial version (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# control
import control.events.events_model as model

# < class CFlight >--------------------------------------------------------------------------------

class CFlight(model.CEventsModel):
    """
    CFlight event class
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_callsign):
        """
        contructor
        """
        # init super class
        super(CFlight, self).__init__()

        # herdados de CEventsModel
        # self.s_name    # event name

        # save event id
        self.s_name = "Flight event"

        # save callsign
        self.__s_callsign = fs_callsign

    # ---------------------------------------------------------------------------------------------
    @property
    def s_callsign(self):
        """
        get callsign
        """
        return self.__s_callsign

# < class CFlightExplode >--------------------------------------------------------------------------

class CFlightExplode(CFlight):
    """
    CFlightExplode event class
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_callsign):
        """
        contructor
        """
        # init super class
        super(CFlightExplode, self).__init__(fs_callsign)

        # herdados de CFlight
        # self.s_name        # event name
        # self.s_callsign    # callsign

        # save event id
        self.s_name = "FlightExplode event"

# < class CFlightKill >-----------------------------------------------------------------------------

class CFlightKill(CFlight):
    """
    CFlightKill event class
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_callsign):
        """
        contructor
        """
        # init super class
        super(CFlightKill, self).__init__(fs_callsign)

        # herdados de CFlight
        # self.s_name        # event name
        # self.s_callsign    # callsign

        # save event id
        self.s_name = "FlightKill event"

# < class CFlightUpdate >---------------------------------------------------------------------------

class CFlightUpdate(CFlight):
    """
    CFlightUpdate event class
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_callsign):
        """
        contructor
        """
        # init super class
        super(CFlightUpdate, self).__init__(fs_callsign)

        # herdados de CFlight
        # self.s_name        # event name
        # self.s_callsign    # callsign

        # save event id
        self.s_name = "FlightUpdate event"

# < the end >--------------------------------------------------------------------------------------
