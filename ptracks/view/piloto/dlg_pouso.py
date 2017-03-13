#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
dlg_pouso

mantém as informações sobre a dialog de pouso

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
import json
import os

# PyQt library
from PyQt4 import QtCore
from PyQt4 import QtGui

# view
import ptracks.view.piloto.dlg_pouso_ui as dlg

# < class CDlgPouso >------------------------------------------------------------------------------

class CDlgPouso(QtGui.QDialog, dlg.Ui_CDlgPouso):
    """
    mantém as informações sobre a dialog de pouso
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, fsck_http, fdct_config, f_strip_cur, flst_pouso, f_parent=None):
        """
        @param fsck_http: socket de comunicação com o servidor
        @param fdct_config: dicionário de configuração
        @param f_strip_cur: strip selecionada
        @param flst_pouso: lista de pousos
        @param f_parent: janela pai
        """
        # init super class
        super(CDlgPouso, self).__init__(f_parent)

        # socket de comunicação
        self.__sck_http = fsck_http
        assert self.__sck_http

        # dicionário de configuração
        self.__dct_config = fdct_config
        assert self.__dct_config is not None

        # strip atual
        self.__strip_cur = f_strip_cur
        assert self.__strip_cur is not None

        # lista de pousos
        self.__lst_pouso = flst_pouso
        assert self.__lst_pouso is not None

        # monta a dialog
        self.setupUi(self)

        # configura título da dialog
        self.setWindowTitle(u"Procedimento de Pouso")

        # configurações de conexões slot/signal
        self.__config_connects()

        # configurações de títulos e mensagens da janela de edição
        self.__config_texts()

        # restaura as configurações da janela de edição
        self.__restore_settings()

        # lista de pousos vazia ?
        if not self.__lst_pouso:
            # carrega a lista
            self.__load_pouso()

        # inicia valores
        self.cbx_pouso.addItems(sorted(self.__lst_pouso))

        # configura botões
        self.bbx_pouso.button(QtGui.QDialogButtonBox.Cancel).setText("&Cancela")
        self.bbx_pouso.button(QtGui.QDialogButtonBox.Ok).setFocus()

        # inicia os parâmetros do pouso
        self.__update_command()

    # ---------------------------------------------------------------------------------------------
    def __config_connects(self):
        """
        configura as conexões slot/signal
        """
        # conecta comboBox
        self.cbx_pouso.currentIndexChanged.connect(self.__on_cbx_currentIndexChanged)

    # ---------------------------------------------------------------------------------------------
    def __config_texts(self):
        """
        DOCUMENT ME!
        """
        # configura títulos e mensagens
        self.__txt_settings = "CDlgPouso"

    # ---------------------------------------------------------------------------------------------
    def get_data(self):
        """
        DOCUMENT ME!
        """
        # return command line
        return self.lbl_comando.text()

    # ---------------------------------------------------------------------------------------------
    def __load_pouso(self):
        """
        carrega a lista de pousos
        """
        # check for requirements
        assert self.__sck_http is not None
        assert self.__dct_config is not None
        assert self.__lst_pouso is not None

        # monta o request dos pousos
        ls_req = "data/arr.json"

        # get server address
        l_srv = self.__dct_config.get("srv.addr", None)

        if l_srv is not None:
            # obtém os dados de pousos do servidor
            l_data = self.__sck_http.get_data(l_srv, ls_req)

            if l_data is not None:
                # coloca o pouso na lista
                self.__lst_pouso.update(json.loads(l_data))

            # senão, não achou no servidor...
            else:
                # logger
                l_log = logging.getLogger("CDlgPouso::__load_pouso")
                l_log.setLevel(logging.ERROR)
                l_log.error(u"<E01: tabela de pousos não existe no servidor.")

        # senão, não achou endereço do servidor
        else:
            # logger
            l_log = logging.getLogger("CDlgPouso::__load_pouso")
            l_log.setLevel(logging.WARNING)
            l_log.warning(u"<E02: srv.addr não existe na configuração.")

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
        # para todas os pousos...
        for l_pouso in self.__lst_pouso:
            # é o pouso selecionada ?
            if unicode(self.cbx_pouso.currentText()) == unicode(l_pouso):
                break

        # pouso
        ls_cmd = "ARR {}".format(l_pouso)

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
