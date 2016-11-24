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
import logging
import os
# import signal
# import subprocess
import sys
# import time
# import traceback

# DBus services
# import dbus

# PyQt library
from PyQt4 import QtCore, QtGui

# model
import model.items.aer_data as aerdata

# import model.figuras.clsFig as clsFig

# view
import view.dbedit.dlg_aer_edit_new as dlgedit
# import view.dbedit.dlgCabCAD as dlgCabCAD
# import view.dbedit.dlgFig as dlgFig
# import view.dbedit.dlgPNS as dlgPNS
# import view.dbedit.dlgPstCAD as dlgPstCAD

import view.dbedit.dlg_aer_data_new_ui as dlgdata

# import view.dbedit.dlgView as dlgView

# control / events
import control.events.events_basic as events

# < module data >----------------------------------------------------------------------------------

# logging level
M_LOG_LVL = logging.DEBUG

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(M_LOG_LVL)

# < class CDlgAerDataNEW >---------------------------------------------------------------------------


class CDlgAerDataNEW(QtGui.QDialog, dlgdata.Ui_DlgAerDataNEW):
    """
    mantém as informações sobre a dialog de edição de aeródromos.
    """
    # galileu dbus service server
    # cSRV_Path = "org.documentroot.Galileu"

    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_control, f_parent=None):
        """
        @param f_control: control manager
        @param f_parent: janela pai
        """
        # verifica parâmetros de entrada
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
        # self._oFig = None
        # self._oPNS = None
        # self._oPst = None

        # pointer para os dicionários a editar
        self.__dct_aer = None
        # self._dctCab = None
        # self._dctFig = None
        # self._dctPNS = None
        # self._dctPst = None

        # self._lstView = [ True for _ in xrange(clsFig.clsFig.cFIG_Max + 3) ]

        # pointer para o DBus services server (Galileu)
        # self._oSrv = None
        # self._oIFace = None

        # inicia o DBus services server (Galileu)
        # self.connectDBus ()

        # monta a dialog
        self.setupUi(self)

        # configurações de conexões slot/signal
        self.config_connects()

        # configurações de títulos e mensagens da janela de edição
        self.config_texts()

        # restaura as configurações da janela de edição
        self.restore_settings()

        # configura título da dialog
        self.setWindowTitle(u"dbEdit [ Edição de Aeródromos ]")

        # faz a carrga inicial do diretório de aeródromos
        QtCore.QTimer.singleShot(0, self.load_initial)

    # ---------------------------------------------------------------------------------------------

    def accept(self):
        """
        callback de btn_ok da dialog de edição.
        faz o accept da dialog.
        """
        # ok para continuar ?
        if self.okToContinue():

            # faz o "accept"
            QtGui.QDialog.accept(self)

            # fecha a janela de edição
            self.close()

    # ---------------------------------------------------------------------------------------------

    def aerDel(self):
        """
        callback de btn_del da dialog de edição.
        deleta um aeródromo da lista.
        """
        # verifica condições de execução
        assert self.qtw_aer_tab is not None
        assert self.__dct_aer is not None

        # obtém o aeródromo selecionado
        self.__aer = self.getCurrentSel(self.__dct_aer, self.qtw_aer_tab)

        if self.__aer is not None:

            # apaga a aeródromo atual ?
            if QtGui.QMessageBox.Yes == QtGui.QMessageBox.question(self,
                                                                   self._txtDelAerTit,
                                                                   self._txtDelAerMsg.format(self.__aer.s_aer_id),
               QtGui.QMessageBox.Yes | QtGui.QMessageBox.No):

                # apaga o aeródromo
                self.aerRemove(self.__aer)
    '''
    # ---------------------------------------------------------------------------------------------

    def aerEdit(self):
        """
        callback de btnEdit da dialog de edição.
        edita um aeródromo da QTableWidget.
        """
        # verifica condições de execução
        assert self.qtw_aer_tab is not None
        assert self.__dct_aer is not None

        # obtém o aeródromo selecionado
        self.__aer = self.getCurrentSel(self.__dct_aer, self.qtw_aer_tab)

        if(self.__aer is not None):

            # cria a dialog de edição de aeródromos
            l_Dlg = dlgAerEditNEW.dlgAerEditNEW(self.__control, self.__aer, self)
            assert l_Dlg

            # processa a dialog de edição de aeródromos (modal)
            if(l_Dlg.exec_ ()):

                # salva em disco as alterações na aeródromo
                # self.__aer.save2Disk(self.__aer._sPN)

                # se ok, atualiza a QTableWidget de aeródromos
                self.aerUpdateWidget ()
    '''
    # ---------------------------------------------------------------------------------------------

    def aerNew(self):
        """
        callback de btnNew da dialog de edição.
        cria um novo aeródromo na lista.
        """
        # cria a dialog de edição de aeródromos
        l_Dlg = dlgAerEditNEW.dlgAerEditNEW(self.__control, None, self)
        assert l_Dlg

        # processa a dialog de edição de aeródromos (modal)
        if l_Dlg.exec_():

            # obtém os dados da edição
            self.__aer = l_Dlg.getData()

            # aeródromo existente ?
            if (self.__aer is not None) and (self.__dct_aer is not None):

                # insere a aeródromo na lista
                self.__dct_aer.append(self.__aer)

                # salva o arquivo no disco
                # self.__aer.save2Disk(l_sPath)

                # se ok, atualiza a QTableWidget de aeródromos
                self.aerUpdateWidget()

    # ---------------------------------------------------------------------------------------------

    def aerRemove(self, f_oAer):
        """
        remove o aeródromo selecionado.

        @param f_oAer: pointer para o aeródromo a remover.
        """
        # verifica condições de execução
        assert f_oAer is not None

        l_log.info("f_oAer: " + str(f_oAer))

        # remove a linha da widget
        self.qtw_aer_tab.removeRow(self.qtw_aer_tab.currentRow())

        # remove o aeródromo da lista
        self.__dct_aer.remove(f_oAer)
        '''
        # remove o arquivo de figuras associado
        l_sFN = l_sPN + ".fig"

        if (( l_sFN is not None) and os.path.exists(l_sFN) and os.path.isfile(l_sFN)):

            l_log.info(u"removeu figuras: " + str(l_sFN))

            # remove o arquivo
            #os.remove(l_sFN)

        # remove o arquivo de pns associado
        l_sFN = l_sPN + ".pns"

        if (( l_sFN is not None) and os.path.exists(l_sFN) and os.path.isfile(l_sFN)):

            l_log.info(u"removeu pns: " + str(l_sFN))

            # remove o arquivo
            #os.remove(l_sFN)

        # remove o arquivo de pistas associado
        l_sFN = l_sPN + ".pst"

        if (( l_sFN is not None) and os.path.exists(l_sFN) and os.path.isfile(l_sFN)):

            l_log.info(u"removeu pistas: " + str(l_sFN))

            # remove o arquivo
            #os.remove(l_sFN)
        '''

    # ---------------------------------------------------------------------------------------------

    def aerSelect(self):
        """
        seleciona um aeródromo a editar.
        """
        # verifica condições de execução
        assert self.__dct_aer is not None
        assert self.qtw_aer_tab is not None

        # obtém o aeródromo selecionado
        self.__aer = self.getCurrentSel(self.__dct_aer, self.qtw_aer_tab)
        # assert self.__aer

        # atualiza a área de dados do aeródromo selecionado
        self.aerUpdateSel()

    # ---------------------------------------------------------------------------------------------

    def aerUpdateList(self):
        """
        atualiza na tela os dados da lista de aeródromos.
        """
        # verifica condições de execução
        assert self.__dct_aer is not None
        assert self.qtw_aer_tab is not None

        # atualiza a QTableWidget de aeródromos
        self.aerUpdateWidget()

        # obtém o aeródromo selecionado
        self.__aer = self.getCurrentSel(self.__dct_aer, self.qtw_aer_tab)
        # assert self.__aer

    # ---------------------------------------------------------------------------------------------

    def aerUpdateSel(self):
        """
        atualiza na tela os dados do aeródromo selecionado.
        """
        # aeródromo selecionado existe ?
        if self.__aer is not None:

            # indicativo do aeródromo
            ls_aer_id = self.__aer.s_aer_id

            # atualiza a visualização do aeródromo
            # self._oSrv.configAer(ls_aer_id, dbus_interface = self.cSRV_Path)

            # identificação
            self.txtAerID.setText(self.__aer.s_aer_id)
            self.qleAerDesc.setText(self.__aer.s_aer_desc)

            # geografia

            # comprimento
            self.sbxComp.setValue(self.__aer.ui_aer_comp)

            # largura
            self.sbxLarg.setValue(self.__aer.ui_aer_larg)

            # declinação magnética
            self.dsbDecl.setValue(self.__aer.f_aer_decl_mag)

            # ARP
            # l_iX, l_iY = self.__aer._oCentro.getPto ()

            # self.txtCntrX.setText(str(l_iX))
            # self.txtCntrY.setText(str(l_iY))

            # elevação
            self.sbxElev.setValue(self.__aer.f_aer_elev)
            '''
            # lista de figuras do aeródromo
            # self.loadFigList(self.__aer)

            # lista de pns do aeródromo
            # self.loadPNSList(self.__aer)

            # lista de pistas do aeródromo
            # self.loadPstList(self.__aer)
            '''
        # senão, o aeródromo não existe
        else:

            # posiciona cursor no início do formulário
            self.txtAerID.setFocus()

    # ---------------------------------------------------------------------------------------------

    def aerUpdateWidget(self):
        """
        atualiza na tela os dados da QTableWidget de aeródromos.
        """
        # verifica condições de execução
        assert self.qtw_aer_tab is not None
        assert self.__dct_aer is not None

        # limpa a QTableWidget
        self.qtw_aer_tab.clear()

        # seta o número de linhas da QTableWidget para o tamanho da lista
        self.qtw_aer_tab.setRowCount(len(self.__dct_aer))

        # seta número de colunas e cabeçalho das colunas
        self.qtw_aer_tab.setColumnCount(2)
        self.qtw_aer_tab.setHorizontalHeaderLabels([u"Indicativo", u"Descrição"])

        # seta QTableWidget
        self.qtw_aer_tab.setAlternatingRowColors(True)
        self.qtw_aer_tab.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        self.qtw_aer_tab.setSelectionBehavior(QtGui.QTableWidget.SelectRows)
        self.qtw_aer_tab.setSelectionMode(QtGui.QTableWidget.SingleSelection)
        self.qtw_aer_tab.setSortingEnabled(False)

        # linha 0 (objeto aeródromo)
        l_oA0 = None

        # linha selecionada (objeto aeródromo)
        l_oSItem = None

        # para cada aeródromo no dicionário...
        for l_iNdx, ls_aer_id in enumerate(sorted(self.__dct_aer.keys())):

            # indicativo do aeródromo
            l_twiAerID = QtGui.QTableWidgetItem(ls_aer_id)
            l_twiAerID.setData(QtCore.Qt.UserRole, QtCore.QVariant(ls_aer_id))

            self.qtw_aer_tab.setItem(l_iNdx, 0, l_twiAerID)

            # é o aeródromo selecionado ?
            if ((self.__aer is not None) and(self.__aer.s_aer_id == ls_aer_id)):

                # salva pointer para o item selecionado
                l_oSItem = l_twiAerID

            # obtém o aeródromo
            l_oAer = self.__dct_aer[ls_aer_id]
            assert l_oAer

            # descrição
            l_twiAerDesc = QtGui.QTableWidgetItem(l_oAer.s_aer_desc)

            self.qtw_aer_tab.setItem(l_iNdx, 1, l_twi_aer_nome)

        # existe um aeródromo selecionado ?
        if(self.__aer is not None):

            # seleciona o item
            self.qtw_aer_tab.setCurrentItem(l_oSItem)

            # posiciona no item selecionado
            self.qtw_aer_tab.scrollToItem(l_oSItem)

            # marca que existe seleção
            l_oSItem.setSelected(True)

        # senão, não existe um aeródromo selecionado
        else:

            # seleciona a primeira linha
            self.qtw_aer_tab.selectRow(0)

            # obtém o aeródromo atual
            self.__aer = self.getCurrentSel(self.__dct_aer, self.qtw_aer_tab)
            # assert self.__aer

        # ajusta o tamanho das colunas pelo conteúdo
        self.qtw_aer_tab.resizeColumnsToContents()

        # habilita a ordenação
        self.qtw_aer_tab.setSortingEnabled(True)
    '''
    # ---------------------------------------------------------------------------------------------

    def aerView(self):
        """
        callback de btnView da dialog de edição.
        abre a dialog de configuração da visualização de aeródromos.
        """
        # cria a dialog de configuração da visualização de aeródromos
        l_Dlg = dlgView.dlgView(self.__control, self, self._lstView)
        assert l_Dlg

        # processa a dialog de configuração da visualização de aeródromos (modal)
        l_Dlg.exec_ ()

    # ---------------------------------------------------------------------------------------------

    def cabEdit(self):
        """
        callback de btnEdit da dialog de edição.
        edita uma cabeceira da QTableWidget.
        """
        # verifica condições de execução
        assert self.qtwTabCab is not None
        assert self._dctCab is not None

        # obtém a cabeceira selecionada
        self._oCab = self.getCurrentSel(self._dctCab, self.qtwTabCab)
        l_log.info("self._oCab: " + str(self._oCab))

        if(self._oCab is not None):

            # cria a dialog de edição de cabeceiras
            l_Dlg = dlgCabCAD.dlgCabCAD(self.__control, self._oCab, self)
            assert l_Dlg

            # processa a dialog de edição de cabeceiras (modal)
            if(l_Dlg.exec_ ()):

                # salva em disco as alterações na cabeceira
                #self._dctCab.save2Disk(self._dctCab._sPN)
                l_log.info("Salvou cabeceira em disco: ")

                # se ok, atualiza a lista de cabeceiras
                self.updateCabWidget ()
    '''
    # ---------------------------------------------------------------------------------------------

    def closeEvent(self, event):
        """
        callback de tratamento do evento Close.

        @param event: ...
        """
        # ok para continuar ?
        if self.okToContinue():

            # obtém os settings
            l_set = QtCore.QSettings()
            assert l_set

            # salva geometria da janela
            l_set.setValue("%s/Geometry" % (self._txtSettings), QtCore.QVariant(self.saveGeometry()))

            # termina o servidor (Galileu)
            # os.kill(self._iPid, signal.SIGTERM)

            # oculta a visualização do aeródromo
            # self._oIFace.hide ()

            # existe a parent window ?
            if(self.__parent is not None):

                # exibe a parent window
                self.__parent.setVisible(True)

        # senão, ignora o request
        else:

            # ignora o evento
            event.ignore()

    # ---------------------------------------------------------------------------------------------

    def config_connects(self):
        """
        configura as conexões slot/signal.
        """
        # aeródromo

        # conecta click a remoção de aeródromo
        self.connect(self.btn_del, QtCore.SIGNAL("clicked()"), self.aerDel)
        '''
        # conecta click a edição de aeródromo
        self.connect(self.btnEdit, QtCore.SIGNAL("clicked()"), self.aerEdit)
        '''
        # conecta click a inclusão de aeródromo
        self.connect(self.btn_new, QtCore.SIGNAL("clicked()"), self.aerNew)

        # conecta click a seleção da linha
        self.connect(self.qtw_aer_tab, QtCore.SIGNAL("itemSelectionChanged()"), self.aerSelect)
        '''
        # conecta click a visualização de aeródromo
        self.connect(self.btnView, QtCore.SIGNAL("clicked()"), self.aerView)
        '''
        # conecta botão Ok
        self.connect(self.bbx_aer_tab, QtCore.SIGNAL("accepted()"), self.accept)

        # conecta botão Cancela
        self.connect(self.bbx_aer_tab, QtCore.SIGNAL("rejected()"), self.reject)

        # configura botões
        self.bbx_aer_tab.button(QtGui.QDialogButtonBox.Cancel).setText("&Cancela")
        self.bbx_aer_tab.button(QtGui.QDialogButtonBox.Ok).setFocus()
        '''
        # cabeceiras

        # conecta click a seleção da linha
        self.connect(self.qtwTabCab, QtCore.SIGNAL("itemSelectionChanged()"), self.selectCab)

        # conecta click a edição de cabeceira
        self.connect(self.btnCabEdit, QtCore.SIGNAL("clicked()"), self.cabEdit)

        # figuras

        # conecta click a seleção da linha
        self.connect(self.qtwTabFig, QtCore.SIGNAL("itemSelectionChanged()"), self.selectFig)

        # conecta click a remoção de figura
        self.connect(self.btnFigDel, QtCore.SIGNAL("clicked()"), self.figDel)

        # conecta click a edição de figura
        self.connect(self.btnFigEdit, QtCore.SIGNAL("clicked()"), self.figEdit)

        # conecta click a inserção de figura
        self.connect(self.btnFigNew, QtCore.SIGNAL("clicked()"), self.figNew)

        # pistas

        # conecta click a seleção da linha
        self.connect(self.qtwTabPst, QtCore.SIGNAL("itemSelectionChanged()"), self.selectPst)

        # conecta click a remoção de pista
        self.connect(self.btnPstDel, QtCore.SIGNAL("clicked()"), self.pstDel)

        # conecta click a edição de pista
        self.connect(self.btnPstEdit, QtCore.SIGNAL("clicked()"), self.pstEdit)

        # conecta click a inserção de pista
        self.connect(self.btnPstNew, QtCore.SIGNAL("clicked()"), self.pstNew)

        # pns

        # conecta click a seleção da linha
        self.connect(self.qtwTabPNS, QtCore.SIGNAL("itemSelectionChanged()"), self.selectPNS)

        # conecta click a remoção de pns
        self.connect(self.btnPNSDel, QtCore.SIGNAL("clicked()"), self.pnsDel)

        # conecta click a edição de pns
        self.connect(self.btnPNSEdit, QtCore.SIGNAL("clicked()"), self.pnsEdit)

        # conecta click a inserção de pns
        self.connect(self.btnPNSNew, QtCore.SIGNAL("clicked()"), self.pnsNew)
        '''
    # ---------------------------------------------------------------------------------------------

    def config_texts(self):
        """
        configura títulos e mensagens.
        """
        self._txtSettings = "CDlgAerDataNEW"

