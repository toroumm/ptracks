#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
pag_update

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

# < class CPagUpdate >-----------------------------------------------------------------------------

class CPagUpdate(QtGui.QWidget):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_parent=None):
        """
        DOCUMENT ME!
        """
        super(CPagUpdate, self).__init__(f_parent)

        lgbx_update = QtGui.QGroupBox("Package selection")
        assert lgbx_update

        lckx_system = QtGui.QCheckBox("Update system")
        assert lckx_system

        lckx_apps = QtGui.QCheckBox("Update applications")
        assert lckx_apps

        lckx_docs = QtGui.QCheckBox("Update documentation")
        assert lckx_docs

        lgbx_package = QtGui.QGroupBox("Existing packages")
        assert lgbx_package

        lqlw_package = QtGui.QListWidget()
        assert lqlw_package

        llwi_qt = QtGui.QListWidgetItem(lqlw_package)
        assert llwi_qt

        llwi_qt.setText("Qt")

        llwi_qsa = QtGui.QListWidgetItem(lqlw_package)
        assert llwi_qsa

        llwi_qsa.setText("QSA")

        llwi_team_builder = QtGui.QListWidgetItem(lqlw_package)
        assert llwi_team_builder

        llwi_team_builder.setText("Teambuilder")

        lbtn_start_update = QtGui.QPushButton("Start update")
        assert lbtn_start_update

        lvlo_update = QtGui.QVBoxLayout()
        assert lvlo_update

        lvlo_update.addWidget(lckx_system)
        lvlo_update.addWidget(lckx_apps)
        lvlo_update.addWidget(lckx_docs)
        lgbx_update.setLayout(lvlo_update)

        lvlo_package = QtGui.QVBoxLayout()
        assert lvlo_package

        lvlo_package.addWidget(lqlw_package)
        lgbx_package.setLayout(lvlo_package)

        lvlo_main = QtGui.QVBoxLayout()
        assert lvlo_main

        lvlo_main.addWidget(lgbx_update)
        lvlo_main.addWidget(lgbx_package)
        lvlo_main.addSpacing(12)
        lvlo_main.addWidget(lbtn_start_update)
        lvlo_main.addStretch(1)

        self.setLayout(lvlo_main)

# < the end >--------------------------------------------------------------------------------------
