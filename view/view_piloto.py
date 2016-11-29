#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
view_piloto

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

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/12"

# < imports >--------------------------------------------------------------------------------------

# python library
import os
import sys

# PyQt library
from PyQt4 import QtCore
from PyQt4 import QtGui

# view
import view.view_manager as view
import view.piloto.wnd_main_piloto as wmain

# control
import control.events.events_basic as events

# < class CViewPiloto >----------------------------------------------------------------------------

class CViewPiloto(view.CViewManager):
    """
    the interface to configuration piloto. Handles all interaction with user.
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control, f_model):
        """
        constructor
        """
        # check input
        assert f_control
        assert f_model

        # initialize super class
        super(CViewPiloto, self).__init__(f_control)

        # herdados de CViewManager
        # self.config        # config manager
        # self.control       # control manager
        # self.dct_config    # dicionário de configuração
        # self.event         # event manager
        # self.model         # model manager

        # salva o model localmente
        self.model = f_model
        assert self.model

        # cria a aplicação
        self.__app = QtGui.QApplication(sys.argv)
        assert self.__app

        # configura alguns parâmetros da aplicação
        self.__app.setOrganizationName("sophosoft")
        self.__app.setOrganizationDomain("sophosoft.com.br")
        self.__app.setApplicationName("piloto")

        self.__app.setWindowIcon(QtGui.QIcon(os.path.join(self.dct_config["dir.img"], "icon.png")))

        # carrega o logo
        l_pix_logo = QtGui.QPixmap(os.path.join(self.dct_config["dir.img"], "logo.jpg"))
        assert l_pix_logo

        # cria a tela de apresentação
        self.__splash = QtGui.QSplashScreen(l_pix_logo, QtCore.Qt.WindowStaysOnTopHint)
        assert self.__splash

        self.__splash.setMask(l_pix_logo.mask())

        # exibe a tela de apresentação
        self.__splash.show()

        # trata os eventos (antes do loop principal)
        self.__app.processEvents()

    # ---------------------------------------------------------------------------------------------
    def notify(self, f_evt):
        """
        callback de recebimento de eventos

        @param f_evt: event
        """
        # check input
        assert f_evt

        # o evento recebido foi um Tick ?
        if isinstance(f_evt, events.CTick):
            # events.CTick
            pass

        # o evento recebido foi um aviso de término da aplicação ?
        elif isinstance(f_evt, events.CQuit):
            # para todos os processos
            # glb_data.G_KEEP_RUN = False

            # events.CQuit
            pass

    # ---------------------------------------------------------------------------------------------
    def run(self):
        """
        executa a aplicação
        """
        # verifica condições de execução
        assert self.__app
        assert self.control
        assert self.model

        # obtém o airspace
        # l_airspace = self._model.oAirspace
        # assert l_airspace

        # obtém o landscape
        # l_landscape = self._model.oLandscape
        # assert l_landscape

        # cria a visualização
        l_wmain = wmain.CWndMainPiloto(self.control)
        assert l_wmain

        # exibe o configurador de simulação
        l_wmain.show()

        # fecha a tela de apresentação
        self.__splash.finish(l_wmain)

        # processa a aplicação
        self.__app.exec_()

# < the end >--------------------------------------------------------------------------------------
