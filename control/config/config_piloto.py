#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
config_piloto

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
__date__ = "2016/03"

# < import >---------------------------------------------------------------------------------------

# python library
import argparse
# import logging
import os

# from ...model 
import model.data as data

# from ...control.config 
import control.config.config_manager as config

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CConfigPiloto >--------------------------------------------------------------------------

class CConfigPiloto(config.CConfigManager):
    """
    mantém as informações de configuração
    """
    # informações comuns de configuração
    __CFG_PILOTO = {"tab.aer": "tabAer",    # tabela de aeródromos
                    "tab.esp": "tabApx",    # tabela de procedimentos de aproximação
                    "tab.esp": "tabEsp",    # tabela de procedimentos de espera
                    "tab.fix": "tabFix",    # tabela de fixos
                    "tab.prf": "tabPrf",    # tabela de performances
                    "tab.sub": "tabSub",    # tabela de procedimentos de subida
                    "tab.trj": "tabTrj",    # tabela de procedimentos de trajetória
                   }  # __CFG_PILOTO

    # ---------------------------------------------------------------------------------------------
    # void (str)
    def __init__(self, fs_config):
        """
        inicia o gerente de configuração

        @param fs_config: full path do arquivo de configuração
        """
        # logger
        # M_LOG.info("__init__:>>")
                
        # init super class
        super(CConfigPiloto, self).__init__(fs_config)

        # herdados de ConfigTracks
        # self.dct_config    # config manager data dictionary

        # carrega os atributos locais no dicionário de configuração
        for l_key in self.__CFG_PILOTO.keys():
            if l_key not in self.dct_config:
                self.dct_config[l_key] = self.__CFG_PILOTO[l_key]

        # l_log.info("self.dct_config: " + str ( self.dct_config ))

        # cria um parser para os argumentos
        l_parser = argparse.ArgumentParser(description="Piloto (C) ICEA 2014-2016.")
        assert l_parser

        # argumento: canal de comunicação
        l_parser.add_argument("-c", "--canal",
                              dest="canal",
                              default=self.dct_config["glb.canal"],
                              help=u"Canal de comunicação (default: {})".format(self.dct_config["glb.canal"]))

        # faz o parser da linha de argumentos
        l_args = l_parser.parse_args()
        assert l_args

        # salva os argumentos no dicionário
        self.dct_config["glb.canal"] = int(l_args.canal)

        # load dirs section
        self.__load_dirs()

        # logger
        # M_LOG.info("__init__:<<")
                
    # ---------------------------------------------------------------------------------------------
    # void (void)
    def __load_dirs(self):
        """
        carrega as configurações de diretórios
        """
        # logger
        # M_LOG.info("__load_dirs:>>")
                
        # monta o diretório de aeródromos
        self.dct_config["dir.aer"] = data.filepath(os.path.join(self.dct_config["dir.dat"], 
                                                                self.dct_config["dir.aer"]))

        # monta o diretório de airspaces 
        self.dct_config["dir.air"] = data.filepath(os.path.join(self.dct_config["dir.dat"],
                                                                self.dct_config["dir.air"]))
                                                                                
        # monta o diretório de procedimentos
        self.dct_config["dir.prc"] = data.filepath(os.path.join(self.dct_config["dir.dat"],
                                                                self.dct_config["dir.prc"]))

        # monta o diretório de tabelas
        self.dct_config["dir.tab"] = data.filepath(os.path.join(self.dct_config["dir.dat"], 
                                                                self.dct_config["dir.tab"]))

        # logger
        # M_LOG.info("__load_dirs:<<")
                
# < the end >--------------------------------------------------------------------------------------
