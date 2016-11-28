#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
prc_decolagem

realizar o procedimento de decolagem

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

# libs
import libs.coords.coord_defs as cdefs

# model
import model.newton.defs_newton as ldefs

import model.emula.cine.abort_prc as abnd
import model.emula.cine.calc_proa_demanda as cpd
import model.emula.cine.trata_associado as tass

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------
def __check_ok(f_atv, f_cine_data):
    """
    preparar a aeronave para decolagem

    @param f_atv: pointer to struct aeronaves
    @param f_cine_data: dados da cinemática
    """
    # logger
    # M_LOG.info("__check_ok:>>")

    # check input
    assert f_atv

    # active flight ?
    # if (not f_atv.v_atv_ok) or (ldefs.E_ATIVA != f_atv.en_trf_est_atv):
        # logger
        # l_log = logging.getLogger("__check_ok")
        # l_log.setLevel(logging.ERROR)
        # l_log.error("<E01: aeronave não ativa.")

        # abort procedure
        # abnd.abort_prc(f_atv)

        # cai fora...
        # return

    # performance ok ?
    # if (f_atv.ptr_trf_prf is None) or (not f_atv.ptr_trf_prf.v_prf_ok):
        # logger
        # l_log = logging.getLogger("__check_ok")
        # l_log.setLevel(logging.ERROR)
        # l_log.error("<E02: performance não existe.")

        # abort procedure
        # abnd.abort_prc(f_atv)

        # cai fora...
        # return

    # pointer to aerodrome
    l_aer = f_cine_data.ptr_aer

    # aerodrome ok ?
    if (l_aer is None) or not l_aer.v_aer_ok:
        # logger
        l_log = logging.getLogger("__check_ok")
        l_log.setLevel(logging.ERROR)
        l_log.error("<E03: aeródromo de decolagem inexistente.")

        # abort procedure
        abnd.abort_prc(f_atv)

        # cancel flight 
        f_atv.en_atv_est_atv = ldefs.E_CANCELADA

        # return
        return

    # pointer to runway
    l_pst = f_cine_data.ptr_pis

    # runway ok ?
    if (l_pst is None) or not l_pst.v_pst_ok:
        # logger
        l_log = logging.getLogger("__check_ok")
        l_log.setLevel(logging.ERROR)
        l_log.error("<E04: pista de decolagem inexistente.")

        # abort procedure
        abnd.abort_prc(f_atv)

        # cancel flight 
        f_atv.en_atv_est_atv = ldefs.E_CANCELADA

        # return
        return

    # aceleração
    f_atv.f_atv_acel = f_atv.ptr_trf_prf.f_prf_raz_max_var_vel * ldefs.D_FATOR_ACEL

    # velocidade atual
    f_atv.f_trf_vel_atu = 0.

    # velocidade de decolagem
    f_atv.f_atv_vel_dem = f_atv.ptr_trf_prf.f_prf_vel_dec

    # rumo da pista
    f_atv.f_trf_pro_atu = \
    f_atv.f_atv_pro_dem = l_pst.i_pst_rumo

    # elevação do aeródromo
    f_atv.f_trf_alt_atu = \
    f_atv.f_atv_alt_dem = l_aer.f_aer_elev
    # M_LOG.debug("f_trf_alt_atu:[{}]".format(f_atv.f_trf_alt_atu))

    # posiciona aeronave na cabeceira da pista em x/y
    f_atv.f_trf_x = l_pst.f_pst_x
    f_atv.f_trf_y = l_pst.f_pst_y

    # sinaliza a fase de processamento de decolagem
    f_atv.en_atv_fase = ldefs.E_FASE_DECOLAGEM

    # logger
    # M_LOG.info("__check_ok:<<")

