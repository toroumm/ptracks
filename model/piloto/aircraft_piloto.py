#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
aircraft_piloto

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
import random
import sys
import time

# libs
import libs.coords.pos_lat_lng as pll

# model
import model.tMath as tmath
import model.stock.aircraft_basic as sanv
import model.piloto.strip_model as mstp

#import model.visadsb.auto_pilot as CAutoPilot
#import model.visadsb.fms as CFMS
#import model.visadsb.instruction as CInstruction
#import model.visadsb.mcp as CMCP
#import model.visadsb.pilot as CPilot

# < class CAircraftPiloto >------------------------------------------------------------------------

class CAircraftPiloto(sanv.CAircraftBasic):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_emula, f_data=None):
        """
        constructor
        """
        # verifica parâmetros de entrada
        assert f_emula

        # inicia a super classe
        super(CAircraftPiloto, self).__init__(f_emula, f_data)

        # herdado de CAircraft
        # self.adiru          # air data inertial reference unit
        # self.s_callsign     # callsign
        # self.s_icao_addr    # icao address
        # self.pos            # posição lat/lng

        # herdado de CAircraftBasic
        # self.airspace            # airspace
        # self.lst_trail           # trail list
        # self.lst_instructions    # instructions list
        # self.v_uninitialized     # flag uninitialized
                                                        
        # import foreign objects
        self.airspace = f_emula.model.airspace
        # assert self.airspace
        
        # self.__weather = f_emula.model.weather
        # assert self.__weather

        # create vectors
        self.__lst_trail = []
        self.__lst_instructions = []

        self.__v_uninitialized = True

        # create aircraft components

        #self._mcp = CMCP.CMCP(self.airspace.f_variation)
        #assert self._mcp is not None

        #self._fms = CFMS.CFMS(self, self.airspace, self.__weather, self.adiru, self._mcp)
        #assert self._fms is not None

        #self._auto_pilot = CAutoPilot.CAutoPilot(self.adiru, self._fms, self._mcp)
        #assert self._auto_pilot is not None

        #self._fms.setAutoPilot(self._auto_pilot)

        #self._pilot = CPilot.CPilot(self, self.airspace, self.__weather, self._fms, self._mcp)
        #assert self._pilot is not None

        # recebeu dados ?
        if f_data is not None:
                
            # recebeu uma lista ?
            if isinstance(f_data, list):
                                        
                # cria uma aeronave com os dados da lista
                self.make_aircraft(f_data, True)
                                                                                        
            # recebeu uma aeronave ?
            elif isinstance(f_data, CAircraftPiloto):
                                                                                                                
                # copia a aeronave
                # self.copy_aircraft(f_data)
                pass
                                                                                                                                                                
            # senão, inicia os dados locais
            else:
                # set initial values
                self.adiru.f_altitude = 10000.
                self.adiru.f_ias = 230.
                self.adiru.f_true_heading = 0.

    # ---------------------------------------------------------------------------------------------
    def get_strip(self):
        """
        return flight strip
        """
        # return
        return mstp.CStripModel()

    # ---------------------------------------------------------------------------------------------
    def instructAltitude(self, f_fAlt):
        """
        give instruction for an altitude
        TODO: FL/ALT
        """
        # TODO

    # ---------------------------------------------------------------------------------------------
    def instructApproach(self, f_appName):
        """
        give instruction for an approach procedure
        """
        '''
        if (f_appName == ""):
            return

        l_inst = CInstruction.CInstruction()
        assert l_inst is not None

        l_inst._iType = CInstruction.CInstruction._APPROACH
        l_inst._oReactTime = time.time() + 2 + (random.random() * 9)

        if self.__v_uninitialized:
            l_inst._oReactTime = 0
            self.__v_uninitialized = False

        l_inst._sText = f_appName
        self.__lst_instructions.append(l_inst)
        '''
    # ---------------------------------------------------------------------------------------------
    def instructDirect(self, f_ptName):
        """
        give instruction for a direct (or shortcut)
        """
        '''
        if (f_ptName == ""):
            return

        l_inst = CInstruction.CInstruction()
        assert l_inst is not None

        l_inst._iType = CInstruction.CInstruction._DIRECT
        l_inst._oReactTime = time.time() + 2 + (random.random() * 9)

        if self.__v_uninitialized:
            l_inst._oReactTime = 0
            self.__v_uninitialized = False

        l_inst._sText = f_ptName

        self.__lst_instructions.append(l_inst)
        '''
    # ---------------------------------------------------------------------------------------------
    def instructHeading(self, f_hdg):
        """
        give instruction for a heading
        """
        '''
        if (f_hdg == 360):
            f_hdg = 0

        l_inst = CInstruction.CInstruction()
        assert l_inst is not None

        l_inst._iType = CInstruction.CInstruction._HDG
        l_inst._oReactTime = time.time() + 2 + (random.random() * 9)

        if self.__v_uninitialized:
            l_inst._oReactTime = 0
            self.__v_uninitialized = False

        l_inst._fNumber = f_hdg

        self.__lst_instructions.append(l_inst)
        '''
    # ---------------------------------------------------------------------------------------------
    def instructRoute(self, f_sRtName):
        """
        give instruction for a standard route
        """
        '''
        if (f_sRtName == ""):
            return

        l_inst = CInstruction.CInstruction()
        assert l_inst is not None

        l_inst._iType = CInstruction.CInstruction._ROUTE
        l_inst._oReactTime = time.time() + 2 + (random.random() * 9)

        if self.__v_uninitialized:
            l_inst._oReactTime = 0
            self.__v_uninitialized = False

        l_inst._sText = f_sRtName

        self.__lst_instructions.append(l_inst)
        '''
    # ---------------------------------------------------------------------------------------------
    def instructSpeed(self, ff_ias):
        """
        give instruction for a speed
        """
        # TODO

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def f_altitude(self):
        """
        TODO
        """
        return self.adiru.f_altitude

    @f_altitude.setter
    def f_altitude(self, f_val):
        """
        set initial altitude
        """
        self.adiru.f_altitude = f_val

# < the end >--------------------------------------------------------------------------------------
