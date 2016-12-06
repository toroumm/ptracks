#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
dlg_direcao

mantém as informações sobre a dialog de direção

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

# PyQt library
from PyQt4 import QtCore
from PyQt4 import QtGui

# view
import view.piloto.dlg_direcao_ui as dlg

# control
import control.control_debug as dbg

# < class CDlgDirecao >----------------------------------------------------------------------------

class CDlgDirecao(QtGui.QDialog, dlg.Ui_CDlgDirecao):
    """
    mantém as informações sobre a dialog de direção
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, ff_proa, f_parent=None):
        """
        @param f_control: control manager
        @param f_parent: janela pai
        """
        # init super class
        super(CDlgDirecao, self).__init__(f_parent)

        # monta a dialog
        self.setupUi(self)

        # configura título da dialog
        self.setWindowTitle(u"Direção")

        # configurações de conexões slot/signal
        self.__config_connects()

        # configurações de títulos e mensagens da janela de edição
        self.__config_texts()

        # restaura as configurações da janela de edição
        self.__restore_settings()

        # inicia valores
        self.sbx_dir.setValue(ff_proa)

        # configura botões
        self.bbx_direcao.button(QtGui.QDialogButtonBox.Cancel).setText("&Cancela")
        self.bbx_direcao.button(QtGui.QDialogButtonBox.Ok).setFocus()

        # inicia os parâmetros da direção
        self.__update_command()

    # ---------------------------------------------------------------------------------------------
    def __config_connects(self):
        """
        configura as conexões slot/signal
        """
        # conecta groupBox
        self.gbx_sentido.clicked.connect(self.__on_gbx_clicked)
        self.gbx_direcao.clicked.connect(self.__on_gbx_clicked)
        self.gbx_razao.clicked.connect(self.__on_gbx_clicked)

        # conecta radioButton
        self.rbt_dir.clicked.connect(self.__on_rbt_clicked)
        self.rbt_esq.clicked.connect(self.__on_rbt_clicked)
        self.rbt_mnr.clicked.connect(self.__on_rbt_clicked)
        self.rbt_grau.clicked.connect(self.__on_rbt_clicked)
        self.rbt_proa.clicked.connect(self.__on_rbt_clicked)

        # conecta spinBox
        self.sbx_dir.valueChanged.connect(self.__on_sbx_valueChanged)
        self.sbx_raz.valueChanged.connect(self.__on_sbx_valueChanged)

    # ---------------------------------------------------------------------------------------------
    def __config_texts(self):
        """
        DOCUMENT ME!
        """
        # configura títulos e mensagens
        self.__txt_settings = "CDlgDirecao"

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
        ls_cmd = "CURVA "

        # direita ?
        if self.rbt_dir.isChecked():
            ls_cmd += "DIR "

        # esquerda ?
        elif self.rbt_esq.isChecked():
            ls_cmd += "ESQ "

        # senão, menor...
        else:
            ls_cmd += "MNR "

        # direção ?
        if self.gbx_direcao.isChecked():
            # graus ?
            if self.rbt_grau.isChecked():
                ls_cmd += "{} GRAUS ".format(self.sbx_dir.value())

            # senão, proa...
            else:
                ls_cmd += "PROA {} ".format(self.sbx_dir.value())

        # razão ?
        if self.gbx_razao.isChecked():
            ls_cmd += "RAZ {} ".format(self.sbx_raz.value())

        # coloca o comando no label
        self.lbl_comando.setText(ls_cmd)

    # =============================================================================================
    # edição de campos
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSignature("bool")
    def __on_gbx_clicked(self, f_val):
        """
        DOCUMENT ME!
        """
        # atualiza comando
        self.__update_command()

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSignature("bool")
    def __on_rbt_clicked(self, f_val):
        """
        DOCUMENT ME!
        """
        # atualiza comando
        self.__update_command()

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSignature("int")
    def __on_sbx_valueChanged(self, f_val):
        """
        DOCUMENT ME!
        """
        # atualiza comando
        self.__update_command()

# < the end >--------------------------------------------------------------------------------------
