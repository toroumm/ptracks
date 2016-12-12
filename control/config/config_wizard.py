#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
config_wizard

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
__date__ = "2015/11"

# < import >---------------------------------------------------------------------------------------

# python library
import os

# model 
import model.common.data as data

# control
import control.config.config_manager as config

# < class CConfigWizard >---------------------------------------------------------------------------

class CConfigWizard(config.CConfigManager):
    """
    mantém as informações de configuração do wizard
    """
    # informações comuns de configuração
    __CFG_WIZARD = {}  # __CFG_WIZARD

    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_config):
        """
        inicia o gerente de configuração do wizard

        @param fs_config: full path do arquivo de configuração
        """
        # init super class
        super(CConfigWizard, self).__init__(fs_config)

        # herdados de CConfigManager
        # self.dct_config    # config manager data dictionary

        # carrega os atributos locais no dicionário de configuração
        for l_key in self.__CFG_WIZARD.keys():
            if l_key not in self.dct_config:
                self.dct_config[l_key] = self.__CFG_WIZARD[l_key]

        # load dirs section
        self.load_dirs()

# < the end >--------------------------------------------------------------------------------------
