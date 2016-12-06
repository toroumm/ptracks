#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
config_newton

módulo que mantém as informações de configuração do gerador de pistas

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

revision 0.3  2015/nov  mlabru
pep8 style conventions

revision 0.2  2014/nov  mlabru
inclusão do dicionário de configuração

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.3$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
import argparse
import os
import socket

# model 
import model.common.data as data

# control
import control.config.config_manager as config

# < class CConfigNewton >--------------------------------------------------------------------------

class CConfigNewton(config.CConfigManager):
    """
    mantém as informações de configuração
    """
    # informações comuns de configuração
    __CFG_NEWTON = {"glb.canal": 3,     # canal
                    "glb.exe": None,    # exercício

                    "srv.addr": "localhost",    # server address
                    "srv.port": 61000,          # server port (61244)

                    "tab.aer": "tabAer",    # tabela de aeródromos
                    "tab.apx": "tabApx",    # tabela de procedimentos de aproximação
                    "tab.esp": "tabEsp",    # tabela de procedimentos de espera
                    "tab.fix": "tabFix",    # tabela de fixos
                    "tab.prf": "tabPrf",    # tabela de performances
                    "tab.sub": "tabSub",    # tabela de procedimentos de subida
                    "tab.trj": "tabTrj",    # tabela de procedimentos de trajetória
                   }  # __CFG_NEWTON

    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_config):
        """
        inicia o gerente de configuração

        @param fs_config: full path do arquivo de configuração
        """
        # init super class
        super(CConfigNewton, self).__init__(fs_config)

        # herdados de CConfigManager
        # self.dct_config    # config manager data dictionary

        # carrega os atributos locais no dicionário de configuração
        for l_key in self.__CFG_NEWTON.keys():
            if l_key not in self.dct_config:
                self.dct_config[l_key] = self.__CFG_NEWTON[l_key]

        # obtém o endereço de IP do servidor e salva no dicionário
        self.dct_config["srv.addr"] = str(socket.gethostbyname(socket.getfqdn()))

        # cria um parser para os argumentos
        l_parser = argparse.ArgumentParser(description="newton (C) 2014-2016.")
        assert l_parser

        # argumento: canal de comunicação
        l_parser.add_argument("-c", "--canal",
                              dest="canal",
                              default=self.dct_config["glb.canal"],
                              help=u"Canal de comunicação (default: {})".format(int(self.dct_config["glb.canal"])))

        # argumento: exercício
        l_parser.add_argument("-e", "--exe",
                              dest="exe",
                              default=self.dct_config["glb.exe"],
                              help=u"Exercício (default: {})".format(self.dct_config["glb.exe"]))

        # faz o parser da linha de argumentos
        l_args = l_parser.parse_args()
        assert l_args

        # salva os argumentos no dicionário
        self.dct_config["glb.canal"] = abs(int(l_args.canal))
        self.dct_config["glb.exe"] = str(l_args.exe)

        # load dirs section
        self.__load_dirs()

    # ---------------------------------------------------------------------------------------------
    def __load_dirs(self):
        """
        carrega as configurações de diretórios
        """
        # monta o diretório de airspaces
        self.dct_config["dir.air"] = data.filepath(os.path.join(self.dct_config["dir.dat"],
                                                                self.dct_config["dir.air"]))

        # monta o diretório de exercícios
        self.dct_config["dir.exe"] = data.filepath(os.path.join(self.dct_config["dir.dat"],
                                                                self.dct_config["dir.exe"]))

        # monta o diretório de procedimentos
        self.dct_config["dir.prc"] = data.filepath(os.path.join(self.dct_config["dir.dat"],
                                                                self.dct_config["dir.prc"]))

        # monta o diretório de tabelas
        self.dct_config["dir.tab"] = data.filepath(os.path.join(self.dct_config["dir.dat"],
                                                                self.dct_config["dir.tab"]))

        # monta o diretório de tráfegos
        self.dct_config["dir.trf"] = data.filepath(os.path.join(self.dct_config["dir.dat"],
                                                                self.dct_config["dir.trf"]))

# < the end >--------------------------------------------------------------------------------------
