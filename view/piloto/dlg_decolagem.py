#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
dlg_decolagem

mantém as informações sobre a dialog de decolagem

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
import view.piloto.dlg_decolagem_ui as dlg

# < class CDlgDecolagem >--------------------------------------------------------------------------

class CDlgDecolagem(QtGui.QDialog, dlg.Ui_CDlgDecolagem):
    """
    mantém as informações sobre a dialog de decolagem
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, fsck_http, fdct_config, f_strip_cur, flst_dep, f_parent=None):
        """
        @param fsck_http: socket de comunicação com o servidor
        @param fdct_config: dicionário de configuração
        @param f_strip_cur: strip selecionada
        @param flst_dep: lista de decolagens
        @param f_parent: janela pai
        """
        # init super class
        super(CDlgDecolagem, self).__init__(f_parent)

        # socket de comunicação
        self.__sck_http = fsck_http
        assert self.__sck_http
        
        # dicionário de configuração
        self.__dct_config = fdct_config
        assert self.__dct_config is not None

        # strip atual
        self.__strip_cur = f_strip_cur
        assert self.__strip_cur is not None

        # lista de decolagens
        self.__lst_dep = flst_dep
        assert self.__lst_dep is not None
                
        # monta a dialog
        self.setupUi(self)

        # configura título da dialog
        self.setWindowTitle(u"Procedimento de Decolagem")

        # configurações de conexões slot/signal
        self.__config_connects()

        # configurações de títulos e mensagens da janela de edição
        self.__config_texts()

        # restaura as configurações da janela de edição
        self.__restore_settings()

        # lista de decolagens vazia ?
        if not self.__lst_dep:
            # carrega a lista
            self.__load_dep()

        # inicia valores
        self.cbx_dep.addItems(sorted(self.__lst_dep))

        # configura botões
        self.bbx_dep.button(QtGui.QDialogButtonBox.Cancel).setText("&Cancela")
        self.bbx_dep.button(QtGui.QDialogButtonBox.Ok).setFocus()

        # inicia os parâmetros da decolagem
        self.__update_command()

    # ---------------------------------------------------------------------------------------------
    def __config_connects(self):
        """
        configura as conexões slot/signal
        """
        # conecta comboBox
        self.cbx_dep.currentIndexChanged.connect(self.__on_cbx_currentIndexChanged)

    # ---------------------------------------------------------------------------------------------
    def __config_texts(self):
        """
        DOCUMENT ME!
        """
        # configura títulos e mensagens
        self.__txt_settings = "CDlgDecolagem"

    # ---------------------------------------------------------------------------------------------
    def get_data(self):
        """
        DOCUMENT ME!
        """
        # return command line
        return self.lbl_comando.text()

    # ---------------------------------------------------------------------------------------------
    def __load_dep(self):
        """
        carrega a lista de decolagens
        """
        # clear to go
        assert self.__sck_http is not None
        assert self.__dct_config is not None
        assert self.__lst_dep is not None
                
        # monta o request das decolagens
        ls_req = "data/dep.json"

        # get server address
        l_srv = self.__dct_config.get("srv.addr", None)
        
        if l_srv is not None:
            # obtém os dados de decolagens do servidor
            l_dict = self.__sck_http.get_data(l_srv, ls_req)

            if l_dict is not None:
                # coloca a decolagens na lista
                self.__lst_dep.update(json.loads(l_dict))

            # senão, não achou no servidor...
            else:
                # logger
                l_log = logging.getLogger("CDlgDecolagem::__load_dep")
                l_log.setLevel(logging.ERROR)
                l_log.error(u"<E01: tabela de decolagens não existe no servidor.")

        # senão, não achou endereço do servidor
        else:
            # logger
            l_log = logging.getLogger("CDlgDecolagem::__load_dep")
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
        # para todas as decolagens...
        for l_dep in self.__lst_dep:
            # é a decolagem selecionada ?
            if self.cbx_dep.currentText() == l_dep:
                break

        # decolagem
        ls_cmd = "DEP {}".format(l_dep)

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
