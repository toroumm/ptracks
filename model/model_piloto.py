#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
model_piloto.

model manager da pilotagem.

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

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import sys

# model
import model.model_manager as model
import model.emula.emula_piloto as emula

# control
import control.events.events_basic as events

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CModelPiloto >---------------------------------------------------------------------------

class CModelPiloto(model.CModelManager):
    """
    piloto model object.
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_control):
        """
        @param f_control: control manager.
        """
        # logger
        # M_LOG.info("__init__:>>")
                
        # verifica parâmetros de entrada
        assert f_control

        # init super class
        super(CModelPiloto, self).__init__(f_control)

        # herdados de CModelManager
        # self.control       # control manager
        # self.event         # event manager
        # self.config        # config manager
        # self.dct_config    # dicionário de configuração

        # variáveis de instância
        self.__airspace = None
        # self.__landscape = None

        # dicionário de performances
        self.__dct_prf = {}
                
        # carrega as tabelas do sistema
        # self.load_tables("BR01")

        # create emula model
        self.__emula_model = emula.CEmulaPiloto(self, f_control)
        assert self.__emula_model
                        
        # logger
        # M_LOG.info("__init__:<<")
                
    # ---------------------------------------------------------------------------------------------

    def load_tables(self, ls_cena):
        """
        abre/cria as tabelas do sistema.

        @param ls_cena: cenário.

        @return flag e mensagem.
        """
        # inicia flag
        lv_ok = True
        ls_msg = "Ok"

        # carrega o landscape
        # lv_ok, ls_msg = self.load_land(ls_cena)

        # tudo Ok ?
        # if lv_ok:

            # carrega o airspace
            # lv_ok, ls_msg = self.load_air(ls_cena)

        # houve erro em alguma fase ?
        if not lv_ok:

            # logger
            l_log = logging.getLogger("CModelPiloto::load_tables")
            l_log.setLevel(M_LOG_LVL)
            l_log.critical(u"<E01: Erro na carga da base de dados ({}).".format(ls_msg))

            # cria um evento de quit
            l_evt = events.Quit()
            assert l_evt

            # dissemina o evento
            self.event.post(l_evt)

            # termina a aplicação
            sys.exit(1)

    # ---------------------------------------------------------------------------------------------
    '''
    def load_air(self, fs_cena):
        """
        faz a carga do airspace.

        @param ls_cena: cenário.

        @return flag e mensagem.
        """
        # obtém o diretório padrão de tabelas
        ls_dir = self.dct_config["dir.air"]

        # nome do diretório vazio ?
        if ls_dir is None:

            # diretório padrão de tabelas
            self.dct_config["dir.air"] = "airs"

            # diretório padrão de tabelas
            ls_dir = "airs"

        # expand user (~)
        ls_dir = os.path.expanduser(ls_dir)

        # diretório não existe ?
        if not os.path.exists(ls_dir):

            # cria o diretório
            os.mkdir(ls_dir)

        # create airspace and weather
        self.__airspace = airspace.modelAirspace(self, ls_dir, fs_cena)
        assert self.__airspace

        # retorna ok
        return True, None

    # ---------------------------------------------------------------------------------------------

    def load_land(self, fs_land):
        """
        faz a carga do landscape.

        @param ls_cena: cenário.

        @return flag e mensagem.
        """
        # obtém o diretório padrão de landscapes
        ls_dir = self.dct_config["dir.map"]

        # nome do diretório vazio ?
        if ls_dir is None:

            # diretório padrão de landscapes
            self.dct_config["dir.map"] = "maps"

            # diretório padrão de landscapes
            ls_dir = "maps"

        # expand user (~)
        ls_dir = os.path.expanduser(ls_dir)

        # diretório não existe ?
        if not os.path.exists(ls_dir):

            # cria o diretório
            os.mkdir(ls_dir)

        # create landscape
        self.__landscape = landscape.modelLandscape(self, ls_dir, fs_land)
        assert self.__landscape

        # retorna ok
        return True, None
    '''
    # ---------------------------------------------------------------------------------------------

    def notify(self, f_event):
        """
        callback de tratamento de eventos recebidos.

        @param f_event: evento recebido.
        """
        pass

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @property
    def airspace(self):
        """
        airspace
        """
        return self.__airspace

    # ---------------------------------------------------------------------------------------------
    '''
    @property
    def landscape(self):
        """
        landscape
        """
        return self.__landscape
    '''
    # ---------------------------------------------------------------------------------------------

    @property
    def emula_model(self):
        """
        flight model
        """
        return self.__emula_model

    # ---------------------------------------------------------------------------------------------

    @property
    def dct_prf(self):
        """
        dicionário de performances
        """
        return self.__dct_prf

# < the end >--------------------------------------------------------------------------------------