# -------------------------------------------------------------------------------------------------
def __do_dep(f_atv, f_cine_data, fstk_context):
    """
    realizar o procedimento de decolagem

    @param f_atv: ponteiro para struct aeronaves
    @param f_cine_data: dados de cinemática
    @param fstk_context: ponteiro para pilha
    """
    # logger
    # M_LOG.info("__do_dep:>>")

    # check input
    assert f_atv
    assert f_cine_data
    assert fstk_context

    # active flight ?
    # if (not f_atv.v_atv_ok) or (ldefs.E_ATIVA != f_atv.en_trf_est_atv):
        # logger
        # l_log = logging.getLogger("__do_dep")
        # l_log.setLevel(logging.ERROR)
        # l_log.error("<E01: aeronave não ativa.")

        # abort procedure
        # abnd.abort_prc(f_atv)

        # cai fora...
        # return

    # performance ok ?
    # if (f_atv.ptr_trf_prf is None) or (not f_atv.ptr_trf_prf.v_prf_ok):
        # logger
        # l_log = logging.getLogger("__do_dep")
        # l_log.setLevel(logging.ERROR)
        # l_log.error("<E02: performance não existe.")

        # abort procedure
        # abnd.abort_prc(f_atv)

        # cai fora...
        # return

    # obtém do contexto a função operacional anterior
    len_fnc_ope_tmp, _, _, _, _ = fstk_context[-1]

    # atingiu a velocidade de decolagem ?
    if f_atv.f_trf_vel_atu != f_atv.ptr_trf_prf.f_prf_vel_dec:
        # não atingiu a velocidade de decolagem, return
        return

    # pointer aerodrome
    l_aer = f_cine_data.ptr_aer

    # aerodrome ok ?
    if (l_aer is None) or not l_aer.v_aer_ok:
        # logger
        l_log = logging.getLogger("__do_dep")
        l_log.setLevel(logging.ERROR)
        l_log.error("<E03: aeródromo de decolagem inexistente.")

        # abort procedure
        abnd.abort_prc(f_atv)

        # cancel flight 
        f_atv.en_atv_est_atv = ldefs.E_CANCELADA

        # return
        return

    # verifica se é uma decolagem com subida ou decolagem pura
    if (ldefs.E_SUBIDA == f_atv.en_trf_fnc_ope_ant) or (ldefs.E_SUBIDA == len_fnc_ope_tmp):
        # pointer to subida
        l_sub = f_cine_data.ptr_sub
        # M_LOG.debug("__do_dep:l_sub:[{}]".format(l_sub))

        # subida ok ?
        if (l_sub is None) or not l_sub.v_prc_ok:
            # logger
            l_log = logging.getLogger("__do_dep")
            l_log.setLevel(logging.ERROR)
            l_log.error("<E04: decolagem/subida inexistente.")

            # abort procedure
            abnd.abort_prc(f_atv)

            # cancel flight 
            f_atv.en_atv_est_atv = ldefs.E_CANCELADA

            # return
            return

        # pointer to first climb breakpoint
        l_brk = l_sub.lst_sub_brk[0]
        # M_LOG.debug("__do_dep:l_brk:[{}]".format(l_brk))

        # breakpoint ok ?
        if (l_brk is None) or not l_brk.v_brk_ok:
            # logger
            l_log = logging.getLogger("__do_dep")
            l_log.setLevel(logging.ERROR)
            l_log.error("<E05: decolagem/subida breakpoint inexistente.")

            # abort procedure
            abnd.abort_prc(f_atv)

            # cancel flight 
            f_atv.en_atv_est_atv = ldefs.E_CANCELADA

            # return
            return

        # pointer to runway
        l_pst = f_cine_data.ptr_pis

        # runway ok ?
        if (l_pst is None) or not l_pst.v_pst_ok:
            # logger
            l_log = logging.getLogger("__do_dep")
            l_log.setLevel(logging.ERROR)
            l_log.error("<E06: pista de decolagem inexistente.")

            # abort procedure
            abnd.abort_prc(f_atv)

            # cancel flight 
            f_atv.en_atv_est_atv = ldefs.E_CANCELADA

            # return
            return

        # calcula a radial entre o 1*brk da subida e a pista
        lf_delta_x = l_brk.f_brk_x - l_pst.f_pst_x
        lf_delta_y = l_brk.f_brk_y - l_pst.f_pst_y

        lf_radial_pstta_brk = cpd.calc_proa_demanda(lf_delta_x , lf_delta_y)

        # calcula o ângulo entre o rumo da pista e o 1*brk da subida
        lf_ang_pista_brk = abs(l_pst.i_pst_rumo - lf_radial_pstta_brk)

        # -----------------------------------------------------------------------------------------
        # regra de cálculo da altitude na decolagem com Subida
        # objetivo: livrar obstáculos na decolagem (montanhas, prédios, ...)
        # limites: ângulo limite de 15 graus entre rumo da pista e o primeiro ponto da subida
        # se a diferença dos ângulos (fAngPistaBkp) for maior que 15 graus, então a altitude
        # de demanda será 400ft (não é nível) acima da elevação do aeródromo
        # se a diferença dos ângulos (fAngPistaBkp) for menor ou igual a 15 graus, a altitude
        # de demanda será 50ft acima da elevação do aeródromo
        # -----------------------------------------------------------------------------------------
        if lf_ang_pista_brk > 15.:
            # calcula 400ft acima da altitude da pista (converte ft -> m)
            f_atv.f_atv_alt_dem = (400. * cdefs.D_CNV_FT2M) + l_aer.f_aer_elev

        # senão,...
        else:
            # calcula 50ft acima da altitude da pista (converte ft -> m)
            f_atv.f_atv_alt_dem = (50. * cdefs.D_CNV_FT2M) + l_aer.f_aer_elev

        # -----------------------------------------------------------------------------------------
        # determina a razão máxima de subida na decolagem para todos os casos
        #
        # PBN (casos de DEP no SBGL e SBRJ)
        # Descomentado este trecho para as seguintes considerações:
        # a) aeródromos com pistas curtas (caso SBGL) as aeronaves consigam aplicar a
        #    RazMaxSubDec, porém o gradiente tem que estar zerado no primeiro ponto da Subida.
        # b) aeródromos com pistas longas, a AnvRazSub possa ser aplicada mediante o cálculo do
        #    gradiente (se houver) para atingir o primeiro ponto da Subida.
        #
        # Obs_1: Com o retorno da verificação do gradiente, evitou-se que aeronaves decolando
        #        em pistas longas chegassem a subir como se fossem foguetes devido ao uso
        #        generalizado da prf_raz_max_sub_dec para todos os casos.
        # Obs_2: Ambos casos a aceleração na DEP tem que ser 4 vezes (campo do arquivo ".ini")
        # -----------------------------------------------------------------------------------------
        if 0. == l_brk.f_brk_raz_vel:
            # razão de subida é a razão máxima de subida na decolagem
            f_atv.f_atv_raz_sub = f_atv.ptr_trf_prf.f_prf_raz_max_sub_dec

        # senão,...
        else:
            # calcula a razão de subida em função do gradiente
            f_atv.f_atv_raz_sub = f_atv.f_trf_vel_atu * l_brk.f_brk_raz_vel

    # decolagem pura, sem subida
    else:
        # -----------------------------------------------------------------------------------------
        # regra de cálculo da altitude na decolagem pura
        # objetivo: livrar obstáculos na decolagem (montanhas, prédios, ...)
        # a altitude de demanda será igual a 50ft acima da elevação do aeródromo
        # -----------------------------------------------------------------------------------------

        # calcula 50ft acima da altitude da pista
        f_atv.f_atv_alt_dem = (50. * cdefs.D_CNV_FT2M) + l_aer.f_aer_elev

        # razão de subida é a razão máxima de subida na decolagem
        f_atv.f_atv_raz_sub = f_atv.ptr_trf_prf.f_prf_raz_max_sub_dec

    # ---------------------------------------------------------------------------------------------
    # regra da velocidade na decolagem
    # objetivo: estabelecer a velocidade limite de 250kt para as aeronaves que estiverem
    # voando abaixo de 10000ft (FL100)
    # ---------------------------------------------------------------------------------------------

    # verifica a altitude atual da aeronave
    if (f_atv.f_trf_alt_atu * cdefs.D_CNV_M2FT) < ldefs.D_ALT_MAX_TMA:
        # determina a velocidade de subida na decolagem (limitada a 250kt)
        f_atv.f_atv_vel_dem = min(f_atv.ptr_trf_prf.f_prf_vel_sub_dec, ldefs.D_VEL_MAX_TMA)

    # ajusta aceleração
    f_atv.f_atv_acel = f_atv.ptr_trf_prf.f_prf_raz_var_vel

    # determina fase final da decolagem
    f_atv.en_atv_fase = ldefs.E_FASE_ESTABILIZADA

    # logger
    # M_LOG.info("__do_dep:<<")

