#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
wpg_termina

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

# PyQt library
from PyQt4 import QtCore
from PyQt4 import QtGui

# wizard
import view.wizard.wizard_page_model as wpm
import view.wizard.wpg_termina_ui as wterm_ui

# < class CWPagTermina >---------------------------------------------------------------------------

class CWPagTermina(wpm.CWizardPageModel, wterm_ui.Ui_WPagTermina):

    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control, f_dlg_wizard=None):
        """
        initializes the wizard

        @param f_dlg_wizard: DOCUMENT ME!
        """
        # inicia super classe
        super(CWPagTermina, self).__init__(f_dlg_wizard)

        # herdados de CWizardPageModel
        # self.dct_config    # dicionário de configuração
        # self.dlg_wizard    # dialog wizard

        # obtém o gerente de configuração
        l_config = f_control.config
        assert l_config

        # obtém o dicionário de configuração
        self.dct_config = l_config.dct_config
        assert self.dct_config

        # monta a widget
        self.setupUi(self)

        # configurações de conexões slot/signal
        self.setup_connects()

    # ---------------------------------------------------------------------------------------------
    def is_complete(self):
        """
        verifica se a form está aceitável
        """
        # clear to go
        assert self.ckbAgree
        return self.ckbAgree.isChecked()

    # ---------------------------------------------------------------------------------------------
    def is_last_page(self):
        """
        DOCUMENT ME!
        """
        # return
        return True

    # ---------------------------------------------------------------------------------------------
    def reset_page(self):
        """
        reseta os campos da form
        """
        # exercício
        self.txtExe.setText(str(self.dct_config["glb.exe"].s_exe_id))

        # canal de comunicação
        self.txtCanal.setText(str(self.dct_config["glb.canal"]))

        # check box
        self.ckbAgree.setChecked(False)

    # ---------------------------------------------------------------------------------------------
    def setup_connects(self):
        """
        configura as conexões slot/signal
        """
        self.connect(self.ckbAgree, QtCore.SIGNAL("toggled(bool)"),
                     self, QtCore.SIGNAL("completeStateChanged()"))

# < the end >--------------------------------------------------------------------------------------
