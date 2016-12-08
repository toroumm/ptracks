#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
dlg_fix_data_new

mantém as informações sobre a dialog de edição da tabela de fixos

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

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.1$"
__author__ = "Milton Abrunhosa"
__date__ = "2014/11"

# < imports >--------------------------------------------------------------------------------------

# python library
import os
import sys

# PyQt library
from PyQt4 import QtCore
from PyQt4 import QtGui

# model
import model.newton.defs_newton as ldefs
import model.items.fix_data as dctfix

# view
import view.dbedit.dlg_fix_edit_new as dlgfix
import view.dbedit.dlg_fix_data_new_ui as dlgfix_ui

# control
import control.events.events_basic as events

# < class CDlgFixDataNEW >-------------------------------------------------------------------------

class CDlgFixDataNEW (QtGui.QDialog, dlgfix_ui.Ui_CDlgFixDataNEW):
    """
    mantém as informações sobre a dialog de edição da tabela de fixos
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control, f_parent=None):
        """
        constructor
        cria a dialog de edição da tabela de fixos

        @param f_control: control manager do editor da base de dados
        @param f_parent: janela vinculada
        """
        # check input
        assert f_control

        # init super class
        super(CDlgFixDataNEW, self).__init__(f_parent)

        # control manage
        self.__control = f_control

        # event manager
        self.__event = f_control.event
        assert self.__event

        # gerente de configuração
        self.__config = f_control.config
        assert self.__config

        # dicionário de configuração
        self.__dct_config = self.__config.dct_config
        assert self.__dct_config

        # model manager
        self.__model = f_control.model
        assert self.__model

        # parent window
        self.__parent = f_parent

        # existe uma parent window ?
        if self.__parent is not None:
            # esconde a parent window
            self.__parent.setVisible(False)

        # pointer para o item corrente
        self.__fix = None

        # pointer para o dicionário a editar
        self.__dct_fix = None

        # monta a dialog
        self.setupUi(self)

        # configurações de conexões slot/signal
        self.__config_connects()

        # configurações de títulos e mensagens da janela de edição
        self.__config_texts()

        # restaura as configurações da janela de edição
        self.__restore_settings()

        # configura título da dialog
        self.setWindowTitle(u"Edição de Fixos")

        # faz a carrga inicial do diretório de fixos
        QtCore.QTimer.singleShot(0, self.__load_initial)

    # ---------------------------------------------------------------------------------------------
    def accept(self):
        """
        callback de btnOk da dialog de edição. faz o accept da dialog
        """
        # ok para continuar ?
        if self.__ok2continue():
            # faz o "accept"
            QtGui.QDialog.accept(self)

            # fecha a janela de edição
            self.close()

    # ---------------------------------------------------------------------------------------------
    def closeEvent(self, f_evt):
        """
        callback de tratamento do evento Close

        @param f_evt: evento
        """
        # ok para continuar ?
        if self.__ok2continue():
            # obtém os settings
            l_set = QtCore.QSettings()
            assert l_set

            # salva geometria da janela
            l_set.setValue("%s/Geometry" % (self.__txt_settings), QtCore.QVariant(self.saveGeometry()))

            # existe a parent window ?
            if self.__parent is not None:
                # exibe a parent window
                self.__parent.setVisible(True)

        # senão, ignora o request
        else:
            # ignora o evento
            f_evt.ignore()

    # ---------------------------------------------------------------------------------------------
    def __config_connects(self):
        """
        configura as conexões slot/signal
        """
        # fixo

        # conecta click a remoção de fixo
        self.btn_del.clicked.connect(self.__fix_del)
        '''
        # conecta click a edição de fixo
        self.btnEdit.clicked.connect(self.fixEdit)
        '''
        # conecta click a inclusão de fixo
        self.btn_new.clicked.connect(self.__fix_new)

        # conecta click a seleção da linha
        self.qtw_fixos.itemSelectionChanged.connect(self.__fix_select)

        # conecta botão Ok
        self.dbb_fixos.accepted.connect(self.accept)

        # conecta botão Cancela
        self.dbb_fixos.rejected.connect(self.reject)

        # configura botões
        self.dbb_fixos.button(QtGui.QDialogButtonBox.Cancel).setText("&Cancela")
        self.dbb_fixos.button(QtGui.QDialogButtonBox.Ok).setFocus()

    # ---------------------------------------------------------------------------------------------
    def __config_texts(self):
        """
        configura títulos e mensagens
        """
        self.__txt_settings = "CDlgFixDataNEW"

        # self.__txt_continue_tit = u"Alterações pendentes"
        # self.__txt_continue_msg = u"Salva alterações pendentes ?"

        self.__txt_del_tit = u"Apaga fixo"
        self.__txt_del_msg = u"Apaga fixo {0} ?"

    # ---------------------------------------------------------------------------------------------
    def __fix_del(self):
        """
        callback de btnDel da dialog de edição. deleta um fixo da lista
        """
        # clear to go
        assert self.qtw_fixos is not None
        assert self.__dct_fix is not None

        # obtém o fixo selecionado
        self.__fix = self.__get_current_sel(self.__dct_fix, self.qtw_fixos)

        if self.__fix is not None:
            # apaga o fixo atual ?
            if QtGui.QMessageBox.Yes == QtGui.QMessageBox.question(self, self.__txt_del_tit,
                                            self.__txt_del_msg.format(self.__fix.s_fix_indc), 
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No):

                # apaga o fixo
                self.__fix_remove(self.__fix)

    # ---------------------------------------------------------------------------------------------
    '''
    def fixEdit ( self ):
        """
        callback de btnEdit da dialog de edição. edita um fixo da QTableWidget
        """
        # clear to go
        assert self.qtw_fixos is not None
        assert self.__dct_fix is not None

        # obtém o fixo selecionado
        self.__fix = self.__get_current_sel(self.__dct_fix, self.qtw_fixos)

        if self.__fix is not None:
            # cria a dialog de edição de fixos
            l_dlg = CDlgFixEditNEW.CDlgFixEditNEW(self.__control, self.__fix, self)
            assert l_dlg

            # processa a dialog de edição de fixos (modal)
            if l_dlg.exec_():
                # salva em disco as alterações no fixo
                # self.__fix.save2Disk(self.__fix._sPN)

                # se ok, atualiza a QTableWidget de fixos
                self.__fix_update_widget()
    '''
    # ---------------------------------------------------------------------------------------------
    def __fix_new(self):
        """
        callback de btnNew da dialog de edição. cria um novo fixo na lista
        """
        # cria a dialog de edição de fixos
        l_dlg = dlgfix.CDlgFixEditNEW(self.__control, None, self)
        assert l_dlg

        # processa a dialog de edição de fixos (modal)
        if l_dlg.exec_():
            # obtém os dados da edição
            self.__fix = l_dlg.get_data()

            # fixo existente ?
            if (self.__fix is not None) and (self.__dct_fix is not None):
                # insere o fixo na lista
                self.__dct_fix.append(self.__fix)

                # salva o arquivo no disco
                # self.__fix.save2Disk(ls_path)

                # se ok, atualiza a QTableWidget de fixos
                self.__fix_update_widget()

    # ---------------------------------------------------------------------------------------------
    def __fix_remove(self, fo_fix):
        """
        remove o fixo selecionado

        @param fo_fix: pointer para o fixo a remover
        """
        # clear to go
        assert fo_fix is not None

        # remove a linha da widget
        self.qtw_fixos.removeRow(self.qtw_fixos.currentRow())

        # remove o fixo da lista
        self.__dct_fix.remove(fo_fix)

    # ---------------------------------------------------------------------------------------------
    def __fix_select(self):
        """
        seleciona o fixo a editar
        """
        # clear to go
        assert self.__dct_fix is not None
        assert self.qtw_fixos is not None

        # obtém o fixo selecionado
        self.__fix = self.__get_current_sel(self.__dct_fix, self.qtw_fixos)
        assert self.__fix

        # atualiza a área de dados do fixo selecionado
        self.__fix_update_sel()

    # ---------------------------------------------------------------------------------------------
    def __fix_update_list(self):
        """
        atualiza na tela os dados da lista de fixos
        """
        # clear to go
        assert self.__dct_fix is not None
        assert self.qtw_fixos is not None

        # atualiza a QTableWidget de fixos
        self.__fix_update_widget()

        # obtém o fixo selecionado
        self.__fix = self.__get_current_sel(self.__dct_fix, self.qtw_fixos)

    # ---------------------------------------------------------------------------------------------
    def __fix_update_sel(self):
        """
        atualiza na tela os dados do fixo selecionado
        """
        # fixo selecionado existe ?
        if self.__fix is not None:
            # indicativo do fixo
            ls_fix_indc = self.__fix.s_fix_indc

            # identificação
            self.txt_indc.setText(self.__fix.s_fix_indc)
            self.qle_desc.setText(self.__fix.s_fix_desc)

            # tipo de fixo

            # VOR
            if ldefs.E_VOR == self.__fix.en_fix_tipo:
                self.ckx_vor.setCheckState(QtCore.Qt.Checked)

            else:
                self.ckx_vor.setCheckState(QtCore.Qt.Unchecked)

            # NDB
            if ldefs.E_NDB == self.__fix.en_fix_tipo:
                self.ckx_ndb.setCheckState(QtCore.Qt.Checked)

            else:
                self.ckx_ndb.setCheckState(QtCore.Qt.Unchecked)

            # DME
            if ldefs.E_DME == self.__fix.en_fix_tipo:
                self.ckx_dme.setCheckState(QtCore.Qt.Checked)

            else:
                self.ckx_dme.setCheckState(QtCore.Qt.Unchecked)

            # freqüência
            self.dsb_freq.setValue(self.__fix.f_fix_freq)

            # posição
            self.__fix.f_fix_lat = None
            self.__fix.f_fix_lng = None

            # l_iX, l_iY = self.__fix.oCentro.getPto ()

            # self.txtCntrX.setText ( str ( l_iX ))
            # self.txtCntrY.setText ( str ( l_iY ))

        # senão, o fixo não existe
        else:
            # posiciona cursor no início do formulário
            self.txt_indc.setFocus()

    # ---------------------------------------------------------------------------------------------
    def __fix_update_widget(self):
        """
        atualiza na tela os dados da QTableWidget de fixos
        """
        # clear to go
        assert self.qtw_fixos is not None
        assert self.__dct_fix is not None

        # limpa a QTableWidget
        self.qtw_fixos.clear()

        # seta o número de linhas da QTableWidget para o tamanho da lista
        self.qtw_fixos.setRowCount(len(self.__dct_fix))

        # seta número de colunas e cabeçalho das colunas
        self.qtw_fixos.setColumnCount(2)
        self.qtw_fixos.setHorizontalHeaderLabels([u"Indicativo", u"Descrição"])

        # seta QTableWidget
        self.qtw_fixos.setAlternatingRowColors(True)
        self.qtw_fixos.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        self.qtw_fixos.setSelectionBehavior(QtGui.QTableWidget.SelectRows)
        self.qtw_fixos.setSelectionMode(QtGui.QTableWidget.SingleSelection)
        self.qtw_fixos.setSortingEnabled(False)

        # linha 0 (objeto fixo)
        lo_A0 = None

        # linha selecionada (objeto fixo)
        lo_sel_item = None

        # para cada fixo no dicionário...
        for li_ndx, ls_fix_indc in enumerate(sorted(self.__dct_fix.keys())):
            # indicativo do fixo
            ltwi_fix_indc = QtGui.QTableWidgetItem(ls_fix_indc)
            ltwi_fix_indc.setData(QtCore.Qt.UserRole, QtCore.QVariant(ls_fix_indc))

            self.qtw_fixos.setItem(li_ndx, 0, ltwi_fix_indc)

            # é o fixo selecionado ?
            if (self.__fix is not None) and (self.__fix.s_fix_indc == ls_fix_indc):
                # salva pointer para o item selecionado
                lo_sel_item = ltwi_fix_indc

            # obtém o fixo
            lo_fix = self.__dct_fix[ls_fix_indc]
            assert lo_fix

            # descrição
            ltwi_fix_desc = QtGui.QTableWidgetItem(lo_fix.s_fix_desc)

            self.qtw_fixos.setItem(li_ndx, 1, ltwi_fix_desc)

        # existe um fixo selecionado ?
        if self.__fix is not None:
            # seleciona o item
            self.qtw_fixos.setCurrentItem(lo_sel_item)

            # posiciona no item selecionado
            self.qtw_fixos.scrollToItem(lo_sel_item)

            # marca que existe seleção
            lo_sel_item.setSelected(True)

        # senão, não existe um fixo selecionado
        else:
            # seleciona a primeira linha
            self.qtw_fixos.selectRow(0)

            # obtém o fixo atual
            self.__fix = self.__get_current_sel(self.__dct_fix, self.qtw_fixos)

        # ajusta o tamanho das colunas pelo conteúdo
        self.qtw_fixos.resizeColumnsToContents()

        # habilita a ordenação
        self.qtw_fixos.setSortingEnabled(True)

    # ---------------------------------------------------------------------------------------------
    def __get_current_data(self, fqtw_tab, fi_col):
        """
        retorna os dados associados a linha selecionada
        """
        # clear to go
        assert fqtw_tab is not None

        # o dado da linha selecionada
        ls_data = ""

        # obtém o item da linha selecionada
        lo_item = self.__get_current_item(fqtw_tab, fi_col)

        # existe uma linha selecionada ?
        if lo_item is not None:
            # obtém o dado associado a linha
            ls_data = lo_item.data(QtCore.Qt.UserRole).toString()

        # retorna o dado associado a linha selecionada
        return ls_data

    # ---------------------------------------------------------------------------------------------
    def __get_current_item(self, fqtw_tab, fi_col):
        """
        retorna o item associado a linha selecionada
        """
        # clear to go
        assert fqtw_tab is not None

        # o item selecionado
        lo_item = None

        # obtém o número da linha selecionada
        li_row = fqtw_tab.currentRow()

        # existe uma linha selecionada ?
        if li_row > -1:
            # obtém o item associado
            lo_item = fqtw_tab.item(li_row, fi_col)
            assert lo_item

        # retorna o item selecionado na lista
        return lo_item

    # ---------------------------------------------------------------------------------------------
    def __get_current_sel(self, f_dct, f_qtw):
        """
        retorna o elemento associado a linha selecionada na lista
        """
        # clear to go
        assert f_dct is not None
        assert f_qtw is not None

        # obtém o index da linha selecionada
        ls_indc = str(self.__get_current_data(f_qtw, 0))

        # indice válido ?
        if ls_indc in f_dct:
            # obtém o elemento selecionado se existir uma linha selecionada
            lo_sel = f_dct[ls_indc]
            assert lo_sel

        # senão, índice inválido
        else:
            # não há elemento selecionado
            lo_sel = None

        # retorna o elemento da linha selecionada na lista
        return lo_sel

    # ---------------------------------------------------------------------------------------------
    def __load_initial(self):
        """
        faz a carga inicial da tabela de fixos
        """
        # dicionário de fixos
        self.__dct_fix = self.__model.dct_fix

        # o dicionário de fixos não existe ?
        if self.__dct_fix is None:
            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # cai fora...
            sys.exit(1)

        # atualiza na tela os dados da tabela de fixos
        self.__fix_update_list()

    # ---------------------------------------------------------------------------------------------
    def __ok2continue(self):
        """
        cria uma messageBox

        @return True se tratou a resposta, senão False
        """
        # resposta
        lv_ans = True
        '''
        # flag de alterações setado ?
        if ( self.__bChanged ):

            # questiona sobre alterações pendentes
            l_Resp = QtGui.QMessageBox.question ( self, self.__txt_continue_tit,
                                                        self.__txt_continue_msg,
                                                        QtGui.QMessageBox.Yes |
                                                        QtGui.QMessageBox.No |
                                                        QtGui.QMessageBox.Cancel )

            # cancela ?
            if ( QtGui.QMessageBox.Cancel == l_Resp ):
                # não sai
                lv_ans = False

            # salva ?
            elif ( QtGui.QMessageBox.Yes == l_Resp ):
                # salva as pendências e sai
                lv_ans = True

            # não salva ?
           else:
               # reseta o flag de alterações...
               self.__bChanged = False

               # ...e sai
               lv_ans = True
        '''
        # retorna a resposta
        return lv_ans

    # ---------------------------------------------------------------------------------------------
    def reject(self):
        """
        DOCUMENT ME!
        """
        # fixo em edição
        self.__fix = None

        # faz o "reject"
        QtGui.QDialog.reject(self)

        # close dialog
        self.close()

    # ---------------------------------------------------------------------------------------------
    def __restore_settings(self):
        """
        restaura as configurações salvas para esta janela
        """
        # obtém os settings
        l_set = QtCore.QSettings()
        assert l_set

        # restaura geometria da janela
        self.restoreGeometry(l_set.value("%s/Geometry" % (self.__txt_settings)).toByteArray())

        # return
        return True

# < the end >--------------------------------------------------------------------------------------
