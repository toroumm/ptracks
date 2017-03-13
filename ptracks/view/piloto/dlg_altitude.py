#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
dlg_altitude

mantém as informações sobre a dialog de altitude

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

# libs
import ptracks.libs.coords.coord_defs as cdefs

# view
import ptracks.view.piloto.dlg_altitude_ui as dlg

# control
import ptracks.control.control_debug as dbg

# < class CDlgAltitude >---------------------------------------------------------------------------

class CDlgAltitude(QtGui.QDialog, dlg.Ui_CDlgAltitude):
    """
    mantém as informações sobre a dialog de altitude
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_strip_cur, fdct_prf, f_parent=None):
        """
        @param f_strip_cur: strip selecionada
        @param fdct_prf: dicionário de performances
        @param f_parent: janela pai
        """
        # check input
        assert f_strip_cur

        # init super class
        super(CDlgAltitude, self).__init__(f_parent)

        # dicionário de performances
        self.__dct_prf = fdct_prf

        # flag altitude 
        self.__v_flag_alt = True

        # monta a dialog
        self.setupUi(self)

        # configura título da dialog
        self.setWindowTitle(u"Altitude")

        # configurações de conexões slot/signal
        self.__config_connects()

        # configurações de títulos e mensagens da janela de edição
        self.__config_texts()

        # restaura as configurações da janela de edição
        self.__restore_settings()

        # inicia valores
        self.sbx_alt.setValue(f_strip_cur.f_alt)
        self.sbx_raz.setValue(f_strip_cur.f_raz)

        # performance existe ?
        if fdct_prf is not None:
            # faixa de razão
            self.sbx_raz.setRange(2.0, self.__dct_prf["raz_max_sub_crz"])

        # senão,...
        else:
            # faixa de razão
            self.sbx_raz.setRange(2.0, 25.)

        # configura botões
        self.bbx_altitude.button(QtGui.QDialogButtonBox.Cancel).setText("&Cancela")
        self.bbx_altitude.button(QtGui.QDialogButtonBox.Ok).setFocus()

        # inicia os parâmetros da altitude
        self.__update_command()

    # ---------------------------------------------------------------------------------------------
    def __config_connects(self):
        """
        configura as conexões slot/signal
        """
        # conecta groupBox
        self.gbx_razao.clicked.connect(self.__on_gbx_clicked)

        # conecta radioButton
        self.rbt_alt.clicked.connect(self.__on_rbt_alt_clicked)
        self.rbt_niv.clicked.connect(self.__on_rbt_niv_clicked)

        # conecta spinBox
        self.sbx_alt.valueChanged.connect(self.__on_sbx_valueChanged)
        self.sbx_raz.valueChanged.connect(self.__on_sbx_valueChanged)

    # ---------------------------------------------------------------------------------------------
    def __config_texts(self):
        """
        DOCUMENT ME!
        """
        # configura títulos e mensagens
        self.__txt_settings = "CDlgAltitude"

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
        # direita ?
        if self.rbt_alt.isChecked():
            ls_cmd = "ALT {} ".format(self.sbx_alt.value())

        # senão, nível...
        else:
            ls_cmd = "NIV {} ".format(self.sbx_alt.value())

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
    def __on_rbt_alt_clicked(self, f_val):
        """
        DOCUMENT ME!
        """
        # obtém o valor atual do campo
        li_val = self.sbx_alt.value()

        # performance existe ?
        if self.__dct_prf is not None:
            # altitude máxima é o teto de serviço
            self.sbx_alt.setRange(0, self.__dct_prf["teto_sv"] * cdefs.D_CNV_M2FT)

        # senão,...
        else:
            # altitude máxima é 50000 ft
            self.sbx_alt.setRange(0, 50000)

        # config spinBox
        self.sbx_alt.setSingleStep(1000)

        # está em modo razão ?
        if not self.__v_flag_alt:
            # converte para altitude
            self.sbx_alt.setValue(li_val * 100)

            # muda o flag para altitude
            self.__v_flag_alt = True

        # atualiza comando
        self.__update_command()

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSignature("bool")
    def __on_rbt_niv_clicked(self, f_val):
        """
        DOCUMENT ME!
        """
        # obtém o valor atual do campo
        li_val = self.sbx_alt.value()

        # performance existe ?
        if self.__dct_prf is not None:
            # calcula o nível 
            li_nivel = int((self.__dct_prf["teto_sv"] * cdefs.D_CNV_M2FT) / 100.)

            # altitude máxima é o teto de serviço
            self.sbx_alt.setRange(0, li_nivel)

        # senão,...
        else:
            # nível máximo é 500
            self.sbx_alt.setRange(0, 500)

        # config spinBox
        self.sbx_alt.setSingleStep(10)

        # está em modo altitude ?
        if self.__v_flag_alt:
            # converte para altitude
            self.sbx_alt.setValue(int(li_val / 100.))

            # muda o flag para razão
            self.__v_flag_alt = False

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
