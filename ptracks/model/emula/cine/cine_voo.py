#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
cine_voo

the flight class. It holds information about a flight and the commands the flight has been given

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
initial version (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import math

# libs
import ptracks.libs.coords.coord_defs as cdefs

# model
import ptracks.model.newton.defs_newton as ldefs

import ptracks.model.emula.cine.cine_calc as cincalc
import ptracks.model.emula.cine.cine_model as cinmodel

import ptracks.model.emula.cine.obtem_brk as obrk
import ptracks.model.emula.cine.prc_aproximacao as apx
import ptracks.model.emula.cine.prc_decolagem as dep
import ptracks.model.emula.cine.prc_dir_fixo as dfix
import ptracks.model.emula.cine.prc_espera as esp
import ptracks.model.emula.cine.prc_pouso as arr
import ptracks.model.emula.cine.prc_subida as sub
import ptracks.model.emula.cine.prc_trajetoria as trj
import ptracks.model.emula.cine.dados_dinamicos as cine
import ptracks.model.emula.cine.trata_associado as tass

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CCineVoo >-------------------------------------------------------------------------------

class CCineVoo(cinmodel.CCineModel):
    """
    the object holding all information concerning a flight
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_engine, f_control):
        """
        @param f_engine: flight engine
        @param f_control: control manager
        """
        # logger
        # M_LOG.info("__init__:>>")

        # check input
        assert f_engine
        assert f_control

        # init super class
        super(CCineVoo, self).__init__(f_engine, f_control)

        # heradados de CCineModel
        # self.atv            # aeronave ativa
        # self.cine_data      # dados de cinemática
        # self.coords         # coordinate system
        # self.dct_aer        # dicionário de aeródromos
        # self.dct_fix        # dicionário de fixos
        # self.dct_prc        # dicionário de procedimentos
        # self.dct_prf        # dicionário de performances
        # self.dct_trf        # dicionário de tráfegos
        # self.engine         # flight engine
        # self.exe            # exercício
        # self.sck_send       # socket de envio
        # self.sim_time       # simulation time
        # self.stk_context    # pilha

        # variação de tempo
        self.__f_delta_t = 0.

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    def update_cinematica(self):
        """
        atualiza os dados cinemáticos da aeronave
        """
        # logger
        # M_LOG.info("update_cinematica:>>")

        # checks
        assert self.atv
        assert self.cine_data
        assert self.sim_time

        # checks
        if (not self.atv.v_atv_ok) or (ldefs.E_ATIVA != self.atv.en_trf_est_atv):
            # logger
            l_log = logging.getLogger("update_cinematica")
            l_log.setLevel(logging.ERROR)
            l_log.error("<E01: aeronave não ativa.")

            # cai fora...
            return

        # obtém a hora atual em segundos
        lf_tempo_atu = self.sim_time.obtem_hora_sim()
        # M_LOG.debug("lf_tempo_atu:[{}]".format(lf_tempo_atu))

        # calcula a variação de tempo desde a ultima atualização
        self.__f_delta_t = lf_tempo_atu - self.atv.l_atv_time_ant
        # M_LOG.debug("lf_delta_t:[{}]".format(self.__f_delta_t))

        # checa se passou algum tempo (1/10th)
        # if self.__f_delta_t < .1:
            # logger
            # l_log = logging.getLogger("update_cinematica")
            # l_log.setLevel(logging.ERROR)
            # l_log.error(u"<E02: delta de tempo muito pequeno.")

            # cai fora...
            # return

        # salva a hora atual
        self.atv.l_atv_time_ant = lf_tempo_atu

        # atualiza os dados cinemáticos
        cine.dados_dinamicos(self.atv, self.cine_data, self.__f_delta_t, self.sim_time)

        # envia as pistas para as consoles
        self.send_trks()

        # logger
        # M_LOG.info("update_cinematica:<<")

    # ---------------------------------------------------------------------------------------------
    def prc_aproximacao(self):
        """
        procedimento de aproximação
        """
        # logger
        # M_LOG.info("prc_aproximacao:><")

        # checks
        assert self.atv
        assert self.cine_data
        assert self.stk_context is not None

        # executa a aproximação
        apx.prc_aproximacao(self.atv, self.cine_data, self.stk_context)

    # ---------------------------------------------------------------------------------------------
    def prc_apx_perdida(self):
        """
        procedimento de aproximação perdida
        """
        # logger
        # M_LOG.info("prc_apx_perdida:><")

        # checks (I)
        assert self.atv

        # verifica condições de execução (II)
        if (not self.atv.v_atv_ok) or (ldefs.E_ATIVA != self.atv.en_trf_est_atv):
            # cai fora...
            return False

    # ---------------------------------------------------------------------------------------------
    def prc_decolagem(self):
        """
        procedimento de decolagem
        """
        # logger
        # M_LOG.info("prc_decolagem:><")

        # checks
        assert self.atv
        assert self.cine_data
        assert self.stk_context is not None

        # executa a decolagem
        dep.prc_decolagem(self.atv, self.cine_data, self.stk_context)

    # ---------------------------------------------------------------------------------------------
    def prc_dir_fixo(self):
        """
        procedimento de direcionamento a fixo
        """
        # logger
        # M_LOG.info("prc_dir_fixo:><")

        # checks
        assert self.atv
        assert self.cine_data
        # assert self.stk_context is not None

        # executa direcionamento a fixo
        dfix.prc_dir_fixo(self.atv, self.cine_data)

    # ---------------------------------------------------------------------------------------------
    def prc_espera(self):
        """
        procedimento de espera
        """
        # logger
        # M_LOG.info("prc_espera:><")

        # checks
        assert self.atv
        assert self.cine_data
        assert self.stk_context is not None

        # executa espera
        esp.prc_espera(self.atv, self.cine_data, self.stk_context, self.__f_delta_t)

    # ---------------------------------------------------------------------------------------------
    def prc_pouso(self):
        """
        procedimento de pouso
        """
        # logger
        # M_LOG.info("prc_pouso:><")

        # checks
        assert self.atv
        # assert self.cine_data
        # assert self.stk_context is not None

        # executa pouso
        arr.prc_pouso(self.atv)  # , self.cine_data, self.stk_context)

    # ---------------------------------------------------------------------------------------------
    def prc_subida(self):
        """
        realiza o procedimento de subida após o procedimento de decolagem
        """
        # logger
        # M_LOG.info("prc_subida:><")

        # checks
        assert self.atv
        assert self.cine_data
        assert self.stk_context is not None

        # executa subida
        sub.prc_subida(self.atv, self.cine_data, self.stk_context)

    # ---------------------------------------------------------------------------------------------
    def prc_trajetoria(self):
        """
        procedimento de trajetória
        """
        # logger
        # M_LOG.info("prc_trajetoria:><")

        # checks
        assert self.atv
        assert self.cine_data
        assert self.stk_context is not None

        # executa trajetória
        trj.prc_trajetoria(self.atv, self.cine_data, self.stk_context)

# < the end >--------------------------------------------------------------------------------------
