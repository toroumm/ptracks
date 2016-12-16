#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
model_visil

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

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2015/fev  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/12"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import os
import sys

# PyQt library
from PyQt4 import QtCore

# libs
import libs.coords.coord_sys as coords

# model
import model.glb_defs as gdefs
import model.model_manager as model

import model.emula.emula_visil as emula
import model.visil.airspace_visil as airs
import model.visil.landscape_visil as lands

# control
import control.events.events_basic as event

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CModelVisil >----------------------------------------------------------------------------

class CModelVisil(model.CModelManager):
    """
    visir model object
    """
    # ---------------------------------------------------------------------------------------------
    # void (???)
    def __init__(self, f_control):
        """
        @param f_control: control manager
        """
        # logger
        # M_LOG.info("__init__:>>")

        # init super class
        super(CModelVisil, self).__init__(f_control)

        # herdados de CModelManager
        # self.app           # the application
        # self.config        # config manager
        # self.dct_config    # dicionário de configuração
        # self.control       # control manager
        # self.event         # event manager

        self.control.splash.showMessage("creating coordinate system...", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.white)
        
        # obtém as coordenadas de referência
        lf_ref_lat = self.dct_config["map.lat"]
        lf_ref_lng = self.dct_config["map.lng"]
        lf_dcl_mag = self.dct_config["map.dcl"]

        # coordinate system
        self.__coords = coords.CCoordSys(lf_ref_lat, lf_ref_lng, lf_dcl_mag)
        assert self.__coords

        self.control.splash.showMessage("loading cenary...", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.white)

        # variáveis de instância
        self.__airspace = None
        self.__landscape = None

        # carrega as tabelas do sistema
        self.__load_cenario("SBSP")

        self.control.splash.showMessage("creating emulation model...", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.white)

        # create emula model
        self.__emula_model = emula.CEmulaVisil(self, f_control)
        assert self.__emula_model

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    # void (???)
    def __load_cenario(self, fs_cena):
        """
        abre/cria as tabelas do sistema

        @param fs_cena: cenário

        @return flag e mensagem
        """
        # logger
        # M_LOG.info("__load_cenario:>>")

        # carrega o landscape
        lv_ok, ls_msg = self.__load_land(fs_cena)

        # tudo Ok ?
        if lv_ok:
            # carrega o airspace
            lv_ok, ls_msg = self.__load_air(fs_cena)

        # houve erro em alguma fase ?
        if not lv_ok:
            # logger
            l_log = logging.getLogger("CModelVisil::__load_cenario")
            l_log.setLevel(logging.NOTSET)
            l_log.critical(u"<E01: erro na carga da base de dados: {}".format(ls_msg))

            # cria um evento de quit
            l_evt = event.CQuit()
            assert l_evt

            # dissemina o evento
            self.event.post(l_evt)

            # termina a aplicação
            sys.exit(1)

        # logger
        # M_LOG.info("__load_cenario:<<")

    # ---------------------------------------------------------------------------------------------
    # void (???)
    def __load_air(self, fs_cena):
        """
        faz a carga do airspace

        @param fs_cena: cenário

        @return flag e mensagem
        """
        # logger
        # M_LOG.info("__load_air:>>")

        # obtém o diretório padrão de airspaces
        ls_dir = self.dct_config["dir.air"]

        # nome do diretório vazio ?
        if ls_dir is None:
            # diretório padrão de airspaces
            self.dct_config["dir.air"] = gdefs.D_DIR_AIR

            # diretório padrão de airspaces
            ls_dir = gdefs.D_DIR_AIR

        # expand user (~)
        ls_dir = os.path.expanduser(ls_dir)

        # diretório não existe ?
        if not os.path.exists(ls_dir):
            # cria o diretório
            os.mkdir(ls_dir)

        # create airspace
        self.__airspace = airs.CAirspaceVisil(self, ls_dir, fs_cena)
        assert self.__airspace

        # carrega os dicionários
        self.__airspace.load_dicts()

        # logger
        # M_LOG.info("__load_air:<<")

        # retorna ok
        return True, None

    # ---------------------------------------------------------------------------------------------
    # void (???)
    def __load_land(self, fs_cena):
        """
        faz a carga do landscape

        @param fs_cena: cenário

        @return flag e mensagem
        """
        # logger
        # M_LOG.info("__load_land:>>")

        # obtém o diretório padrão de landscapes
        ls_dir = self.dct_config["dir.map"]

        # nome do diretório vazio ?
        if ls_dir is None:
            # diretório padrão de landscapes
            self.dct_config["dir.map"] = gdefs.D_DIR_MAP

            # diretório padrão de landscapes
            ls_dir = gdefs.D_DIR_MAP

        # expand user (~)
        ls_dir = os.path.expanduser(ls_dir)

        # diretório não existe ?
        if not os.path.exists(ls_dir):
            # cria o diretório
            os.mkdir(ls_dir)

        # create landscape
        self.__landscape = lands.CLandscapeVisil(self, ls_dir, fs_cena)
        assert self.__landscape

        # carrega os dicionários
        self.__landscape.load_dicts()

        # logger
        # M_LOG.info("__load_land:<<")

        # retorna ok
        return True, None

    # ---------------------------------------------------------------------------------------------
    # void (???)
    def notify(self, f_evt):
        """
        callback de tratamento de eventos recebidos

        @param f_evt: evento recebido
        """
        # logger
        # M_LOG.info("notify:><")
        pass

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def airspace(self):
        """
        get airspace
        """
        return self.__airspace

    # ---------------------------------------------------------------------------------------------
    @property
    def coords(self):
        """
        get coordinate system
        """
        return self.__coords

    @coords.setter
    def coords(self, f_val):
        """
        set coordinate system
        """
        self.__coords = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def emula_model(self):
        """
        get emula model
        """
        return self.__emula_model

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_esp(self):
        """
        get esperas
        """
        return self.__airspace.dct_esp

    # ---------------------------------------------------------------------------------------------
    @property
    def landscape(self):
        """
        get landscape
        """
        return self.__landscape

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_sub(self):
        """
        get subidas
        """
        return self.__airspace.dct_sub

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_trj(self):
        """
        get trajetórias
        """
        return self.__airspace.dct_trj

# < the end >--------------------------------------------------------------------------------------
