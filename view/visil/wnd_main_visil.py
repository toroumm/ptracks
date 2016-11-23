#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
wnd_main_visil

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

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/12"

# < imports >--------------------------------------------------------------------------------------

# Python library
import logging
import random
import sys
import time

# PyQt library
from PyQt4 import QtCore
from PyQt4 import QtGui

# model
import model.glb_data as gdata
import model.newton.defs_newton as ndefs
import model.visil.defs_visil as ldefs
# import model.visil.airspace as airs
# import model.visil.landscape as lands
# import model.visil.weather as wtr
import model.visil.strip_model as mstp
import model.visil.strip_table_model as stm

# view
import view.visil.slate_radar as sltrdr
import view.visil.statusbar_visil as stbar
import view.visil.strip_visil as strp
#import view.visil.wid_runway_config as wrc
#import view.visil.wid_weather_config as wwc
import view.visil.wnd_main_visil_ui as wndmain_ui

# control
import control.events.events_basic as events

# resources
import icons_rc
import resources_visil_rc

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CWndMainVisil >--------------------------------------------------------------------------

class CWndMainVisil(QtGui.QMainWindow, wndmain_ui.Ui_wndMainVisil):
    """
    DOCUMENT ME!
    """
    # signals
    # C_SIG_STRIP_CHG = QtCore.pyqtSignal(anv.CAircraftPiloto)
    # C_SIG_STRIP_DEL = QtCore.pyqtSignal(anv.CAircraftPiloto)
    # C_SIG_STRIP_INS = QtCore.pyqtSignal(anv.CAircraftPiloto)
    # C_SIG_STRIP_SEL = QtCore.pyqtSignal(anv.CAircraftPiloto)
                    
    # ---------------------------------------------------------------------------------------------
    # void (?)
    def __init__(self, f_control):
        """
        constructor

        @param f_control: control manager
        """
        # logger
        # M_LOG.info("__init__:>>")

        # check input
        assert f_control

        # inicia a super classe
        super(CWndMainVisil, self).__init__()

        # save control manager
        self.__control = f_control
        # save model manager
        self.__model = f_control.model
        # save event manager
        self.__event = f_control.event

        # register as event listener
        self.__event.register_listener(self)
        '''
        # save config manager
        self.__config = f_control.config
        assert self.__config

        # save config dictionary
        self.__dct_config = self.__config.dct_config
        assert self.__dct_config
        '''
        # init color dictionary
        gdata.G_DCT_COLORS = {}
                
        # load color dictionary
        for l_key, l_val in f_control.view.colors.c_dct_color.iteritems():
            gdata.G_DCT_COLORS[l_key] = QtGui.QColor(l_val[1][0], l_val[1][1], l_val[1][2])

        # save airspace
        self.__airspace = f_control.model.airspace
                
        # save flights dictionary
        self.__dct_flight = f_control.model.emula_model.dct_flight  
        assert self.__dct_flight is not None
                        
        # procedures dictionary
        self.__dct_visual = {}
                        
        # current strip
        self.__strip_cur = None
                
        # create main Ui
        self.setupUi(self)

        # the slate radar is the main widget
        self.__slate_radar = sltrdr.CSlateRadar(f_control, self)
        assert self.__slate_radar

        # the radar screen goes to central widget
        self.setCentralWidget(self.__slate_radar)

        # window title
        self.setWindowTitle(self.tr(u"ViSIL 0.1 [Visualização]", None,))

        # create status bar
        self.status_bar = stbar.CStatusBarVisil(self)
        assert self.status_bar

        # config statusBar
        self.setStatusBar(self.status_bar)

        # config flight strips
        self.__config_strips()

        # create windows elements
        self.__create_actions()
        self.__create_toolbars()
        self.__config_toolboxes()

        # make SIGNAL-SLOT connections
        self.__make_connections()

        # get initial values from weather()
        # self.__weather.initSignals()

        # read saved settings
        self.__read_settings()

        # XXX
        self.xxx()

        # clock timer (1s cycle)
        self.__i_timer_clock = self.startTimer(1000)

        # fetch aircrafts data timer (1s cycle)
        self.__i_timer_fetch = self.startTimer(1000)
                
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
        QtGui.QMessageBox.about(self, self.tr("About ViSIL"),
                                      self.tr("Lorem ipsum dolor sit amet, no vim quas animal intellegam.\n"
                                              "Click pro ad impetus tractatos deterruisset. Atqui tritani ut.\n"
                                              "Per postea conclusionemque ad, discere scripserit referrentur.\n"
                                              "Eos esse commune atomorum et, ex mei appareat platonem.\n"
                                              "Use the middle mouse button to center your radar screen.\n"
                                              "pre-alpha release! Please report bugs to bugtrack@icea.gov.br"))

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
            # save actual config
            self.__write_settings()

            # accept
            f_evt.accept()

            # create CQuit event
            l_evt = events.CQuit()
            assert l_evt

            # dispatch event
            self.__event.post(l_evt)

        # otherwise, continua...
        else:
            # ignore
            f_evt.ignore()

        # logger
        # M_LOG.info("closeEvent:<<")

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
        self.qtv_stp.setColumnHidden(ldefs.D_STP_ID, True)
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
    def __config_toolboxes(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__config_toolboxes:>>")

        ###
        # toolbox

        # config toolbox
        self.tool_box.setEnabled(True)

        ###
        # procedures toolbox

        assert self.tree_procs

        # config 
        # self.tree_procs.setHeaderHidden(True)
        self.tree_procs.setHeaderLabels(["Procedure", "Description", "Breakpoints"])

        # cria a procedures tree
        self.__add_procs(self.tree_procs.invisibleRootItem())
        self.tree_procs.itemChanged.connect(self.tree_procs_changed)

        ###
        # navaids toolbox

        assert self.tree_navaids

        # config 
        # self.tree_navaids.setHeaderHidden(True)
        self.tree_navaids.setHeaderLabels(["Navaid", "Description"])

        # cria a procedures tree
        self.__add_navaids(self.tree_navaids.invisibleRootItem())
        self.tree_navaids.itemChanged.connect(self.tree_navaids_changed)

        ###
        # runways toolbox

        # create page runways widget
        #self._widPageRunwayConfig = wrc.widRunwayConfig(self)
        #assert self._widPageRunwayConfig

        # runways have to be dynamically added
        #for l_oRWY in self.__airspace.lstRWY:
            #self._widPageRunwayConfig.addRunway(l_oRWY.sName)

        # config page runways widget
        #self._widPageRunwayConfig.setGeometry(QtCore.QRect(0, 0, 212, 79))

        # put page runways in toolbox
        #self.tool_box.addItem(self._widPageRunwayConfig, self.tr("Runways"))

        ###
        # weather toolbox

        # create page weather widget
        #self._widPageWeatherConfig = wwc.widWeatherConfig(self)
        #assert self._widPageWeatherConfig

        # config page runways widget
        #self._widPageWeatherConfig.setGeometry(QtCore.QRect(0, 0, 212, 79))

        # put page weather in toolbox
        #self.tool_box.addItem(self._widPageWeatherConfig, self.tr("Weather"))

        ###
        # landscape toolbox

        # create landscape tree view
        #self._qtwPageLand = QtGui.QTreeWidget()
        #assert self._qtwPageLand

        # config landscape tree widget
        #self._qtwPageLand.setGeometry(QtCore.QRect(0, 0, 212, 158))
        #self._qtwPageLand.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        #### self._qtwPageLand.setModel ( model )
        #self._qtwPageLand.setUniformRowHeights(True)
        #self._qtwPageLand.headerItem().setText(0, self.tr("Graphical Items"))
        #self._qtwPageLand.itemChanged.connect(self.__update_checks)

        # carrega dos dados na QTreeView
        #self.__load_tree_view(self._qtwPageLand, self.__landscape.treeMaps.toDict())

        # put page in toolbox
        #self.tool_box.addItem(self._qtwPageLand, self.tr("Landscape"))

        ###
        # airspace toolbox

        # create airspace tree view
        #self._qtwPageAirs = QtGui.QTreeWidget()
        #assert self._qtwPageAirs

        # config airspace tree widget
        #self._qtwPageAirs.setGeometry(QtCore.QRect(0, 0, 212, 158))
        #self._qtwPageAirs.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        ##### self._qtwPageAirs.setModel ( model )
        #self._qtwPageAirs.setUniformRowHeights(True)
        #self._qtwPageAirs.headerItem().setText(0, self.tr("Graphical Items"))
        #self._qtwPageAirs.itemChanged.connect(self.__update_checks)

        # carrega dos dados na QTreeView
        #self.__load_tree_view(self._qtwPageAirs, self.__landscape.treeMaps.toDict())

        # put page in toolbox
        #self.tool_box.addItem(self._qtwPageAirs, self.tr("Airspace"))

        # select toolbox item
        self.tool_box.setCurrentIndex(0)

        # logger
        # M_LOG.info("__config_toolboxes:<<")

    # ---------------------------------------------------------------------------------------------
    # void (?)
    def __create_actions(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__create_actions:>>")

        # action new
        self.__act_new = QtGui.QAction(QtGui.QIcon(":/pixmaps/gamenew.xpm"), self.tr("&New"), self)
        assert self.__act_new is not None

        # config action new
        self.__act_new.setShortcut(self.tr("Ctrl+N"))
        self.__act_new.setStatusTip(self.tr("Start a new console"))
        # FIXME
        self.__act_new.setEnabled(False)

        # connect action new
        self.__act_new.triggered.connect(self.newCons)

        # action pause
        self.__act_pause = QtGui.QAction(QtGui.QIcon(":/pixmaps/gamepause.xpm"), self.tr("&Pause"), self)
        assert self.__act_pause is not None

        # config action pause
        self.__act_pause.setCheckable(True)
        self.__act_pause.setChecked(False)
        self.__act_pause.setShortcut(self.tr("Ctrl+P"))
        self.__act_pause.setStatusTip(self.tr("Pause the console"))

        # action quit
        self.__act_quit = QtGui.QAction(QtGui.QIcon(":/pixmaps/gamequit.xpm"), self.tr("&Quit"), self)
        assert self.__act_quit is not None

        # config action quit
        self.__act_quit.setShortcut(self.tr("Ctrl+Q"))
        self.__act_quit.setStatusTip(self.tr("Leave the console"))

        # connect action quit
        self.__act_quit.triggered.connect(QtGui.qApp.closeAllWindows)

        # action zoomIn
        self.__act_zoom_in = QtGui.QAction(QtGui.QIcon(":/pixmaps/zoomin.xpm"), self.tr("Zoom &In"), self)
        assert self.__act_zoom_in is not None

        # config action zoomIn
        self.__act_zoom_in.setShortcut(self.tr("Ctrl++"))
        self.__act_zoom_in.setStatusTip(self.tr("Set coverage of radar screen"))

        self.__act_zoom_in.triggered.connect(self.__slate_radar.zoom_in)
        self.__act_zoom_in.triggered.connect(self.__slate_radar.showRange)

        # action zoomOut
        self.__act_zoom_out = QtGui.QAction(QtGui.QIcon(":/pixmaps/zoomout.xpm"), self.tr("Zoom &Out"), self)
        assert self.__act_zoom_out is not None

        # config action zoomOut
        self.__act_zoom_out.setShortcut(self.tr("Ctrl+-"))
        self.__act_zoom_out.setStatusTip(self.tr("Set coverage of radar screen"))

        self.__act_zoom_out.triggered.connect(self.__slate_radar.zoom_out)
        self.__act_zoom_out.triggered.connect(self.__slate_radar.showRange)

        # action invert
        self.__act_invert = QtGui.QAction(QtGui.QIcon(":/pixmaps/invert.xpm"), self.tr("&Invert Screen"), self)
        assert self.__act_invert is not None

        # config action invert
        self.__act_invert.setCheckable(True)
        self.__act_invert.setChecked(False)
        self.__act_invert.setShortcut(self.tr("Ctrl+I"))
        self.__act_invert.setStatusTip(self.tr("Invert radar screen"))

        # action about
        self.__act_about = QtGui.QAction(self.tr("&About"), self)
        assert self.__act_about is not None

        # config action about
        self.__act_about.setStatusTip(self.tr("About ViSIL"))

        # connect action about
        self.__act_about.triggered.connect(self.about)

        # action aboutQt
        self.__act_about_qt = QtGui.QAction(self.tr("About &Qt"), self)
        assert self.__act_about_qt is not None

        # config action aboutQt
        self.__act_about_qt.setStatusTip(self.tr("About Qt"))

        # connect action aboutQt
        self.__act_about_qt.triggered.connect(QtGui.qApp.aboutQt)

        # logger
        # M_LOG.info("__create_actions:<<")

    # ---------------------------------------------------------------------------------------------
    # void (?)
    def __create_toolbars(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__create_toolbars:>>")

        # create toolBar file
        ltbr_file = self.addToolBar(self.tr("File"))
        assert ltbr_file is not None

        ltbr_file.addAction(self.__act_quit)
        ltbr_file.addAction(self.__act_new)
        ltbr_file.addAction(self.__act_pause)

        # create toolBar view
        ltbr_view = self.addToolBar(self.tr("View"))
        assert ltbr_view is not None

        ltbr_view.addAction(self.__act_zoom_out)
        ltbr_view.addAction(self.__act_zoom_in)
        ltbr_view.addAction(self.__act_invert)

        # create toolBar help
        ltbr_help = self.addToolBar(self.tr("Help"))
        assert ltbr_help is not None

        ltbr_help.addAction(self.__act_about)
        ltbr_help.addAction(self.__act_about_qt)

        # logger
        # M_LOG.info("__create_toolbars:<<")

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
    def __load_tree_view(self, f_parent, f_dat):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__load_tree_view:>>")

        # recebeu um dicionário ?
        if isinstance(f_dat, dict):
            # para todos os ítens no dicionário...
            for l_key, l_val in f_dat.iteritems():
                # cria uma linha de mapa
                l_item = QtGui.QTreeWidgetItem(f_parent)
                assert l_item

                # configura o item
                l_item.setText(0, l_key)
                l_item.setCheckState(0, QtCore.Qt.Checked)
                l_item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)

                # seleciona o ícone pelo tipo de mapa
                if l_key.startswith("MAP"):
                    l_item.setIcon(0, QtGui.QIcon(QtGui.QPixmap(":/Camera.png")))

                elif l_key.startswith("NDB"):
                    l_item.setIcon(0, QtGui.QIcon(QtGui.QPixmap(":/Transform.png")))

                elif l_key.startswith("Navaids"):
                    l_item.setIcon(0, QtGui.QIcon(QtGui.QPixmap(":/Light.png")))

                else:
                    l_item.setIcon(0, QtGui.QIcon(QtGui.QPixmap(":/Transform.png")))

                # expande a árvore
                l_item.setExpanded(True)

                # propaga os itens
                self.__load_tree_view(l_item, l_val)

        # otherwise, é uma lista
        else:
            '''
            # para todos os ítens na lista...
            for l_txt in f_dat:

                # cria uma linha de mapa
                l_item = QtGui.QTreeWidgetItem ( f_parent )
                assert l_item

                # configura o item
                l_item.setText ( 0, l_txt )
                l_item.setCheckState ( 0, QtCore.Qt.Unchecked )
                l_item.setFlags ( QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled )
            '''
            # save nome do mapa na widget
            f_parent.setData(0, QtCore.Qt.WhatsThisRole, QtCore.QVariant(f_dat))

        # logger
        # M_LOG.info("__load_tree_view:<<")

    # ---------------------------------------------------------------------------------------------
    # void (?)
    def __make_connections(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__make_connections:>>")

        # verifica condições de execução
        #assert self.__weather is not None
        #assert self._widPageWeatherConfig is not None
        assert self.__slate_radar is not None

        assert self.__act_pause is not None
        assert self.__act_zoom_in is not None
        assert self.__act_zoom_out is not None
        assert self.__act_invert is not None

        # self.__weather.qnhChanged.connect(self._widPageWeatherConfig.setQNH)
        # self.__weather.surfaceWindChanged.connect(self._widPageWeatherConfig.setSurfaceWind)
        # self.__weather.aloftWindChanged.connect(self._widPageWeatherConfig.setAloftWind)
        # self.__weather.qnhChanged.connect(self.showQNH)
        # self.__weather.qnhChanged.connect(self.showTL)
        # self.__weather.surfaceWindChanged.connect(self.showWind)

        self.__act_pause.toggled.connect(self.__slate_radar.pause)
        self.__act_invert.toggled.connect(self.__slate_radar.invert)

        # logger
        # M_LOG.info("__make_connections:<<")

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def newCons(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("newCons:>>")
        pass

    # -->FIXME
    #    del self.__slate_radar
    #    del self.__weather

    #    self.__weather = clsWeather.clsWeather ( self.__airspace )
    #    assert self.__weather is not None

    #    self.__slate_radar = widRadarScope.widRadarScope ( self )
    #    assert self.__slate_radar is not None

    #    self.setCentralWidget ( self.__slate_radar )

    #    self.__make_connections ()

    #    self.__weather.initSignals ()

        # logger
        # M_LOG.info("newCons:<<")

    # ---------------------------------------------------------------------------------------------
    # void (?)
    def notify(self, f_evt):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("notify:>>")

        pass

        # logger
        # M_LOG.info("notify:<<")

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

            # habilita botoeira
            # self.gbx_comandos.setEnabled(True)

            # inicia o comando
            # self.lbl_comando.setText("{}: ".format(self.__strip_cur.s_callsign))

            # desabilita o envio
            # self.btn_send.setEnabled(False)

            # emit signal
            # self.C_SIG_STRIP_SEL.emit(self.__strip_cur)

        # M_LOG.debug("strip: " + str(self.__strip_cur))

        # logger
        # M_LOG.info("__on_strip_row_changed:<<")

    # ---------------------------------------------------------------------------------------------
    # void (?)
    def __read_settings(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__read_settings:>>")

        l_settings = QtCore.QSettings("ICEA", "visil")

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

        l_ret = QtGui.QMessageBox.warning(self,
                    self.tr("ViSIL"),
                    self.tr("Do you want to quit ViSIL ?"),
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.Default, QtGui.QMessageBox.No)

        if l_ret == QtGui.QMessageBox.Yes:
            # logger
            # M_LOG.info("__really_quit:<E01")

            # return SIM
            return True

        # logger
        # M_LOG.info("__really_quit:<<")

        # return NÃO
        return False

    # ---------------------------------------------------------------------------------------------
    # void (?)
    def __recursive_checks(self, fo_parent):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__recursive_checks:>>")

        # obtém o checkState
        l_checkState = fo_parent.checkState(0)

        # o nó é uma folha ? (i.e. sem filhos)
        if 0 == fo_parent.childCount():
            # o nó tem dados associados ?
            if fo_parent.data(0, QtCore.Qt.WhatsThisRole).toPyObject() is not None:
                # obtém o nome do mapa
                l_sName = fo_parent.data(0, QtCore.Qt.WhatsThisRole).toPyObject()[0]

                # nome válido ?
                if l_sName is not None:
                    # obtém o mapa
                    l_map = self.__slate_radar.findMap(l_sName)

                    # achou o mapa ?
                    if l_map is not None:
                        # muda o status de exibição
                        l_map.showMap(QtCore.Qt.Checked == l_checkState)

        # para todos os filhos...
        for l_i in xrange(fo_parent.childCount()):
            # muda o checkState
            fo_parent.child(l_i).setCheckState(0, l_checkState)
            fo_parent.child(l_i).setDisabled(QtCore.Qt.Unchecked == l_checkState)

            # o nó tem dados associados ?
            if fo_parent.data(0, QtCore.Qt.WhatsThisRole).toPyObject() is not None:
                # obtém o nome do mapa
                l_sName = fo_parent.child(l_i).data(0, QtCore.Qt.WhatsThisRole).toPyObject()[0]
                # M_LOG.debug("l_sName: " + l_sName)

                # nome válido ?
                if l_sName is not None:
                    # obtém o mapa
                    l_map = self.__slate_radar.findMap(l_sName)

                    # achou o mapa ?
                    if l_map is not None:
                        # muda o status de exibição
                        l_map.showMap(QtCore.Qt.Checked == l_checkState)

            # propaga aos filhos
            self.__recursive_checks(fo_parent.child(l_i))

        # logger
        # M_LOG.info("__recursive_checks:<<")

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(int)
    def showCoords(self, f_coords):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("showCoords:>>")

        self.status_bar.lblCoords.setText(u"99ᵒ 99' 99\" N 999ᵒ 99' 99\" E" % int(f_coords))

        # logger
        # M_LOG.info("showCoords:<<")

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(int)
    def showQNH(self, f_qnh):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("showQNH:>>")

        self.status_bar.lblQNH.setText("Q%d" % int(f_qnh))

        # logger
        # M_LOG.info("showQNH:<<")

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(int)
    def showTL(self, f_qnh):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("showTL:>>")

        # TODO: airport specific
        if f_qnh >= 1013.:
            l_tl = 60.

        else:
            l_tl = 70.

        self.status_bar.lblTL.setText("TL%d" % int(l_tl))

        # logger
        # M_LOG.info("showTL:<<")

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(int, int)
    def showWind(self, f_dir, f_v):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("showWind:>>")

        if f_v == 0.:
            l_windstring = "CALM"

        else:
            l_windstring = "%d%c/%dkt" % (int(f_dir), u'°'.encode("utf-8")[1:], int(f_v))

        self.status_bar.lblWind.setText(l_windstring)

        # logger
        # M_LOG.info("showWind:<<")

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(QtCore.QTimerEvent)
    def timerEvent(self, f_evt):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("timerEvent:>>")

        # clock timer event ?
        if f_evt.timerId() == self.__i_timer_clock:
            # display simulation time
            self.lbl_hora.setText(self.__control.sim_time.get_hora_format())

        # flight data fetch timer event ?
        elif f_evt.timerId() == self.__i_timer_fetch:
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
                    # self.C_SIG_STRIP_INS.emit(l_flight)

                # otherwise, update data...
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

        # logger
        # M_LOG.info("timerEvent:<<")

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot("QTreeWidgetItem", int)
    def __update_checks(self, f_item, f_iColumn):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__update_checks:>>")

        # checkState is stored on column 0
        if 0 != f_iColumn:
            # logger
            # M_LOG.info("__update_checks:<E01: checkState is stored on column 0.")

            # return
            return

        # propaga
        self.__recursive_checks(f_item)

        # logger
        # M_LOG.info("__update_checks:<<")

    # ---------------------------------------------------------------------------------------------
    # void (?)
    def __write_settings(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__write_settings:>>")

        l_settings = QtCore.QSettings("ICEA", "visil")

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

        # build the list widgets
        for i in xrange(8):
            listItem = QtGui.QListWidgetItem(self.qlw_strips)
            listItem.setSizeHint(QtCore.QSize(300, 63))  # Or else the widget items will overlap (irritating bug)
            self.qlw_strips.setItemWidget(listItem, strp.CWidStrip(self.__control, i, self))

        # logger
        # M_LOG.info("xxx:<<")

    # ---------------------------------------------------------------------------------------------
    # void (?)
    def __add_navaids(self, f_parent):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__add_navaids:>>")

        l_column = 0

        dme_item = self.__add_tree_parent(f_parent, l_column, ["DMEs"], "data DME")
        vor_item = self.__add_tree_parent(f_parent, l_column, ["VORs"], "data VOR")
        ndb_item = self.__add_tree_parent(f_parent, l_column, ["NDBs"], "data NDB")
        wpt_item = self.__add_tree_parent(f_parent, l_column, ["Waypoints"], "data Waypoints")

        # for all navaids...
        for l_fix in self.__airspace.dct_fix.values():
            # build item
            llst_data = [ndefs.D_FMT_FIX.format(l_fix.s_fix_indc), l_fix.s_fix_desc]

            # DME ?
            if ndefs.E_DME == l_fix.en_fix_tipo:
                # list DME
                self.__add_tree_child(dme_item, l_column, llst_data, True)

            # NDB ?
            elif ndefs.E_NDB == l_fix.en_fix_tipo:
                # list NDB
                self.__add_tree_child(ndb_item, l_column, llst_data, True)

            # VOR ?
            elif ndefs.E_VOR == l_fix.en_fix_tipo:
                # list VOR
                self.__add_tree_child(vor_item, l_column, llst_data, True)

            # otherwise,...
            else:
                # list waypoints
                self.__add_tree_child(wpt_item, l_column, llst_data, True)

            # save on dictionary
            self.__dct_visual[ndefs.D_FMT_FIX.format(l_fix.s_fix_indc)] = True

        # logger
        # M_LOG.info("__add_navaids:<<")

    # ---------------------------------------------------------------------------------------------
    # void (?)
    def __add_procs(self, f_parent):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__add_procs:>>")

        l_column = 0

        aproximacoes_item = self.__add_tree_parent(f_parent, l_column, [u"Aproximações"], "data Aproximações")

        # for all approachs...
        for l_apx in self.__airspace.dct_apx.values():
            # build item
            llst_data = [ndefs.D_FMT_APX.format(l_apx.i_prc_id), l_apx.s_prc_desc, str(len(l_apx.lst_apx_brk))]

            # list approach
            self.__add_tree_child(aproximacoes_item, l_column, llst_data, True)

            # save on dictionary
            self.__dct_visual[ndefs.D_FMT_APX.format(l_apx.i_prc_id)] = True

        esperas_item = self.__add_tree_parent(f_parent, l_column, ["Esperas"], "data Esperas")

        # for all holdings...
        for l_esp in self.__airspace.dct_esp.values():
            # build item
            llst_data = [ndefs.D_FMT_ESP.format(l_esp.i_prc_id), l_esp.s_prc_desc, str(0)]

            # list holding
            self.__add_tree_child(esperas_item, l_column, llst_data, True)

            # save on dictionary
            self.__dct_visual[ndefs.D_FMT_ESP.format(l_esp.i_prc_id)] = True

        subidas_item = self.__add_tree_parent(f_parent, l_column, ["Subidas"], "data Subidas")

        # for all subidas...
        for l_sub in self.__airspace.dct_sub.values():
            # build item
            llst_data = [ndefs.D_FMT_SUB.format(l_sub.i_prc_id), l_sub.s_prc_desc, str(len(l_sub.lst_sub_brk))]

            # list subida
            self.__add_tree_child(subidas_item, l_column, llst_data, True)

            # save on dictionary
            self.__dct_visual[ndefs.D_FMT_SUB.format(l_sub.i_prc_id)] = True

        trajetorias_item = self.__add_tree_parent(f_parent, l_column, [u"Trajetórias"], "data Trajetorias")

        # for all trajectories...
        for l_trj in self.__airspace.dct_trj.values():
            # build item
            llst_data = [ndefs.D_FMT_TRJ.format(l_trj.i_prc_id), l_trj.s_prc_desc, str(len(l_trj.lst_trj_brk))]

            # list trajectory
            self.__add_tree_child(trajetorias_item, l_column, llst_data, True)                                        

            # save on dictionary
            self.__dct_visual[ndefs.D_FMT_TRJ.format(l_trj.i_prc_id)] = True

        # logger
        # M_LOG.info("__add_procs:<<")

    # ---------------------------------------------------------------------------------------------
    # void (?)
    def __add_tree_parent(self, f_parent, f_column, flst_val, l_data):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__add_tree_parent:>>")

        # create item
        l_item = QtGui.QTreeWidgetItem(f_parent, flst_val)
        assert l_item
        
        # set item data
        l_item.setData(f_column, QtCore.Qt.UserRole, l_data)
        l_item.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.ShowIndicator)
        l_item.setExpanded(True)

        # logger
        # M_LOG.info("__add_tree_parent:<<")

        # return
        return l_item

    # ---------------------------------------------------------------------------------------------
    # void (?)
    def __add_tree_child(self, f_parent, f_column, flst_val, l_data):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__add_tree_child:>>")

        # create item
        l_item = QtGui.QTreeWidgetItem(f_parent, flst_val)
        assert l_item

        # save data on item
        l_item.setData(f_column, QtCore.Qt.UserRole, l_data)

        # set initial state to checked
        l_item.setCheckState(f_column, QtCore.Qt.Checked)

        # logger
        # M_LOG.info("__add_tree_child:<<")

        # return
        return l_item

    # ---------------------------------------------------------------------------------------------
    # void (?)
    def tree_navaids_changed(self, f_item, f_column):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("tree_navaids_changed:>>")

        # item checked ?
        if f_item.checkState(f_column) == QtCore.Qt.Checked:
            # M_LOG.debug("tree_navaids_changed: checked {}/{}".format(f_item, f_item.text(f_column)))

            # save data on item
            f_item.setData(f_column, QtCore.Qt.UserRole, True)

            # change dictionary
            self.__dct_visual[f_item.text(f_column)] = True

        # item unchecked ?
        elif f_item.checkState(f_column) == QtCore.Qt.Unchecked:
            # M_LOG.debug("tree_navaids_changed: unchecked {}/{}".format(f_item, f_item.text(f_column)))

            # save data on item
            f_item.setData(f_column, QtCore.Qt.UserRole, False)

            # change dictionary
            self.__dct_visual[f_item.text(f_column)] = False

        # otherwise,...
        else:
            pass  # l_log.warning("tree_navaids_changed:<E01: what else ?")

        # update radar scope
        self.__slate_radar.repaint()
        
        # logger
        # M_LOG.info("tree_navaids_changed:<<")

    # ---------------------------------------------------------------------------------------------
    # void (?)
    def tree_procs_changed(self, f_item, f_column):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("tree_procs_changed:>>")

        # item checked ?
        if f_item.checkState(f_column) == QtCore.Qt.Checked:
            # save data on item
            f_item.setData(f_column, QtCore.Qt.UserRole, True)

            # change dictionary
            self.__dct_visual[f_item.text(f_column)] = True

        # item unchecked ?
        elif f_item.checkState(f_column) == QtCore.Qt.Unchecked:
            # save data on item
            f_item.setData(f_column, QtCore.Qt.UserRole, False)

            # change dictionary
            self.__dct_visual[f_item.text(f_column)] = False

        # otherwise,...
        else:
            pass  # l_log.warning("tree_procs_changed:<E01: what else ?")

        # update radar scope
        self.__slate_radar.repaint()
        
        # logger
        # M_LOG.info("tree_procs_changed:<<")

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_visual(self):
        """
        get visual dictionary
        """
        return self.__dct_visual

# < the end >--------------------------------------------------------------------------------------
