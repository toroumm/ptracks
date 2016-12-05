#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
aircraft_basic

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
import random
import sys
import time

# libs
import libs.coords.pos_lat_lng as pll

# model
import model.tMath as tmath
import model.stock.aircraft as sanv

# < class CAircraftBasic >-------------------------------------------------------------------------

class CAircraftBasic(sanv.CAircraft):
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
        super(CAircraftBasic, self).__init__()

        # herdado de CAircraft
        # self.adiru          # air data inertial reference unit
        # self.s_callsign     # callsign
        # self.s_icao_addr    # icao address
        # self.pos            # posição lat/lng
        # self.s_status       # situação

        # herdado de CADIRU
        # self.adiru.f_alt             # altitude
        # self.adiru.f_ias             # instrument air speed
        # self.adiru.f_proa            # proa em relação ao norte magnético
        # self.adiru.f_true_heading    # proa em relação ao norte verdadeiro
        # self.adiru.f_vel             # velocidade

        # import foreign objects
        self.__airspace = f_emula.model.airspace

        # create vectors
        self.__lst_trail = []
        self.__lst_instructions = []

        self.__v_uninitialized = True

        # recebeu dados ?
        if f_data is not None:
            # recebeu uma lista ?
            if isinstance(f_data, list):
                # cria uma aeronave com os dados da lista
                self.make_aircraft(f_data, True)

            # recebeu uma aeronave ?
            elif isinstance(f_data, CAircraftBasic):
                # copia a aeronave
                # self.copy_aircraft(f_data)
                pass

            # senão, inicia os dados locais
            else:
                # set initial values
                self.adiru.f_alt = 10000.
                self.adiru.f_ias = 230.
                self.adiru.f_vel = 230.
                self.adiru.f_proa = 0.
                self.adiru.f_true_heading = 0.

    # ---------------------------------------------------------------------------------------------
    def init_position(self, f_oPos):
        """
        set initial position and radar position
        """
        # check input
        # assert f_control

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
    def make_aircraft(self, f_data, fv_initial=False):
        """
        create an aircraft from list
        """
        # check input
        assert f_data is not None

        # inicia o índice de dados
        li_ndx = 0

        # identificacao da aeronave
        self.s_icao_addr = str(f_data[li_ndx])
        li_ndx += 1

        # código transponder (ssr)
        self.__i_ssr = int(f_data[li_ndx])
        li_ndx += 1

        # spi
        li_spi = int(f_data[li_ndx])
        li_ndx += 1

        # altitude (m)
        self.adiru.f_alt = float(f_data[li_ndx])
        li_ndx += 1

        # latitude
        lf_lat = float(f_data[li_ndx])
        li_ndx += 1

        # longitude
        lf_lng = float(f_data[li_ndx])
        li_ndx += 1

        self.pos = pll.CPosLatLng(lf_lat, lf_lng)
        assert self.pos

        # if fv_initial:
            # self.pos = pll.CPosLatLng(lf_lat, lf_lng)
            # assert self.pos

        # velocidade (kt)
        lf_vel = float(f_data[li_ndx])
        li_ndx += 1

        self.adiru.f_ias = lf_vel
        self.adiru.f_vel = lf_vel

        # razão de subida
        self.__f_raz = float(f_data[li_ndx])
        li_ndx += 1

        # proa
        lf_pro = float(f_data[li_ndx])
        li_ndx += 1

        self.adiru.f_proa = lf_pro
        self.adiru.f_true_heading = lf_pro

        # callsign
        self.s_callsign = str(f_data[li_ndx])
        li_ndx += 1

        # performance
        self.__s_prf = str(f_data[li_ndx])
        li_ndx += 1

        # hora
        self.__i_hora = float(f_data[li_ndx])
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
        self.make_aircraft(f_data)

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
        # self.pos = self.pos

        # salva o intervalo do rastro
        self.__f_trail_interval = ff_tim

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def i_hora(self):
        """
        get hora
        """
        return self.__i_hora

    @i_hora.setter
    def i_hora(self, f_val):
        """
        set hora
        """
        self.__i_hora = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def s_prf(self):
        """
        get performance
        """
        return self.__s_prf

    @s_prf.setter
    def s_prf(self, f_val):
        """
        set performance
        """
        self.__s_prf = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_raz(self):
        """
        get razão de descida/subida
        """
        return self.__f_raz

    @f_raz.setter
    def f_raz(self, f_val):
        """
        set razão de descida/subida
        """
        self.__f_raz = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def i_ssr(self):
        """
        get transponder code
        """
        return self.__i_ssr

    @i_ssr.setter
    def i_ssr(self, f_val):
        """
        set transponder code
        """
        self.__i_ssr = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def lst_trail(self):
        """
        get trail list
        """
        return self.__lst_trail

    @lst_trail.setter
    def lst_trail(self, f_val):
        """
        set trail list
        """
        self.__lst_trail = f_val

# < the end >--------------------------------------------------------------------------------------
