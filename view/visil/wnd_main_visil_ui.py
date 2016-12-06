# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './wnd_main_visil.ui'
#
# Created: Mon Dec  5 13:39:49 2016
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_wndMainVisil(object):
    def setupUi(self, wndMainVisil):
        wndMainVisil.setObjectName(_fromUtf8("wndMainVisil"))
        wndMainVisil.resize(1169, 889)
        wndMainVisil.setLocale(QtCore.QLocale(QtCore.QLocale.Portuguese, QtCore.QLocale.Brazil))
        self.centralwidget = QtGui.QWidget(wndMainVisil)
        self.centralwidget.setMouseTracking(True)
        self.centralwidget.setStyleSheet(_fromUtf8("background-color: rgb(0, 0, 0);"))
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        wndMainVisil.setCentralWidget(self.centralwidget)
        self.status_bar = QtGui.QStatusBar(wndMainVisil)
        self.status_bar.setObjectName(_fromUtf8("status_bar"))
        wndMainVisil.setStatusBar(self.status_bar)
        self.dck_lista_voos = QtGui.QDockWidget(wndMainVisil)
        self.dck_lista_voos.setStyleSheet(_fromUtf8(""))
        self.dck_lista_voos.setFloating(False)
        self.dck_lista_voos.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable)
        self.dck_lista_voos.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dck_lista_voos.setObjectName(_fromUtf8("dck_lista_voos"))
        self.dwc_lista = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dwc_lista.sizePolicy().hasHeightForWidth())
        self.dwc_lista.setSizePolicy(sizePolicy)
        self.dwc_lista.setObjectName(_fromUtf8("dwc_lista"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.dwc_lista)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.lbl_hora = QtGui.QLabel(self.dwc_lista)
        self.lbl_hora.setStyleSheet(_fromUtf8("font: 65 italic 26pt \"Courier New\";\n"
"color:rgb(0, 170, 0);"))
        self.lbl_hora.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_hora.setObjectName(_fromUtf8("lbl_hora"))
        self.verticalLayout_2.addWidget(self.lbl_hora)
        self.wid_lv = QtGui.QWidget(self.dwc_lista)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wid_lv.sizePolicy().hasHeightForWidth())
        self.wid_lv.setSizePolicy(sizePolicy)
        self.wid_lv.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);\n"
"background-color: #729fcf;"))
        self.wid_lv.setObjectName(_fromUtf8("wid_lv"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.wid_lv)
        self.horizontalLayout_3.setSpacing(3)
        self.horizontalLayout_3.setMargin(3)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.lbl_icon = QtGui.QLabel(self.wid_lv)
        self.lbl_icon.setText(_fromUtf8(""))
        self.lbl_icon.setPixmap(QtGui.QPixmap(_fromUtf8(":/images/compile16.png")))
        self.lbl_icon.setObjectName(_fromUtf8("lbl_icon"))
        self.horizontalLayout_3.addWidget(self.lbl_icon)
        self.lbl_title = QtGui.QLabel(self.wid_lv)
        self.lbl_title.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);\n"
"font: 14pt \"Arial\";"))
        self.lbl_title.setObjectName(_fromUtf8("lbl_title"))
        self.horizontalLayout_3.addWidget(self.lbl_title)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_2.addWidget(self.wid_lv)
        self.qtv_stp = QtGui.QTableView(self.dwc_lista)
        self.qtv_stp.setObjectName(_fromUtf8("qtv_stp"))
        self.verticalLayout_2.addWidget(self.qtv_stp)
        self.dck_lista_voos.setWidget(self.dwc_lista)
        wndMainVisil.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dck_lista_voos)
        self.action_exit = QtGui.QAction(wndMainVisil)
        self.action_exit.setObjectName(_fromUtf8("action_exit"))

        self.retranslateUi(wndMainVisil)
        QtCore.QMetaObject.connectSlotsByName(wndMainVisil)

    def retranslateUi(self, wndMainVisil):
        wndMainVisil.setWindowTitle(_translate("wndMainVisil", "ViSIL 0.1 [Visualização]", None))
        self.lbl_hora.setText(_translate("wndMainVisil", "12:00:00", None))
        self.lbl_title.setText(_translate("wndMainVisil", "Lista de Vôos", None))
        self.action_exit.setText(_translate("wndMainVisil", "Sair", None))
        self.action_exit.setShortcut(_translate("wndMainVisil", "Ctrl+X", None))

import resources_rc
