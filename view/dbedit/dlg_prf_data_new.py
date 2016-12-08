#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
dlg_prf_data_new

mantém as informações sobre a dialog de edição da tabela de performances

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

# view
import view.dbedit.dlg_prf_edit_new as dlgprf
import view.dbedit.dlg_prf_data_new_ui as dlgprf_ui

# control
import control.events.events_basic as events

# < class CDlgPrfDataNEW >---------------------------------------------------------------------------

class CDlgPrfDataNEW (QtGui.QDialog, dlgprf_ui.Ui_CDlgPrfDataNEW):
    """
    mantém as informações sobre a dialog de edição da tabela de performances
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control, f_parent=None):
        """
        constructor

        @param f_control: control manager
        @param f_parent: parent widget
        """
        # check input
        assert f_control

        # init super class
        super(CDlgPrfDataNEW, self).__init__(f_parent)

        # control manager
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

        # pointer para os itens correntes
        self.__prf = None

        # pointer para o dicionário a editar
        self.__dct_prf = None

        # monta a dialog
        self.setupUi(self)

        # configurações de conexões slot/signal
        self.__config_connects()

        # configurações de títulos e mensagens da janela de edição
        self.__config_texts()

        # restaura as configurações da janela de edição
        self.__restore_settings()

        # configura título da dialog
        self.setWindowTitle(u"Edição de Performances")

        # faz a carrga inicial do diretório de performances
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

        @param f_evt: event
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
        # performance

        # conecta click a remoção de performance
        self.btn_del.clicked.connect(self.prf_del)
        '''
        # conecta click a edição de performance
        self.btn_edit.clicked.connect(self.prf_edit)
        '''
        # conecta click a inclusão de performance
        self.btn_new.clicked.connect(self.prf_new)

        # conecta click a seleção da linha
        self.qtw_perfs.itemSelectionChanged.connect(self.prf_select)

        # conecta botão Ok
        self.dbb_perfs.accepted.connect(self.accept)

        # conecta botão Cancela
        self.dbb_perfs.rejected.connect(self.reject)

        # configura botões
        self.dbb_perfs.button(QtGui.QDialogButtonBox.Cancel).setText("&Cancela")
        self.dbb_perfs.button(QtGui.QDialogButtonBox.Ok).setFocus()

    # ---------------------------------------------------------------------------------------------
    def __config_texts(self):
        """
        configura títulos e mensagens
        """
        self.__txt_settings = "CDlgPrfDataNEW"
        '''
        self.__txt_continue_tit = u"Alterações pendentes"
        self.__txt_continue_msg = u"Salva alterações pendentes ?"
        '''
        self.__txt_del_tit = u"Apaga performance"
        self.__txt_del_msg = u"Apaga performance {0} ?"

    # ---------------------------------------------------------------------------------------------
    def prf_del(self):
        """
        callback de btn_del da dialog de edição. deleta um performance da lista
        """
        # clear to go
        assert self.qtw_perfs is not None
        assert self.__dct_prf is not None

        # performance selecionada
        self.__prf = self.__get_current_sel(self.__dct_prf, self.qtw_perfs)

        if self.__prf is not None:
            # apaga a performance atual ?
            if QtGui.QMessageBox.Yes == QtGui.QMessageBox.question(self, self.__txt_del_tit,
                                            self.__txt_del_msg.format(self.__prf.s_prf_id),
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No):
                # apaga a performance
                self.__prf_remove(self.__prf)

    # ---------------------------------------------------------------------------------------------
    '''
    def prf_edit ( self ):
        """
        callback de btn_edit da dialog de edição. edita um performance da QTableWidget
        """
        # clear to go
        assert self.qtw_perfs is not None
        assert self.__dct_prf is not None

        # obtém a performance selecionado
        self.__prf = self.__get_current_sel(self.__dct_prf, self.qtw_perfs)

        if self.__prf is not None:
            # cria a dialog de edição de performances
            l_dlg = dlgprf.dlgPrfEditNEW(self.__control, self.__prf, self)
            assert l_dlg

            # processa a dialog de edição de performances (modal)
            if l_dlg.exec_():
                # salva em disco as alterações na performance
                # self.__prf.save2Disk(self.__prf._sPN)

                # se ok, atualiza a QTableWidget de performances
                self.__prf_update_widget()
    '''
    # ---------------------------------------------------------------------------------------------
    def prf_new(self):
        """
        callback de btn_new da dialog de edição. cria um nova performance na lista
        """
        # cria a dialog de edição de performances
        l_dlg = dlgprf.CDlgPrfEditNEW(self.__control, None, self)
        assert l_dlg

        # processa a dialog de edição de performances (modal)
        if l_dlg.exec_():
            # obtém os dados da edição
            self.__prf = l_dlg.get_data()

            # performance existente ?
            if (self.__prf is not None) and (self.__dct_prf is not None):
                # insere a performance na lista
                self.__dct_prf.append(self.__prf)

                # arquivo no disco
                # self.__prf.save2Disk(ls_path)

                # se ok, atualiza a QTableWidget de performances
                self.__prf_update_widget()

    # ---------------------------------------------------------------------------------------------
    def __prf_remove(self, fo_prf):
        """
        remove a performance selecionada

        @param  fo_prf : pointer para a performance a remover
        """
        # clear to go
        assert fo_prf is not None

        # remove a linha da widget
        self.qtw_perfs.removeRow(self.qtw_perfs.currentRow())

        # remove a performance da lista
        self.__dct_prf.remove(fo_prf)

    # ---------------------------------------------------------------------------------------------
    def prf_select(self):
        """
        seleciona um performance a editar
        """
        # clear to go
        assert self.__dct_prf is not None
        assert self.qtw_perfs is not None

        # obtém a performance selecionado
        self.__prf = self.__get_current_sel(self.__dct_prf, self.qtw_perfs)
        assert self.__prf

        # atualiza a área de dados da performance selecionado
        self.__prf_update_sel()

    # ---------------------------------------------------------------------------------------------
    def prf_update_list(self):
        """
        atualiza na tela os dados da lista de performances
        """
        # clear to go
        assert self.__dct_prf is not None
        assert self.qtw_perfs is not None

        # atualiza a QTableWidget de performances
        self.__prf_update_widget()

        # obtém a performance selecionada
        self.__prf = self.__get_current_sel(self.__dct_prf, self.qtw_perfs)

    # ---------------------------------------------------------------------------------------------
    def __prf_update_sel(self):
        """
        atualiza na tela os dados da performance selecionado
        """
        # performance selecionado existe ?
        if self.__prf is not None:
            # indicativo da performance
            ls_prf_id = self.__prf.s_prf_id

            # identificação
            self.txt_id.setText(self.__prf.s_prf_id)
            self.qle_desc.setText(self.__prf.s_prf_desc)
            '''
            # geografia

            # comprimento
            self.txtComp.setText ( str ( self.__prf._uiPrfComp ))

            # largura
            self.txtLarg.setText ( str ( self.__prf._uiPrfLarg ))

            # diferença de declinação magnética
            self.txtDecl.setText ( str ( self.__prf._fPrfDeclMag ))

            # ARP
            l_iX, l_iY = self.__prf._oCentro.getPto ()

            self.txtCntrX.setText ( str ( l_iX ))
            self.txtCntrY.setText ( str ( l_iY ))

            # altitude
            self.txtAlt.setText ( str ( self.__prf._uiPrfAlt ))
            '''
        # senão, a performance não existe
        else:
            # posiciona cursor no início do formulário
            self.txt_id.setFocus()

    # ---------------------------------------------------------------------------------------------
    def __prf_update_widget(self):
        """
        atualiza na tela os dados da QTableWidget de performances
        """
        # clear to go
        assert self.qtw_perfs is not None
        assert self.__dct_prf is not None

        # limpa a QTableWidget
        self.qtw_perfs.clear()

        # seta o número de linhas da QTableWidget para o tamanho da lista
        self.qtw_perfs.setRowCount(len(self.__dct_prf))

        # seta número de colunas e cabeçalho das colunas
        self.qtw_perfs.setColumnCount(2)
        self.qtw_perfs.setHorizontalHeaderLabels([u"Indicativo", u"Descrição"])

        # seta QTableWidget
        self.qtw_perfs.setAlternatingRowColors(True)
        self.qtw_perfs.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        self.qtw_perfs.setSelectionBehavior(QtGui.QTableWidget.SelectRows)
        self.qtw_perfs.setSelectionMode(QtGui.QTableWidget.SingleSelection)
        self.qtw_perfs.setSortingEnabled(False)

        # linha 0 (objeta performance)
        lo_A0 = None

        # linha selecionada (objeta performance)
        lo_sitem = None

        # para cada performance no dicionário...
        for li_ndx, ls_prf_id in enumerate(sorted(self.__dct_prf.keys())):
            # indicativo da performance
            ltwi_id = QtGui.QTableWidgetItem(ls_prf_id)
            ltwi_id.setData(QtCore.Qt.UserRole, QtCore.QVariant(ls_prf_id))

            self.qtw_perfs.setItem(li_ndx, 0, ltwi_id)

            # é a performance selecionado ?
            if (self.__prf is not None) and (self.__prf.s_prf_id == ls_prf_id):
                # salva pointer para o item selecionado
                lo_sitem = ltwi_id

            # obtém a performance
            lo_prf = self.__dct_prf[ls_prf_id]
            assert lo_prf

            # descrição
            ltwi_desc = QtGui.QTableWidgetItem(lo_prf.s_prf_desc)

            self.qtw_perfs.setItem(li_ndx, 1, ltwi_desc)

        # existe um performance selecionado ?
        if self.__prf is not None:
            # seleciona o item
            self.qtw_perfs.setCurrentItem(lo_sitem)

            # posiciona no item selecionado
            self.qtw_perfs.scrollToItem(lo_sitem)

            # marca que existe seleção
            lo_sitem.setSelected(True)

        # senão, não existe um performance selecionado
        else:
            # seleciona a primeira linha
            self.qtw_perfs.selectRow(0)

            # obtém a performance atual
            self.__prf = self.__get_current_sel(self.__dct_prf, self.qtw_perfs)

        # ajusta o tamanho das colunas pelo conteúdo
        self.qtw_perfs.resizeColumnsToContents()

        # habilita a ordenação
        self.qtw_perfs.setSortingEnabled(True)

    # ---------------------------------------------------------------------------------------------
    def __get_current_data(self, f_qtw, fi_col):
        """
        retorna os dados associados a linha selecionada
        """
        # clear to go
        assert f_qtw is not None

        # o dado da linha selecionada
        ls_data = ""

        # obtém o item da linha selecionada
        lo_item = self.__get_current_item(f_qtw, fi_col)

        # existe uma linha selecionada ?
        if lo_item is not None:
            # obtém o dado associado a linha
            ls_data = lo_item.data(QtCore.Qt.UserRole).toString()

        # retorna o dado associado a linha selecionada
        return ls_data

    # ---------------------------------------------------------------------------------------------
    def __get_current_item(self, f_qtw, fi_col):
        """
        retorna o item associado a linha selecionada
        """
        # clear to go
        assert f_qtw is not None

        # o item selecionado
        lo_item = None

        # obtém o número da linha selecionada
        li_row = f_qtw.currentRow()

        # existe uma linha selecionada ?
        if li_row > -1:
            # obtém o item associado
            lo_item = f_qtw.item(li_row, fi_col)
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
        ls_id = str(self.__get_current_data(f_qtw, 0))

        # indice válido ?
        if ls_id in f_dct:
            # obtém o elemento selecionado se existir uma linha selecionada
            lo_sel = f_dct[ls_id]
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
        faz a carga inicial da tabela de performances
        """
        # obtém o dicionário de performances
        self.__dct_prf = self.__model.dct_prf

        # o dicionário de performances não existe ?
        if self.__dct_prf is None:
            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # cai fora...
            sys.exit(1)

        # atualiza na tela os dados da tabela de performances
        self.prf_update_list()

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
        if self.__bChanged:
            # questiona sobre alterações pendentes
            l_Resp = QtGui.QMessageBox.question ( self, self.__txt_continue_tit,
                                                        self.__txt_continue_msg,
                                                        QtGui.QMessageBox.Yes |
                                                        QtGui.QMessageBox.No |
                                                        QtGui.QMessageBox.Cancel )

            # cancela ?
            if QtGui.QMessageBox.Cancel == l_Resp:
                # não sai
                lv_ans = False

            # salva ?
            elif QtGui.QMessageBox.Yes == l_Resp:
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
        """
        # reset performance
        self.__prf = None

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
