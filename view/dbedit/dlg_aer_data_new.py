#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
dlg_aer_data_new

mantém as informações sobre a dialog de edição da tabela de aeródromos

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
from PyQt4 import QtGui

# view
import view.dbedit.dlg_aer_edit_new as dlgedit
import view.dbedit.dlg_aer_data_new_ui as dlgnew_ui

# control
import control.events.events_basic as events

# < class CDlgAerDataNEW >---------------------------------------------------------------------------

class CDlgAerDataNEW(QtGui.QDialog, dlgnew_ui.Ui_CDlgAerDataNEW):
    """
    mantém as informações sobre a dialog de edição de aeródromos
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
        super(CDlgAerDataNEW, self).__init__(f_parent)

        # salva o control manager localmente
        self.__control = f_control

        # obtém o dicionário de configuração
        self.__dct_config = f_control.config.dct_config
        assert self.__dct_config

        # obtém o model manager
        self.__model = f_control.model
        assert self.__model

        # salva a parent window localmente
        self.__parent = f_parent

        # existe uma parent window ?
        if self.__parent is not None:
            # esconde a parent window
            self.__parent.setVisible(False)

        # pointer para os itens correntes
        self.__aer = None
        # self._oCab = None
        # self._oPst = None

        # pointer para os dicionários a editar
        self.__dct_aer = None
        # self._dctCab = None
        # self._dctPst = None

        # monta a dialog
        self.setupUi(self)

        # configurações de conexões slot/signal
        self.__config_connects()

        # configurações de títulos e mensagens da janela de edição
        self.__config_texts()

        # restaura as configurações da janela de edição
        self.__restore_settings()

        # configura título da dialog
        self.setWindowTitle(u"Edição de Aeródromos")

        # faz a carrga inicial do diretório de aeródromos
        QtCore.QTimer.singleShot(0, self.__load_initial)

    # ---------------------------------------------------------------------------------------------
    def accept(self):
        """
        callback de btn_ok da dialog de edição. faz o accept da dialog
        """
        # ok para continuar ?
        if self.okToContinue():
            # faz o "accept"
            QtGui.QDialog.accept(self)

            # fecha a janela de edição
            self.close()

    # ---------------------------------------------------------------------------------------------
    def __aer_del(self):
        """
        callback de btn_del_aer da dialog de edição. deleta um aeródromo da lista
        """
        # clear to go
        assert self.qtw_aer is not None
        assert self.__dct_aer is not None

        # obtém o aeródromo selecionado
        self.__aer = self.__get_current_sel(self.__dct_aer, self.qtw_aer)

        if self.__aer is not None:
            # apaga a aeródromo atual ?
            if QtGui.QMessageBox.Yes == QtGui.QMessageBox.question(self,
                                                                   self.__txt_del_aer_Tit,
                                                                   self.__txt_del_aer_Msg.format(self.__aer.s_aer_indc),
               QtGui.QMessageBox.Yes | QtGui.QMessageBox.No):

                # apaga o aeródromo
                self.__aer_remove(self.__aer)
    '''
    # ---------------------------------------------------------------------------------------------
    def __aer_edit(self):
        """
        callback de btnEdit da dialog de edição. edita um aeródromo da QTableWidget
        """
        # clear to go
        assert self.qtw_aer is not None
        assert self.__dct_aer is not None

        # obtém o aeródromo selecionado
        self.__aer = self.__get_current_sel(self.__dct_aer, self.qtw_aer)

        if self.__aer is not None:
            # cria a dialog de edição de aeródromos
            l_dlg = dlgAerEditNEW.dlgAerEditNEW(self.__control, self.__aer, self)
            assert l_dlg

            # processa a dialog de edição de aeródromos (modal)
            if l_dlg.exec_ ():
                # salva em disco as alterações na aeródromo
                # self.__aer.save2Disk(self.__aer._sPN)

                # se ok, atualiza a QTableWidget de aeródromos
                self.__aer_update_widget ()
    '''
    # ---------------------------------------------------------------------------------------------
    def __aer_new(self):
        """
        callback de btnNew da dialog de edição. cria um novo aeródromo na lista
        """
        # cria a dialog de edição de aeródromos
        l_dlg = dlgedit.CDlgAerEditNEW(self.__control, None, self)
        assert l_dlg

        # processa a dialog de edição de aeródromos (modal)
        if l_dlg.exec_():
            # obtém os dados da edição
            self.__aer = l_dlg.get_data()

            # aeródromo existente ?
            if (self.__aer is not None) and (self.__dct_aer is not None):
                # insere a aeródromo na lista
                self.__dct_aer.append(self.__aer)

                # salva o arquivo no disco
                # self.__aer.save2Disk(ls_path)

                # se ok, atualiza a QTableWidget de aeródromos
                self.__aer_update_widget()

    # ---------------------------------------------------------------------------------------------
    def __aer_remove(self, fo_aer):
        """
        remove o aeródromo selecionado

        @param fo_aer: pointer para o aeródromo a remover
        """
        # clear to go
        assert fo_aer is not None

        # remove a linha da widget
        self.qtw_aer.removeRow(self.qtw_aer.currentRow())

        # remove o aeródromo da lista
        self.__dct_aer.remove(fo_aer)
        '''
        # remove o arquivo de pistas associado
        l_sFN = l_sPN + ".pst"

        if (( l_sFN is not None) and os.path.exists(l_sFN) and os.path.isfile(l_sFN)):
            # remove o arquivo
            #os.remove(l_sFN)
        '''
    # ---------------------------------------------------------------------------------------------
    def __aer_select(self):
        """
        seleciona um aeródromo a editar
        """
        # clear to go
        assert self.__dct_aer is not None
        assert self.qtw_aer is not None

        # obtém o aeródromo selecionado
        self.__aer = self.__get_current_sel(self.__dct_aer, self.qtw_aer)

        # atualiza a área de dados do aeródromo selecionado
        self.__aer_update_sel()

    # ---------------------------------------------------------------------------------------------
    def __aer_update_list(self):
        """
        atualiza na tela os dados da lista de aeródromos
        """
        # clear to go
        assert self.__dct_aer is not None
        assert self.qtw_aer is not None

        # atualiza a QTableWidget de aeródromos
        self.__aer_update_widget()

        # obtém o aeródromo selecionado
        self.__aer = self.__get_current_sel(self.__dct_aer, self.qtw_aer)

    # ---------------------------------------------------------------------------------------------
    def __aer_update_sel(self):
        """
        atualiza na tela os dados do aeródromo selecionado
        """
        # aeródromo selecionado existe ?
        if self.__aer is not None:
            # indicativo do aeródromo
            ls_aer_indc = self.__aer.s_aer_indc

            # identificação
            self.txt_indc.setText(self.__aer.s_aer_indc)
            self.qle_desc.setText(self.__aer.s_aer_desc)

            # geografia

            # declinação magnética
            self.dsb_decl.setValue(self.__aer.f_aer_dcl_mag)

            # ARP
            # l_iX, l_iY = self.__aer._oCentro.getPto ()

            # self.txtCntrX.setText(str(l_iX))
            # self.txtCntrY.setText(str(l_iY))

            # elevação
            self.sbx_elev.setValue(self.__aer.f_aer_elev)
            '''
            # lista de pistas do aeródromo
            # self.loadPstList(self.__aer)
            '''
        # senão, o aeródromo não existe
        else:
            # posiciona cursor no início do formulário
            self.txt_indc.setFocus()

    # ---------------------------------------------------------------------------------------------
    def __aer_update_widget(self):
        """
        atualiza na tela os dados da QTableWidget de aeródromos
        """
        # clear to go
        assert self.qtw_aer is not None
        assert self.__dct_aer is not None

        # limpa a QTableWidget
        self.qtw_aer.clear()

        # seta o número de linhas da QTableWidget para o tamanho da lista
        self.qtw_aer.setRowCount(len(self.__dct_aer))

        # seta número de colunas e cabeçalho das colunas
        self.qtw_aer.setColumnCount(2)
        self.qtw_aer.setHorizontalHeaderLabels([u"Indicativo", u"Descrição"])

        # seta QTableWidget
        self.qtw_aer.setAlternatingRowColors(True)
        self.qtw_aer.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        self.qtw_aer.setSelectionBehavior(QtGui.QTableWidget.SelectRows)
        self.qtw_aer.setSelectionMode(QtGui.QTableWidget.SingleSelection)
        self.qtw_aer.setSortingEnabled(False)

        # linha 0 (objeto aeródromo)
        lo_A0 = None

        # linha selecionada (objeto aeródromo)
        lo_sitem = None

        # para cada aeródromo no dicionário...
        for li_ndx, ls_aer_indc in enumerate(sorted(self.__dct_aer.keys())):
            # indicativo do aeródromo
            ltwi_indc = QtGui.QTableWidgetItem(ls_aer_indc)
            ltwi_indc.setData(QtCore.Qt.UserRole, QtCore.QVariant(ls_aer_indc))

            self.qtw_aer.setItem(li_ndx, 0, ltwi_indc)

            # é o aeródromo selecionado ?
            if (self.__aer is not None) and (self.__aer.s_aer_indc == ls_aer_indc):
                # salva pointer para o item selecionado
                lo_sitem = ltwi_indc

            # obtém o aeródromo
            lo_aer = self.__dct_aer[ls_aer_indc]
            assert lo_aer

            # descrição
            ltwi_desc = QtGui.QTableWidgetItem(lo_aer.s_aer_desc)

            self.qtw_aer.setItem(li_ndx, 1, ltwi_desc)

        # existe um aeródromo selecionado ?
        if self.__aer is not None:
            # seleciona o item
            self.qtw_aer.setCurrentItem(lo_sitem)

            # posiciona no item selecionado
            self.qtw_aer.scrollToItem(lo_sitem)

            # marca que existe seleção
            lo_sitem.setSelected(True)

        # senão, não existe um aeródromo selecionado
        else:
            # seleciona a primeira linha
            self.qtw_aer.selectRow(0)

            # obtém o aeródromo atual
            self.__aer = self.__get_current_sel(self.__dct_aer, self.qtw_aer)

        # ajusta o tamanho das colunas pelo conteúdo
        self.qtw_aer.resizeColumnsToContents()

        # habilita a ordenação
        self.qtw_aer.setSortingEnabled(True)
    '''
    # ---------------------------------------------------------------------------------------------
    def cabEdit(self):
        """
        callback de btnEdit da dialog de edição. edita uma cabeceira da QTableWidget
        """
        # clear to go
        assert self.qtwTabCab is not None
        assert self._dctCab is not None

        # obtém a cabeceira selecionada
        self._oCab = self.__get_current_sel(self._dctCab, self.qtwTabCab)

        if self._oCab is not None:
            # cria a dialog de edição de cabeceiras
            l_dlg = dlgCabCAD.dlgCabCAD(self.__control, self._oCab, self)
            assert l_dlg

            # processa a dialog de edição de cabeceiras (modal)
            if l_dlg.exec_ ():
                # salva em disco as alterações na cabeceira
                #self._dctCab.save2Disk(self._dctCab._sPN)

                # se ok, atualiza a lista de cabeceiras
                self.updateCabWidget ()
    '''
    # ---------------------------------------------------------------------------------------------
    def closeEvent(self, f_evt):
        """
        callback de tratamento do evento Close

        @param f_evt: ...
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
        # aeródromo

        # conecta click a remoção de aeródromo
        self.connect(self.btn_del_aer, QtCore.SIGNAL("clicked()"), self.__aer_del)
        '''
        # conecta click a edição de aeródromo
        self.connect(self.btnEdit, QtCore.SIGNAL("clicked()"), self.__aer_edit)
        '''
        # conecta click a inclusão de aeródromo
        self.connect(self.btn_new_aer, QtCore.SIGNAL("clicked()"), self.__aer_new)

        # conecta click a seleção da linha
        self.connect(self.qtw_aer, QtCore.SIGNAL("itemSelectionChanged()"), self.__aer_select)
        '''
        # conecta click a visualização de aeródromo
        self.connect(self.btnView, QtCore.SIGNAL("clicked()"), self.aerView)
        '''
        # conecta botão Ok
        self.connect(self.dbb_aer, QtCore.SIGNAL("accepted()"), self.accept)

        # conecta botão Cancela
        self.connect(self.dbb_aer, QtCore.SIGNAL("rejected()"), self.reject)

        # configura botões
        self.dbb_aer.button(QtGui.QDialogButtonBox.Cancel).setText("&Cancela")
        self.dbb_aer.button(QtGui.QDialogButtonBox.Ok).setFocus()
        '''
        # cabeceiras

        # conecta click a seleção da linha
        self.connect(self.qtwTabCab, QtCore.SIGNAL("itemSelectionChanged()"), self.selectCab)

        # conecta click a edição de cabeceira
        self.connect(self.btnCabEdit, QtCore.SIGNAL("clicked()"), self.cabEdit)

        # pistas

        # conecta click a seleção da linha
        self.connect(self.qtwTabPst, QtCore.SIGNAL("itemSelectionChanged()"), self.selectPst)

        # conecta click a remoção de pista
        self.connect(self.btnPstDel, QtCore.SIGNAL("clicked()"), self.pstDel)

        # conecta click a edição de pista
        self.connect(self.btnPstEdit, QtCore.SIGNAL("clicked()"), self.pstEdit)

        # conecta click a inserção de pista
        self.connect(self.btnPstNew, QtCore.SIGNAL("clicked()"), self.pstNew)
        '''
    # ---------------------------------------------------------------------------------------------
    def __config_texts(self):
        """
        configura títulos e mensagens
        """
        self.__txt_settings = "CDlgAerDataNEW"

