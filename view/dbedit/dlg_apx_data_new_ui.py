# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './dlg_apx_data_new.ui'
#
# Created: Wed Dec  7 12:55:05 2016
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

class Ui_CDlgApxDataNEW(object):
    def setupUi(self, CDlgApxDataNEW):
        CDlgApxDataNEW.setObjectName(_fromUtf8("CDlgApxDataNEW"))
        CDlgApxDataNEW.setWindowModality(QtCore.Qt.WindowModal)
        CDlgApxDataNEW.resize(587, 665)
        CDlgApxDataNEW.setLocale(QtCore.QLocale(QtCore.QLocale.Portuguese, QtCore.QLocale.Brazil))
        CDlgApxDataNEW.setSizeGripEnabled(True)
        CDlgApxDataNEW.setModal(True)
        self.horizontalLayout_4 = QtGui.QHBoxLayout(CDlgApxDataNEW)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.splitter_2 = QtGui.QSplitter(CDlgApxDataNEW)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.widPrcTab = QtGui.QWidget(self.splitter_2)
        self.widPrcTab.setObjectName(_fromUtf8("widPrcTab"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.widPrcTab)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.qtwPrcTab = QtGui.QTableWidget(self.widPrcTab)
        self.qtwPrcTab.setObjectName(_fromUtf8("qtwPrcTab"))
        self.qtwPrcTab.setColumnCount(0)
        self.qtwPrcTab.setRowCount(0)
        self.verticalLayout_4.addWidget(self.qtwPrcTab)
        self.widPrcDat = QtGui.QWidget(self.splitter_2)
        self.widPrcDat.setObjectName(_fromUtf8("widPrcDat"))
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.widPrcDat)
        self.verticalLayout_8.setMargin(0)
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.frmPrcID = QtGui.QFrame(self.widPrcDat)
        self.frmPrcID.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frmPrcID.setFrameShadow(QtGui.QFrame.Raised)
        self.frmPrcID.setObjectName(_fromUtf8("frmPrcID"))
        self.gridLayout_2 = QtGui.QGridLayout(self.frmPrcID)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.qlePrcDesc = QtGui.QLineEdit(self.frmPrcID)
        self.qlePrcDesc.setObjectName(_fromUtf8("qlePrcDesc"))
        self.gridLayout_2.addWidget(self.qlePrcDesc, 2, 1, 1, 1)
        self.lblPrcDesc = QtGui.QLabel(self.frmPrcID)
        self.lblPrcDesc.setObjectName(_fromUtf8("lblPrcDesc"))
        self.gridLayout_2.addWidget(self.lblPrcDesc, 2, 0, 1, 1)
        self.lblPrcID = QtGui.QLabel(self.frmPrcID)
        self.lblPrcID.setObjectName(_fromUtf8("lblPrcID"))
        self.gridLayout_2.addWidget(self.lblPrcID, 1, 0, 1, 1)
        self.txtPrcID = QtGui.QLabel(self.frmPrcID)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.txtPrcID.setFont(font)
        self.txtPrcID.setObjectName(_fromUtf8("txtPrcID"))
        self.gridLayout_2.addWidget(self.txtPrcID, 1, 1, 1, 1)
        self.verticalLayout_8.addWidget(self.frmPrcID)
        self.qtwPage = QtGui.QTabWidget(self.widPrcDat)
        self.qtwPage.setObjectName(_fromUtf8("qtwPage"))
        self.pagTrj = QtGui.QWidget()
        self.pagTrj.setObjectName(_fromUtf8("pagTrj"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.pagTrj)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.gbxTrjPts = QtGui.QGroupBox(self.pagTrj)
        self.gbxTrjPts.setObjectName(_fromUtf8("gbxTrjPts"))
        self.verticalLayout = QtGui.QVBoxLayout(self.gbxTrjPts)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.qtwTabTrj = QtGui.QTableWidget(self.gbxTrjPts)
        self.qtwTabTrj.setObjectName(_fromUtf8("qtwTabTrj"))
        self.qtwTabTrj.setColumnCount(0)
        self.qtwTabTrj.setRowCount(0)
        self.verticalLayout.addWidget(self.qtwTabTrj)
        self.widget_3 = QtGui.QWidget(self.gbxTrjPts)
        self.widget_3.setObjectName(_fromUtf8("widget_3"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.widget_3)
        self.horizontalLayout_6.setMargin(0)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.btnUp = QtGui.QPushButton(self.widget_3)
        self.btnUp.setEnabled(False)
        self.btnUp.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/dbedit/go-up.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnUp.setIcon(icon)
        self.btnUp.setObjectName(_fromUtf8("btnUp"))
        self.horizontalLayout_6.addWidget(self.btnUp)
        self.btnDown = QtGui.QPushButton(self.widget_3)
        self.btnDown.setEnabled(False)
        self.btnDown.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/dbedit/go-down.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnDown.setIcon(icon1)
        self.btnDown.setObjectName(_fromUtf8("btnDown"))
        self.horizontalLayout_6.addWidget(self.btnDown)
        self.btnTrjNew = QtGui.QPushButton(self.widget_3)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/dbedit/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnTrjNew.setIcon(icon2)
        self.btnTrjNew.setObjectName(_fromUtf8("btnTrjNew"))
        self.horizontalLayout_6.addWidget(self.btnTrjNew)
        self.btnTrjDel = QtGui.QPushButton(self.widget_3)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/dbedit/delete.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnTrjDel.setIcon(icon3)
        self.btnTrjDel.setObjectName(_fromUtf8("btnTrjDel"))
        self.horizontalLayout_6.addWidget(self.btnTrjDel)
        self.verticalLayout.addWidget(self.widget_3)
        self.verticalLayout_3.addWidget(self.gbxTrjPts)
        self.gbxTrjPos = QtGui.QGroupBox(self.pagTrj)
        self.gbxTrjPos.setObjectName(_fromUtf8("gbxTrjPos"))
        self.gridLayout_6 = QtGui.QGridLayout(self.gbxTrjPos)
        self.gridLayout_6.setMargin(3)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.cbxTCrd = QtGui.QComboBox(self.gbxTrjPos)
        self.cbxTCrd.setMinimumSize(QtCore.QSize(150, 0))
        self.cbxTCrd.setObjectName(_fromUtf8("cbxTCrd"))
        self.gridLayout_6.addWidget(self.cbxTCrd, 0, 0, 1, 1)
        self.stkTCrd = QtGui.QStackedWidget(self.gbxTrjPos)
        self.stkTCrd.setObjectName(_fromUtf8("stkTCrd"))
        self.crdCart = QtGui.QWidget()
        self.crdCart.setObjectName(_fromUtf8("crdCart"))
        self.gridLayout_7 = QtGui.QGridLayout(self.crdCart)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.lblCartX = QtGui.QLabel(self.crdCart)
        self.lblCartX.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblCartX.setObjectName(_fromUtf8("lblCartX"))
        self.gridLayout_7.addWidget(self.lblCartX, 0, 0, 1, 1)
        self.lblCartY = QtGui.QLabel(self.crdCart)
        self.lblCartY.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblCartY.setObjectName(_fromUtf8("lblCartY"))
        self.gridLayout_7.addWidget(self.lblCartY, 1, 0, 1, 1)
        self.lblCartZ = QtGui.QLabel(self.crdCart)
        self.lblCartZ.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblCartZ.setObjectName(_fromUtf8("lblCartZ"))
        self.gridLayout_7.addWidget(self.lblCartZ, 2, 0, 1, 1)
        self.dsbCartX = QtGui.QDoubleSpinBox(self.crdCart)
        self.dsbCartX.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.dsbCartX.setDecimals(0)
        self.dsbCartX.setMinimum(-50000.0)
        self.dsbCartX.setMaximum(50000.0)
        self.dsbCartX.setSingleStep(100.0)
        self.dsbCartX.setObjectName(_fromUtf8("dsbCartX"))
        self.gridLayout_7.addWidget(self.dsbCartX, 0, 1, 1, 1)
        self.dsbCartY = QtGui.QDoubleSpinBox(self.crdCart)
        self.dsbCartY.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.dsbCartY.setDecimals(0)
        self.dsbCartY.setMinimum(-50000.0)
        self.dsbCartY.setMaximum(50000.0)
        self.dsbCartY.setSingleStep(100.0)
        self.dsbCartY.setObjectName(_fromUtf8("dsbCartY"))
        self.gridLayout_7.addWidget(self.dsbCartY, 1, 1, 1, 1)
        self.dsbCartZ = QtGui.QDoubleSpinBox(self.crdCart)
        self.dsbCartZ.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.dsbCartZ.setDecimals(0)
        self.dsbCartZ.setMinimum(0.0)
        self.dsbCartZ.setMaximum(80000.0)
        self.dsbCartZ.setSingleStep(100.0)
        self.dsbCartZ.setObjectName(_fromUtf8("dsbCartZ"))
        self.gridLayout_7.addWidget(self.dsbCartZ, 2, 1, 1, 1)
        self.stkTCrd.addWidget(self.crdCart)
        self.crdPFix = QtGui.QWidget()
        self.crdPFix.setObjectName(_fromUtf8("crdPFix"))
        self.gridLayout_8 = QtGui.QGridLayout(self.crdPFix)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.lblPFixDist = QtGui.QLabel(self.crdPFix)
        self.lblPFixDist.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblPFixDist.setObjectName(_fromUtf8("lblPFixDist"))
        self.gridLayout_8.addWidget(self.lblPFixDist, 0, 0, 1, 1)
        self.sbxPFixDist = QtGui.QSpinBox(self.crdPFix)
        self.sbxPFixDist.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sbxPFixDist.setMaximum(50000)
        self.sbxPFixDist.setSingleStep(100)
        self.sbxPFixDist.setObjectName(_fromUtf8("sbxPFixDist"))
        self.gridLayout_8.addWidget(self.sbxPFixDist, 0, 1, 1, 1)
        self.lblPFixAzim = QtGui.QLabel(self.crdPFix)
        self.lblPFixAzim.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblPFixAzim.setObjectName(_fromUtf8("lblPFixAzim"))
        self.gridLayout_8.addWidget(self.lblPFixAzim, 1, 0, 1, 1)
        self.sbxPFixAzim = QtGui.QSpinBox(self.crdPFix)
        self.sbxPFixAzim.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sbxPFixAzim.setMaximum(360)
        self.sbxPFixAzim.setSingleStep(3)
        self.sbxPFixAzim.setObjectName(_fromUtf8("sbxPFixAzim"))
        self.gridLayout_8.addWidget(self.sbxPFixAzim, 1, 1, 1, 1)
        self.lblPFixFixo = QtGui.QLabel(self.crdPFix)
        self.lblPFixFixo.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblPFixFixo.setObjectName(_fromUtf8("lblPFixFixo"))
        self.gridLayout_8.addWidget(self.lblPFixFixo, 2, 0, 1, 1)
        self.cbxPFixFixo = QtGui.QComboBox(self.crdPFix)
        self.cbxPFixFixo.setObjectName(_fromUtf8("cbxPFixFixo"))
        self.gridLayout_8.addWidget(self.cbxPFixFixo, 2, 1, 1, 1)
        self.stkTCrd.addWidget(self.crdPFix)
        self.crdGeo = QtGui.QWidget()
        self.crdGeo.setObjectName(_fromUtf8("crdGeo"))
        self.gridLayout_9 = QtGui.QGridLayout(self.crdGeo)
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        self.lblGeoLat = QtGui.QLabel(self.crdGeo)
        self.lblGeoLat.setMinimumSize(QtCore.QSize(140, 0))
        self.lblGeoLat.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblGeoLat.setObjectName(_fromUtf8("lblGeoLat"))
        self.gridLayout_9.addWidget(self.lblGeoLat, 0, 0, 1, 1)
        self.qleGeoLat = QtGui.QLineEdit(self.crdGeo)
        self.qleGeoLat.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.qleGeoLat.setObjectName(_fromUtf8("qleGeoLat"))
        self.gridLayout_9.addWidget(self.qleGeoLat, 0, 1, 1, 1)
        self.lblGeoLng = QtGui.QLabel(self.crdGeo)
        self.lblGeoLng.setMinimumSize(QtCore.QSize(0, 0))
        self.lblGeoLng.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblGeoLng.setObjectName(_fromUtf8("lblGeoLng"))
        self.gridLayout_9.addWidget(self.lblGeoLng, 1, 0, 1, 1)
        self.qleGeoLng = QtGui.QLineEdit(self.crdGeo)
        self.qleGeoLng.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.qleGeoLng.setObjectName(_fromUtf8("qleGeoLng"))
        self.gridLayout_9.addWidget(self.qleGeoLng, 1, 1, 1, 1)
        self.lblGeoAlt = QtGui.QLabel(self.crdGeo)
        self.lblGeoAlt.setMinimumSize(QtCore.QSize(0, 0))
        self.lblGeoAlt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblGeoAlt.setObjectName(_fromUtf8("lblGeoAlt"))
        self.gridLayout_9.addWidget(self.lblGeoAlt, 2, 0, 1, 1)
        self.qsbGeoAlt = QtGui.QSpinBox(self.crdGeo)
        self.qsbGeoAlt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.qsbGeoAlt.setMaximum(80000)
        self.qsbGeoAlt.setSingleStep(100)
        self.qsbGeoAlt.setObjectName(_fromUtf8("qsbGeoAlt"))
        self.gridLayout_9.addWidget(self.qsbGeoAlt, 2, 1, 1, 1)
        self.stkTCrd.addWidget(self.crdGeo)
        self.crdPol = QtGui.QWidget()
        self.crdPol.setObjectName(_fromUtf8("crdPol"))
        self.gridLayout_10 = QtGui.QGridLayout(self.crdPol)
        self.gridLayout_10.setObjectName(_fromUtf8("gridLayout_10"))
        self.lblPolDist = QtGui.QLabel(self.crdPol)
        self.lblPolDist.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblPolDist.setObjectName(_fromUtf8("lblPolDist"))
        self.gridLayout_10.addWidget(self.lblPolDist, 0, 0, 1, 1)
        self.lblPolAzim = QtGui.QLabel(self.crdPol)
        self.lblPolAzim.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblPolAzim.setObjectName(_fromUtf8("lblPolAzim"))
        self.gridLayout_10.addWidget(self.lblPolAzim, 1, 0, 1, 1)
        self.lblPolAlt = QtGui.QLabel(self.crdPol)
        self.lblPolAlt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblPolAlt.setObjectName(_fromUtf8("lblPolAlt"))
        self.gridLayout_10.addWidget(self.lblPolAlt, 2, 0, 1, 1)
        self.sbxPolDist = QtGui.QSpinBox(self.crdPol)
        self.sbxPolDist.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sbxPolDist.setMaximum(50000)
        self.sbxPolDist.setSingleStep(100)
        self.sbxPolDist.setObjectName(_fromUtf8("sbxPolDist"))
        self.gridLayout_10.addWidget(self.sbxPolDist, 0, 1, 1, 1)
        self.sbxPolAzim = QtGui.QSpinBox(self.crdPol)
        self.sbxPolAzim.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sbxPolAzim.setMaximum(360)
        self.sbxPolAzim.setSingleStep(3)
        self.sbxPolAzim.setObjectName(_fromUtf8("sbxPolAzim"))
        self.gridLayout_10.addWidget(self.sbxPolAzim, 1, 1, 1, 1)
        self.sbxPolAlt = QtGui.QSpinBox(self.crdPol)
        self.sbxPolAlt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sbxPolAlt.setMaximum(80000)
        self.sbxPolAlt.setSingleStep(100)
        self.sbxPolAlt.setObjectName(_fromUtf8("sbxPolAlt"))
        self.gridLayout_10.addWidget(self.sbxPolAlt, 2, 1, 1, 1)
        self.stkTCrd.addWidget(self.crdPol)
        self.gridLayout_6.addWidget(self.stkTCrd, 0, 1, 1, 1)
        self.verticalLayout_3.addWidget(self.gbxTrjPos)
        self.widget = QtGui.QWidget(self.pagTrj)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gbxTrjVel = QtGui.QGroupBox(self.widget)
        self.gbxTrjVel.setObjectName(_fromUtf8("gbxTrjVel"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.gbxTrjVel)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.sbxTrjVel = QtGui.QSpinBox(self.gbxTrjVel)
        self.sbxTrjVel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sbxTrjVel.setMaximum(1000)
        self.sbxTrjVel.setSingleStep(10)
        self.sbxTrjVel.setObjectName(_fromUtf8("sbxTrjVel"))
        self.horizontalLayout_2.addWidget(self.sbxTrjVel)
        self.horizontalLayout.addWidget(self.gbxTrjVel)
        self.gbxPrjProc = QtGui.QGroupBox(self.widget)
        self.gbxPrjProc.setObjectName(_fromUtf8("gbxPrjProc"))
        self.horizontalLayout_14 = QtGui.QHBoxLayout(self.gbxPrjProc)
        self.horizontalLayout_14.setObjectName(_fromUtf8("horizontalLayout_14"))
        self.cbxTrjPrc = QtGui.QComboBox(self.gbxPrjProc)
        self.cbxTrjPrc.setObjectName(_fromUtf8("cbxTrjPrc"))
        self.horizontalLayout_14.addWidget(self.cbxTrjPrc)
        self.horizontalLayout.addWidget(self.gbxPrjProc)
        self.verticalLayout_3.addWidget(self.widget)
        self.qtwPage.addTab(self.pagTrj, _fromUtf8(""))
        self.pagNav = QtGui.QWidget()
        self.pagNav.setObjectName(_fromUtf8("pagNav"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.pagNav)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.frmNavSet = QtGui.QFrame(self.pagNav)
        self.frmNavSet.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frmNavSet.setFrameShadow(QtGui.QFrame.Raised)
        self.frmNavSet.setObjectName(_fromUtf8("frmNavSet"))
        self.gridLayout_3 = QtGui.QGridLayout(self.frmNavSet)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.lblNavProa = QtGui.QLabel(self.frmNavSet)
        self.lblNavProa.setObjectName(_fromUtf8("lblNavProa"))
        self.gridLayout_3.addWidget(self.lblNavProa, 0, 0, 1, 1)
        self.lblNavAlt = QtGui.QLabel(self.frmNavSet)
        self.lblNavAlt.setObjectName(_fromUtf8("lblNavAlt"))
        self.gridLayout_3.addWidget(self.lblNavAlt, 2, 0, 1, 1)
        self.lblNavVel = QtGui.QLabel(self.frmNavSet)
        self.lblNavVel.setObjectName(_fromUtf8("lblNavVel"))
        self.gridLayout_3.addWidget(self.lblNavVel, 3, 0, 1, 1)
        self.sbxNavProa = QtGui.QSpinBox(self.frmNavSet)
        self.sbxNavProa.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sbxNavProa.setMinimum(-1)
        self.sbxNavProa.setMaximum(360)
        self.sbxNavProa.setSingleStep(1)
        self.sbxNavProa.setObjectName(_fromUtf8("sbxNavProa"))
        self.gridLayout_3.addWidget(self.sbxNavProa, 0, 1, 1, 1)
        self.sbxNavVel = QtGui.QSpinBox(self.frmNavSet)
        self.sbxNavVel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sbxNavVel.setMinimum(-1)
        self.sbxNavVel.setMaximum(1000)
        self.sbxNavVel.setSingleStep(50)
        self.sbxNavVel.setObjectName(_fromUtf8("sbxNavVel"))
        self.gridLayout_3.addWidget(self.sbxNavVel, 3, 1, 1, 1)
        self.sbxNavAlt = QtGui.QSpinBox(self.frmNavSet)
        self.sbxNavAlt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sbxNavAlt.setMinimum(-1)
        self.sbxNavAlt.setMaximum(80000)
        self.sbxNavAlt.setSingleStep(500)
        self.sbxNavAlt.setObjectName(_fromUtf8("sbxNavAlt"))
        self.gridLayout_3.addWidget(self.sbxNavAlt, 2, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.frmNavSet)
        self.frmNavPrc = QtGui.QFrame(self.pagNav)
        self.frmNavPrc.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frmNavPrc.setFrameShadow(QtGui.QFrame.Raised)
        self.frmNavPrc.setObjectName(_fromUtf8("frmNavPrc"))
        self.verticalLayout_12 = QtGui.QVBoxLayout(self.frmNavPrc)
        self.verticalLayout_12.setObjectName(_fromUtf8("verticalLayout_12"))
        self.gbxNavPrc = QtGui.QGroupBox(self.frmNavPrc)
        self.gbxNavPrc.setObjectName(_fromUtf8("gbxNavPrc"))
        self.horizontalLayout_11 = QtGui.QHBoxLayout(self.gbxNavPrc)
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.cbxNavPrc = QtGui.QComboBox(self.gbxNavPrc)
        self.cbxNavPrc.setObjectName(_fromUtf8("cbxNavPrc"))
        self.horizontalLayout_11.addWidget(self.cbxNavPrc)
        self.verticalLayout_12.addWidget(self.gbxNavPrc)
        self.verticalLayout_2.addWidget(self.frmNavPrc)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.qtwPage.addTab(self.pagNav, _fromUtf8(""))
        self.pagEsp = QtGui.QWidget()
        self.pagEsp.setObjectName(_fromUtf8("pagEsp"))
        self.verticalLayout_9 = QtGui.QVBoxLayout(self.pagEsp)
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.frmEspSet = QtGui.QFrame(self.pagEsp)
        self.frmEspSet.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frmEspSet.setFrameShadow(QtGui.QFrame.Raised)
        self.frmEspSet.setObjectName(_fromUtf8("frmEspSet"))
        self.gridLayout_4 = QtGui.QGridLayout(self.frmEspSet)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.lblEspFixo = QtGui.QLabel(self.frmEspSet)
        self.lblEspFixo.setObjectName(_fromUtf8("lblEspFixo"))
        self.gridLayout_4.addWidget(self.lblEspFixo, 0, 0, 1, 1)
        self.lblEspSent = QtGui.QLabel(self.frmEspSet)
        self.lblEspSent.setObjectName(_fromUtf8("lblEspSent"))
        self.gridLayout_4.addWidget(self.lblEspSent, 2, 0, 1, 1)
        self.lblEspRumo = QtGui.QLabel(self.frmEspSet)
        self.lblEspRumo.setObjectName(_fromUtf8("lblEspRumo"))
        self.gridLayout_4.addWidget(self.lblEspRumo, 3, 0, 1, 1)
        self.sbxEspRumo = QtGui.QSpinBox(self.frmEspSet)
        self.sbxEspRumo.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sbxEspRumo.setMaximum(360)
        self.sbxEspRumo.setSingleStep(5)
        self.sbxEspRumo.setObjectName(_fromUtf8("sbxEspRumo"))
        self.gridLayout_4.addWidget(self.sbxEspRumo, 3, 1, 1, 1)
        self.cbxEspFixo = QtGui.QComboBox(self.frmEspSet)
        self.cbxEspFixo.setObjectName(_fromUtf8("cbxEspFixo"))
        self.gridLayout_4.addWidget(self.cbxEspFixo, 0, 1, 1, 1)
        self.cbxEspSent = QtGui.QComboBox(self.frmEspSet)
        self.cbxEspSent.setObjectName(_fromUtf8("cbxEspSent"))
        self.gridLayout_4.addWidget(self.cbxEspSent, 2, 1, 1, 1)
        self.verticalLayout_9.addWidget(self.frmEspSet)
        self.frmEspPrc = QtGui.QFrame(self.pagEsp)
        self.frmEspPrc.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frmEspPrc.setFrameShadow(QtGui.QFrame.Raised)
        self.frmEspPrc.setObjectName(_fromUtf8("frmEspPrc"))
        self.verticalLayout_13 = QtGui.QVBoxLayout(self.frmEspPrc)
        self.verticalLayout_13.setObjectName(_fromUtf8("verticalLayout_13"))
        self.gbxEspProc = QtGui.QGroupBox(self.frmEspPrc)
        self.gbxEspProc.setObjectName(_fromUtf8("gbxEspProc"))
        self.horizontalLayout_13 = QtGui.QHBoxLayout(self.gbxEspProc)
        self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
        self.cbxEspProc = QtGui.QComboBox(self.gbxEspProc)
        self.cbxEspProc.setObjectName(_fromUtf8("cbxEspProc"))
        self.horizontalLayout_13.addWidget(self.cbxEspProc)
        self.verticalLayout_13.addWidget(self.gbxEspProc)
        self.verticalLayout_9.addWidget(self.frmEspPrc)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem2)
        self.qtwPage.addTab(self.pagEsp, _fromUtf8(""))
        self.verticalLayout_8.addWidget(self.qtwPage)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem3)
        self.frmPrcBBX = QtGui.QFrame(self.widPrcDat)
        self.frmPrcBBX.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frmPrcBBX.setFrameShadow(QtGui.QFrame.Raised)
        self.frmPrcBBX.setObjectName(_fromUtf8("frmPrcBBX"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.frmPrcBBX)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.btnNew = QtGui.QPushButton(self.frmPrcBBX)
        self.btnNew.setIcon(icon2)
        self.btnNew.setObjectName(_fromUtf8("btnNew"))
        self.horizontalLayout_3.addWidget(self.btnNew)
        self.btnDel = QtGui.QPushButton(self.frmPrcBBX)
        self.btnDel.setIcon(icon3)
        self.btnDel.setObjectName(_fromUtf8("btnDel"))
        self.horizontalLayout_3.addWidget(self.btnDel)
        self.bbxPrcTab = QtGui.QDialogButtonBox(self.frmPrcBBX)
        self.bbxPrcTab.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.bbxPrcTab.setObjectName(_fromUtf8("bbxPrcTab"))
        self.horizontalLayout_3.addWidget(self.bbxPrcTab)
        self.verticalLayout_8.addWidget(self.frmPrcBBX)
        self.horizontalLayout_4.addWidget(self.splitter_2)
        self.lblCartX.setBuddy(self.dsbCartX)
        self.lblCartY.setBuddy(self.dsbCartY)
        self.lblCartZ.setBuddy(self.dsbCartZ)
        self.lblNavProa.setBuddy(self.sbxNavProa)
        self.lblNavAlt.setBuddy(self.sbxNavAlt)
        self.lblNavVel.setBuddy(self.sbxNavVel)
        self.lblEspFixo.setBuddy(self.cbxEspFixo)
        self.lblEspSent.setBuddy(self.cbxEspSent)
        self.lblEspRumo.setBuddy(self.sbxEspRumo)

        self.retranslateUi(CDlgApxDataNEW)
        self.qtwPage.setCurrentIndex(2)
        self.stkTCrd.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(CDlgApxDataNEW)
        CDlgApxDataNEW.setTabOrder(self.qtwPrcTab, self.qtwPage)
        CDlgApxDataNEW.setTabOrder(self.qtwPage, self.qtwTabTrj)
        CDlgApxDataNEW.setTabOrder(self.qtwTabTrj, self.btnUp)
        CDlgApxDataNEW.setTabOrder(self.btnUp, self.btnDown)
        CDlgApxDataNEW.setTabOrder(self.btnDown, self.btnTrjNew)
        CDlgApxDataNEW.setTabOrder(self.btnTrjNew, self.btnTrjDel)
        CDlgApxDataNEW.setTabOrder(self.btnTrjDel, self.cbxTCrd)
        CDlgApxDataNEW.setTabOrder(self.cbxTCrd, self.dsbCartX)
        CDlgApxDataNEW.setTabOrder(self.dsbCartX, self.dsbCartY)
        CDlgApxDataNEW.setTabOrder(self.dsbCartY, self.dsbCartZ)
        CDlgApxDataNEW.setTabOrder(self.dsbCartZ, self.sbxTrjVel)
        CDlgApxDataNEW.setTabOrder(self.sbxTrjVel, self.cbxTrjPrc)
        CDlgApxDataNEW.setTabOrder(self.cbxTrjPrc, self.sbxNavProa)
        CDlgApxDataNEW.setTabOrder(self.sbxNavProa, self.sbxNavAlt)
        CDlgApxDataNEW.setTabOrder(self.sbxNavAlt, self.sbxNavVel)
        CDlgApxDataNEW.setTabOrder(self.sbxNavVel, self.cbxNavPrc)
        CDlgApxDataNEW.setTabOrder(self.cbxNavPrc, self.cbxEspFixo)
        CDlgApxDataNEW.setTabOrder(self.cbxEspFixo, self.cbxEspSent)
        CDlgApxDataNEW.setTabOrder(self.cbxEspSent, self.sbxEspRumo)
        CDlgApxDataNEW.setTabOrder(self.sbxEspRumo, self.cbxEspProc)
        CDlgApxDataNEW.setTabOrder(self.cbxEspProc, self.sbxPolAlt)
        CDlgApxDataNEW.setTabOrder(self.sbxPolAlt, self.sbxPFixDist)
        CDlgApxDataNEW.setTabOrder(self.sbxPFixDist, self.cbxPFixFixo)
        CDlgApxDataNEW.setTabOrder(self.cbxPFixFixo, self.sbxPFixAzim)
        CDlgApxDataNEW.setTabOrder(self.sbxPFixAzim, self.qleGeoLat)
        CDlgApxDataNEW.setTabOrder(self.qleGeoLat, self.sbxPolDist)
        CDlgApxDataNEW.setTabOrder(self.sbxPolDist, self.qleGeoLng)
        CDlgApxDataNEW.setTabOrder(self.qleGeoLng, self.qsbGeoAlt)
        CDlgApxDataNEW.setTabOrder(self.qsbGeoAlt, self.sbxPolAzim)

    def retranslateUi(self, CDlgApxDataNEW):
        CDlgApxDataNEW.setWindowTitle(_translate("CDlgApxDataNEW", "Edição de Aproximações", None))
        self.lblPrcDesc.setText(_translate("CDlgApxDataNEW", "Descrição:", None))
        self.lblPrcID.setText(_translate("CDlgApxDataNEW", "Indicativo:", None))
        self.txtPrcID.setText(_translate("CDlgApxDataNEW", "PRC001", None))
        self.gbxTrjPts.setTitle(_translate("CDlgApxDataNEW", "Pontos da Trajetória", None))
        self.btnTrjNew.setText(_translate("CDlgApxDataNEW", "Novo", None))
        self.btnTrjDel.setText(_translate("CDlgApxDataNEW", "Remove", None))
        self.gbxTrjPos.setTitle(_translate("CDlgApxDataNEW", "Posicão", None))
        self.lblCartX.setText(_translate("CDlgApxDataNEW", "X:", None))
        self.lblCartY.setText(_translate("CDlgApxDataNEW", "Y:", None))
        self.lblCartZ.setText(_translate("CDlgApxDataNEW", "Z:", None))
        self.dsbCartX.setSuffix(_translate("CDlgApxDataNEW", " m", None))
        self.dsbCartY.setSuffix(_translate("CDlgApxDataNEW", " m", None))
        self.dsbCartZ.setSuffix(_translate("CDlgApxDataNEW", " ft", None))
        self.lblPFixDist.setText(_translate("CDlgApxDataNEW", "Distância:", None))
        self.sbxPFixDist.setSuffix(_translate("CDlgApxDataNEW", " m", None))
        self.lblPFixAzim.setText(_translate("CDlgApxDataNEW", "Azimute:", None))
        self.sbxPFixAzim.setSuffix(_translate("CDlgApxDataNEW", " °", None))
        self.lblPFixFixo.setText(_translate("CDlgApxDataNEW", "Fixo:", None))
        self.lblGeoLat.setText(_translate("CDlgApxDataNEW", "Latitude:", None))
        self.lblGeoLng.setText(_translate("CDlgApxDataNEW", "Longitude:", None))
        self.lblGeoAlt.setText(_translate("CDlgApxDataNEW", "Altitude:", None))
        self.qsbGeoAlt.setSuffix(_translate("CDlgApxDataNEW", " ft", None))
        self.lblPolDist.setText(_translate("CDlgApxDataNEW", "Distância:", None))
        self.lblPolAzim.setText(_translate("CDlgApxDataNEW", "Azimute:", None))
        self.lblPolAlt.setText(_translate("CDlgApxDataNEW", "Altitude:", None))
        self.sbxPolDist.setSuffix(_translate("CDlgApxDataNEW", " m", None))
        self.sbxPolAzim.setSuffix(_translate("CDlgApxDataNEW", " °", None))
        self.sbxPolAlt.setSuffix(_translate("CDlgApxDataNEW", " ft", None))
        self.gbxTrjVel.setTitle(_translate("CDlgApxDataNEW", "Velocidade", None))
        self.sbxTrjVel.setSuffix(_translate("CDlgApxDataNEW", " kt", None))
        self.gbxPrjProc.setTitle(_translate("CDlgApxDataNEW", "Procedimento", None))
        self.qtwPage.setTabText(self.qtwPage.indexOf(self.pagTrj), _translate("CDlgApxDataNEW", "Trajetórias", None))
        self.lblNavProa.setText(_translate("CDlgApxDataNEW", "Proa:", None))
        self.lblNavAlt.setText(_translate("CDlgApxDataNEW", "Altitude:", None))
        self.lblNavVel.setText(_translate("CDlgApxDataNEW", "Velocidade:", None))
        self.sbxNavProa.setSpecialValueText(_translate("CDlgApxDataNEW", "Manter Atual", None))
        self.sbxNavProa.setSuffix(_translate("CDlgApxDataNEW", " °", None))
        self.sbxNavVel.setSpecialValueText(_translate("CDlgApxDataNEW", "Manter Atual", None))
        self.sbxNavVel.setSuffix(_translate("CDlgApxDataNEW", " kt", None))
        self.sbxNavAlt.setSpecialValueText(_translate("CDlgApxDataNEW", "Manter Atual", None))
        self.sbxNavAlt.setSuffix(_translate("CDlgApxDataNEW", " ft", None))
        self.gbxNavPrc.setTitle(_translate("CDlgApxDataNEW", "Procedimento", None))
        self.qtwPage.setTabText(self.qtwPage.indexOf(self.pagNav), _translate("CDlgApxDataNEW", "Navegacão", None))
        self.lblEspFixo.setText(_translate("CDlgApxDataNEW", "Fixo:", None))
        self.lblEspSent.setText(_translate("CDlgApxDataNEW", "Sentido:", None))
        self.lblEspRumo.setText(_translate("CDlgApxDataNEW", "Rumo:", None))
        self.sbxEspRumo.setSuffix(_translate("CDlgApxDataNEW", " °", None))
        self.gbxEspProc.setTitle(_translate("CDlgApxDataNEW", "Procedimento", None))
        self.qtwPage.setTabText(self.qtwPage.indexOf(self.pagEsp), _translate("CDlgApxDataNEW", "Esperas", None))
        self.btnNew.setText(_translate("CDlgApxDataNEW", "Novo", None))
        self.btnDel.setText(_translate("CDlgApxDataNEW", "Remove", None))

import resources_rc
