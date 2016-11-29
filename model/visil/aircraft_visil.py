#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
aircraft_visil

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

#import model.visadsb.auto_pilot as CAutoPilot
#import model.visadsb.fms as CFMS
#import model.visadsb.instruction as CInstruction
#import model.visadsb.mcp as CMCP
#import model.visadsb.pilot as CPilot

# < class CAircraftVisil >-------------------------------------------------------------------------

class CAircraftVisil(sanv.CAircraftBasic):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_emula, f_data=None):
        """
        constructor
        """
        # check input
        assert f_emula

        # inicia a super classe
        super(CAircraftVisil, self).__init__(f_emula, f_data)

        # herdado de CAircraft
        # self.adiru          # air data inertial reference unit
        # self.s_callsign     # callsign
        # self.s_icao_addr    # icao address
        # self.pos            # posição lat/lng

        # import foreign objects
        self.__airspace = f_emula.model.airspace
        assert self.__airspace

        # self.__weather = f_emula.model.weather
        # assert self.__weather

        # create vectors
        self.__lst_trail = []
        self.__lst_instructions = []

        self.__v_uninitialized = True

        # create aircraft components

        #self._mcp = CMCP.CMCP(self.__airspace.f_variation)
        #assert self._mcp is not None

        #self._fms = CFMS.CFMS(self, self.__airspace, self.__weather, self.adiru, self._mcp)
        #assert self._fms is not None

        #self._auto_pilot = CAutoPilot.CAutoPilot(self.adiru, self._fms, self._mcp)
        #assert self._auto_pilot is not None

        #self._fms.setAutoPilot(self._auto_pilot)

        #self._pilot = CPilot.CPilot(self, self.__airspace, self.__weather, self._fms, self._mcp)
        #assert self._pilot is not None

        # recebeu dados ?
        if f_data is not None:
            # recebeu uma lista ?
            if isinstance(f_data, list):
                # cria uma aeronave com os dados da lista
                self.__make_aircraft(f_data, True)

            # recebeu uma aeronave ?
            elif isinstance(f_data, CAircraftVisil):
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
    def fly(self, t):
        """
        do periodic updates (position, altitude, speed,...) variable t specifies time in microseconds
        """
        # check input
        # assert f_control
        '''
        tas = self._fms.TAS()

        # any instructions ?
        for l_inst in self.__lst_instructions:
            if l_inst._oReactTime <= time.time():
                self._pilot.accept(l_inst)
                self.__lst_instructions.remove(l_inst)

        # make FMS decisions
        self._fms.decide()

        # update Position in two halves
        self._auto_pilot.move(self.adiru.f_true_heading, tas, t / 2000.)
        # self._auto_pilot.move(tmath.trackOpposite(self.__weather.get_wind_dir(self.adiru.f_altitude)),
        #                                           self.__weather.get_wind_spd(self.adiru.f_altitude), t / 2000.)
        self._auto_pilot.move(tmath.trackOpposite(0.), 0., t / 2000.)

        target_hdg = self._mcp.targetHeading()

        if self._mcp.lateralMode() != CMCP.CMCP._C_LMODE_HDG:
            target_hdg = self._fms.targetHeading()

        # change HDG
        if self.adiru.f_true_heading != target_hdg:
            self._auto_pilot.turn(target_hdg, t)

        # update Position in two halves
        self._auto_pilot.move(self.adiru.f_true_heading, tas, t / 2000.)
        # self._auto_pilot.move(tmath.trackOpposite(self.__weather.get_wind_dir(self.adiru.f_altitude)),
        #                                           self.__weather.get_wind_spd(self.adiru.f_altitude), t / 2000.)
        self._auto_pilot.move(tmath.trackOpposite(0.), 0., t / 2000.)
        '''
    # ---------------------------------------------------------------------------------------------
    def init_position(self, f_oPos):
        """
        set initial position and radar position
        """
        # check input
        # assert f_control

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
        # check input
        # assert f_control
        '''
        if (f_appName == ""):
            # logger
            # M_LOG.info("<E01")

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
        # check input
        # assert f_control
        '''
        if (f_ptName == ""):
            # logger
            # M_LOG.info("<E01")

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
        # check input
        # assert f_control
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
        # check input
        # assert f_control
        '''
        if (f_sRtName == ""):
            # logger
            # M_LOG.info("<E01")

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

    # ---------------------------------------------------------------------------------------------
    def isClimbing(self):
        """
        is the aircraft climbing ?
        """
        # TODO
        return False

    # ---------------------------------------------------------------------------------------------
    def isDescending(self):
        """
        is the aircraft descending ?
        """
        # TODO
        return False

    # ---------------------------------------------------------------------------------------------
    def __make_aircraft(self, f_data, fv_initial=False):
        """
        create an aircraft from list
        """
        # check input
        assert f_data is not None

        # inicia o indice de dados
        li_ndx = 0

        # identificacao da aeronave
        li_id = int(f_data[li_ndx])
        li_ndx += 1

        # código transponder (ssr)
        li_ssr = int(f_data[li_ndx])
        li_ndx += 1

        # spi
        li_spi = int(f_data[li_ndx])
        li_ndx += 1

        # altitude
        lf_alt = float(f_data[li_ndx])
        li_ndx += 1

        self.adiru.f_altitude = lf_alt

        # latitude
        lf_lat = float(f_data[li_ndx])
        li_ndx += 1

        # longitude
        lf_lng = float(f_data[li_ndx])
        li_ndx += 1

        self.adiru.pos = pll.CPosLatLng(lf_lat, lf_lng)
        assert self.adiru.pos

        if fv_initial:
            self.pos = pll.CPosLatLng(lf_lat, lf_lng)
            assert self.pos

        # velocidade
        lf_vel = float(f_data[li_ndx])
        li_ndx += 1

        self.adiru.f_ias = lf_vel

        # razão de subida
        lf_raz = float(f_data[li_ndx])
        li_ndx += 1

        # proa
        lf_pro = float(f_data[li_ndx])
        li_ndx += 1

        self.adiru.f_true_heading = lf_pro

        # callsign
        ls_ind = str(f_data[li_ndx])
        li_ndx += 1

        self.s_callsign = ls_ind

        # performance
        ls_prf = str(f_data[li_ndx])
        li_ndx += 1

        # hora
        lf_tim = float(f_data[li_ndx])
        li_ndx += 1

    # ---------------------------------------------------------------------------------------------
    def radar_ground_speed(self):
        """
        determine groundspeed from radar history
        """
        if len(self.__lst_trail) < 3:
            # return
            return 0

        # calculate ground speed
        l_gs = tmath.distLL(self.__lst_trail[-1], self.pos) / (self.__f_trail_interval / 1000.) * 3600.

        # return
        return l_gs

    # ---------------------------------------------------------------------------------------------
    def radar_magnetic_track(self):
        """
        determine magnetic track from radar history
        """
        if len(self.__lst_trail) < 3:
            # return
            return 0

        # determine magnetic track
        l_tr = round(tmath.track(self.__lst_trail[-1], self.pos) + self.__airspace.f_variation, 0)

        # need normalize ?
        if l_tr < 0:
            # normalize angle
            l_tr += 360

        # return
        return l_tr

    # ---------------------------------------------------------------------------------------------
    def trail(self, fi_ndx):
        """
        get position of radar history point #n
        """
        # exists trail ?
        if not self.__lst_trail:
            # return
            return None

        # index out of range ?
        if fi_ndx >= len(self.__lst_trail):
            # return
            return None

        # return
        return self.__lst_trail[len(self.__lst_trail) - 1 - fi_ndx]

    # ---------------------------------------------------------------------------------------------
    def update_data(self, f_data):
        """
        update data
        """
        # update aircraft data
        self.__make_aircraft(f_data)

    # ---------------------------------------------------------------------------------------------
    def update_radar_position(self, ff_tim):
        """
        get new radar position, and push old one into history
        """
        # check input
        # assert f_control

        # obtém a última posção conhecida
        l_last_pos = pll.CPosLatLng(self.pos)
        assert l_last_pos is not None

        # coloca no rastro
        self.__lst_trail.append(l_last_pos)

        # atualiza a posição da aeronave
        self.pos = self.adiru.pos

        # salva o intervalo do rastro
        self.__f_trail_interval = ff_tim

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

    # ---------------------------------------------------------------------------------------------
    @property
    def f_ias(self):
        """
        get instrument air speed
        """
        return self.adiru.f_ias

    @f_ias.setter
    def f_ias(self, f_val):
        """
        set initial speed
        """
        self.adiru.f_ias = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def position(self):
        """
        get last position
        """
        return self.pos

    @position.setter
    def position(self, f_val):
        """
        set last position
        """
        self.pos = f_val
        self.adiru.pos = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_true_heading(self):
        """
        get instrument air speed
        """
        return self.adiru.f_true_heading

    @f_true_heading.setter
    def f_true_heading(self, f_val):
        """
        set initial speed
        """
        self.adiru.f_true_heading = f_val

# < the end >--------------------------------------------------------------------------------------