# -------------------------------------------------------------------------------------------------
def prc_decolagem(f_atv, f_cine_data, fstk_context):
    """
    @param f_atv: ponteiro para struct aeronaves
    @param f_cine_data: ponteiro para pilha
    @param fstk_context: pilha de contexto
    """
    # logger
    # M_LOG.info("prc_decolagem:>>")

    # check input
    assert f_atv
    assert f_cine_data
    assert fstk_context

    # active flight ?
    if (not f_atv.v_atv_ok) or (ldefs.E_ATIVA != f_atv.en_trf_est_atv):
        # logger
        l_log = logging.getLogger("prc_decolagem")
        l_log.setLevel(logging.ERROR)
        l_log.error("<E01: aeronave não ativa.")

        # abort procedure
        abnd.abort_prc(f_atv)

        # cai fora...
        return

    # performance ok ?
    if (f_atv.ptr_trf_prf is None) or (not f_atv.ptr_trf_prf.v_prf_ok):
        # logger
        l_log = logging.getLogger("prc_decolagem")
        l_log.setLevel(logging.ERROR)
        l_log.error("<E02: performance não existe.")

        # abort procedure
        abnd.abort_prc(f_atv)

        # cai fora...
        return

    # processa as fases

    # fase de preparação ?
    if ldefs.E_FASE_ZERO == f_atv.en_atv_fase:
        # verifica condição para execução
        __check_ok(f_atv, f_cine_data)

    # fase de decolagem ?
    elif ldefs.E_FASE_DECOLAGEM == f_atv.en_atv_fase:
        # realiza o processamento
        __do_dep(f_atv, f_cine_data, fstk_context)

    # fase estabilizada ?
    elif ldefs.E_FASE_ESTABILIZADA == f_atv.en_atv_fase:
        # verifica o término da decolagem
        if f_atv.f_trf_alt_atu == f_atv.f_atv_alt_dem:
            # obtém do contexto a função operacional anterior
            len_fnc_ope_tmp, _, _, _, _ = fstk_context[-1]

            # restaura a pilha de procedimento ou por comando de pilotagem
            if (ldefs.E_SUBIDA == f_atv.en_trf_fnc_ope_ant) or (ldefs.E_SUBIDA == len_fnc_ope_tmp):
                # restaura a pilha de procedimento
                tass.restaura_associado(f_atv, f_cine_data, fstk_context)

            # senão,...
            else:
                # decolagem incluida num tráfego, coloca em MANUAL
                f_atv.f_atv_alt_dem = f_atv.ptr_trf_prf.f_prf_teto_sv
                f_atv.en_trf_fnc_ope = ldefs.E_MANUAL

    # senão,...
    else:
        # logger
        l_log = logging.getLogger("prc_decolagem")
        l_log.setLevel(logging.ERROR)
        l_log.error("<E04: fase da decolagem não identificada.")

        # abort procedure
        abnd.abort_prc(f_atv)

    # logger
    # M_LOG.info("prc_decolagem:<<")

# < the end >--------------------------------------------------------------------------------------
