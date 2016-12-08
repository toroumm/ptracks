#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
dlg_aer_edit_new

mantém as informações sobre a dialog de edição de aeródromos

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

# PyQt library
from PyQt4 import QtCore
from PyQt4 import QtGui

# model
import model.items.aer_new as model

# view
import view.dbedit.dlg_aer_edit_new_ui as dlg

# < class CDlgAerEditNEW >-------------------------------------------------------------------------

class CDlgAerEditNEW(QtGui.QDialog, dlg.Ui_CDlgAerEditNEW):
    """
    mantém as informações sobre a dialog de edição de aeródromos
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control, f_aer=None, f_parent=None):
        """
        @param f_control: control manager
        @param f_aer: aeródromo
        @param f_parent: janela pai
        """
        # verifica parâmetros de entrada
        assert f_control

        # init super class
        super(CDlgAerEditNEW, self).__init__(f_parent)

        # control manager
        #self._control = f_control

        # obtém o gerente de configuração
        #self._config = f_control.oConfig
        #assert self._config

        # obtém o dicionário de configuração
        #self._dct_config = self._config.dct_config
        #assert self._dct_config

        # salva a parent window
        self._parent = f_parent

        # salva os parâmetros
        self._aer = f_aer

        # pathnames
        self._s_pn = None

        # monta a dialog
        self.setupUi(self)

        # configura título da dialog
        self.setWindowTitle(u"Edição de Aeródromos")

        # atualiza na tela os dados do aeródromo
        self.update_data()

        # configurações de conexões slot/signal
        self.config_connects()

        # configurações de títulos e mensagens da janela de edição
        self.config_texts()

        # restaura as configurações da janela de edição
        self.restore_settings()

        # configura botões
        self.bbxEditAer.button(QtGui.QDialogButtonBox.Cancel).setText("&Cancela")
        self.bbxEditAer.button(QtGui.QDialogButtonBox.Ok).setFocus()

        # força uma passgem pela edição de chave
        self.on_qleInd_textEdited(QtCore.QString())

    # ---------------------------------------------------------------------------------------------
    def accept(self):
        """
        DOCUMENT ME!
        """
        # aeródromo existe ?
        if self._aer is not None:
            # salva edição do aeródromo
            self.accept_edit()

        # senão, aeródromo não existe
        else:
            # salva novo aeródromo
            self.accept_new()

        # call super
        QtGui.QDialog.accept(self)

    # ---------------------------------------------------------------------------------------------
    def accept_edit(self):
        """
        DOCUMENT ME!
        """
        # dicionário de modificações
        ldct_alt = {}

        # identificação

        # indicativo
        ls_ind = str(self.qleInd.text()).strip().upper()

        if self._aer.s_ind != ls_ind:
            ldct_alt["Ind"] = ls_ind

        # descrição
        ls_desc = str(self.qleDsc.text()).strip()

        if self._aer.s_desc != ls_desc:
            ldct_alt["Dsc"] = ls_desc

        # área

        # comprimento
        lf_comp = self.qsbComp.value()

        if self._aer.f_comp != lf_comp:
            ldct_alt["Comp"] = lf_comp

        # largura
        l_fLarg = self.qsbLarg.value()

        if self._aer.f_larg != l_fLarg:
            ldct_alt["Larg"] = l_fLarg

        # altitude
        l_uiAlt = self.qsbAlt.value()

        if self._aer.ui_alt != l_uiAlt:
            ldct_alt["Alt"] = l_uiAlt

        # centro
        l_fCentroX = self.qsbCentroX.value()
        l_fCentroY = self.qsbCentroY.value()

        if (self._aer.centro.get_pto()[0] != l_fCentroX) or (self._aer.centro.get_pto()[1] != l_fCentroY):
            ldct_alt["Centro"] = (l_fCentroX, l_fCentroY)

        # diferença de declinação magnética
        l_iDifDecl = self.qsbDifDecl.value()

        if self._aer.i_dif_decl != l_iDifDecl:
            ldct_alt["DifDecl"] = l_iDifDecl

        # atualiza o aeródromo
        self._aer.updateAer(ldct_alt)

    # ---------------------------------------------------------------------------------------------
    def accept_new(self):
        """
        DOCUMENT ME!
        """
        # cria um novo aeródromo
        self._aer = model.AerNEW()
        assert self._aer

        # identificação

        # indicativo
        ls_ind = str(self.qleInd.text()).strip().upper()

        # descrição
        ls_desc = str(self.qleDsc.text()).strip()

        # geografia

        # comprimento
        lf_comp = self.qsbComp.value()

        # largura
        lf_larg = self.qsbLarg.value()

        # altitude
        lui_alt = self.qsbAlt.value()

        # centro
        lf_centro_X = self.qsbCentroX.value()
        lf_centro_Y = self.qsbCentroY.value()

        # diferença de declinação magnética
        li_dif_decl = self.qsbDifDecl.value()

        # atualiza o pathname
        if self._s_pn is not None:
            self._aer.s_pn = self._s_pn

        # atualiza o aeródromo
        self._aer.updateAer0211([None, ls_ind, ls_desc,
                                 lf_comp, lf_larg, lui_alt,
                                 (lf_centro_X, lf_centro_Y), li_dif_decl])  # , self._oFigTab)

    # ---------------------------------------------------------------------------------------------
    def config_connects(self):
        """
        configura as conexões slot/signal
        """
        # conecta botão Ok da edição de aeródromo
        self.connect(self.bbxEditAer, QtCore.SIGNAL("accepted()"), self.accept)

        # conecta botão Cancela da edição de aeródromo
        self.connect(self.bbxEditAer, QtCore.SIGNAL("rejected()"), self.reject)

        # conect fim de edição da chave
        self.connect(self.qleInd, QtCore.SIGNAL("editingFinished()"), self.editingFinished)

    # ---------------------------------------------------------------------------------------------
    def config_texts(self):
        """
        """
        # configura títulos e mensagens
        self._txtSettings = "CDlgAerEditNEW"

    # ---------------------------------------------------------------------------------------------
    def editingFinished(self):
        """
        DOCUMENT ME!
        """
        # obtém a chave digitada
#       ls_ind = str(self.qleInd.text()).strip().upper()

        # checa se digitou uma chave válida para o aeródromo
#       l_bEnable =(ls_ind != "")

        # habilita / desabilita os botões
#       self.bbxEditAer.button(QtGui.QDialogButtonBox.Ok).setEnabled(l_bEnable)

        # remoção de aeronave
#       self.btnDel.setEnabled(l_bEnable)

        # edição de aeronave
#       self.btnEdit.setEnabled(l_bEnable)

        # inserção de aeronave
#       self.btnNew.setEnabled(l_bEnable)

        # checa se digitou uma chave válida para o aeródromo
#       if l_bEnable:
            # pathname do arquivo de aeródromo
#           self._s_pn = os.path.join(self._cfgs [ "dir.exe" ], ls_ind + ".xrc")

            # pathname da tabela de aeronaves do aeródromo
#           self._sTabPath = os.path.join(self._cfgs [ "dir.anv" ], ls_ind + ".anv")

        # return
        return

    # ---------------------------------------------------------------------------------------------
    def get_data(self):
        """
        DOCUMENT ME!
        """
        return self._aer

    # ---------------------------------------------------------------------------------------------
    def reject(self):
        """
        DOCUMENT ME!
        """
        self._aer = None

        # faz o "reject"
        QtGui.QDialog.reject(self)

    # ---------------------------------------------------------------------------------------------
    def restore_settings(self):
        """
        restaura as configurações salvas para esta janela
        """
        # obtém os settings
        l_set = QtCore.QSettings("sophosoft", "dbedit")
        assert l_set

        # restaura geometria da janela
        self.restoreGeometry(l_set.value("%s/Geometry" % (self._txtSettings)).toByteArray())

        # return
        return True

    # ---------------------------------------------------------------------------------------------
    def update_data(self):
        """
        atualiza na tela os a área de dados do aeródromo selecionado
        """
        # aeródromo existe ?
        if self._aer is not None:
            # identificação
            self.qleInd.setText(self._aer.s_ind)
            self.qleDsc.setText(self._aer.s_desc)

            # área

            # comprimento
            self.qsbComp.setValue(self._aer.f_comp)

            # largura
            self.qsbLarg.setValue(self._aer.f_larg)

            # diferença de declinação magnética
            self.qsbDifDecl.setValue(self._aer.i_dif_decl)

            # centro
            li_x, li_y = self._aer.centro.get_pto()

            self.qsbCentroX.setValue(li_x)
            self.qsbCentroY.setValue(li_y)

            # altitude
            self.qsbAlt.setValue(self._aer.ui_alt)

        # senão, é um novo aeródromo
        else:
            # posiciona cursor no início do formulário
            self.qleInd.setFocus()

    # =============================================================================================
    # edição de campos
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @QtCore.pyqtSignature("QString")
    def on_qleInd_textEdited(self, f_qszVal):
        """
        DOCUMENT ME!
        """
        # habilita / desabilita os botões
        self.bbxEditAer.button(QtGui.QDialogButtonBox.Ok).setEnabled(not self.qleInd.text().isEmpty())

# < the end >--------------------------------------------------------------------------------------
