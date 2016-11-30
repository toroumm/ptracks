#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
airspace_piloto

basic model manager
load from one configuration file all configured tables

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
__author__ = "mlabru, sophosoft"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
import os

# model
import model.stock.airspace_basic as airs

import model.items.esp_data as espdata
import model.items.sub_data as subdata
import model.items.trj_data as trjdata

# import model.piloto.defs_piloto as ldefs

# < class CAirspacePiloto >------------------------------------------------------------------------

class CAirspacePiloto(airs.CAirspaceBasic):
    """
    piloto airspace
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_model):
        """
        @param f_model: model manager
        """
        # check input
        assert f_model

        # init super class
        super(CAirspacePiloto, self).__init__(f_model)

        # herdado de CAirspaceBasic
        # self.model           # model manager 
        # self.event           # event manager
        # self.config          # config manager
        # self.dct_aer         # dicionário de aeródromos
        # self.dct_fix         # dicionário de fixos
        # self.dct_fix_indc    # dicionário de fixos por indicativo
        # self.lst_arr_dep     # lista de pousos/decolagens

        # procedimentos de espera
        self.__dct_esp = {}

        # procedimentos de subida
        self.__dct_sub = {}

        # procedimentos de trajetória
        self.__dct_trj = {}

    # ---------------------------------------------------------------------------------------------
    def load_dicts(self):
        """
        DOCUMENT ME!
        """
        # monta o nome da tabela de procedimentos de espera
        ls_path = os.path.join(self.dct_config["dir.prc"], self.dct_config["tab.esp"])

        # carrega a tabela de procedimentos de espera em um dicionário
        self.__dct_esp = espdata.CEspData(self.model, ls_path)
        assert self.__dct_esp is not None

        # monta o nome da tabela de procedimentos de subida
        ls_path = os.path.join(self.dct_config["dir.prc"], self.dct_config["tab.sub"])

        # carrega a tabela de procedimentos de subida em um dicionário
        self.__dct_sub = subdata.CSubData(self.model, ls_path)
        assert self.__dct_sub is not None

        # monta o nome da tabela de procedimentos de trajetória
        ls_path = os.path.join(self.dct_config["dir.prc"], self.dct_config["tab.trj"])

        # carrega a tabela de procedimentos de trajetória em um dicionário
        self.__dct_trj = trjdata.CTrjData(self.model, ls_path)
        assert self.__dct_trj is not None

        # resolve os procedimentos dos break-points
        # self.resolv_procs()

    # ---------------------------------------------------------------------------------------------
    def notify(self, f_event):
        """
        callback de tratamento de eventos recebidos

        @param f_event: evento recebido
        """
        # return
        return
        
    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_esp(self):
        """
        get esperas
        """
        return self.__dct_esp

    @dct_esp.setter
    def dct_esp(self, f_val):
        """
        set esperas
        """
        self.__dct_esp = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_sub(self):
        """
        get subidas
        """
        return self.__dct_sub

    @dct_sub.setter
    def dct_sub(self, f_val):
        """
        set subidas
        """
        self.__dct_sub = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_trj(self):
        """
        get trajetórias
        """
        return self.__dct_trj

    @dct_trj.setter
    def dct_trj(self, f_val):
        """
        set trajetórias
        """
        self.__dct_trj = f_val

# < the end >--------------------------------------------------------------------------------------
