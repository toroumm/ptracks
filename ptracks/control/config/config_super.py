#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
config_super

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

# < import >---------------------------------------------------------------------------------------

# python library
import os

# model 
import ptracks.model.common.data as data

# control
import ptracks.control.config.config_manager as config

# < class CConfigSuper >---------------------------------------------------------------------------

class CConfigSuper(config.CConfigManager):
    """
    mantém as informações de configuração
    """
    # informações comuns de configuração
    __CFG_SUPER = {}  # __CFG_SUPER

    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_config):
        """
        inicia o gerente de configuração

        @param fs_config: full path do arquivo de configuração
        """
        # init super class
        super(CConfigSuper, self).__init__(fs_config)

        # herdados de CConfigManager
        # self.dct_config    # config manager data dictionary

        # carrega os atributos locais no dicionário de configuração
        for l_key in self.__CFG_SUPER.keys():
            if l_key not in self.dct_config:
                self.dct_config[l_key] = self.__CFG_SUPER[l_key]

        # load dirs section
        self.load_dirs()

# < the end >--------------------------------------------------------------------------------------
