#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
dlg_config

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

revision 0.2  2017/jan  mlabru
pep8 style conventions

revision 0.1  2016/dez  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2017/01"

# < imports >--------------------------------------------------------------------------------------

# PyQt library
from PyQt4 import QtCore
from PyQt4 import QtGui

try:
    import view.resources.super_resources_rc2
    
except ImportError:
    import view.resources.super_resources_rc3

# view
# import view.super.page_model as wpm
import view.super.pag_config as pcfg
import view.super.pag_query as pqry
import view.super.pag_update as pupd

# < class CDlgConfig >-----------------------------------------------------------------------------

class CDlgConfig(QtGui.QDialog):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_parent=None):
        """
        initializes the wizard
        """
        # init super class
        super(CDlgConfig, self).__init__(f_parent)

        self.__wdg_contents = QtGui.QListWidget()
        assert self.__wdg_contents
        
        self.__wdg_contents.setViewMode(QtGui.QListView.IconMode)
        self.__wdg_contents.setIconSize(QtCore.QSize(96, 84))
        self.__wdg_contents.setMovement(QtGui.QListView.Static)
        self.__wdg_contents.setMaximumWidth(128)
        self.__wdg_contents.setSpacing(12)

        self.__wdg_pages = QtGui.QStackedWidget()
        assert self.__wdg_pages
        
        self.__wdg_pages.addWidget(pcfg.CPagConfig())
        self.__wdg_pages.addWidget(pupd.CPagUpdate())
        self.__wdg_pages.addWidget(pqry.CPagQuery())

        lbtn_close = QtGui.QPushButton("Close")
        assert lbtn_close

        lbtn_close.clicked.connect(self.close)

        self.__create_icons()

        self.__wdg_contents.setCurrentRow(0)

        lhlo_horizontal = QtGui.QHBoxLayout()
        assert lhlo_horizontal
        
        lhlo_horizontal.addWidget(self.__wdg_contents)
        lhlo_horizontal.addWidget(self.__wdg_pages, 1)

        lhlo_buttons = QtGui.QHBoxLayout()
        assert lhlo_buttons
        
        lhlo_buttons.addStretch(1)
        lhlo_buttons.addWidget(lbtn_close)

        lvlo_main = QtGui.QVBoxLayout()
        assert lvlo_main 

        lvlo_main.addLayout(lhlo_horizontal)
        lvlo_main.addStretch(1)
        lvlo_main.addSpacing(12)
        lvlo_main.addLayout(lhlo_buttons)

        self.setLayout(lvlo_main)

        self.setWindowTitle("Config Dialog")

    # ---------------------------------------------------------------------------------------------
    def __change_page(self, f_current, f_previous):
        """
        DOCUMENT ME!
        """
        if not f_current:
            f_current = f_previous

        self.__wdg_pages.setCurrentIndex(self.__wdg_contents.row(f_current))

    # ---------------------------------------------------------------------------------------------
    def __create_icons(self):
        """
        DOCUMENT ME!
        """
        lbtn_config = QtGui.QListWidgetItem(self.__wdg_contents)
        assert lbtn_config
        
        lbtn_config.setIcon(QtGui.QIcon(':/images/config.png'))
        lbtn_config.setText("Configuration")
        lbtn_config.setTextAlignment(QtCore.Qt.AlignHCenter)
        lbtn_config.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        lbtn_update = QtGui.QListWidgetItem(self.__wdg_contents)
        assert lbtn_update

        lbtn_update.setIcon(QtGui.QIcon(':/images/update.png'))
        lbtn_update.setText("Update")
        lbtn_update.setTextAlignment(QtCore.Qt.AlignHCenter)
        lbtn_update.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        lbtn_query = QtGui.QListWidgetItem(self.__wdg_contents)
        assert lbtn_query

        lbtn_query.setIcon(QtGui.QIcon(':/images/query.png'))
        lbtn_query.setText("Query")
        lbtn_query.setTextAlignment(QtCore.Qt.AlignHCenter)
        lbtn_query.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        self.__wdg_contents.currentItemChanged.connect(self.__change_page)

# < the end >--------------------------------------------------------------------------------------
