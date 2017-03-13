#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
dock_procedures

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

# PyQt library
from PyQt4 import QtCore
from PyQt4 import QtGui

# model
import ptracks.model.newton.defs_newton as ndefs

# view
import ptracks.view.common.dock_procedures_ui as dckprc_ui

# control
# import control.control_debug as dbg

# import control.events.events_basic as events
# import control.events.events_config as evtcfg

# resources
import ptracks.view.resources.resources_rc

# < class CDockProcedures >------------------------------------------------------------------------

class CDockProcedures(QtGui.QDockWidget, dckprc_ui.Ui_dck_procedures):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control, f_parent):
        """
        constructor

        @param f_control: control manager
        @param f_parent: parent widget
        """
        # check input
        assert f_control

        # init super classe
        super(CDockProcedures, self).__init__(f_parent)

        # control
        self.__control = f_control
        # event
        # self.__event = f_control.event

        # register as event listener
        # self.__event.register_listener(self)

        # airspace
        self.__airspace = f_control.model.airspace

        # procedures dictionary
        self.__dct_visual = {}

        # create main Ui
        self.setupUi(self)

        # create windows elements
        self.__config_toolboxes()

    # ---------------------------------------------------------------------------------------------
    def __config_toolboxes(self):
        """
        DOCUMENT ME!
        """
        ###
        # toolbox

        # config toolbox
        self.tbx_procedures.setEnabled(True)

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
        #self.tbx_procedures.addItem(self._widPageRunwayConfig, self.tr("Runways"))

        ###
        # weather toolbox

        # create page weather widget
        #self._widPageWeatherConfig = wwc.widWeatherConfig(self)
        #assert self._widPageWeatherConfig

        # config page runways widget
        #self._widPageWeatherConfig.setGeometry(QtCore.QRect(0, 0, 212, 79))

        # put page weather in toolbox
        #self.tbx_procedures.addItem(self._widPageWeatherConfig, self.tr("Weather"))

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
        #self.tbx_procedures.addItem(self._qtwPageLand, self.tr("Landscape"))

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
        #self.tbx_procedures.addItem(self._qtwPageAirs, self.tr("Airspace"))

        # select toolbox item
        self.tbx_procedures.setCurrentIndex(0)

    # ---------------------------------------------------------------------------------------------
    def __load_tree_view(self, f_parent, f_dat):
        """
        DOCUMENT ME!
        """
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
                    l_item.setIcon(0, QtGui.QIcon(QtGui.QPixmap(":/images/maps.png")))

                elif l_key.startswith("NDB"):
                    l_item.setIcon(0, QtGui.QIcon(QtGui.QPixmap(":/images/ndb.png")))

                elif l_key.startswith("Navaids"):
                    l_item.setIcon(0, QtGui.QIcon(QtGui.QPixmap(":/images/navaid.png")))

                else:
                    l_item.setIcon(0, QtGui.QIcon(QtGui.QPixmap(":/images/navaid.png")))

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

    # ---------------------------------------------------------------------------------------------
    def __add_navaids(self, f_parent):
        """
        DOCUMENT ME!
        """
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

    # ---------------------------------------------------------------------------------------------
    def __add_procs(self, f_parent):
        """
        DOCUMENT ME!
        """
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

    # ---------------------------------------------------------------------------------------------
    def __add_tree_parent(self, f_parent, f_column, flst_val, l_data):
        """
        DOCUMENT ME!
        """
        # create item
        l_item = QtGui.QTreeWidgetItem(f_parent, flst_val)
        assert l_item

        # set item data
        l_item.setData(f_column, QtCore.Qt.UserRole, l_data)
        l_item.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.ShowIndicator)
        l_item.setExpanded(True)

        # return
        return l_item

    # ---------------------------------------------------------------------------------------------
    def __add_tree_child(self, f_parent, f_column, flst_val, l_data):
        """
        DOCUMENT ME!
        """
        # create item
        l_item = QtGui.QTreeWidgetItem(f_parent, flst_val)
        assert l_item

        # save data on item
        l_item.setData(f_column, QtCore.Qt.UserRole, l_data)

        # set initial state to checked
        l_item.setCheckState(f_column, QtCore.Qt.Checked)

        # return
        return l_item

    # ---------------------------------------------------------------------------------------------
    def tree_navaids_changed(self, f_item, f_column):
        """
        DOCUMENT ME!
        """
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
            # logger
            l_log = logging.getLogger("CDockProcedures::tree_navaids_changed")
            l_log.setLevel(logging.ERROR)
            l_log.error(u"<E01: what else ?")

        # update radar scope
        # self.__slate_radar.repaint()

    # ---------------------------------------------------------------------------------------------
    def tree_procs_changed(self, f_item, f_column):
        """
        DOCUMENT ME!
        """
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
            # logger
            l_log = logging.getLogger("CDockProcedures::tree_procs_changed")
            l_log.setLevel(logging.ERROR)
            l_log.error(u"<E01: what else ?")

        # update radar scope
        # self.__slate_radar.repaint()

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
