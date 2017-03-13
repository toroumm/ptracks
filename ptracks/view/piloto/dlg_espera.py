#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
dlg_espera

mantém as informações sobre a dialog de espera

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
__date__ = "2015/12"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import json
import os

# PyQt library
from PyQt4 import QtCore
from PyQt4 import QtGui

# view
import ptracks.view.piloto.dlg_espera_ui as dlg

# < class CDlgEspera >-----------------------------------------------------------------------------

class CDlgEspera(QtGui.QDialog, dlg.Ui_CDlgEspera):
    """
    mantém as informações sobre a dialog de espera
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, fsck_http, fdct_config, f_strip_cur, fdct_esp, f_parent=None):
        """
        @param fsck_http: socket de comunicação com o servidor
        @param fdct_config: dicionário de configuração
        @param f_strip_cur: strip selecionada
        @param fdct_esp: dicionário de esperas
        @param f_parent: janela pai
        """
        # init super class
        super(CDlgEspera, self).__init__(f_parent)

        # socket de comunicação
        self.__sck_http = fsck_http
        assert self.__sck_http

        # dicionário de configuração
        self.__dct_config = fdct_config
        assert self.__dct_config is not None

        # dicionário de esperas
        self.__dct_esp = self.__load_esp(fdct_esp)
        assert self.__dct_esp is not None

        # monta a dialog
        self.setupUi(self)

        # configura título da dialog
        self.setWindowTitle(u"Procedimento de Espera")

        # configurações de conexões slot/signal
        self.__config_connects()

        # configurações de títulos e mensagens da janela de edição
        self.__config_texts()

        # restaura as configurações da janela de edição
        self.__restore_settings()

        # coloca as esperas na comboBox
        self.cbx_esp.addItems(sorted(self.__dct_esp.values()))

        # configura botões
        self.bbx_espera.button(QtGui.QDialogButtonBox.Cancel).setText("&Cancela")
        self.bbx_espera.button(QtGui.QDialogButtonBox.Ok).setFocus()

        # inicia os parâmetros da espera
        self.__update_command()

    # ---------------------------------------------------------------------------------------------
    def __config_connects(self):
        """
        configura as conexões slot/signal
        """
        # conecta spinBox
        self.cbx_esp.currentIndexChanged.connect(self.__on_cbx_currentIndexChanged)

    # ---------------------------------------------------------------------------------------------
    def __config_texts(self):
        """
        DOCUMENT ME!
        """
        # configura títulos e mensagens
        self.__txt_settings = "CDlgEspera"

    # ---------------------------------------------------------------------------------------------
    def get_data(self):
        """
        DOCUMENT ME!
        """
        # return command line
        return self.lbl_comando.text()

    # ---------------------------------------------------------------------------------------------
    def __load_esp(self, fdct_esp):
        """
        carrega o dicionário de esperas
        """
        # clear to go
        assert self.__sck_http is not None
        assert self.__dct_config is not None

        # resposta
        ldct_ans = {}

        # dicionário vazio ?
        if not fdct_esp:
            # monta o request das esperas
            ls_req = "data/esp.json"

            # get server address
            l_srv = self.__dct_config.get("srv.addr", None)

            if l_srv is not None:
                # obtém os dados de esperas do servidor
                l_data = self.__sck_http.get_data(l_srv, ls_req)

                if l_data is not None:
                    # coloca a esperas no dicionário
                    ldct_ans = json.loads(l_data)

                # senão, não achou no servidor...
                else:
                    # logger
                    l_log = logging.getLogger("CDlgEspera::__load_esp")
                    l_log.setLevel(logging.ERROR)
                    l_log.error(u"<E01: tabela de esperas não existe no servidor.")

            # senão, não achou endereço do servidor
            else:
                # logger
                l_log = logging.getLogger("CDlgEspera::__load_esp")
                l_log.setLevel(logging.WARNING)
                l_log.warning(u"<E02: srv.addr não existe na configuração.")

        # senão,...
        else:
            # para todas as esperas...
            for l_esp in fdct_esp.values():
                # coloca na resposta
                ldct_ans[l_esp.i_prc_id] = l_esp.s_prc_desc

        # return
        return ldct_ans

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
        # para todas as esperas...
        for l_key, l_esp in self.__dct_esp.iteritems():
            # é a espera selecionada ?
            if self.cbx_esp.currentText() == l_esp:
                break

        # inicia o comando
        ls_cmd = "ESP {}".format(l_key)

        # coloca o comando no label
        self.lbl_comando.setText(ls_cmd)

    # =============================================================================================
    # edição de campos
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSignature("int")
    def __on_cbx_currentIndexChanged(self, f_val):
        """
        DOCUMENT ME!
        """
        # atualiza comando
        self.__update_command()

# < the end >--------------------------------------------------------------------------------------
