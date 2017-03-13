#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
dlg_wizard

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

# model
import ptracks.model.common.glb_data as gdata

# wizard
import ptracks.view.wizard.wizard_model as model
import ptracks.view.wizard.wpg_config_canal as wcanal
import ptracks.view.wizard.wpg_config_exe as wexe
import ptracks.view.wizard.wpg_termina as wterm

# < class CDlgWizard >-----------------------------------------------------------------------------

class CDlgWizard(model.CWizardModel):
    """
    initializes the wizard
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control, f_parent=None):
        """
        initializes the wizard
        """
        # inicia a super classe
        super(CDlgWizard, self).__init__(f_parent)

        # obtém o dicionário de configuração
        self.__dct_config = f_control.config.dct_config
        assert self.__dct_config

        # página de configuração do canal de comunicação
        self.__pag_canal = wcanal.CWPagConfigCanal(f_control, self)
        assert self.__pag_canal

        # página de configuração de exercício
        self.__pag_config_exe = wexe.CWPagConfigExe(f_control, self)
        assert self.__pag_config_exe

        # página de confirmação
        self.__pag_termina = wterm.CWPagTermina(f_control, self)
        assert self.__pag_termina

        # primeira página (entry-point)
        self.setFirstPage(self.__pag_config_exe)

        # geometria da janela
        self.setWindowTitle(self.tr(u"Gerador de Pistas [Configurador de Simulação]"))
        self.resize(660, 520)

    # ---------------------------------------------------------------------------------------------
    def accept(self):
        """
        initializes the wizard
        """
        # finaliza o sistema
        self.close()

        # obtém o exercício
        l_exe = self.__dct_config["glb.exe"]
        assert l_exe

        # obtém o canal
        li_canal = int(self.__dct_config["glb.canal"])
        assert 2 < li_canal < 201

        # parâmetros do simulador
        l_args = ["-e", "%s" % (l_exe.s_exe_id), "-c", "%d" % (li_canal)]

        # executa o simulador
        # os.execlp("python", "python", "-OO", "newton.py", *l_args)
        os.execlp("sh", "sh", "newton", *l_args)

    # =============================================================================================
    # data
    # =============================================================================================
            
    # ---------------------------------------------------------------------------------------------
    @property
    def pag_canal(self):
        """
        get page canal
        """
        return self.__pag_canal
                                                        
    # ---------------------------------------------------------------------------------------------
    @property
    def pag_config_exe(self):
        """
        get page config exe
        """
        return self.__pag_config_exe
                                                        
    # ---------------------------------------------------------------------------------------------
    @property
    def pag_termina(self):
        """
        get page termina
        """
        return self.__pag_termina
                                                        
# < the end >--------------------------------------------------------------------------------------
