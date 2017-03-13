#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
dlg_velocidade

mantém as informações sobre a dialog de velocidade

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
import logging
import os

# PyQt library
from PyQt4 import QtCore
from PyQt4 import QtGui

# view
import ptracks.view.piloto.dlg_velocidade_ui as dlg

# control
import ptracks.control.control_debug as dbg

# < class CDlgVelocidade >----------------------------------------------------------------------------

class CDlgVelocidade(QtGui.QDialog, dlg.Ui_CDlgVelocidade):
    """
    mantém as informações sobre a dialog de velocidade
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_strip_cur, fdct_prf, f_parent=None):
        """
        @param f_strip_cur: strip selecionada
        @param fdct_prf: dicionário de performances
        @param f_parent: janela pai.
        """
        # init super class
        super(CDlgVelocidade, self).__init__(f_parent)

        # dicionário de performances
        self.__dct_prf = fdct_prf
                
        # monta a dialog
        self.setupUi(self)

        # configura título da dialog
        self.setWindowTitle(u"Velocidade")

        # configurações de conexões slot/signal
        self.__config_connects()

        # configurações de títulos e mensagens da janela de edição
        self.__config_texts()

        # restaura as configurações da janela de edição
        self.__restore_settings()

        # inicia valores
        self.sbx_vel.setValue(f_strip_cur.f_vel)
        
        # performance existe ?
        if fdct_prf is not None:
            # faixa de velocidade
            self.sbx_vel.setRange(1., self.__dct_prf["vel_max_crz"])

        # senão,...
        else:
            # faixa de velocidade
            self.sbx_vel.setRange(1., 500.)

        # configura botões
        self.bbx_velocidade.button(QtGui.QDialogButtonBox.Cancel).setText("&Cancela")
        self.bbx_velocidade.button(QtGui.QDialogButtonBox.Ok).setFocus()

        # inicia os parâmetros da velocidade
        self.__update_command()

    # ---------------------------------------------------------------------------------------------
    def __config_connects(self):
        """
        configura as conexões slot/signal
        """
        # conecta spinBox
        self.sbx_vel.valueChanged.connect(self.__on_sbx_valueChanged)

        # conecta botão Ok da edição de velocidade
        # self.bbx_velocidade.accepted.connect(self.__accept)

        # conecta botão Cancela da edição de velocidade
        # self.bbx_velocidade.rejected.connect(self.__reject)

    # ---------------------------------------------------------------------------------------------
    def __config_texts(self):
        """
        DOCUMENT ME!
        """
        # configura títulos e mensagens
        self.__txt_settings = "CDlgVelocidade"

    # ---------------------------------------------------------------------------------------------
    def get_data(self):
        """
        DOCUMENT ME!
        """
        # return command line
        return self.lbl_comando.text()

    # ---------------------------------------------------------------------------------------------
    def __restore_settings(self):
        """
        restaura as configurações salvas para esta janela
        """
        # obtém os settings
        l_set = QtCore.QSettings("sophosoft", "piloto")
        assert l_set

        # restaura geometria da janela
        self.restoreGeometry(l_set.value("%s/Geometry" % (self.__txt_settings)).toByteArray())

    # ---------------------------------------------------------------------------------------------
    def __update_command(self):
        """
        DOCUMENT ME!
        """
        # inicia o comando
        ls_cmd = "VEL {} ".format(self.sbx_vel.value())

        # coloca o comando no label
        self.lbl_comando.setText(ls_cmd)

    # =============================================================================================
    # edição de campos
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSignature("int")
    def __on_sbx_valueChanged(self, f_val):
        """
        DOCUMENT ME!
        """
        # atualiza comando
        self.__update_command()

# < the end >--------------------------------------------------------------------------------------
