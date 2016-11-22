#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
airspace_newton

basic model manager
load from one configuration file all configured tables

revision 0.3  2015/nov  mlabru
pep8 style conventions

revision 0.2  2014/nov  mlabru
inclusão do event manager e config manager

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.3$"
__author__ = "mlabru, sophosoft"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import os

# model
import model.stock.airspace_basic as airs

import model.items.apx_data as apxdata
import model.items.esp_data as espdata
import model.items.sub_data as subdata
import model.items.trj_data as trjdata

import model.newton.defs_newton as ldefs

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CAirspaceNewton >-------------------------------------------------------------------------

class CAirspaceNewton(airs.CAirspaceBasic):
    """
    newton airspace
    """
    # ---------------------------------------------------------------------------------------------
    # void (?)
    def __init__(self, f_model):
        """
        @param f_model: model manager
        """
        # logger
        # M_LOG.info("__init__:>>")

        # init super class
        super(CAirspaceNewton, self).__init__(f_model)

        # herdado de CAirspaceBasic
        # self.model           # model manager 
        # self.event           # event manager
        # self.config          # config manager
        # self.dct_aer         # dicionário de aeródromos
        # self.dct_fix         # dicionário de fixos
        # self.dct_fix_indc    # dicionário de fixos por indicativo

        # procedimentos de aproximação
        self.__dct_apx = {}

        # procedimentos de espera
        self.__dct_esp = {}

        # procedimentos de subida
        self.__dct_sub = {}

        # procedimentos de trajetória
        self.__dct_trj = {}

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    # void (?)
    def get_aer_pst(self, fs_aer, fs_pst):
        """
        obtém o pointer para o aeródromo e pista

        @param fs_aer: indicativo do aeródromo
        @param fs_pst: indicativo da pista

        @return pointer para o aeródromo e pista
        """
        # logger
        # M_LOG.info("get_aer_pst:>>")

        # obtém o aeródromo
        l_aer = self.dct_aer.get(fs_aer, None)

        if l_aer is None:
            # logger
            l_log = logging.getLogger("CAirspaceNewton::get_aer_pst")
            l_log.setLevel(logging.ERROR)
            l_log.error(u"<E01: não existe aeródromo [{}].".format(fs_aer))

            # retorna pointers
            return None, None

        # obtém a pista
        l_pst = l_aer.dct_aer_pistas.get(fs_pst, None)

        if l_pst is None:
            # logger
            l_log = logging.getLogger("CAirspaceNewton::get_aer_pst")
            l_log.setLevel(logging.ERROR)
            l_log.error(u"<E02: não existe pista [{}] no aeródromo [{}].".format(fs_pst, fs_aer))

            # retorna pointers
            return l_aer, None

        # logger
        # M_LOG.info("get_aer_pst:<<")

        # retorna pointers
        return l_aer, l_pst

    # ---------------------------------------------------------------------------------------------
    # void (obj)
    def get_brk_prc(self, f_brk):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("get_brk_prc:>>")

        # existe procedimento associado ?
        if f_brk.ptr_brk_prc is not None:
            # obtém o procedimento e a função operacional
            f_brk.ptr_brk_prc, f_brk.en_brk_fnc_ope = self.get_ptr_prc(f_brk.ptr_brk_prc)

        # logger
        # M_LOG.info("get_brk_prc:<<")

    # ---------------------------------------------------------------------------------------------
    # void (?)
    def get_ptr_prc(self, fs_prc):
        """
        obtém o pointer e a função operacional de um procedimento

        @param fs_prc: procedimento no formato XXX9999

        @return pointer e função operacional
        """
        # logger
        # M_LOG.info("get_ptr_prc:>>")

        # não existe procedimento ?
        if fs_prc is None:
            # logger
            l_log = logging.getLogger("CAirspaceNewton::get_ptr_prc")
            l_log.setLevel(logging.ERROR)
            l_log.error(u"<E01: não existe procedimento.")

            # retorna pointer & função
            return None, ldefs.E_NOPROC

        # obtém o procedimento
        ls_prc = fs_prc[:3]
        # M_LOG.debug("get_ptr_prc:ls_prc: " + str(ls_prc))

        # obtém o número do procedimento
        li_num_prc = int(fs_prc[3:])
        # M_LOG.debug("get_ptr_prc:li_num_prc: " + str(li_num_prc))

        # é uma aproximação ?
        if "APX" == ls_prc:
            # check dicionário de aproximação
            assert self.__dct_apx is not None

            # obtém o procedimento de aproximação pelo número
            lptr_prc = self.__dct_apx.get(li_num_prc, None)
            # M_LOG.debug("get_ptr_prc:lptr_prc: " + str(lptr_prc))

            # função operacional da aproximação
            le_fnc_ope = ldefs.E_APROXIMACAO if lptr_prc is not None else ldefs.E_NOPROC

        # é uma espera ?
        elif "ESP" == ls_prc:
            # check dicionário de espera
            assert self.__dct_esp is not None

            # obtém o procedimento de espera pelo número
            lptr_prc = self.__dct_esp.get(li_num_prc, None)
            # M_LOG.debug("get_ptr_prc:lptr_prc: " + str(lptr_prc))

            # função operacional da espera
            le_fnc_ope = ldefs.E_ESPERA if lptr_prc is not None else ldefs.E_NOPROC

        # é uma subida ?
        elif "SUB" == ls_prc:
            # check dicionário de subidas
            assert self.__dct_sub is not None

            # obtém o procedimento de subida pelo número
            lptr_prc = self.__dct_sub.get(li_num_prc, None)
            # M_LOG.debug("get_ptr_prc:lptr_prc: " + str(lptr_prc))

            # função operacional da subidas
            le_fnc_ope = ldefs.E_SUBIDA if lptr_prc is not None else ldefs.E_NOPROC

        # é uma trajetória ?
        elif "TRJ" == ls_prc:
            # check dicionário de trajetórias
            assert self.__dct_trj is not None

            # obtém o procedimento de trajetória pelo número
            lptr_prc = self.__dct_trj.get(li_num_prc, None)
            # M_LOG.debug("get_ptr_prc:lptr_prc: " + str(lptr_prc))

            # função operacional da trajetória
            le_fnc_ope = ldefs.E_TRAJETORIA if lptr_prc is not None else ldefs.E_NOPROC

        # senão, procedimento desconhecido
        else:
            # logger
            l_log = logging.getLogger("CAirspaceNewton::get_ptr_prc")
            l_log.setLevel(logging.ERROR)
            l_log.error(u"<E02: procedimento [{}] desconhecido. fallback to noProc.".format(fs_prc))

            # sem procedimento
            lptr_prc = None
            le_fnc_ope = ldefs.E_NOPROC

        # função operacional sem procedimento ?
        if (lptr_prc is None) and (ldefs.E_NOPROC != le_fnc_ope):
            # logger
            l_log = logging.getLogger("CAirspaceNewton::get_ptr_prc")
            l_log.setLevel(logging.ERROR)
            l_log.error(u"<E03: função operacional:[{}] sem procedimento:[{}].".format(ls_prc, li_num_prc))

        # logger
        # M_LOG.info("get_ptr_prc:<<")

        # retorna pointer & função
        return lptr_prc, le_fnc_ope

    # ---------------------------------------------------------------------------------------------
    # void (?)
    def load_dicts(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("load_dicts:>>")

        # monta o nome da tabela de procedimentos de aproximação
        ls_path = os.path.join(self.dct_config["dir.prc"], self.dct_config["tab.apx"])

        # carrega a tabela de procedimentos de aproximação em um dicionário
        self.__dct_apx = apxdata.CApxData(self.model, ls_path)
        assert self.__dct_apx is not None

        # monta o nome da tabela de procedimentos de espera
        ls_path = os.path.join(self.dct_config["dir.prc"], self.dct_config["tab.esp"])

        # carrega a tabela de procedimentos de espera em um dicionário
        self.__dct_esp = espdata.CEspData(self.model, ls_path)
        assert self.__dct_esp is not None

        # monta o nome da tabela de procedimentos de subida
        ls_path = os.path.join(self.dct_config["dir.prc"], self.dct_config["tab.sub"])

        # carrega a tabela de procedimentos de subida em um dicionário
        self.__dct_sub = subdata.CSubData(self.model, ls_path)
        assert self.__dct_sub is not None

        # monta o nome da tabela de procedimentos de trajetória
        ls_path = os.path.join(self.dct_config["dir.prc"], self.dct_config["tab.trj"])

        # carrega a tabela de procedimentos de trajetória em um dicionário
        self.__dct_trj = trjdata.CTrjData(self.model, ls_path)
        assert self.__dct_trj is not None

        # resolve os procedimentos dos breakpoints
        self.resolv_procs()

        # logger
        # M_LOG.info("load_dicts:<<")

    # ---------------------------------------------------------------------------------------------
    # void (?)
    def notify(self, f_event):
        """
        callback de tratamento de eventos recebidos

        @param f_event: evento recebido
        """
        # logger
        # M_LOG.info("notify:><")

    # ---------------------------------------------------------------------------------------------
    # void (void)
    def resolv_procs(self):
        """
        resolve os procedimentos dos breakpoints. Os procedimentos, ainda no formato XXX9999 são
        validados e resolvidos.
        """
        # logger
        # M_LOG.info("resolv_procs:>>")

        # para todos os procedimentos de aproximação...
        for l_apx in self.__dct_apx.values():
            # aproximação ok ?
            if l_apx is not None:
                # obtém o dicionário de esperas
                ldct_esp = self.__dct_esp
                assert ldct_esp

                # tem aproximação perdida ?
                # if 'S' == l_apx.v_apx_ape:
                    # pointer para a aproximação perdida
                    # l_apx.ptr_apx_prc_ape, _ = self.find_ptr_ape(l_apx.ptr_apx_aer, l_apx.ptr_apx_pis)
                    # assert l_apx.ptr_apx_prc_ape

                # obtém o procedimento de espera pelo número
                l_apx.ptr_apx_prc_esp = lptr_prc = self.__dct_esp.get(l_apx.ptr_apx_prc_esp, None)
                # M_LOG.debug("resolv_procs::l_apx.ptr_apx_prc_esp: " + str(l_apx.ptr_apx_prc_esp))

                # espera ok ?
                if l_apx.ptr_apx_prc_esp is None:
                    # logger
                    l_log = logging.getLogger("CAirspaceNewton::resolv_procs")
                    l_log.setLevel(logging.WARNING)
                    l_log.warning(u"<E02: aproximação [{}] sem espera.".format(l_apx.i_prc_id))
                '''
                # tem ILS ?
                if 'S' == l_apx.vApxILS:
                    # obtém o pointer para o ILS
                    l_apx.pApxPrcILS = self.find_ptr_ils(l_apx.pApxPtrAer.sAerID, l_apx.pApxPtrPis.sPisID)
                    assert l_apx.pApxPrcILS
                '''
                # para todos breakpoints da aproximação...
                for l_brk in l_apx.lst_apx_brk:
                    self.get_brk_prc(l_brk)
        '''
        # para todos os procedimentos de aproximação perdida...
        for l_prc_ape in self.__dct_ape:
            # obtém os dados da aproximação perdida
            l_ape = self.__dct_ape[l_prc_ape]

            if l_ape is not None:
                # para todos breakpoints da aproximação perdida...
                for l_brk in l_ape.aApeLstBrk:
                    self.get_brk_prc(l_brk)

        # para todos os procedimentos de ILS...
        for l_prc_ils in self.__dct_ils:
            # obtém os dados da ILS
            l_ils = self.__dct_ils[l_prc_ils]

            if l_ils is not None:
                # pointer do pouso
                l_ils.pIlsPtrPouso = self.findDepPtr ( l_ils.pILSPtrAer.sAerID, l_ils.pILSPtrPis.sPisID )
                assert l_ils.pIlsPtrPouso

                # obtém o procedimento e a função
                l_ils.pILSPtrPrc, l_ils.eILSPrc = self.get_ptr_prc(l_ils.eILSPrc)
        '''
        # para todos os procedimentos de subida...
        for l_sub in self.__dct_sub.values():
            # subida ok ?  
            if l_sub is not None:
                """
                # associa o número da decolagem
                l_sub.pSubPrcDec = self.find_prc_dep ( l_sub.pSubPtrAer.sAerID, l_sub.pSubPtrPis.sPisID )
                assert l_sub.pSubPtrDec
                """
                # para todos breakpoints da subida...
                for l_brk in l_sub.lst_sub_brk:
                    self.get_brk_prc(l_brk)

        # para todos os procedimentos de trajetória...
        for l_trj in self.__dct_trj.values():
            # trajetória ok ?
            if l_trj is not None:
                # para todos breakpoints da trajetória...
                for l_brk in l_trj.lst_trj_brk:
                    self.get_brk_prc(l_brk)

        # logger
        # M_LOG.info("resolv_procs:<<")

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_apx(self):
        """
        get aproximação
        """
        return self.__dct_apx

    @dct_apx.setter
    def dct_apx(self, f_val):
        """
        set aproximação
        """
        self.__dct_apx = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_esp(self):
        """
        get esperas
        """
        return self.__dct_esp

    @dct_esp.setter
    def dct_esp(self, f_val):
        """
        set esperas
        """
        self.__dct_esp = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_sub(self):
        """
        get subidas
        """
        return self.__dct_sub

    @dct_sub.setter
    def dct_sub(self, f_val):
        """
        set subidas
        """
        self.__dct_sub = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_trj(self):
        """
        get trajetórias
        """
        return self.__dct_trj

    @dct_trj.setter
    def dct_trj(self, f_val):
        """
        set trajetórias
        """
        self.__dct_trj = f_val

# < the end >--------------------------------------------------------------------------------------
