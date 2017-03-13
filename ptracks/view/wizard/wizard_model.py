#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
wizard_model

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

# python library
import os
import sys

# PyQt library
from PyQt4 import QtCore, QtGui

# < class CWizardModel >---------------------------------------------------------------------------

class CWizardModel(QtGui.QDialog):

    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_parent=None):
        """
        initializes the wizard

        @param  f_parent: DOCUMENT ME!
        """
        # inicia a super classe
        super(CWizardModel, self).__init__(f_parent)

        # tem uma janela superior ?
        if f_parent is not None:
            # salva a parent window localmente
            self._wndParent = f_parent

            # esconde a parent window
            self._wndParent.setVisible(False)

        self._aoHistory = []

        self._btnCncl = QtGui.QPushButton(self.tr("&Cancela"))
        self._btnBack = QtGui.QPushButton(self.tr("< &Volta"))
        self._btnNext = QtGui.QPushButton(self.tr(u"&Próxima >"))
        self._btnTerm = QtGui.QPushButton(self.tr(u"&Ativa Simulação"))

        self.connect(self._btnCncl, QtCore.SIGNAL("clicked()"), self.reject)
        self.connect(self._btnBack, QtCore.SIGNAL("clicked()"), self.btnBackClicked)
        self.connect(self._btnNext, QtCore.SIGNAL("clicked()"), self.btnNextClicked)
        self.connect(self._btnTerm, QtCore.SIGNAL("clicked()"), self.accept)

        l_hblButton = QtGui.QHBoxLayout()
        assert l_hblButton is not None

        l_hblButton.addStretch(1)

        l_hblButton.addWidget(self._btnCncl)
        l_hblButton.addWidget(self._btnBack)
        l_hblButton.addWidget(self._btnNext)
        l_hblButton.addWidget(self._btnTerm)

        self._vblMain = QtGui.QVBoxLayout()
        assert self._vblMain is not None

        self._vblMain.addLayout(l_hblButton)

        self.setLayout(self._vblMain)

    # ---------------------------------------------------------------------------------------------
    def accept(self):
        """
        DOCUMENT ME!
        """
        # prossegue via "accept" default
        QtGui.QDialog.accept(self)

    # ---------------------------------------------------------------------------------------------
    def btnBackClicked(self):
        """
        DOCUMENT ME!
        """
        l_pagOld = self._aoHistory.pop()
        assert l_pagOld

        l_pagOld.reset_page()

        self.switchPage(l_pagOld)

    # ---------------------------------------------------------------------------------------------
    def btnNextClicked(self):
        """
        DOCUMENT ME!
        """
        l_pagOld = self._aoHistory[-1]
        assert l_pagOld

        l_pagNew = l_pagOld.next_page()
        assert l_pagNew

        l_pagNew.reset_page()

        self._aoHistory.append(l_pagNew)

        self.switchPage(l_pagOld)

    # ---------------------------------------------------------------------------------------------
    def completeStateChanged(self):
        """
        DOCUMENT ME!
        """
        l_pagAtu = self._aoHistory[-1]
        assert l_pagAtu

        if l_pagAtu.is_last_page():
            self._btnTerm.setEnabled(l_pagAtu.is_complete())

        else:
            self._btnNext.setEnabled(l_pagAtu.is_complete())

    # ---------------------------------------------------------------------------------------------
    def historyPages(self):
        """
        DOCUMENT ME!
        """
        # retorna o histórico de páginas
        return self._aoHistory

    # ---------------------------------------------------------------------------------------------
    def setFirstPage(self, f_pag):
        """
        DOCUMENT ME!
        """
        f_pag.reset_page()

        self._aoHistory.append(f_pag)

        self.switchPage(None)

    # ---------------------------------------------------------------------------------------------
    def switchPage(self, f_pagOld):
        """
        DOCUMENT ME!

        @param  f_pagOld : DOCUMENT ME!
        """
        if f_pagOld is not None:
            f_pagOld.hide()

            self._vblMain.removeWidget(f_pagOld)

            self.disconnect(f_pagOld, QtCore.SIGNAL("completeStateChanged())"), self.completeStateChanged)

        l_pagNew = self._aoHistory[-1]
        assert l_pagNew

        self._vblMain.insertWidget(0, l_pagNew)

        l_pagNew.show()
        l_pagNew.setFocus()

        self.connect(l_pagNew, QtCore.SIGNAL("completeStateChanged()"), self.completeStateChanged)

        self._btnBack.setEnabled(len(self._aoHistory) != 1)

        if l_pagNew.is_last_page():
            self._btnNext.setEnabled(False)
            self._btnTerm.setDefault(True)

        else:
            self._btnNext.setDefault(True)
            self._btnTerm.setEnabled(False)

        self.completeStateChanged()

# < the end >--------------------------------------------------------------------------------------