#       self._txtContinueTit = u"TrackS - Alterações pendentes"
#       self._txtContinueMsg = u"Salva alterações pendentes ?"

        self._txtDelAerTit = u"TrackS - Apaga aeródromo"
        self._txtDelAerMsg = u"Apaga aeródromo {0} ?"
        '''
        self._txtDelCabTit = "TrackS - Apaga cabeceira"
        self._txtDelCabMsg = "Apaga cabeceira {0} ?"

        self._txtDelFigTit = "TrackS - Apaga figura"
        self._txtDelFigMsg = "Apaga figura {0} ?"

        self._txtDelPNSTit = "TrackS - Apaga ponto no solo"
        self._txtDelPNSMsg = "Apaga ponto {0} ?"

        self._txtDelPstTit = "TrackS - Apaga pista"
        self._txtDelPstMsg = "Apaga pista {0} ?"
        '''
    '''
    # ---------------------------------------------------------------------------------------------

    def connectDBus(self):
        """
        inicia o DBUS services server (Galileu).
        """
        # start dbus services
        l_bus = dbus.SessionBus ()
        assert l_bus

        # try to connect server (Galileu)
        try:

            # try to connect the remote object
            self._oSrv = l_bus.get_object(self.cSRV_Path, "/Galileu")
            assert self._oSrv

            # create an Interface wrapper for the remote object
            self._oIFace = dbus.Interface(self._oSrv, self.cSRV_Path)
            assert self._oIFace

            # introspection is automatically supported
            l_log.info("Introspect: " + str(self._oSrv.Introspect(dbus_interface = "org.freedesktop.DBus.Introspectable")))

        # on exception...
        except dbus.DBusException:

            # print stack trace
            traceback.print_exc ()

            # system abort
            sys.exit(1)

    # ---------------------------------------------------------------------------------------------

    def figDel(self):
        """
        callback de btn_del da dialog de edição.
        deleta uma figura da lista.
        """
        # verifica condições de execução
        assert self._dctFig is not None
        assert self.qtwTabFig is not None

        # obtém a figura selecionada
        self._oFig = self.getCurrentSel(self._dctFig, self.qtwTabFig)
        l_log.info("self._oFig: " + str(self._oFig))

        if(self._oFig is not None):

            # apaga a figura atual ?
            if(QtGui.QMessageBox.Yes == QtGui.QMessageBox.question(self,
                                              self._txtDelFigTit,
                                              self._txtDelFigMsg.format(self._oFig._sDesc),
                                              QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)):

                # obtém o ID da figura selecionada
                l_lID = self.getCurrentData(self.qtwTabFig, 1)
                l_log.info("l_lID: " + str(l_lID))

                # apaga a visualização da figura
                self._oSrv.apagaItem(l_lID, dbus_interface = self.cSRV_Path)

                # apaga a figura da lista
                self.removeFig(self._oFig)

                # salva em disco as alterações na lista de figuras
                self._dctFig.save2Disk ()

    # ---------------------------------------------------------------------------------------------

    def figEdit(self):

        """
        callback de btnEdit da dialog de edição.
        edita uma figura da QTableWidget.
        """

        # logger
        l_log.info("__init__:>>")

        # verifica condições de execução
        assert self.qtwTabFig is not None
        assert self._dctFig is not None

        # obtém a figura selecionada
        self._oFig = self.getCurrentSel(self._dctFig, self.qtwTabFig)

        if(self._oFig is not None):

            # cria a dialog de edição de figuras
            l_Dlg = dlgFig.dlgFig(self.__control, self, self._oFig)
            assert l_Dlg

            # processa a dialog de edição de figuras (modal)
            if(l_Dlg.exec_ ()):

                # salva em disco as alterações na lista de figuras
                self._dctFig.save2Disk ()

                # se ok, atualiza a lista de figuras
                #self.updateFigWidget ()

    # ---------------------------------------------------------------------------------------------

    def figNew(self):
        """
        callback de btnNew da dialog de edição.
        cria uma nova figura na lista.
        """
        # cria a dialog de edição de figuras
        l_Dlg = dlgFig.dlgFig(self.__control, self , None)
        assert l_Dlg

        # processa a dialog de edição de figuras (modal)
        if(l_Dlg.exec_ ()):

            # obtém os dados da edição
            self._oFig = l_Dlg.getData ()

            # figura existe ?
            if (( self._oFig is not None) and(self._dctFig is not None)):

                # insere a figura na lista
                self._dctFig.append(self._oFig)

                # salva em disco as alterações na lista de figuras
                self._dctFig.save2Disk ()

                # se ok, atualiza a lista de figuras
                #self.updateFigWidget ()
    '''
    # ---------------------------------------------------------------------------------------------

    def getCurrentData(self, f_qtwTab, f_iCol):
        """
        retorna os dados associados a linha selecionada.
        """
        # verifica condições de execução
        assert f_qtwTab is not None
        l_log.info("f_qtwTab: " + str(f_qtwTab))

        # o dado da linha selecionada
        l_sData = ""

        # obtém o item da linha selecionada
        l_oItem = self.getCurrentItem(f_qtwTab, f_iCol)
        l_log.info("l_oItem: " + str(l_oItem))

        # existe uma linha selecionada ?
        if l_oItem is not None:

            # obtém o dado associado a linha
            l_sData = l_oItem.data(QtCore.Qt.UserRole).toString()
            l_log.info("l_sData: " + str(l_sData))

        # retorna o dado associado a linha selecionada
        return l_sData

    # ---------------------------------------------------------------------------------------------

    def getCurrentItem(self, f_qtwTab, f_iCol):
        """
        retorna o item associado a linha selecionada.
        """
        # o item selecionado
        l_oItem = None

        # verifica condições de execução
        assert f_qtwTab is not None
        l_log.info("f_qtwTab: " + str(f_qtwTab))

        # obtém o número da linha selecionada
        l_iRow = f_qtwTab.currentRow()
        l_log.info("l_iRow: " + str(l_iRow))

        # existe uma linha selecionada ?
        if l_iRow > -1:

            # obtém o item associado
            l_oItem = f_qtwTab.item(l_iRow, f_iCol)
            l_log.info("l_oItem: " + str(l_oItem))
            assert l_oItem

        # retorna o item selecionado na lista
        return l_oItem

    # ---------------------------------------------------------------------------------------------

    def getCurrentSel(self, f_dct, f_qtw):
        """
        retorna o elemento associado a linha selecionada na lista.
        """
        # verifica condições de execução
        assert f_dct is not None
        assert f_qtw is not None

        # l_log.info("f_dct: " + str(f_dct))

        # obtém o index da linha selecionada
        l_sID = self.getCurrentData(f_qtw, 0)
        # l_log.info("l_sID: " + str(l_sID))

        # indice válido ?
        if str(l_sID) in f_dct:

            # obtém o elemento selecionado se existir uma linha selecionada
            l_oSel = f_dct[str(l_sID)]
            assert l_oSel
            # l_log.info("l_oSel: " + str(l_oSel))

        # senão, índice inválido
        else:

            # não há elemento selecionado
            l_oSel = None

        # retorna o elemento da linha selecionada na lista
        return l_oSel
    '''
    # ---------------------------------------------------------------------------------------------

    def loadCabList(self, f_oPst):
        """
        faz a carga da lista de cabeceiras de pista.

        @param f_oPst: pista atual.
        """
        l_log.info("f_oPst: " + str(f_oPst))

        # verifica parâmetros de entrada
        assert f_oPst is not None

        # carrega a lista de cabeceiras de pista
        self._dctCab = f_oPst._dctCab

        # atualiza dados na tela
        self.updateCabList ()

    # ---------------------------------------------------------------------------------------------

    def loadFigList(self, f_oAer):
        """
        faz a carga da lista de figuras.

        @param f_oAer: aeródromo atual.
        """
        # verifica parâmetros de entrada
        assert f_oAer is not None

        # carrega a lista de figuras
        self._dctFig = f_oAer._dctFig

        # atualiza dados na tela
        self.updateFigList ()
    '''
    # ---------------------------------------------------------------------------------------------

    def load_initial(self):
        """
        faz a carga inicial da tabela de aeródromos.
        """
        # obtém o dicionário de aeródromos
        self.__dct_aer = self.__model.airspace.dct_aer

        # o dicionário de aeródromos não existe ?
        if self.__dct_aer is None:

            # logger
            l_log = logging.getLogger("CDlgAerDataNEW::load_initial")
            l_log.setLevel(M_LOG_LVL)
            l_log.critical(u"<E01: Tabela de aeródromos não carregada !")

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__control.event.post(l_evt)

            # cai fora...
            sys.exit(1)

        # atualiza na tela os dados da tabela de aeródromos
        self.aerUpdateList()
    '''
    # ---------------------------------------------------------------------------------------------

    def loadPNSList(self, f_oAer):
        """
        faz a carga da lista de pns.

        @param f_oAer: aeródromo atual.
        """
        # carrega a lista de pns
        self._dctPNS = f_oAer._dctPNS

        # atualiza dados na tela
        self.updatePNSList ()

    # ---------------------------------------------------------------------------------------------

    def loadPstList(self, f_oAer):
        """
        faz a carga da lista de pistas.

        @param f_oAer: aeródromo atual.
        """
        # carrega a lista de pistas
        self._dctPst = f_oAer._dctPst
        l_log.info("self._dctPst: " + str(self._dctPst))

        # atualiza dados na tela
        self.updatePstList ()
    '''
    # ---------------------------------------------------------------------------------------------

    def okToContinue(self):
        """
        cria uma messageBox.

        @return True se tratou a resposta, senão False.
        """
        # resposta
        l_bAns = True
        '''
        l_log.info("self._bChanged: " + str(self._bChanged))

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
                l_bAns = False

            # salva ?
            elif(QtGui.QMessageBox.Yes == l_Resp):

                # salva as pendências e sai
                l_bAns = True

            # não salva ?
            else:

                # reseta o flag de alterações...
                self._bChanged = False
                l_log.info("self._bChanged: " + str(self._bChanged))

                # ...e sai
                l_bAns = True
        '''
        # retorna a resposta
        return l_bAns
    '''
    # ---------------------------------------------------------------------------------------------

    def pnsDel(self):
        """
        callback de btn_del da dialog de edição.
        remove um pns da lista.
        """
        # verifica condições de execução
        assert self.qtwTabPNS is not None
        assert self._dctPNS is not None

        # obtém o pns selecionado
        self._oPNS = self.getCurrentSel(self._dctPNS, self.qtwTabPNS)

        if(self._oPNS is not None):

            # apaga o pns atual ?
            if(QtGui.QMessageBox.Yes == QtGui.QMessageBox.question(self,
                                              self._txtDelPNSTit,
                                              self._txtDelPNSMsg.format(str(self._oPNS._iNum)),
                                              QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)):

                # remove o pns da lista
                self.removePNS(self._oPNS)

                # salva em disco as alterações no pns
                self._dctPNS.save2Disk(self._dctPNS._sPN)

    # ---------------------------------------------------------------------------------------------

    def pnsEdit(self):
        """
        callback de btnEdit da dialog de edição.
        edita um pns da QTableWidget.
        """
        # verifica condições de execução
        assert self.qtwTabPNS is not None
        assert self._dctPNS is not None

        # obtém o pns selecionado
        self._oPNS = self.getCurrentSel(self._dctPNS, self.qtwTabPNS)

        if(self._oPNS is not None):

            # cria a dialog de edição de pns
            l_Dlg = dlgPNS.dlgPNS(self.__control, self, self._oPNS)
            assert l_Dlg

            # processa a dialog de edição de pns (modal)
            if(l_Dlg.exec_ ()):

                # salva em disco as alterações no pns
                self._dctPNS.save2Disk(self._dctPNS._sPN)

                # se ok, atualiza a lista de pns
                self.updatePNSWidget ()

    # ---------------------------------------------------------------------------------------------

    def pnsNew(self):
        """
        callback de btnNew da dialog de edição.
        cria um novo pns na lista.
        """
        # cria a dialog de edição de pns
        l_Dlg = dlgPNS.dlgPNS(self.__control, self, None)
        assert l_Dlg

        # processa a dialog de edição de pns (modal)
        if(l_Dlg.exec_ ()):

            # obtém os dados da edição
            self._oPNS = l_Dlg.getData ()

            # pns existe ?
            if (( self._oPNS is not None) and(self._dctPNS is not None)):

                # insere o pns na lista
                self._dctPNS [ self._oPNS._iNum ] = self._oPNS

                # salva o arquivo no disco
                self._dctPNS.save2Disk(self._dctPNS._sPN)

                # se ok, atualiza a lista de pns
                self.updatePNSWidget ()

    # ---------------------------------------------------------------------------------------------

    def pstDel(self):
        """
        callback de btn_del da dialog de edição.
        deleta uma pista da lista.
        """
        # verifica condições de execução
        assert self.qtwTabPst is not None
        assert self._dctPst is not None

        # obtém a pista selecionada
        self._oPst = self.getCurrentSel(self._dctPst, self.qtwTabPst)
        l_log.info("self._oPst: " + str(self._oPst))

        if(self._oPst is not None):

            # apaga a pista atual ?
            if(QtGui.QMessageBox.Yes == QtGui.QMessageBox.question (
                                              self, self._txtDelPstTit,
                                              self._txtDelPstMsg.format(""),
                                              QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)):

                # apaga a pista
                self.removePst(self._oPst)

    # ---------------------------------------------------------------------------------------------

    def pstEdit(self):
        """
        callback de btnEdit da dialog de edição.
        edita uma pista da QTableWidget.
        """
        # verifica condições de execução
        assert self.qtwTabPst is not None
        assert self._dctPst is not None

        # obtém a pista selecionada
        self._oPst = self.getCurrentSel(self._dctPst, self.qtwTabPst)
        l_log.info("self._oPst: " + str(self._oPst))

        if(self._oPst is not None):

            # cria a dialog de edição de pistas
            l_Dlg = dlgPstCAD.dlgPstCAD(self.__control, self._oPst, self)
            assert l_Dlg

            # processa a dialog de edição de pistas (modal)
            if(l_Dlg.exec_ ()):

                # salva em disco as alterações na pista
                #self._dctPst.save2Disk(self._dctPst._sPN)
                l_log.info("Salvou pista em disco: " + self._dctPst._sPN)

                # se ok, atualiza a QTableWidget de pistas
                self.updatePstWidget ()

    # ---------------------------------------------------------------------------------------------

    def pstNew(self):
        """
        callback de btnNew da dialog de edição.
        cria uma nova pista na lista.
        """
        # cria a dialog de edição de pistas
        l_Dlg = dlgPstCAD.dlgPstCAD(self.__control, None, self)
        assert l_Dlg

        # processa a dialog de edição de pistas (modal)
        if(l_Dlg.exec_ ()):

            # obtém os dados da edição
            self._oPst = l_Dlg.getData ()

            # pista existente ?
            if (( self._oPst is not None) and(self._dctPst is not None)):

                # insere a pista na lista
                self._dctPst.append(self._oPst)

                # salva o arquivo no disco
                l_sPath = os.path.join(self.__dct_config["dir.aer"], self._oPst._sInd + ".pst")
                l_log.info("l_sPath: " + str(l_sPath))

                # salva o arquivo no disco
                self._oPst.save2Disk(l_sPath)

                # se ok, atualiza a lista de pistas
                self.updatePstWidget ()
    '''
    # ---------------------------------------------------------------------------------------------

    def reject(self):

        self.__aer = None

        # faz o "reject"
        QtGui.QDialog.reject(self)

        self.close()
    '''
    # ---------------------------------------------------------------------------------------------

    def removeFig(self, f_oFig):
        """
        remove a figura selecionada.

        @param f_oFig: pointer para a figura a remover.
        """
        # verifica condições de execução
        assert f_oFig is not None

        l_log.info("f_oFig: " + str(f_oFig))

        # remove a linha da widget
        self.qtwTabFig.removeRow(self.qtwTabFig.currentRow ())

        # remove a figura da lista
        self._dctFig.remove(f_oFig)

    # ---------------------------------------------------------------------------------------------

    def removePNS(self, f_oPNS):
        """
        remove o pns selecionado.

        @param f_oPNS: pointer para o pns a remover.
        """
        # verifica condições de execução
        assert f_oPNS is not None

        l_log.info("f_oPNS: " + str(f_oPNS))

        # remove a linha da widget
        self.qtwTabPNS.removeRow(self.qtwTabPNS.currentRow ())

        # remove o pns da lista
        self._dctPNS.remove(f_oPNS)

    # ---------------------------------------------------------------------------------------------

    def removePst(self, f_oPst):
        """
        remove a pista selecionada.

        @param f_oPst: pointer para a pista a remover.
        """
        # verifica condições de execução
        assert f_oPst is not None

        l_log.info("f_oPst: " + str(f_oPst))

        # remove a linha da widget
        self.qtwTabPst.removeRow(self.qtwTabPst.currentRow ())

        # remove a pista da lista
        self._dctPst.remove(f_oPst)
    '''
    # ---------------------------------------------------------------------------------------------

    def restore_settings(self):
        """
        restaura as configurações salvas para esta janela.
        """
        # obtém os settings
        l_set = QtCore.QSettings("sophosoft", "dbedit")
        assert l_set

        # restaura geometria da janela
        self.restoreGeometry(l_set.value("%s/Geometry" % (self._txtSettings)).toByteArray())

        return True
    '''
    # ---------------------------------------------------------------------------------------------

    def selectCab(self):
        """
        seleciona uma cabeceira a editar.
        """
        # verifica condições de execução
        assert self._dctCab is not None
        assert self.qtwTabCab is not None

        # obtém a cabeceira selecionada
        self._oCab = self.getCurrentSel(self._dctCab, self.qtwTabCab)

        l_log.info("self._oCab: " + str(self._oCab))

        # atualiza a área de dados do aeródromo selecionado
        #self.updateCabSel ()

    # ---------------------------------------------------------------------------------------------

    def selectFig(self):
        """
        seleciona uma figura a editar.
        """
        # verifica condições de execução
        assert self._dctFig is not None
        assert self.qtwTabFig is not None

        # obtém a figura selecionada
        #self._oFig = self.getCurrentSel(self._dctFig, self.qtwTabFig)
        l_log.info("self._oFig: " + str(self._oFig))

        # obtém o pointer para o desenho da figura selecionada
        l_lID = self.getCurrentData(self.qtwTabFig, 1)
        l_log.info("l_lID: " + str(l_lID))

        # destaca a figura atual
        self._oSrv.selectItem(l_lID, dbus_interface = self.cSRV_Path)

        # atualiza a área de dados da figura selecionada
        #self.updateFigSel ()

    # ---------------------------------------------------------------------------------------------

    def selectPst(self):
        """
        seleciona uma pista a editar.
        """
        # verifica condições de execução
        assert self._dctPst is not None
        assert self.qtwTabPst is not None

        # obtém a pista selecionada
        self._oPst = self.getCurrentSel(self._dctPst, self.qtwTabPst)

        l_log.info("self._oPst: " + str(self._oPst))

        # atualiza a área de dados da pista selecionada
        #self.updatePstSel ()

    # ---------------------------------------------------------------------------------------------

    def selectPNS(self):
        """
        seleciona um pns a editar.
        """
        # verifica condições de execução
        assert self._dctPNS is not None
        assert self.qtwTabPNS is not None

        # obtém o pns selecionado
        self._oPNS = self.getCurrentSel(self._dctPNS, self.qtwTabPNS)

        l_log.info("self._oPNS: " + str(self._oPNS))

        # obtém o pointer para o desenho do pns selecionado
        l_lID = self.getCurrentData(self.qtwTabPNS, 1)

        l_log.info("l_lID: " + str(l_lID))

        # destaca o ponto atual
        self._oSrv.selectItem(l_lID, dbus_interface = self.cSRV_Path)

        # atualiza a área de dados do pns selecionado
        #self.updatePNSSel ()

    # ---------------------------------------------------------------------------------------------

    def updateCabList(self):
        """
        atualiza na tela os dados da lista de cabeceiras.
        """
        # verifica condições de execução
        assert self._dctCab is not None
        assert self.qtwTabCab is not None

        # atualiza a QTableWidget de cabeceiras
        self.updateCabWidget ()

        # obtém a cabeceira selecionada
        self._oCab = self.getCurrentSel(self._dctCab, self.qtwTabCab)

    # ---------------------------------------------------------------------------------------------

    def updateCabWidget(self):
        """
        atualiza na tela os dados da lista de cabeceiras.
        """
        # linha 0 (objeto cabeceira)
        l_oC0 = None

        # linha selecionada (objeto cabeceira)
        l_oSItem = None

        # verifica condições de execução
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
        for l_iNdx, l_oCab in enumerate(self._dctCab):

            # salva uma referência para a cabeceira se for a primeira linha da lista
            l_oC0 = l_oCab if(0 == l_iNdx) else None

            # identificação/nome da cabeceira
            l_oItem = QtGui.QTableWidgetItem(l_oCab._sID)
            l_oItem.setData(QtCore.Qt.UserRole, QtCore.QVariant(long(l_iNdx)))

            self.qtwTabCab.setItem(l_iNdx, 0, l_oItem)

            # a cabeceira selecionada é a atual ?
            if (( self._oCab is not None) and(id(self._oCab) == id(l_oCab))):

                # marca como selecionado
                l_oSItem = l_oItem

            # descrição da cabeceira
            l_oItem = QtGui.QTableWidgetItem(l_oCab._sDesc)

            self.qtwTabCab.setItem(l_iNdx, 1, l_oItem)

        # existe uma cabeceira selecionada ?
        if(l_oSItem is not None):

            # flag selecionado
            l_oSItem.setSelected(True)

            # item atual é a cabeceira selecionada
            self.qtwTabCab.setCurrentItem(l_oSItem)

            # posiciona na cabeceira selecionada
            self.qtwTabCab.scrollToItem(l_oSItem)

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

    def updateFigList(self):
        """
        atualiza na tela os dados da lista de figuras.
        """
        # verifica condições de execução
        assert self._dctFig is not None)
        assert self.qtwTabFig is not None)

        # atualiza a QTableWidget de figuras
        self.updateFigWidget ()

        # obtém a figura selecionada
        self._oFig = self.getCurrentSel(self._dctFig, self.qtwTabFig)

    # ---------------------------------------------------------------------------------------------

    def updateFigWidget(self):
        """
        atualiza na tela a QTableWidget de figuras.
        """
        # linha 0 (objeto figura)
        l_oF0 = None

        # linha selecionada (objeto figura)
        l_oSItem = None


        # logger
        l_log.info("__init__:>>")

        # verifica condições de execução
        assert self._dctFig is not None)
        assert self.qtwTabFig is not None)

        # limpa a QTableWidget
        self.qtwTabFig.clear ()

        # seta o número de linhas da QTableWidget para o tamanho da lista
        self.qtwTabFig.setRowCount(len(self._dctFig))

        # seta número de colunas
        self.qtwTabFig.setColumnCount(2)

        # seta cabeçalho das colunas
        self.qtwTabFig.setHorizontalHeaderLabels([ "Tipo", u"Descrição" ])

        # seta QTableWidget
        self.qtwTabFig.setAlternatingRowColors(True)
        self.qtwTabFig.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        self.qtwTabFig.setSelectionBehavior(QtGui.QTableWidget.SelectRows)
        self.qtwTabFig.setSelectionMode(QtGui.QTableWidget.SingleSelection)
        self.qtwTabFig.setSortingEnabled(False)

        # percorre a lista de figuras
        for l_iNdx, l_oFig in enumerate(self._dctFig):

            # salva uma referência para a figuras se for a primeira linha da lista
            l_oF0 = l_oFig if(0 == l_iNdx) else None

            # atualiza a visualização da figura
            l_lID = self._oSrv.desenhaItem(l_oFig.getDataList (), l_iNdx,
                                             dbus_interface = self.cSRV_Path)

            # tipo
            l_oItem = QtGui.QTableWidgetItem("{0}".format(l_oFig._btTipo))
            l_oItem.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            l_oItem.setData(QtCore.Qt.UserRole, QtCore.QVariant(long(l_iNdx)))

            self.qtwTabFig.setItem(l_iNdx, 0, l_oItem)

            # a figura atual é a selecionada ?
            if (( self._oFig is not None) and(id(self._oFig) == id(l_oFig))):

                # marca como selecionada
                l_oSItem = l_oItem

            # descrição
            l_oItem = QtGui.QTableWidgetItem(l_oFig._sDesc)
            l_oItem.setData(QtCore.Qt.UserRole, QtCore.QVariant(long(l_lID)))

            self.qtwTabFig.setItem(l_iNdx, 1, l_oItem)

        # existe uma figura selecionada ?
        if(l_oSItem is not None):

            # flag selecionado
            l_oSItem.setSelected(True)

            # item atual é a figura selecionada
            self.qtwTabFig.setCurrentItem(l_oSItem)

            # posiciona na figura selecionada
            self.qtwTabFig.scrollToItem(l_oSItem)

        # senão, não existe uma figura selecionada
        else:

            # seleciona a primeira figura
            self.qtwTabFig.selectRow(0)

            # salva o figura atual
            self._oFig = l_oF0

        # ajusta o tamanho das colunas pelo conteúdo
        self.qtwTabFig.resizeColumnsToContents ()

        # habilita a ordenação
        self.qtwTabFig.setSortingEnabled(True)

    # ---------------------------------------------------------------------------------------------

    def updatePNSList(self):
        """
        atualiza na tela os dados da lista de pns.
        """
        # verifica condições de execução
        assert self._dctPNS is not None)
        assert self.qtwTabPNS is not None)

        # atualiza a QTableWidget de pns
        self.updatePNSWidget ()

        # obtém o pns selecionado
        self._oPNS = self.getCurrentSel(self._dctPNS, self.qtwTabPNS)

    # ---------------------------------------------------------------------------------------------

    def updatePNSWidget(self):
        """
        atualiza na tela a QTableWidget de pns.
        """

        # linha 0 (objeto pns)
        l_oP0 = None

        # linha selecionada (objeto pns)
        l_oSItem = None

        # verifica condições de execução
        assert self._dctPNS is not None)
        assert self.qtwTabPNS is not None)

        # limpa a QTableWidget
        self.qtwTabPNS.clear ()

        # seta o número de linhas da QTableWidget para o tamanho da lista
        self.qtwTabPNS.setRowCount(len(self._dctPNS))

        # seta número de colunas
        self.qtwTabPNS.setColumnCount(3)

        # seta cabeçalho das colunas
        self.qtwTabPNS.setHorizontalHeaderLabels([ "Nr.Pto", u"Descrição", "Adj" ])

        # seta QTableWidget
        self.qtwTabPNS.setAlternatingRowColors(True)
        self.qtwTabPNS.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        self.qtwTabPNS.setSelectionBehavior(QtGui.QTableWidget.SelectRows)
        self.qtwTabPNS.setSelectionMode(QtGui.QTableWidget.SingleSelection)
        self.qtwTabPNS.setSortingEnabled(False)

        # percorre a lista de pns
        for l_iNdx, l_oPNS in self._dctPNS.iteritems ():

            # salva uma referência para o PNS se for a primeira linha da lista
            l_oP0 = l_oPNS if(0 == l_iNdx) else None

            # número do pns
            l_oItem = QtGui.QTableWidgetItem("%02d" %(l_oPNS._iNum))
            l_oItem.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            l_oItem.setData(QtCore.Qt.UserRole, QtCore.QVariant(long(l_oPNS._iNum)))

            self.qtwTabPNS.setItem(l_iNdx, 0, l_oItem)

            # o pns atual é o selecionado ?
            if (( self._oPNS is not None) and(id(self._oPNS) == id(l_oPNS))):

                # marca como selecionado
                l_oSItem = l_oItem

            # atualiza a visualização do pns
            l_lID = self._oSrv.desenhaPNS(l_oPNS.getDataList (), l_iNdx + 100,
                                            dbus_interface = self.cSRV_Path)

            # descrição
            l_oItem = QtGui.QTableWidgetItem(l_oPNS._sDesc)
            l_oItem.setData(QtCore.Qt.UserRole, QtCore.QVariant(long(l_lID)))

            self.qtwTabPNS.setItem(l_iNdx, 1, l_oItem)

            # lista de pontos adjacentes
            #l_oItem = QtGui.QTableWidgetItem("{0}".format(l_oPNS._dctAdj))
            #l_oItem.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

            l_oItem = QtGui.QTableWidgetItem(str(l_oPNS._dctAdj))

            self.qtwTabPNS.setItem(l_iNdx, 2, l_oItem)

        # existe um ponto selecionado ?
        if(l_oSItem is not None):

            # flag selecionado
            l_oSItem.setSelected(True)

            # item atual é o ponto selecionado
            self.qtwTabPNS.setCurrentItem(l_oSItem)

            # posiciona na ponto selecionado
            self.qtwTabPNS.scrollToItem(l_oSItem)

        # senão, não existe um ponto selecionado
        else:

            # seleciona o primeira ponto
            self.qtwTabPNS.selectRow(0)

            # salva o figura atual
            self._oPNS = l_oP0

        # ajusta o tamanho das colunas pelo conteúdo
        self.qtwTabPNS.resizeColumnsToContents ()

        # habilita a ordenação
        self.qtwTabPNS.setSortingEnabled(True)

    # ---------------------------------------------------------------------------------------------

    def updatePstList(self):
        """
        atualiza na tela os dados da lista de pistas.
        """
        # verifica condições de execução
        assert self._dctPst is not None)
        assert self.qtwTabPst is not None)

        # atualiza a QTableWidget de pistas
        self.updatePstWidget ()

        # obtém a pista selecionada
        self._oPst = self.getCurrentSel(self._dctPst, self.qtwTabPst)

    # ---------------------------------------------------------------------------------------------

    def updatePstWidget(self):

        """
        atualiza na tela a QTableWidget de pistas.
        """

        # linha 0 (objeto pista)
        l_oP0 = None

        # linha selecionada (objeto pista)
        l_oSItem = None

        # verifica condições de execução
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
        for l_iNdx, l_oPst in enumerate(self._dctPst):

            # salva uma referência para a pista se for a primeira linha da lista
            l_oP0 = l_oPst if(0 == l_iNdx) else None

            # descrição da pista
            l_oItem = QtGui.QTableWidgetItem(l_oPst._sDesc)
            l_oItem.setData(QtCore.Qt.UserRole, QtCore.QVariant(long(l_iNdx)))

            self.qtwTabPst.setItem(l_iNdx, 0, l_oItem)

            # o pista atual é a selecionada ?
            if (( self._oPst is not None) and(id(self._oPst) == id(l_oPst))):

                # marca como selecionado
                l_oSItem = l_oItem

        # existe uma pista selecionada ?
        if(l_oSItem is not None):

            # flag selecionado
            l_oSItem.setSelected(True)

            # item atual é a pista selecionada
            self.qtwTabPst.setCurrentItem(l_oSItem)

            # posiciona na pista selecionada
            self.qtwTabPst.scrollToItem(l_oSItem)

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
