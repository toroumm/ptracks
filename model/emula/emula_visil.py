#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
emula_visil

DOCUMENT ME!

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2015/fev  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "mlabru, sophosoft"
__date__ = "2015/12"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import sys
import threading
import time

# model
import model.glb_data as gdata
import model.glb_defs as gdefs

import model.emula.emula_model as model
import model.visil.aircraft_visil as canv

# control
import control.events.events_flight as events

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CEmulaVisil >----------------------------------------------------------------------------

class CEmulaVisil (model.CEmulaModel):
    """
    the flight model class generates new flights and handles their movement. It has a list of
    flight objects holding all flights that are currently active. The flights are generated when
    activation time comes, or quando ja foi ativado na confecção do exercicio. Once a flight has
    been generated it is handed by the flight engine
    """
    # ---------------------------------------------------------------------------------------------
    # void (?)
    def __init__(self, f_model, f_control):
        """
        initializes the app and prepares everything

        @param f_model: model manager
        @param f_control: control manager
        """
        # logger
        # M_LOG.info("__init__:>>")

        # verifica parametros de entrada
        assert f_control

        # inicia a super classe
        super(CEmulaVisil, self).__init__(f_model, f_control)

        # herdados de CEmulaModel
        # self.config        # config manager
        # self.dct_config    # dicionário de configuração
        # self.control       # control manager
        # self.event         # event manager
        # self.dct_flight    # dictionary for all active flights
        # self.model         # model manager

        # obtém a queue de dados
        self.__q_rcv_trks = f_control.q_rcv_trks
        assert self.__q_rcv_trks

        # obtém o data listener
        self.__sck_rcv_trks = f_control.sck_rcv_trks
        assert self.__sck_rcv_trks

        # cria a trava da lista de vôos
        gdata.G_LCK_FLIGHT = threading.Lock()
        assert gdata.G_LCK_FLIGHT

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    # void (?)
    def run(self):
        """
        checks whether it's time to created another flight
        """
        # logger
        # M_LOG.info("run:>>")

        # check de colisão
        lf_tim_evnt = self.dct_config["tim.evnt"]

        # enquanto não inicia...
        while not gdata.G_KEEP_RUN:
            # aguarda 1 seg
            time.sleep(1)

        # inicia o recebimento de mensagens de dados
        self.__sck_rcv_trks.start()

        # loop
        while gdata.G_KEEP_RUN:
            # obtém o tempo inicial em segundos
            ll_now = time.time()

            # obtém um item da queue de entrada
            llst_data = self.__q_rcv_trks.get()
            # M_LOG.debug("llst_data: (%s)" % str(llst_data))

            # queue tem dados ?
            if llst_data:
                # mensagem de status de aeronave ?
                if gdefs.D_MSG_NEW == int(llst_data[0]):
                    ls_callsign = llst_data[10]
                    # M_LOG.debug("run:callsign:[{}]".format(llst_data[10]))

                    # trava a lista de vôos
                    gdata.G_LCK_FLIGHT.acquire()

                    try:
                        # aeronave já está no dicionário ?
                        if ls_callsign in self.dct_flight:
                            # atualiza os dados da aeronave
                            self.dct_flight[ls_callsign].update_data(llst_data[1:])

                        # senão, aeronave nova...
                        else:
                            # create new aircraft
                            self.dct_flight[ls_callsign] = canv.CAircraftVisil(self, llst_data[1:])
                            assert self.dct_flight[ls_callsign]

                    finally:
                        # libera a lista de vôos
                        gdata.G_LCK_FLIGHT.release()

                    # cria um evento de atualização de aeronave
                    l_evt = events.CFlightUpdate(ls_callsign)
                    assert (l_evt)

                    # dissemina o evento
                    self.event.post(l_evt)

                # mensagem de eliminação de aeronave ?
                # elif gdefs.D_MSG_KLL == int(llst_data[0]):
                    '''
                    # coloca a mensagem na queue
                    # M_LOG.debug("Elimina: (%s)" % str(ls_callsign))

                    # trava a lista de vôos
                    gdata.G_LCK_FLIGHT.acquire()

                    try:
                        # aeronave está no dicionário ?
                        if ls_callsign in self.dctFlight:
                            # retira a aeronave do dicionário
                            del self.dctFlight[ls_callsign]

                    finally:
                        # libera a lista de vôos
                        gdata.G_LCK_FLIGHT.release()

                    # cria um evento de eliminação de aeronave
                    l_evt = events.CFlightKill(ls_callsign)
                    assert l_evt
                    # M_LOG.debug("l_evt: " + str(l_evt))

                    # dissemina o evento
                    self.event.post(l_evt)'''

                # senão, mensagem não reconhecida ou não tratada
                else:
                    # logger
                    l_log = logging.getLogger("CEmulaVisil::run")
                    l_log.setLevel(logging.WARNING)
                    l_log.warning("<E01: Mensagem não reconhecida ou não tratada.")

            # obtém o tempo final em segundos e calcula o tempo decorrido
            ll_dif = time.time() - ll_now

            # esta adiantado ?
            if lf_tim_evnt > ll_dif:
                # permite o scheduler (1/10th)
                time.sleep(lf_tim_evnt - ll_dif)

        # logger
        # M_LOG.info("run:<<")

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def sck_rcv_trks(self):
        """
        get data listener
        """
        return self.__sck_rcv_trks

# < the end >--------------------------------------------------------------------------------------
