#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
wnd_main_piloto.

DOCUMENT ME!

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2015/fev  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "mlabru, sophosoft"
__date__ = "2015/12"

# < imports >--------------------------------------------------------------------------------------

# Python library
import json
import logging
import random
import sys
import time

# PyQt library
from PyQt4 import QtCore
from PyQt4 import QtGui

# model
import model.glb_defs as gdefs

import model.piloto.aircraft_piloto as anv
import model.piloto.defs_piloto as ldefs
import model.piloto.strip_model as mstp
import model.piloto.strip_table_model as stm

# view
import view.piloto.statusbar_piloto as statusbar
import view.piloto.strip_visil as strips
import view.piloto.wnd_main_piloto_ui as wndmain_ui

import view.piloto.dlg_altitude as dlgalt
import view.piloto.dlg_direcao as dlgdir
import view.piloto.dlg_velocidade as dlgvel

# control
import control.events.events_basic as events
import control.events.events_config as evtcfg

# resources
import icons_rc
import resources_visil_rc

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CWndMainPiloto >---------------------------------------------------------------------------

class CWndMainPiloto(QtGui.QMainWindow, wndmain_ui.Ui_wndMainPiloto):

    # signals
    # C_SIG_STRIP_CHG = QtCore.pyqtSignal(anv.CAircraftPiloto)
    # C_SIG_STRIP_DEL = QtCore.pyqtSignal(anv.CAircraftPiloto)
    C_SIG_STRIP_INS = QtCore.pyqtSignal(anv.CAircraftPiloto)
    C_SIG_STRIP_SEL = QtCore.pyqtSignal(anv.CAircraftPiloto)

    # ---------------------------------------------------------------------------------------------
    # void (?)
    def __init__(self, f_control):
        """
        @param f_control: control manager.
        """
        # logger
        # M_LOG.info("__init__:>>")

        # verifica parâmetros de entrada
        assert f_control

        # inicia a super classe
        super(CWndMainPiloto, self).__init__()

        # salva o control manager localmente
        self.__control = f_control
        assert self.__control

        # salva o dicionário de performances
        self.__dct_prf = f_control.model.dct_prf
        assert self.__dct_prf is not None

        # salva o dicionário de aeronaves
        self.__dct_flight = f_control.model.emula_model.dct_flight
        assert self.__dct_flight is not None

        # obtém o dicionário de configuração
        self.__dct_config = f_control.config.dct_config
        assert self.__dct_config

        # salva o socket de envio
        self.__sck_snd_cpil = f_control.sck_snd_cpil
        assert self.__sck_snd_cpil

        # salva o socket de recebimento
        self.__sck_http = f_control.sck_http
        assert self.__sck_http

        # obtém o event manager
        self.__event = f_control.event
        assert self.__event

        # current strip
        self.__strip_cur = None

        # create main menu Ui
        self.setupUi(self)

        # window title
        self.setWindowTitle(self.tr("Piloto 0.1 [Pilotagem]", None))

        # create windows elements
        self.__statusbar = statusbar.CStatusBarPiloto(self)
        assert self.__statusbar

        # config statusBar
        self.setStatusBar(self.__statusbar)

        # create windows elements
        self.__config_strips()

        # create windows elements
        self.__config_buttons()

        # self.createActions()
        # self.createMenus()
        # self.createToolBars()
        # self.createDocks()
        # self.createToolBoxes()

        # make SIGNAL-SLOT connections
        self.__make_connections()

        # read saved settings
        self.__read_settings()

        # registra a sí próprio como recebedor de eventos
        self.__event.register_listener(self)

        # XXX
        self.xxx()

        # fetch anv data timer (1s cycle)
        self.__i_timer_fetch = self.startTimer(1000)

        # fetch status data timer (2s cycle)
        self.__i_timer_status = self.startTimer(2000)

        # config tableview
        self.qtv_stp.setFocus()
        self.qtv_stp.setCurrentIndex(self.__stp_model.index(0, 0))

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def about(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("about:>>")

        # show about box
        QtGui.QMessageBox.about(self, self.tr("About Piloto", None),
                                      self.tr("Activate runways for arrival in the Settings. Runway Config Dialog\n"
                                              "Click Blips to give instructions.\n"
                                              "Press 'h' for heading, 'd' for direct, 'r' for routing, 'a' for approach clearance.\n"
                                              "Press Escape or RMB to cancel.\n"
                                              "Use the middle mouse button to center your radar screen.\n"
                                              "[vertical navigation and departing aircraft not yet implemented]\n"
                                              "pre-alpha release! Please report bugs to openapproach@aufroof.org", None))

        # logger
        # M_LOG.info("about:<<")

    # ---------------------------------------------------------------------------------------------
    # @QtCore.pyqtSlot()
    def closeEvent(self, f_evt):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("closeEvent:>>")

        # really quit ?
        if self.__really_quit():

            # salva a configuração atual
            self.__write_settings()

            # accept
            f_evt.accept()

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

        # senão, continua...
        else:
            # ignore
            f_evt.ignore()

        # logger
        # M_LOG.info("closeEvent:<<")

    # ---------------------------------------------------------------------------------------------
    # void (?)
    def __config_buttons(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__config_buttons:>>")

        # groupBox
        # self.gbx_comandos.setEnabled(False)

        ###
        # dialogs

        self.__dlg_altitude = None
        self.__dlg_direcao = None
        self.__dlg_velocidade = None

        ###
        # buttons

        self.btn_cmd_altitude.setEnabled(True)
        self.btn_cmd_direcao.setEnabled(True)
        self.btn_cmd_velocidade.setEnabled(True)

        # logger
        # M_LOG.info("__config_buttons:<<")

    # ---------------------------------------------------------------------------------------------
    # void (?)
    def __config_strips(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__config_strips:>>")

        ###
        # strips

        # strips table model
        self.__stp_model = stm.CStripTableModel()
        assert self.__stp_model

        # make connections
        # self.__stp_model.dataChanged.connect(self.__on_strip_data_changed)

        # config strip tableview
        self.qtv_stp.setModel(self.__stp_model)
        self.qtv_stp.setSelectionMode(QtGui.QTableView.SingleSelection)
        self.qtv_stp.setSelectionBehavior(QtGui.QTableView.SelectRows)
        self.qtv_stp.setColumnHidden(ldefs.D_STP_0, True)
        self.qtv_stp.resizeColumnsToContents()

        # make connections
        self.qtv_stp.selectionModel().currentRowChanged.connect(self.__on_strip_row_changed)

        # initial change
        self.__on_strip_row_changed(self.qtv_stp.currentIndex(), self.qtv_stp.currentIndex())

        # config ins/del buttons
        # self.btn_stp_ins.clicked.connect(self.__on_strip_add)
        # self.btn_stp_del.clicked.connect(self.__on_strip_remove)

        # logger
        # M_LOG.info("__config_strips:<<")

    # ---------------------------------------------------------------------------------------------
    # void (?)
    def __get_current_strip(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__get_current_strip:>>")

        # get current index
        l_index = self.qtv_stp.currentIndex()
                
        if not l_index.isValid():
            # return
            return None

        # get current row
        l_row = l_index.row()

        # get strip
        self.__strip_cur = self.__stp_model.lst_strips[l_row]
        assert self.__strip_cur

        # get strip info
        # l_info = self.__stp_model.data(self.__stp_model.index(l_row, ldefs.D_FIX_INFO)).toString()

        # M_LOG.debug("__on_strip_remove:l_strip.info: " + str(l_strip.s_info))
        # M_LOG.debug("__on_strip_remove:l_strip.info: " + str(l_info))

        # logger
        # M_LOG.info("__get_current_strip:<<")

        # return current strip
        return self.__strip_cur
        
    # ---------------------------------------------------------------------------------------------
    # void (?)
    def __get_status(self, f_strip):
        """
        DOCUMENT ME!

        @param f_strip: strip selecionada
        """
        # logger
        # M_LOG.info("__get_status:>>")

        # check input parameters
        # assert f_strip

        # nenhuma strip selecionada ?
        if f_strip is None:
            # logger
            # M_LOG.info("__get_status:<E01: nenhuma strip selecionada.")

            # return
            return

        # monta o request de status
        ls_req = "data/status.json?{}".format(f_strip.s_callsign)
        # M_LOG.debug("__get_status:ls_req:[{}]".format(ls_req))

        # get server address
        l_srv = self.__dct_config.get("srv.addr", None)
        
        if l_srv is not None:
            # obtém os dados de status da aneronave
            l_status = self.__sck_http.get_data(l_srv, ls_req)
            # M_LOG.debug("__get_status:l_status:[{}]".format(l_status))

            if (l_status is not None) and (l_status != ""):
                # salva os dados nos widgets
                ldct_status = json.loads(l_status)
                # M_LOG.debug("__get_status:ldct_status:[{}]".format(ldct_status))

            # senão, não achou no servidor...
            else:
                # logger
                l_log = logging.getLogger("CWndMainPiloto::__get_status")
                l_log.setLevel(logging.NOTSET)
                l_log.error(u"<E01: aeronave({}) não existe no servidor.".format(f_strip.s_callsign))

        # senão, não achou endereço do servidor
        else:
            # logger
            l_log = logging.getLogger("CWndMainPiloto::__get_status")
            l_log.setLevel(logging.NOTSET)
            l_log.warning(u"<E02: srv.addr não existe na configuração.")

        # logger
        # M_LOG.info("__get_status:<<")
        
    # ---------------------------------------------------------------------------------------------
    # void (?)
    def __make_connections(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__make_connections:>>")

        # verifica condições de execução
        # assert self._oWeather is not None
        # assert self._widPageWeatherConfig is not None
        # assert self.__widRadarScope is not None

        # assert self._actPause is not None
        # assert self._actZoomIn is not None
        # assert self._actZoomOut is not None
        # assert self._actInvert is not None

        # self._oWeather.qnhChanged.connect(self._widPageWeatherConfig.setQNH)
        # self._oWeather.surfaceWindChanged.connect(self._widPageWeatherConfig.setSurfaceWind)
        # self._oWeather.aloftWindChanged.connect(self._widPageWeatherConfig.setAloftWind)
        # self._oWeather.qnhChanged.connect(self.showQNH)
        # self._oWeather.qnhChanged.connect(self.showTL)
        # self._oWeather.surfaceWindChanged.connect(self.showWind)

        # self._actPause.toggled.connect(self.__widRadarScope.pause)
        # self._actZoomIn.triggered.connect(self.__widRadarScope.zoomIn)
        # self._actZoomIn.triggered.connect(self.__widRadarScope.showRange)
        # self._actZoomOut.triggered.connect(self.__widRadarScope.zoomOut)
        # self._actZoomOut.triggered.connect(self.__widRadarScope.showRange)
        # self._actInvert.toggled.connect(self.__widRadarScope.invert)

        # self.C_SIG_STRIP_CHG.connect(self.__on_strip_data_changed)

        # verifica condições de execução
        assert self.btn_cmd_altitude
        assert self.btn_cmd_direcao
        assert self.btn_cmd_velocidade
        
        # buttons connection
        self.btn_cmd_altitude.clicked.connect(self.__on_btn_cmd_altitude)
        self.btn_cmd_direcao.clicked.connect(self.__on_btn_cmd_direcao)
        self.btn_cmd_velocidade.clicked.connect(self.__on_btn_cmd_velocidade)

        # verifica condições de execução
        assert self.btn_send

        # send connection
        self.btn_send.clicked.connect(self.__on_btn_send)

        # logger
        # M_LOG.info("__make_connections:<<")

    # ---------------------------------------------------------------------------------------------
    # @QtCore.pyqtSlot()
    def notify(self, f_evt):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("notify:>>")

        # verifica parâmetros de entrada
        assert f_evt
                
        # recebeu um aviso de término da aplicação ?
        if isinstance(f_evt, events.CQuit):
            # para todos os processos
            # gdata.G_KEEP_RUN = False
                                                                        
            # aguarda o término das tasks
            time.sleep(1)
                                                                                                        
            # termina a aplicação
            # sys.exit()

        # recebeu um aviso de configuração de exercício ?
        elif isinstance(f_evt, evtcfg.CConfigExe):
            # atualiza exercício
            self.__statusbar.update_exe(f_evt.s_exe)

        # recebeu um aviso de hora de simulação ?
        elif isinstance(f_evt, evtcfg.CConfigHora):
            # atualiza horário
            self.__statusbar.update_hora(f_evt.t_hora)

        # logger
        # M_LOG.info("notify:<<")

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __on_btn_cmd_altitude(self):
        """
        callback do botão altitude da botoeira
        """
        # logger
        # M_LOG.info("__on_btn_cmd_altitude:>>")

        # existe strip selecionada ?
        if self.__get_current_strip() is not None:
            # obtém os dados de performance
            ldct_prf = self.__dct_prf.get(self.__strip_cur.s_prf, None)
            # M_LOG.debug("ldct_prf:[{}]".format(ldct_prf))

            # cria a dialog de altitude
            self.__dlg_altitude = dlgalt.CDlgAltitude(self.__strip_cur, ldct_prf, self)
            assert self.__dlg_altitude
                                                                                                    
            # exibe a dialog de altitude
            if self.__dlg_altitude.exec_():
                # coloca o comando no label
                self.lbl_comando.setText("{}: {}".format(self.__strip_cur.s_callsign, self.__dlg_altitude.get_data()))
                # M_LOG.debug("dialog data: " + str(self.lbl_comando.text()))

                # habilita o envio
                self.btn_send.setEnabled(True)

            # senão, <cancel>
            else:
                pass  # M_LOG.debug("dialog data: REJECTED !!!!")

        # logger
        # M_LOG.info("__on_btn_cmd_altitude:<<")

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __on_btn_cmd_direcao(self):
        """
        callback do botão direção da botoeira
        """
        # logger
        # M_LOG.info("__on_btn_cmd_direcao:>>")

        # existe strip selecionada ?
        if self.__get_current_strip() is not None:
            # já existe a dialog de direção ?
            if self.__dlg_direcao is None:
                # cria a dialog de direção
                self.__dlg_direcao = dlgdir.CDlgDirecao(self.__strip_cur.f_proa, self)
                assert self.__dlg_direcao
                                                                                                    
            # exibe a dialog de direção
            if self.__dlg_direcao.exec_():
                # coloca o comando no label
                self.lbl_comando.setText("{}: {}".format(self.__strip_cur.s_callsign, self.__dlg_direcao.get_data()))
                # M_LOG.debug("dialog data: " + str(self.__dlg_direcao.get_data()))

                # habilita o envio
                self.btn_send.setEnabled(True)

            # senão, <cancel>
            else:
                pass  # M_LOG.debug("dialog data: REJECTED !!!!")

        # logger
        # M_LOG.info("__on_btn_cmd_direcao:<<")

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __on_btn_cmd_velocidade(self):
        """
        callback do botão velocidade da botoeira
        """
        # logger
        # M_LOG.info("__on_btn_cmd_velocidade:>>")

        # existe strip selecionada ?
        if self.__get_current_strip() is not None:
            # obtém os dados de performance
            ldct_prf = self.__dct_prf.get(self.__strip_cur.s_prf, None)
            # M_LOG.debug("ldct_prf:[{}]".format(ldct_prf))

            # cria a dialog de velocidade
            self.__dlg_velocidade = dlgvel.CDlgVelocidade(self.__strip_cur, ldct_prf, self)
            assert self.__dlg_velocidade
                                                                                                    
            # exibe a dialog de velocidade
            if self.__dlg_velocidade.exec_():
                # coloca o comando no label
                self.lbl_comando.setText("{}: {}".format(self.__strip_cur.s_callsign, self.__dlg_velocidade.get_data()))
                # M_LOG.debug("dialog data: " + str(self.__dlg_velocidade.get_data()))

                # habilita o envio
                self.btn_send.setEnabled(True)

            # senão, <cancel>
            else:
                pass  # M_LOG.debug("dialog data: REJECTED !!!!")

        # logger
        # M_LOG.info("__on_btn_cmd_velocidade:<<")

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __on_btn_send(self):
        """
        callback do botão send
        """
        # logger
        # M_LOG.info("__on_btn_send:>>")
        
        # obtém o comando do label
        ls_cmd = self.lbl_comando.text()
        # M_LOG.debug("send command: " + str(self.lbl_comando.text()))

        # monta o buffer de envio
        ls_buff = str(gdefs.D_MSG_VRS) + gdefs.D_MSG_SEP + \
                  str(gdefs.D_MSG_PIL) + gdefs.D_MSG_SEP + \
                  str(ls_cmd)                
        # M_LOG.debug("ls_buff: " + str(ls_buff))

        # envia o comando
        self.__sck_snd_cpil.send_data(ls_buff)

        # coloca o comando no history
        self.qlw_history.insertItem(0, ls_cmd)

        # deshabilita o envio
        self.btn_send.setEnabled(False)

        # reset command
        if self.__strip_cur is not None:
            # limpa o comando
            self.lbl_comando.setText("{}: ".format(self.__strip_cur.s_callsign))

        # senão,...
        else:
            # limpa o comando
            self.lbl_comando.setText("")

        # logger
        # M_LOG.info("__on_btn_send:<<")

    # ---------------------------------------------------------------------------------------------
    '''
    # @QtCore.pyqtSlot()
    def __on_strip_add(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__on_strip_add:>>")

        # check exec conditions
        assert self.__scene
        assert self.__stp_model

        assert self.qtv_stp
        assert self.btn_stp_ins
        assert self.btn_stp_del

        # get row count
        l_row = self.__stp_model.rowCount()

        # insert row at end
        self.__stp_model.insertRows(l_row)

        # get row index
        l_index = self.__stp_model.index(l_row, 0)

        # get model
        l_strip = self.__stp_model.lst_strips[l_row]
        assert l_strip

        # insert strip on view
        self.__scene.strip_inserted(l_strip)

        # emit signal
        self.C_SIG_STRIP_INS.emit(l_strip)

        # resets the model to its original state in any attached views
        self.__stp_model.reset()

        # ajusta as colunas da view
        self.qtv_stp.resizeColumnsToContents()
        self.qtv_stp.setColumnHidden(ldefs.D_STP_0, True)

        # config ins/del buttons
        self.btn_stp_ins.setEnabled(True)
        self.btn_stp_del.setEnabled(self.__stp_model.rowCount() > 0)

        # get tableview
        self.qtv_stp.setFocus()
        self.qtv_stp.setCurrentIndex(l_index)
        self.qtv_stp.edit(l_index)

        # logger
        # M_LOG.info("__on_strip_add:>>")
    '''
    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(QtCore.QModelIndex,QtCore.QModelIndex)
    def __on_strip_row_changed(self, f_index_new, f_index_old):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__on_strip_row_changed:>>")

        # is index valid ?
        if f_index_old.isValid():
            # get old strip
            l_strip_old = self.__stp_model.lst_strips[f_index_old.row()]
            assert l_strip_old

            # M_LOG.debug("old strip callsign: " + str(l_strip_old.s_callsign))

        # is index valid ?
        if f_index_new.isValid():
            # get new strip
            self.__strip_cur = self.__stp_model.lst_strips[f_index_new.row()]
            assert self.__strip_cur

            # obtém o status da aeronave
            self.__get_status(self.__strip_cur)

            # habilita botoeira
            self.gbx_comandos.setEnabled(True)

            # inicia o comando
            self.lbl_comando.setText("{}: ".format(self.__strip_cur.s_callsign))

            # desabilita o envio
            self.btn_send.setEnabled(False)

            # emit signal
            self.C_SIG_STRIP_SEL.emit(self.__strip_cur)

        # M_LOG.debug("strip: " + str(self.__strip_cur))

        # logger
        # M_LOG.info("__on_strip_row_changed:<<")

    # ---------------------------------------------------------------------------------------------
    '''
    @QtCore.pyqtSlot(QtCore.QModelIndex, QtCore.QModelIndex)
    def __on_strip_data_changed(self, f_index_tl, f_index_br):
        """
        @param f_index_tl: topLeft index
        @param f_index_br: bottomRight index
        """
        # logger
        # M_LOG.info("__on_strip_data_changed:>>")

        # check input parameters
        assert f_index_tl

        # check exec conditions
        assert self.__stp_model
        # assert self.__scene

        # is index valid ?
        if f_index_tl.isValid():

            # get strip
            l_strip = self.__stp_model.lst_strips[f_index_tl.row()]
            assert l_strip

            # change strip on scene
            # self.__scene.strip_changed(l_strip)

        # logger
        # M_LOG.info("__on_strip_data_changed:<<")
    '''
    # ---------------------------------------------------------------------------------------------
    '''
    # @QtCore.pyqtSlot()
    def __on_strip_remove(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__on_strip_remove:>>")

        # check exec conditions
        assert self.__scene
        assert self.__stp_model

        assert self.qtv_stp
        assert self.btn_stp_ins
        assert self.btn_stp_del

        # get current index
        l_index = self.qtv_stp.currentIndex()

        if not l_index.isValid():
            return

        # get current row
        l_row = l_index.row()

        # get strip
        l_strip = self.__stp_model.lst_strips[l_row]
        assert l_strip

        # get strip info
        l_info = self.__stp_model.data(self.__stp_model.index(l_row, ldefs.D_FIX_INFO)).toString()

        # M_LOG.debug("__on_strip_remove:l_strip.info: " + str(l_strip.s_info))
        # M_LOG.debug("__on_strip_remove:l_strip.info: " + str(l_info))

        # ask user if it's ok
        if QtGui.QMessageBox.No == QtGui.QMessageBox.question(self, "Remove Strip",
                                       "Remove strip {} ?".format(l_info),
                                       QtGui.QMessageBox.Yes|QtGui.QMessageBox.No):
            # return
            return

        # remove a linha do modelo
        self.__stp_model.removeRows(l_row)

        # ajusta as colunas da view
        self.qtv_stp.resizeColumnsToContents()
        self.qtv_stp.setColumnHidden(ldefs.D_STP_0, True)

        # config ins/del buttons
        self.btn_stp_ins.setEnabled(True)
        self.btn_stp_del.setEnabled(self.__stp_model.rowCount() > 0)

        # select strip
        # self.__on_strip_row_changed(self.qtv_stp.currentIndex(), self.qtv_stp.currentIndex())

        # remove strip from scene
        self.__scene.remove_item(l_strip)

        # logger
        # M_LOG.info("__on_strip_remove:>>")
    '''
    # ---------------------------------------------------------------------------------------------
    # void (?)
    def __read_settings(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__read_settings:>>")

        l_settings = QtCore.QSettings("ICEA", "piloto")

        l_pos = l_settings.value("pos", QtCore.QPoint(200, 200)).toPoint()
        l_size = l_settings.value("size", QtCore.QSize(400, 400)).toSize()

        self.resize(l_size)
        self.move(l_pos)

        # logger
        # M_LOG.info("__read_settings:<<")

    # ---------------------------------------------------------------------------------------------
    # void (?)
    def __really_quit(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__really_quit:>>")

        l_ret = QtGui.QMessageBox.warning(self, self.tr("Piloto", None),
                                                self.tr("Do you want to quit Pilot ?", None),
                                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.Default, QtGui.QMessageBox.No)

        if QtGui.QMessageBox.Yes == l_ret:
            # logger
            # M_LOG.info("__really_quit:<E01")

            # retorna SIM
            return True

        # logger
        # M_LOG.info("__really_quit:<<")

        # retorna NÃO
        return False

    # ---------------------------------------------------------------------------------------------
    # void (?)
    @QtCore.pyqtSlot(QtCore.QTimerEvent)
    def timerEvent(self, f_evt):

        # logger
        # M_LOG.info("timerEvent:>>")

        # timer de fetch de dados de aeronave acionado ?
        if f_evt.timerId() == self.__i_timer_fetch:
            # for all flights...
            for l_callsign, l_flight in self.__dct_flight.iteritems():
                # M_LOG.debug("timerEvent:l_callsign: " + str(l_callsign))

                # new flight ?
                if l_flight not in self.__stp_model.lst_strips:
                    # insert flight on model
                    self.__stp_model.lst_strips.append(l_flight)

                    # reset flag de modificações
                    self.__stp_model.v_dirty = False

                    # emit signal
                    self.C_SIG_STRIP_INS.emit(l_flight)

                # senão, update data...
                # else:
                    # select strip
                    # self.__on_strip_data_changed(self.qtv_stp.currentIndex(), self.qtv_stp.currentIndex())
                
                    # reset flag de modificações
                    # self.__stp_model.v_dirty = True

                    # emit signal
                    # self.C_SIG_STRIP_CHG.emit(l_flight)

            # update view
            # self.__stp_model.dataChanged.emit(self.qtv_stp.currentIndex(), self.qtv_stp.currentIndex())
            self.__stp_model.layoutChanged.emit()

            # ajusta as colunas da view
            self.qtv_stp.resizeColumnsToContents()

        # timer de status de aeronave acionado ?
        elif f_evt.timerId() == self.__i_timer_status:
            # obtém o status da aeronave selecionada
            self.__get_status(self.__strip_cur)

        # logger
        # M_LOG.info("timerEvent:<<")

    # ---------------------------------------------------------------------------------------------
    # void (?)
    def __write_settings(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__write_settings:>>")

        l_settings = QtCore.QSettings("ICEA", "piloto")

        l_settings.setValue("pos", self.pos())
        l_settings.setValue("size", self.size())

        # logger
        # M_LOG.info("__write_settings:<<")

    # ---------------------------------------------------------------------------------------------
    # void (?)
    def xxx(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("xxx:>>")

        ###
        # strips

        # M_LOG.debug("xxx:dct_flight: " + str(self.__dct_flight))

        # build the list widgets
        for i in xrange(8):
            listItem = QtGui.QListWidgetItem(self.qlw_strips)
            listItem.setSizeHint(QtCore.QSize(300, 63))  # Or else the widget items will overlap(irritating bug)

            self.qlw_strips.setItemWidget(listItem, strips.CWidStrip(self.__control, i, self))

        # logger
        # M_LOG.info("xxx:<<")

# < the end >--------------------------------------------------------------------------------------
