# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './dlg_aproximacao.ui'
#
# Created: Tue Dec  6 11:23:22 2016
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

class Ui_CDlgAproximacao(object):
    def setupUi(self, CDlgAproximacao):
        CDlgAproximacao.setObjectName(_fromUtf8("CDlgAproximacao"))
        CDlgAproximacao.resize(259, 151)
        self.verticalLayout_2 = QtGui.QVBoxLayout(CDlgAproximacao)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gbx_aproximacao = QtGui.QGroupBox(CDlgAproximacao)
        self.gbx_aproximacao.setObjectName(_fromUtf8("gbx_aproximacao"))
        self.verticalLayout = QtGui.QVBoxLayout(self.gbx_aproximacao)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.cbx_apx = QtGui.QComboBox(self.gbx_aproximacao)
        self.cbx_apx.setObjectName(_fromUtf8("cbx_apx"))
        self.verticalLayout.addWidget(self.cbx_apx)
        self.verticalLayout_2.addWidget(self.gbx_aproximacao)
        self.lbl_comando = QtGui.QLabel(CDlgAproximacao)
        self.lbl_comando.setStyleSheet(_fromUtf8("background-color:rgb(0, 0, 0);\n"
"color:rgb(0, 190, 0)"))
        self.lbl_comando.setObjectName(_fromUtf8("lbl_comando"))
        self.verticalLayout_2.addWidget(self.lbl_comando)
        self.bbx_aproximacao = QtGui.QDialogButtonBox(CDlgAproximacao)
        self.bbx_aproximacao.setOrientation(QtCore.Qt.Horizontal)
        self.bbx_aproximacao.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.bbx_aproximacao.setObjectName(_fromUtf8("bbx_aproximacao"))
        self.verticalLayout_2.addWidget(self.bbx_aproximacao)

        self.retranslateUi(CDlgAproximacao)
        QtCore.QObject.connect(self.bbx_aproximacao, QtCore.SIGNAL(_fromUtf8("accepted()")), CDlgAproximacao.accept)
        QtCore.QObject.connect(self.bbx_aproximacao, QtCore.SIGNAL(_fromUtf8("rejected()")), CDlgAproximacao.reject)
        QtCore.QMetaObject.connectSlotsByName(CDlgAproximacao)

    def retranslateUi(self, CDlgAproximacao):
        CDlgAproximacao.setWindowTitle(_translate("CDlgAproximacao", "Aproximação", None))
        self.gbx_aproximacao.setTitle(_translate("CDlgAproximacao", "Aproximações", None))
        self.lbl_comando.setText(_translate("CDlgAproximacao", "APX 1001", None))

