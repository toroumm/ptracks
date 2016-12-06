# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './dock_procedures.ui'
#
# Created: Mon Dec  5 13:39:38 2016
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

class Ui_dck_procedures(object):
    def setupUi(self, dck_procedures):
        dck_procedures.setObjectName(_fromUtf8("dck_procedures"))
        dck_procedures.resize(316, 480)
        self.dwc_procedures = QtGui.QWidget()
        self.dwc_procedures.setObjectName(_fromUtf8("dwc_procedures"))
        self.verticalLayout = QtGui.QVBoxLayout(self.dwc_procedures)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.wid_tbx_head = QtGui.QWidget(self.dwc_procedures)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wid_tbx_head.sizePolicy().hasHeightForWidth())
        self.wid_tbx_head.setSizePolicy(sizePolicy)
        self.wid_tbx_head.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);\n"
"background-color: #729fcf;"))
        self.wid_tbx_head.setObjectName(_fromUtf8("wid_tbx_head"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.wid_tbx_head)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setMargin(3)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lbl_icon = QtGui.QLabel(self.wid_tbx_head)
        self.lbl_icon.setText(_fromUtf8(""))
        self.lbl_icon.setPixmap(QtGui.QPixmap(_fromUtf8(":/images/compile16.png")))
        self.lbl_icon.setObjectName(_fromUtf8("lbl_icon"))
        self.horizontalLayout.addWidget(self.lbl_icon)
        self.lbl_title = QtGui.QLabel(self.wid_tbx_head)
        self.lbl_title.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);\n"
"font: 14pt \"Arial\";"))
        self.lbl_title.setObjectName(_fromUtf8("lbl_title"))
        self.horizontalLayout.addWidget(self.lbl_title)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addWidget(self.wid_tbx_head)
        self.tbx_procedures = QtGui.QToolBox(self.dwc_procedures)
        self.tbx_procedures.setObjectName(_fromUtf8("tbx_procedures"))
        self.pag_procs = QtGui.QWidget()
        self.pag_procs.setGeometry(QtCore.QRect(0, 0, 98, 93))
        self.pag_procs.setObjectName(_fromUtf8("pag_procs"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.pag_procs)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tree_procs = QtGui.QTreeWidget(self.pag_procs)
        self.tree_procs.setObjectName(_fromUtf8("tree_procs"))
        self.tree_procs.headerItem().setText(0, _fromUtf8("1"))
        self.verticalLayout_2.addWidget(self.tree_procs)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/execute.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tbx_procedures.addItem(self.pag_procs, icon, _fromUtf8(""))
        self.pag_navaids = QtGui.QWidget()
        self.pag_navaids.setGeometry(QtCore.QRect(0, 0, 98, 93))
        self.pag_navaids.setObjectName(_fromUtf8("pag_navaids"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.pag_navaids)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.tree_navaids = QtGui.QTreeWidget(self.pag_navaids)
        self.tree_navaids.setObjectName(_fromUtf8("tree_navaids"))
        self.tree_navaids.headerItem().setText(0, _fromUtf8("1"))
        self.verticalLayout_3.addWidget(self.tree_navaids)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/navaid.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tbx_procedures.addItem(self.pag_navaids, icon1, _fromUtf8(""))
        self.pag_runways = QtGui.QWidget()
        self.pag_runways.setEnabled(False)
        self.pag_runways.setGeometry(QtCore.QRect(0, 0, 298, 299))
        self.pag_runways.setObjectName(_fromUtf8("pag_runways"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.pag_runways)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.tree_runways = QtGui.QTreeWidget(self.pag_runways)
        self.tree_runways.setObjectName(_fromUtf8("tree_runways"))
        self.tree_runways.headerItem().setText(0, _fromUtf8("1"))
        self.verticalLayout_4.addWidget(self.tree_runways)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/linepointer.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tbx_procedures.addItem(self.pag_runways, icon2, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tbx_procedures)
        dck_procedures.setWidget(self.dwc_procedures)

        self.retranslateUi(dck_procedures)
        self.tbx_procedures.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(dck_procedures)

    def retranslateUi(self, dck_procedures):
        self.lbl_title.setText(_translate("dck_procedures", "Procedures", None))
        self.tbx_procedures.setItemText(self.tbx_procedures.indexOf(self.pag_procs), _translate("dck_procedures", "Procedures", None))
        self.tbx_procedures.setItemText(self.tbx_procedures.indexOf(self.pag_navaids), _translate("dck_procedures", "Navaids", None))
        self.tbx_procedures.setItemText(self.tbx_procedures.indexOf(self.pag_runways), _translate("dck_procedures", "Runways", None))

import resources_rc
