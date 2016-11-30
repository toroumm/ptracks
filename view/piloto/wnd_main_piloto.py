#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
wnd_main_piloto

DOCUMENT ME!

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

import sip
sip.setapi('QString', 2)

# PyQt library
from PyQt4 import QtCore
from PyQt4 import QtGui

# model
import model.glb_defs as gdefs

import model.piloto.aircraft_piloto as anv
import model.piloto.defs_piloto as ldefs
# import model.piloto.strip_model as mstp
import model.piloto.strip_table_model as stm

# view
import view.piloto.statusbar_piloto as statusbar
import view.piloto.strip_visil as strips
import view.piloto.wnd_main_piloto_ui as wndmain_ui

import view.piloto.dlg_altitude as dlgalt
import view.piloto.dlg_decolagem as dlgdep
import view.piloto.dlg_direcao as dlgdir
import view.piloto.dlg_dir_fixo as dlgfix
import view.piloto.dlg_espera as dlgesp
import view.piloto.dlg_pouso as dlgarr
import view.piloto.dlg_subida as dlgsub
import view.piloto.dlg_trajetoria as dlgtrj
import view.piloto.dlg_velocidade as dlgvel

# control
import control.control_debug as dbg

import control.events.events_basic as events
import control.events.events_config as evtcfg

# resources
# import icons_rc
# import resources_visil_rc

# < class CWndMainPiloto >---------------------------------------------------------------------------

