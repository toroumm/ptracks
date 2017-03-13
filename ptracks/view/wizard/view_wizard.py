#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
view_wizard

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
import time

# PyQt library
from PyQt4 import QtCore
from PyQt4 import QtGui

# view
import ptracks.view.view_manager as view
import ptracks.view.wizard.dlg_wizard as wzd

# control
import ptracks.control.events.events_basic as events

# < class CViewWizard >-----------------------------------------------------------------------------

class CViewWizard(view.CViewManager):
    """
    the interface to configuration wizard. Handles all interaction with user
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control):
        """
        initializes the display
        """
        # check input
        assert f_control

        # initialize super class
        super(CViewWizard, self).__init__(f_control)

        # herdados de CViewManager
        # self.config        # config
        # self.dct_config    # dicionário de configuração
        # self.control       # control
        # self.event         # event
        # self.model         # model

        # control
        self.control = f_control
        assert self.control

        # model
        # self.model = f_control.model
        # assert self._model

        # event
        self.event = f_control.event
        assert self.event

        # registra a sí próprio como recebedor de eventos
        # self._event.register_listener(self)

        # config
        self.config = f_control.config
        assert self.config

        # dicionário de configuração
        self.dct_config = self.config.dct_config
        assert self.dct_config

        # cria a aplicação
        self._app = QtGui.QApplication(sys.argv)
        assert self._app

        # configura alguns parâmetros da aplicação
        self._app.setOrganizationName("sophosoft")
        self._app.setOrganizationDomain("sophosoft.com.br")
        self._app.setApplicationName("merlin")

        self._app.setWindowIcon(QtGui.QIcon(os.path.join(self.dct_config["dir.img"], "icon.png")))

    # ---------------------------------------------------------------------------------------------
    def notify(self, f_event):
        """
        callback de recebimento de eventos

        @param f_event: event
        """
        # check input
        assert f_event

        if isinstance(f_event, events.CTick):
            pass
                
    # ---------------------------------------------------------------------------------------------
    def run(self):
        """
        executa a aplicação
        """
        # verifica condições de execução
        assert self._app

        # get start time
        ll_start = time.time()

        # carrega o logo
        l_pix_logo = QtGui.QPixmap(os.path.join(self.dct_config["dir.img"], "logo.png"))
        assert l_pix_logo

        # cria a tela de apresentação
        l_splash = QtGui.QSplashScreen(l_pix_logo, QtCore.Qt.SplashScreen | QtCore.Qt.WindowStaysOnTopHint)
        assert l_splash

        # cria a tela de apresentação
        l_splash.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # aplica a máscara
        l_splash.setMask(l_pix_logo.mask())

        # cria a fonte das mensagens
        l_font = QtGui.QFont(l_splash.font())
        assert l_font

        # ajusta tamanho da fonte
        l_font.setPointSize(l_font.pointSize() + 5)

        # configura a fonte
        l_splash.setFont(l_font)

        # exibe a tela de apresentação
        l_splash.show()

        # inicia o contador
        # l_count = 0

        # simulate something that takes time
        while (time.time() - ll_start) < 2:
            # trata os eventos(antes do loop principal)
            self._app.processEvents()

            # exibe a mensagem
            # l_splash.showMessage(l_splash.tr(u"Carregando as páginas %1...").arg(l_count),
            #     QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeft, QtCore.Qt.white)

            # incrementa o contador
            # l_count += 1

            # simulate something that takes time
            time.sleep(0.001)

        # cria o configurador de simulação
        l_wzd = wzd.CDlgWizard(self.control)
        assert l_wzd

        # exibe o configurador de simulação
        l_wzd.show()

        # fecha a tela de apresentação
        l_splash.finish(l_wzd)

        # processa a aplicação
        self._app.exec_()

# < the end >--------------------------------------------------------------------------------------
