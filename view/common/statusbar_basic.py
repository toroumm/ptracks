#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
statusbar_basic

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

# pyQt library
from PyQt4 import Qt
from PyQt4 import QtCore
from PyQt4 import QtGui

# < class CStatusBarBasic >------------------------------------------------------------------------

class CStatusBarBasic(QtGui.QStatusBar):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_parent=None):
        """
        constructor
        """
        # verifica parâmetros de entrada
        assert f_parent

        # init super class
        super(CStatusBarBasic, self).__init__(f_parent)

        # QMainWindow
        self.__parent = f_parent

        # local variables
        self.__lbl_coord = None
        self.__lbl_exe = None
        self.__lbl_hora = None
        self.__lbl_msg = None
        self.__lbl_range = None

        # config status bar
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.setAttribute(QtCore.Qt.WA_NoSystemBackground)

        # self.setBackgroundMode(QtCore.Qt.NoBackground)
        # self.setStyleSheet("color: black;\nbackground-color: transparent;")

        # create permanent widgets
        self.__create_statusbar_labels()

        # add widgets in status bar
        self.addWidget(self.__lbl_msg)

        # add permanent widgets in status bar
        self.addPermanentWidget(self.__lbl_coord)
        self.addPermanentWidget(self.__lbl_range)
        self.addPermanentWidget(self.__lbl_exe)
        self.addPermanentWidget(self.__lbl_hora)

        # exibe a status bar
        self.show()

        # show temporary message (5s)
        self.showMessage(QtGui.QApplication.translate("CStatusBarBasic", "Ready", None, QtGui.QApplication.UnicodeUTF8), 5000)

    # ---------------------------------------------------------------------------------------------
    def __create_statusbar_labels(self):
        """
        DOCUMENT ME!
        """
        # mensagem
        self.__lbl_msg = QtGui.QLabel(self)
        assert self.__lbl_msg

        self.__lbl_msg.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.__lbl_msg.setMinimumSize(self.__lbl_msg.sizeHint())

        # coordinates label
        self.__lbl_coord = QtGui.QLabel(self)
        assert self.__lbl_coord

        self.__lbl_coord.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.__lbl_coord.setMinimumSize(self.__lbl_coord.sizeHint())

        # range label
        self.__lbl_range = QtGui.QLabel(self)
        assert self.__lbl_range

        self.__lbl_range.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.__lbl_range.setMinimumSize(self.__lbl_range.sizeHint())
        self.__lbl_range.setAutoFillBackground(True)

        l_pal = self.__lbl_range.palette()
        l_col = QtGui.QColor(255, 255, 150)
        assert l_col

        l_pal.setColor(QtGui.QPalette.Window, l_col)
        self.__lbl_range.setPalette(l_pal)

        # exercício
        self.__lbl_exe = QtGui.QLabel(self)
        assert self.__lbl_exe

        self.__lbl_exe.setAlignment(QtCore.Qt.AlignHCenter)
        self.__lbl_exe.setMinimumSize(self.__lbl_exe.sizeHint())
        self.__lbl_exe.setAutoFillBackground(True)

        l_pal = self.__lbl_exe.palette()
        l_pal.setColor(QtGui.QPalette.Window, QtGui.QColor(150, 255, 255))

        self.__lbl_exe.setPalette(l_pal)

        # horário
        self.__lbl_hora = QtGui.QLabel(self)
        assert self.__lbl_hora

        self.__lbl_hora.setAlignment(QtCore.Qt.AlignHCenter)
        self.__lbl_hora.setMinimumSize(self.__lbl_hora.sizeHint())
        self.__lbl_hora.setAutoFillBackground(True)

        l_pal = self.__lbl_hora.palette()
        l_pal.setColor(QtGui.QPalette.Window, QtGui.QColor(255, 255, 150))

        self.__lbl_hora.setPalette(l_pal)

    # ---------------------------------------------------------------------------------------------
    def update_coordinates(self, fs_coordinates, fv_update=True):
        """
        updates the latitude and longitude on the status bar of radar screen
        """
        # flag update ?
        if fv_update:
            # set latitude/longitude coordinates label
            self.__lbl_coord.setText(fs_coordinates)

            # update status bar
            self.update()

    # ---------------------------------------------------------------------------------------------
    def update_exe(self, fs_exe, fv_update=True):
        """
        DOCUMENT ME!
        """
        # flag update ?
        if fv_update:
            # independant mode ?
            self.__lbl_exe.setText(fs_exe)

            # update status bar
            self.update()

    # ---------------------------------------------------------------------------------------------
    def update_hora(self, fs_hora, fv_update=True):
        """
        DOCUMENT ME!
        """
        # set hora label
        self.__lbl_hora.setText(fs_hora)

        # flag update ?
        if fv_update:
            # update status bar
            self.update()

    # ---------------------------------------------------------------------------------------------
    def update_msg(self, fs_msg, fv_update=True):
        """
        DOCUMENT ME!
        """
        # flag update ?
        if fv_update:
            # set message label
            self.__lbl_msg.setText(fs_msg)

            # update status bar
            self.update()

    # ---------------------------------------------------------------------------------------------
    def update_range(self, fi_range, fv_update=True):
        """
        updates the range on the status bar of radar windows
        """
        # flag update ?
        if fv_update:
            # set range label
            self.__lbl_range.setText("R%d" % fi_range)

            # update status bar
            self.update()

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def lbl_coord(self):
        """
        get coordenadas
        """
        return self.__lbl_coord

    @lbl_coord.setter
    def lbl_coord(self, f_val):
        """
        set coordenadas
        """
        self.__lbl_coord = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def lbl_exe(self):
        """
        get exercício
        """
        return self.__lbl_exe

    @lbl_exe.setter
    def lbl_exe(self, f_val):
        """
        set exercício
        """
        self.__lbl_exe = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def lbl_hora(self):
        """
        get hora
        """
        return self.__lbl_hora

    @lbl_hora.setter
    def lbl_hora(self, f_val):
        """
        set hora
        """
        self.__lbl_hora = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def lbl_msg(self):
        """
        get message
        """
        return self.__lbl_msg

    @lbl_msg.setter
    def lbl_msg(self, f_val):
        """
        set message
        """
        self.__lbl_msg = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def parent(self):
        """
        get parent
        """
        return self.__parent

    @parent.setter
    def parent(self, f_val):
        """
        set parent
        """
        self.__parent = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def lbl_range(self):
        """ 
        get range
        """
        return self.__lbl_range

    @lbl_range.setter
    def lbl_range(self, f_val):
        """ 
        set range
        """
        self.__lbl_range = f_val

# < the end >--------------------------------------------------------------------------------------