class CWndMainPiloto(QtGui.QMainWindow, wndmain_ui.Ui_wndMainPiloto):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    # signals
    # C_SIG_STRIP_CHG = QtCore.pyqtSignal(anv.CAircraftPiloto)
    # C_SIG_STRIP_DEL = QtCore.pyqtSignal(anv.CAircraftPiloto)
    C_SIG_STRIP_INS = QtCore.pyqtSignal(anv.CAircraftPiloto)
    C_SIG_STRIP_SEL = QtCore.pyqtSignal(anv.CAircraftPiloto)

    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control):
        """
        @param f_control: control manager
        """
        # check input
        assert f_control

        # inicia a super classe
        super(CWndMainPiloto, self).__init__()

        # salva o control manager localmente
        self.__control = f_control
        assert self.__control

        # salva a lista de pousos
        self.__lst_arr = f_control.model.lst_arr_dep
        assert self.__lst_arr is not None

        # salva a lista de decolagens
        self.__lst_dep = f_control.model.lst_arr_dep
        assert self.__lst_dep is not None

        # salva o dicionário de esperas
        self.__dct_esp = f_control.model.dct_esp
        assert self.__dct_esp is not None

        # salva o dicionário de fixos
        self.__dct_fix = f_control.model.dct_fix
        assert self.__dct_fix is not None

        # salva o dicionário de performances
        self.__dct_prf = f_control.model.dct_prf
        assert self.__dct_prf is not None

        # salva o dicionário de subidas
        self.__dct_sub = f_control.model.dct_sub
        assert self.__dct_sub is not None

        # salva o dicionário de trajetórias
        self.__dct_trj = f_control.model.dct_trj
        assert self.__dct_trj is not None

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
        self.status_bar = statusbar.CStatusBarPiloto(self)
        assert self.status_bar

        # config statusBar
        self.setStatusBar(self.status_bar)

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

        # fetch aircrafts data timer (1s cycle)
        self.__i_timer_fetch = self.startTimer(1000)

        # fetch status data timer (2s cycle)
        self.__i_timer_status = self.startTimer(2000)

        # config tableview
        self.qtv_stp.setFocus()
        self.qtv_stp.setCurrentIndex(self.__stp_model.index(0, 0))

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def about(self):
        """
        DOCUMENT ME!
        """
        # show about box
        QtGui.QMessageBox.about(self, self.tr("About Piloto", None),
                                      self.tr("Activate runways for arrival in the Settings. Runway Config Dialog\n"
                                              "Click Blips to give instructions.\n"
                                              "Press 'h' for heading, 'd' for direct, 'r' for routing, 'a' for approach clearance.\n"
                                              "Press Escape or RMB to cancel.\n"
                                              "Use the middle mouse button to center your radar screen.\n"
                                              "[vertical navigation and departing aircraft not yet implemented]\n"
                                              "pre-alpha release! Please report bugs to openapproach@aufroof.org", None))

    # ---------------------------------------------------------------------------------------------
    # @QtCore.pyqtSlot()
    def closeEvent(self, f_evt):
        """
        DOCUMENT ME!
        """
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

    # ---------------------------------------------------------------------------------------------
    def __config_buttons(self):
        """
        DOCUMENT ME!
        """
        ###
        # buttons

        # nenhuma aeronave selecionada ?
        if self.__strip_cur is None:
            # disable all buttons
            self.btn_cancela.setEnabled(False)

            self.btn_cmd_altitude.setEnabled(False)
            self.btn_cmd_direcao.setEnabled(False)
            self.btn_cmd_velocidade.setEnabled(False)

            self.btn_prc_ape.setEnabled(False)
            self.btn_prc_apx.setEnabled(False)
            self.btn_prc_arr.setEnabled(False)
            self.btn_prc_dep.setEnabled(False)
            self.btn_prc_dir_fixo.setEnabled(False)
            self.btn_prc_esp.setEnabled(False)
            self.btn_prc_ils.setEnabled(False)
            # self.btn_prc_sub.setEnabled(False)
            self.btn_prc_trj.setEnabled(False)

            self.btn_cod_emg.setEnabled(False)
            self.btn_cod_spi.setEnabled(False)
            self.btn_cod_ssr.setEnabled(False)

        # senão, tem aeronave selecionada
        else:
            # enable buttons
            self.btn_cancela.setEnabled(False)

            self.btn_cmd_altitude.setEnabled(True)
            self.btn_cmd_direcao.setEnabled(True)
            self.btn_cmd_velocidade.setEnabled(True)

            self.btn_prc_ape.setEnabled(False)
            self.btn_prc_apx.setEnabled(False)
            self.btn_prc_arr.setEnabled(self.__strip_cur.f_alt > 0.)
            self.btn_prc_dep.setEnabled(self.__strip_cur.f_alt == 0.)
            self.btn_prc_dir_fixo.setEnabled(True)
            self.btn_prc_esp.setEnabled(True)
            self.btn_prc_ils.setEnabled(False)
            # self.btn_prc_sub.setEnabled(True)
            self.btn_prc_trj.setEnabled(True)

            self.btn_cod_emg.setEnabled(False)
            self.btn_cod_spi.setEnabled(False)
            self.btn_cod_ssr.setEnabled(False)

    # ---------------------------------------------------------------------------------------------
    def __config_strips(self):
        """
        DOCUMENT ME!
        """
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

    # ---------------------------------------------------------------------------------------------
    def __get_current_strip(self):
        """
        DOCUMENT ME!
        """
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

        # dbg.M_DBG.debug("__on_strip_remove:l_strip.info: " + str(l_strip.s_info))
        # dbg.M_DBG.debug("__on_strip_remove:l_strip.info: " + str(l_info))

        # return current strip
        return self.__strip_cur

    # ---------------------------------------------------------------------------------------------
    def __get_status(self, f_strip):
        """
        DOCUMENT ME!

        @param f_strip: strip selecionada
        """
        # check input parameters
        # assert f_strip

        # nenhuma strip selecionada ?
        if f_strip is None:
            # nenhuma strip selecionada. return
            return

        # monta o request de status
        ls_req = "data/status.json?{}".format(f_strip.s_callsign)
        # dbg.M_DBG.debug("__get_status:ls_req:[{}]".format(ls_req))

        # get server address
        l_srv = self.__dct_config.get("srv.addr", None)

        if l_srv is not None:
            # obtém os dados de status da aneronave
            l_status = self.__sck_http.get_data(l_srv, ls_req)
            # dbg.M_DBG.debug("__get_status:l_status:[{}]".format(l_status))

            if (l_status is not None) and (l_status != ""):
                # obtém os dados de status
                ldct_status = json.loads(l_status)
                # dbg.M_DBG.debug("__get_status:ldct_status:[{}]".format(ldct_status))

                # salva os dados nos widgets
                self.__set_status(ldct_status)

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

    # ---------------------------------------------------------------------------------------------
    def __make_connections(self):
        """
        DOCUMENT ME!
        """
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

        self.btn_prc_arr.clicked.connect(self.__on_btn_prc_arr)
        self.btn_prc_dep.clicked.connect(self.__on_btn_prc_dep)
        self.btn_prc_dir_fixo.clicked.connect(self.__on_btn_prc_dir_fixo)
        self.btn_prc_esp.clicked.connect(self.__on_btn_prc_esp)
        # self.btn_prc_sub.clicked.connect(self.__on_btn_prc_sub)
        self.btn_prc_trj.clicked.connect(self.__on_btn_prc_trj)

        # verifica condições de execução
        assert self.btn_send

        # send connection
        self.btn_send.clicked.connect(self.__on_btn_send)

    # ---------------------------------------------------------------------------------------------
    # @QtCore.pyqtSlot()
    def notify(self, f_evt):
        """
        DOCUMENT ME!
        """
        # check input
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
            self.status_bar.update_exe(f_evt.s_exe)

        # recebeu um aviso de hora de simulação ?
        elif isinstance(f_evt, evtcfg.CConfigHora):
            # atualiza horário
            self.status_bar.update_hora(f_evt.t_hora)

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __on_btn_cmd_altitude(self):
        """
        callback do botão altitude da botoeira
        """
        # existe strip selecionada ?
        if self.__get_current_strip() is not None:
            # obtém os dados de performance
            ldct_prf = self.__dct_prf.get(self.__strip_cur.s_prf, None)
            # dbg.M_DBG.debug("ldct_prf:[{}]".format(ldct_prf))

            # cria a dialog de altitude
            self.__dlg_altitude = dlgalt.CDlgAltitude(self.__strip_cur, ldct_prf, self)
            assert self.__dlg_altitude

            # exibe a dialog de altitude
            if self.__dlg_altitude.exec_():
                # coloca o comando no label
                self.lbl_comando.setText("{}: {}".format(self.__strip_cur.s_callsign, self.__dlg_altitude.get_data()))
                # dbg.M_DBG.debug("dialog data: " + str(self.lbl_comando.text()))

                # habilita o envio
                self.btn_send.setEnabled(True)

            # senão, <cancel>
            else: pass
                # dbg.M_DBG.debug("dialog data: REJECTED !!!!")

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __on_btn_cmd_direcao(self):
        """
        callback do botão direção da botoeira
        """
        # existe strip selecionada ?
        if self.__get_current_strip() is not None:
            # cria a dialog de direção
            self.__dlg_direcao = dlgdir.CDlgDirecao(self.__strip_cur.f_proa, self)
            assert self.__dlg_direcao

            # exibe a dialog de direção
            if self.__dlg_direcao.exec_():
                # coloca o comando no label
                self.lbl_comando.setText("{}: {}".format(self.__strip_cur.s_callsign, self.__dlg_direcao.get_data()))
                # dbg.M_DBG.debug("dialog data: " + str(self.__dlg_direcao.get_data()))

                # habilita o envio
                self.btn_send.setEnabled(True)

            # senão, <cancel>
            else: pass
                # dbg.M_DBG.debug("dialog data: REJECTED !!!!")

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __on_btn_cmd_velocidade(self):
        """
        callback do botão velocidade da botoeira
        """
        # existe strip selecionada ?
        if self.__get_current_strip() is not None:
            # obtém os dados de performance
            ldat_prf = self.__dct_prf.get(self.__strip_cur.s_prf, None)
            # dbg.M_DBG.debug("ldat_prf:[{}]".format(ldat_prf))

            # cria a dialog de velocidade
            self.__dlg_velocidade = dlgvel.CDlgVelocidade(self.__strip_cur, ldat_prf, self)
            assert self.__dlg_velocidade

            # exibe a dialog de velocidade
            if self.__dlg_velocidade.exec_():
                # coloca o comando no label
                self.lbl_comando.setText("{}: {}".format(self.__strip_cur.s_callsign, self.__dlg_velocidade.get_data()))
                # dbg.M_DBG.debug("dialog data: " + str(self.__dlg_velocidade.get_data()))

                # habilita o envio
                self.btn_send.setEnabled(True)

            # senão, <cancel>
            else: pass
                # dbg.M_DBG.debug("dialog data: REJECTED !!!!")

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __on_btn_prc_arr(self):
        """
        callback do botão procedimento de pouso da botoeira
        """
        # existe strip selecionada ?
        if self.__get_current_strip() is not None:
            # cria a dialog de pouso
            ldlg_pouso = dlgarr.CDlgPouso(self.__sck_http, self.__dct_config, self.__strip_cur, self.__lst_arr, self)
            assert ldlg_pouso

            # exibe a dialog de pouso
            if ldlg_pouso.exec_():
                # coloca o comando no label
                self.lbl_comando.setText("{}: {}".format(self.__strip_cur.s_callsign, ldlg_pouso.get_data()))
                # dbg.M_DBG.debug("dialog data: " + str(ldlg_pouso.get_data()))

                # habilita o envio
                self.btn_send.setEnabled(True)

            # senão, <cancel>
            else: pass
                # dbg.M_DBG.debug("dialog data: REJECTED !!!!")

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __on_btn_prc_dep(self):
        """
        callback do botão procedimento de decolagem da botoeira
        """
        # existe strip selecionada ?
        if self.__get_current_strip() is not None:
            # cria a dialog de decolagem
            ldlg_decolagem = dlgdep.CDlgDecolagem(self.__sck_http, self.__dct_config, self.__strip_cur, self.__lst_dep, self)
            assert ldlg_decolagem

            # exibe a dialog de pouso
            if ldlg_decolagem.exec_():
                # coloca o comando no label
                self.lbl_comando.setText("{}: {}".format(self.__strip_cur.s_callsign, ldlg_decolagem.get_data()))
                # dbg.M_DBG.debug("dialog data: " + str(ldlg_decolagem.get_data()))

                # habilita o envio
                self.btn_send.setEnabled(True)

            # senão, <cancel>
            else: pass
                # dbg.M_DBG.debug("dialog data: REJECTED !!!!")

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __on_btn_prc_dir_fixo(self):
        """
        callback do botão procedimento de direcionamento a fixo da botoeira
        """
        # existe strip selecionada ?
        if self.__get_current_strip() is not None:
            # cria a dialog de espera
            ldlg_dir_fixo = dlgfix.CDlgDirFixo(self.__sck_http, self.__dct_config, self.__strip_cur, self.__dct_fix, self)
            assert ldlg_dir_fixo

            # exibe a dialog de direcionamento a fixo
            if ldlg_dir_fixo.exec_():
                # coloca o comando no label
                self.lbl_comando.setText("{}: {}".format(self.__strip_cur.s_callsign, ldlg_dir_fixo.get_data()))
                # dbg.M_DBG.debug("dialog data: " + str(ldlg_dir_fixo.get_data()))

                # habilita o envio
                self.btn_send.setEnabled(True)

            # senão, <cancel>
            else: pass
                # dbg.M_DBG.debug("dialog data: REJECTED !!!!")

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __on_btn_prc_esp(self):
        """
        callback do botão procedimento de espera da botoeira
        """
        # existe strip selecionada ?
        if self.__get_current_strip() is not None:
            # cria a dialog de espera
            ldlg_espera = dlgesp.CDlgEspera(self.__sck_http, self.__dct_config, self.__strip_cur, self.__dct_esp, self)
            assert ldlg_espera

            # exibe a dialog de espera
            if ldlg_espera.exec_():
                # coloca o comando no label
                self.lbl_comando.setText("{}: {}".format(self.__strip_cur.s_callsign, ldlg_espera.get_data()))
                # dbg.M_DBG.debug("dialog data: " + str(ldlg_espera.get_data()))

                # habilita o envio
                self.btn_send.setEnabled(True)

            # senão, <cancel>
            else: pass
                # dbg.M_DBG.debug("dialog data: REJECTED !!!!")

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __on_btn_prc_sub(self):
        """
        callback do botão procedimento de subida da botoeira
        """
        # logger
        # dbg.M_DBG.info("__on_btn_prc_sub:>>")

        # existe strip selecionada ?
        if self.__get_current_strip() is not None:
            # cria a dialog de subida
            ldlg_subida = dlgsub.CDlgSubida(self.__sck_http, self.__dct_config, self.__strip_cur, self.__dct_sub, self)
            assert ldlg_subida

            # exibe a dialog de subida
            if ldlg_subida.exec_():
                # coloca o comando no label
                self.lbl_comando.setText("{}: {}".format(self.__strip_cur.s_callsign, ldlg_subida.get_data()))
                # dbg.M_DBG.debug("dialog data: " + str(ldlg_subida.get_data()))

                # habilita o envio
                self.btn_send.setEnabled(True)

            # senão, <cancel>
            else: pass
                # dbg.M_DBG.debug("dialog data: REJECTED !!!!")

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __on_btn_prc_trj(self):
        """
        callback do botão procedimento de trajetória da botoeira
        """
        # existe strip selecionada ?
        if self.__get_current_strip() is not None:
            # cria a dialog de trajetória
            ldlg_trajetoria = dlgtrj.CDlgTrajetoria(self.__sck_http, self.__dct_config, self.__strip_cur, self.__dct_trj, self)
            assert ldlg_trajetoria

            # exibe a dialog de trajetória
            if ldlg_trajetoria.exec_():
                # coloca o comando no label
                self.lbl_comando.setText("{}: {}".format(self.__strip_cur.s_callsign, ldlg_trajetoria.get_data()))
                # dbg.M_DBG.debug("dialog data: " + str(ldlg_trajetoria.get_data()))

                # habilita o envio
                self.btn_send.setEnabled(True)

            # senão, <cancel>
            else: pass
                # dbg.M_DBG.debug("dialog data: REJECTED !!!!")

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __on_btn_send(self):
        """
        callback do botão send
        """
        # obtém o comando do label
        ls_cmd = self.lbl_comando.text()
        # dbg.M_DBG.debug("send command: " + str(self.lbl_comando.text()))

        # monta o buffer de envio
        ls_buff = str(gdefs.D_MSG_VRS) + gdefs.D_MSG_SEP + \
                  str(gdefs.D_MSG_PIL) + gdefs.D_MSG_SEP + \
                  str(ls_cmd)
        # dbg.M_DBG.debug("ls_buff: " + str(ls_buff))

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

    # ---------------------------------------------------------------------------------------------
    '''
    # @QtCore.pyqtSlot()
    def __on_strip_add(self):
        """
        DOCUMENT ME!
        """
        # logger
        # dbg.M_DBG.info("__on_strip_add:>>")

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
        # dbg.M_DBG.info("__on_strip_add:>>")
    '''
    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(QtCore.QModelIndex,QtCore.QModelIndex)
    def __on_strip_row_changed(self, f_index_new, f_index_old):
        """
        DOCUMENT ME!
        """
        # is index valid ?
        if f_index_old.isValid():
            # get old strip
            l_strip_old = self.__stp_model.lst_strips[f_index_old.row()]
            assert l_strip_old

            # dbg.M_DBG.debug("old strip callsign: " + str(l_strip_old.s_callsign))

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

        # dbg.M_DBG.debug("strip: " + str(self.__strip_cur))

        # reconfig buttons
        self.__config_buttons()

    # ---------------------------------------------------------------------------------------------
    '''
    @QtCore.pyqtSlot(QtCore.QModelIndex, QtCore.QModelIndex)
    def __on_strip_data_changed(self, f_index_tl, f_index_br):
        """
        @param f_index_tl: topLeft index
        @param f_index_br: bottomRight index
        """
        # logger
        # dbg.M_DBG.info("__on_strip_data_changed:>>")

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
        # dbg.M_DBG.info("__on_strip_data_changed:<<")
    '''
    # ---------------------------------------------------------------------------------------------
    '''
    # @QtCore.pyqtSlot()
    def __on_strip_remove(self):
        """
        DOCUMENT ME!
        """
        # logger
        # dbg.M_DBG.info("__on_strip_remove:>>")

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

        # dbg.M_DBG.debug("__on_strip_remove:l_strip.info: " + str(l_strip.s_info))
        # dbg.M_DBG.debug("__on_strip_remove:l_strip.info: " + str(l_info))

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
        # dbg.M_DBG.info("__on_strip_remove:>>")
    '''
    # ---------------------------------------------------------------------------------------------
    def __read_settings(self):
        """
        DOCUMENT ME!
        """
        l_settings = QtCore.QSettings("ICEA", "Piloto")

        l_pos = l_settings.value("pos", QtCore.QPoint(200, 200)).toPoint()
        l_size = l_settings.value("size", QtCore.QSize(400, 400)).toSize()

        self.resize(l_size)
        self.move(l_pos)

    # ---------------------------------------------------------------------------------------------
    def __really_quit(self):
        """
        DOCUMENT ME!
        """
        l_ret = QtGui.QMessageBox.warning(self, self.tr("Piloto", None),
                                                self.tr("Do you want to quit Pilot ?", None),
                                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.Default, QtGui.QMessageBox.No)

        if QtGui.QMessageBox.Yes == l_ret:
            # retorna SIM
            return True

        # retorna NÃO
        return False

    # ---------------------------------------------------------------------------------------------
    def __set_status(self, fdct_status):
        """
        DOCUMENT ME!
        """
        # obtém a função operacional atual
        ls_fnc_ope = fdct_status.get("fnc_ope", None)

        # obtém o número do procedimento
        ls_prc_id = fdct_status.get("prc_id", None)

        # set label
        self.lbl_prc.setText("{}/{}".format(ls_fnc_ope, ls_prc_id))

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(QtCore.QTimerEvent)
    def timerEvent(self, f_evt):
        """
        DOCUMENT ME!
        """
        # timer de fetch de dados de aeronave acionado ?
        if f_evt.timerId() == self.__i_timer_fetch:
            # for all flights...
            for l_callsign, l_flight in self.__dct_flight.iteritems():
                # dbg.M_DBG.debug("timerEvent:l_callsign: " + str(l_callsign))

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

    # ---------------------------------------------------------------------------------------------
    def __write_settings(self):
        """
        DOCUMENT ME!
        """
        l_settings = QtCore.QSettings("ICEA", "Piloto")

        l_settings.setValue("pos", self.pos())
        l_settings.setValue("size", self.size())

    # ---------------------------------------------------------------------------------------------
    def xxx(self):
        """
        DOCUMENT ME!
        """
        ###
        # strips

        # dbg.M_DBG.debug("xxx:dct_flight: " + str(self.__dct_flight))

        # build the list widgets
        for i in xrange(10):
            listItem = QtGui.QListWidgetItem(self.qlw_strips)
            listItem.setSizeHint(QtCore.QSize(300, 63))  # Or else the widget items will overlap(irritating bug)

            self.qlw_strips.setItemWidget(listItem, strips.CWidStrip(self.__control, i, self))

# < the end >--------------------------------------------------------------------------------------