#       self._txtContinueTit = u"TrackS - Alterações pendentes"
#       self._txtContinueMsg = u"Salva alterações pendentes ?"

        self.__txt_del_aer_Tit = u"Apaga aeródromo"
        self.__txt_del_aer_Msg = self.__txt_del_aer_Tit + u" {0} ?"
        '''
        self.__txt_del_CabTit = "Apaga cabeceira"
        self.__txt_del_CabMsg = self.__txt_del_CabTit + " {0} ?"

        self.__txt_del_pst_Tit = "Apaga pista"
        self.__txt_del_pst_Msg = "Apaga pista {0} ?"
        '''
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
        # o item selecionado
        lo_item = None

        # clear to go
        assert f_qtw is not None

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
    '''
    # ---------------------------------------------------------------------------------------------
    def loadCabList(self, f_oPst):
        """
        faz a carga da lista de cabeceiras de pista

        @param f_oPst: pista atual
        """
        # check input
        assert f_oPst is not None

        # carrega a lista de cabeceiras de pista
        self._dctCab = f_oPst._dctCab

        # atualiza dados na tela
        self.updateCabList ()
    '''
    # ---------------------------------------------------------------------------------------------
    def __load_initial(self):
        """
        faz a carga inicial da tabela de aeródromos
        """
        # obtém o dicionário de aeródromos
        self.__dct_aer = self.__model.dct_aer

        # o dicionário de aeródromos não existe ?
        if self.__dct_aer is None:
            # logger
            l_log = logging.getLogger("CDlgAerDataNEW::__load_initial")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E01: Tabela de aeródromos não carregada.")

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__control.event.post(l_evt)

            # cai fora...
            sys.exit(1)

        # atualiza na tela os dados da tabela de aeródromos
        self.__aer_update_list()
    '''
    # ---------------------------------------------------------------------------------------------
    def loadPstList(self, fo_aer):
        """
        faz a carga da lista de pistas

        @param fo_aer: aeródromo atual
        """
        # carrega a lista de pistas
        self._dctPst = fo_aer._dctPst

        # atualiza dados na tela
        self.updatePstList ()
    '''
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
        if(self._bChanged):

            # questiona sobre alterações pendentes
            l_Resp = QtGui.QMessageBox.question(self, self._txtContinueTit,
                                                        self._txtContinueMsg,
                                                        QtGui.QMessageBox.Yes |
                                                        QtGui.QMessageBox.No |
                                                        QtGui.QMessageBox.Cancel)

            # cancela ?
            if(QtGui.QMessageBox.Cancel == l_Resp):

                # não sai
                lv_ans = False

            # salva ?
            elif(QtGui.QMessageBox.Yes == l_Resp):

                # salva as pendências e sai
                lv_ans = True

            # não salva ?
            else:

                # reseta o flag de alterações...
                self._bChanged = False

                # ...e sai
                lv_ans = True
        '''
        # retorna a resposta
        return lv_ans
    '''
    # ---------------------------------------------------------------------------------------------
    def pstDel(self):
        """
        callback de btn_del_pst da dialog de edição
        deleta uma pista da lista
        """
        # clear to go
        assert self.qtwTabPst is not None
        assert self._dctPst is not None

        # obtém a pista selecionada
        self._oPst = self.__get_current_sel(self._dctPst, self.qtwTabPst)

        if(self._oPst is not None):

            # apaga a pista atual ?
            if(QtGui.QMessageBox.Yes == QtGui.QMessageBox.question (
                                              self, self.__txt_del_pst_Tit,
                                              self.__txt_del_pst_Msg.format(""),
                                              QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)):

                # apaga a pista
                self.removePst(self._oPst)

    # ---------------------------------------------------------------------------------------------
    def pstEdit(self):
        """
        callback de btnEdit da dialog de edição. edita uma pista da QTableWidget
        """
        # clear to go
        assert self.qtwTabPst is not None
        assert self._dctPst is not None

        # obtém a pista selecionada
        self._oPst = self.__get_current_sel(self._dctPst, self.qtwTabPst)

        if(self._oPst is not None):
            # cria a dialog de edição de pistas
            l_dlg = dlgPstCAD.dlgPstCAD(self.__control, self._oPst, self)
            assert l_dlg

            # processa a dialog de edição de pistas (modal)
            if(l_dlg.exec_ ()):
                # salva em disco as alterações na pista
                #self._dctPst.save2Disk(self._dctPst._sPN)

                # se ok, atualiza a QTableWidget de pistas
                self.updatePstWidget ()

    # ---------------------------------------------------------------------------------------------
    def pstNew(self):
        """
        callback de btnNew da dialog de edição. cria uma nova pista na lista
        """
        # cria a dialog de edição de pistas
        l_dlg = dlgPstCAD.dlgPstCAD(self.__control, None, self)
        assert l_dlg

        # processa a dialog de edição de pistas (modal)
        if(l_dlg.exec_ ()):

            # obtém os dados da edição
            self._oPst = l_dlg.getData ()

            # pista existente ?
            if (( self._oPst is not None) and(self._dctPst is not None)):

                # insere a pista na lista
                self._dctPst.append(self._oPst)

                # salva o arquivo no disco
                l_sPath = os.path.join(self.__dct_config["dir.aer"], self._oPst._sInd + ".pst")

                # salva o arquivo no disco
                self._oPst.save2Disk(l_sPath)

                # se ok, atualiza a lista de pistas
                self.updatePstWidget ()
    '''
    # ---------------------------------------------------------------------------------------------
    def reject(self):
        """
        DOCUMENT ME!
        """
        # reset aer
        self.__aer = None

        # faz o "reject"
        QtGui.QDialog.reject(self)

        # close dialog
        self.close()
    '''
    # ---------------------------------------------------------------------------------------------
    def removePst(self, f_oPst):
        """
        remove a pista selecionada

        @param f_oPst: pointer para a pista a remover
        """
        # clear to go
        assert f_oPst is not None

        # remove a linha da widget
        self.qtwTabPst.removeRow(self.qtwTabPst.currentRow ())

        # remove a pista da lista
        self._dctPst.remove(f_oPst)
    '''
    # ---------------------------------------------------------------------------------------------
    def __restore_settings(self):
        """
        restaura as configurações salvas para esta janela
        """
        # obtém os settings
        l_set = QtCore.QSettings("sophosoft", "dbedit")
        assert l_set

        # restaura geometria da janela
        self.restoreGeometry(l_set.value("%s/Geometry" % (self.__txt_settings)).toByteArray())

        # return
        return True
    '''
    # ---------------------------------------------------------------------------------------------
    def selectCab(self):
        """
        seleciona uma cabeceira a editar
        """
        # clear to go
        assert self._dctCab is not None
        assert self.qtwTabCab is not None

        # obtém a cabeceira selecionada
        self._oCab = self.__get_current_sel(self._dctCab, self.qtwTabCab)

        # atualiza a área de dados do aeródromo selecionado
        #self.updateCabSel ()

    # ---------------------------------------------------------------------------------------------
    def selectPst(self):
        """
        seleciona uma pista a editar
        """
        # clear to go
        assert self._dctPst is not None
        assert self.qtwTabPst is not None

        # obtém a pista selecionada
        self._oPst = self.__get_current_sel(self._dctPst, self.qtwTabPst)

        # atualiza a área de dados da pista selecionada
        #self.updatePstSel ()

    # ---------------------------------------------------------------------------------------------
    def updateCabList(self):
        """
        atualiza na tela os dados da lista de cabeceiras
        """
        # clear to go
        assert self._dctCab is not None
        assert self.qtwTabCab is not None

        # atualiza a QTableWidget de cabeceiras
        self.updateCabWidget ()

        # obtém a cabeceira selecionada
        self._oCab = self.__get_current_sel(self._dctCab, self.qtwTabCab)

    # ---------------------------------------------------------------------------------------------
    def updateCabWidget(self):
        """
        atualiza na tela os dados da lista de cabeceiras
        """
        # linha 0 (objeto cabeceira)
        l_oC0 = None

        # linha selecionada (objeto cabeceira)
        lo_sitem = None

        # clear to go
        assert self._dctCab is not None
        assert self.qtwTabCab is not None

        # limpa a QTableWidget
        self.qtwTabCab.clear ()

        # seta o número de linhas da QTableWidget para o tamanho da lista
        self.qtwTabCab.setRowCount(len(self._dctCab))

        # seta número de colunas
        self.qtwTabCab.setColumnCount(2)

        # seta cabeçalho das colunas
        self.qtwTabCab.setHorizontalHeaderLabels([ "Id", u"Descrição" ])

        # seta QTableWidget
        self.qtwTabCab.setAlternatingRowColors(True)
        self.qtwTabCab.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        self.qtwTabCab.setSelectionBehavior(QtGui.QTableWidget.SelectRows)
        self.qtwTabCab.setSelectionMode(QtGui.QTableWidget.SingleSelection)
        self.qtwTabCab.setSortingEnabled(False)

        # percorre a lista de cabeceiras
        for li_ndx, l_oCab in enumerate(self._dctCab):
            # salva uma referência para a cabeceira se for a primeira linha da lista
            l_oC0 = l_oCab if(0 == li_ndx) else None

            # identificação/nome da cabeceira
            lo_item = QtGui.QTableWidgetItem(l_oCab._sID)
            lo_item.setData(QtCore.Qt.UserRole, QtCore.QVariant(long(li_ndx)))

            self.qtwTabCab.setItem(li_ndx, 0, lo_item)

            # a cabeceira selecionada é a atual ?
            if (( self._oCab is not None) and(id(self._oCab) == id(l_oCab))):
                # marca como selecionado
                lo_sitem = lo_item

            # descrição da cabeceira
            lo_item = QtGui.QTableWidgetItem(l_oCab._sDesc)

            self.qtwTabCab.setItem(li_ndx, 1, lo_item)

        # existe uma cabeceira selecionada ?
        if(lo_sitem is not None):
            # flag selecionado
            lo_sitem.setSelected(True)

            # item atual é a cabeceira selecionada
            self.qtwTabCab.setCurrentItem(lo_sitem)

            # posiciona na cabeceira selecionada
            self.qtwTabCab.scrollToItem(lo_sitem)

        # senão, não existe uma cabeceira selecionada
        else:
            # seleciona a primeira cabeceira
            self.qtwTabCab.selectRow(0)

            # salva a cabeceira atual
            self._oCab = l_oC0

        # ajusta o tamanho das colunas pelo conteúdo
        self.qtwTabCab.resizeColumnsToContents ()

        # habilita a ordenação
        self.qtwTabCab.setSortingEnabled(True)

    # ---------------------------------------------------------------------------------------------
    def updatePstList(self):
        """
        atualiza na tela os dados da lista de pistas
        """
        # clear to go
        assert self._dctPst is not None)
        assert self.qtwTabPst is not None)

        # atualiza a QTableWidget de pistas
        self.updatePstWidget ()

        # obtém a pista selecionada
        self._oPst = self.__get_current_sel(self._dctPst, self.qtwTabPst)

    # ---------------------------------------------------------------------------------------------
    def updatePstWidget(self):
        """
        atualiza na tela a QTableWidget de pistas
        """
        # linha 0 (objeto pista)
        l_oP0 = None

        # linha selecionada (objeto pista)
        lo_sitem = None

        # clear to go
        assert self._dctPst is not None)
        assert self.qtwTabPst is not None)

        # limpa a QTableWidget
        self.qtwTabPst.clear ()

        # seta o número de linhas da QTableWidget para o tamanho da lista
        self.qtwTabPst.setRowCount(len(self._dctPst))

        # seta número de colunas
        self.qtwTabPst.setColumnCount(1)

        # seta cabeçalho das colunas
        self.qtwTabPst.setHorizontalHeaderLabels([ u"Descrição" ])

        # seta QTableWidget
        self.qtwTabPst.setAlternatingRowColors(True)
        self.qtwTabPst.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        self.qtwTabPst.setSelectionBehavior(QtGui.QTableWidget.SelectRows)
        self.qtwTabPst.setSelectionMode(QtGui.QTableWidget.SingleSelection)
        self.qtwTabPst.setSortingEnabled(False)

        # percorre a lista de pistas
        for li_ndx, l_oPst in enumerate(self._dctPst):
            # salva uma referência para a pista se for a primeira linha da lista
            l_oP0 = l_oPst if(0 == li_ndx) else None

            # descrição da pista
            lo_item = QtGui.QTableWidgetItem(l_oPst._sDesc)
            lo_item.setData(QtCore.Qt.UserRole, QtCore.QVariant(long(li_ndx)))

            self.qtwTabPst.setItem(li_ndx, 0, lo_item)

            # o pista atual é a selecionada ?
            if (( self._oPst is not None) and(id(self._oPst) == id(l_oPst))):
                # marca como selecionado
                lo_sitem = lo_item

        # existe uma pista selecionada ?
        if(lo_sitem is not None):
            # flag selecionado
            lo_sitem.setSelected(True)

            # item atual é a pista selecionada
            self.qtwTabPst.setCurrentItem(lo_sitem)

            # posiciona na pista selecionada
            self.qtwTabPst.scrollToItem(lo_sitem)

        # senão, não existe uma pista selecionada
        else:
            # seleciona a primeira pista
            self.qtwTabPst.selectRow(0)

            # salva a pista atual
            self._oPst = l_oP0

        # ajusta o tamanho das colunas pelo conteúdo
        self.qtwTabPst.resizeColumnsToContents ()

        # habilita a ordenação
        self.qtwTabPst.setSortingEnabled(True)

        # lista de cabeceiras da pista
        self.loadCabList(self._oPst)
    '''
# < the end >--------------------------------------------------------------------------------------
