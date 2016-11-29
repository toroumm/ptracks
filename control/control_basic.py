#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
control_basic

the control basic interface

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

revision 0.3  2016/ago  mlabru
pequenas correções e otimizações

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial version (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.3$"
__author__ = "Milton Abrunhosa"
__date__ = "2016/08"

# < imports >--------------------------------------------------------------------------------------

# control
import control.control_manager as control

# < class CControlBasic >--------------------------------------------------------------------------

class CControlBasic(control.CControlManager):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_path=None):
        """
        constructor

        @param fs_path: path do arquivo de configuração
        """
        # init super class
        super(CControlBasic, self).__init__(fs_path)

        # herdados de CControlManager
        # self.event     # event manager
        # self.config    # opções de configuração
        # self.model     # model manager
        # self.view      # view manager
        # self.voip      # biblioteca de VoIP

        # flight control
        self.__ctr_flight = None

        # simulation statistics
        self.__sim_stat = None

        # simulation timer
        self.__sim_time = None

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def ctr_flight(self):
        """
        get flight control
        """
        return self.__ctr_flight

    @ctr_flight.setter
    def ctr_flight(self, f_val):
        """
        set flight control
        """
        self.__ctr_flight = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def sim_stat(self):
        """
        get simulation statistics
        """
        return self.__sim_stat

    @sim_stat.setter
    def sim_stat(self, f_val):
        """
        set simulation statistics
        """
        self.__sim_stat = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def sim_time(self):
        """
        get simulation timer
        """
        return self.__sim_time

    @sim_time.setter
    def sim_time(self, f_val):
        """
        set simulation timer
        """
        self.__sim_time = f_val

# < the end >--------------------------------------------------------------------------------------
