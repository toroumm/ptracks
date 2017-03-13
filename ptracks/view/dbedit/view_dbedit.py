#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
view_dbedit

code for the view manager

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

# view
import ptracks.view.view_manager as view
import ptracks.view.common.color_manager as clrm

import ptracks.view.dbedit.wnd_main_dbedit as wmain

# control
import ptracks.control.events.events_basic as events

# < class CViewDBEdit >----------------------------------------------------------------------------

class CViewDBEdit(view.CViewManager):
    """
    módulo view do editor da base de dados. É a classe de interface. Trata as interações com o
    usuário
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control):
        """
        constructor
        
        @param f_control: control manager
        """
        # check input
        assert f_control

        # inicia a super classe
        super(CViewDBEdit, self).__init__(f_control)

        # herdados de CViewManager
        # self.app           # the application
        # self.config        # config manager
        # self.dct_config    # dicionário de configuração
        # self.control       # control manager
        # self.event         # event manager
        # self.model         # model manager

        # show message
        self.control.splash.showMessage("loading colour table...", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.white)
                
        # color manager 
        self.__colors = clrm.CColorManager(self.config)
                
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
        exec application
        """
        # clear to go
        assert self.control
        assert self.app

        # create main window
        l_wmain = wmain.CWndMainDBEdit(self.control)
        assert l_wmain

        # show main window
        l_wmain.show()

        # dismiss splash screen
        self.control.splash.finish(l_wmain)

        # exec application
        self.app.exec_()

# < the end >--------------------------------------------------------------------------------------
