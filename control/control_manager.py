#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
control_manager

coordinates communications between the model, views and controllers through the use of events

revision 0.4  2016/ago  mlabru
pequenas correções e otimizações

revision 0.3  2015/nov  mlabru
pep8 style conventions

revision 0.2  2014/nov  mlabru
inclusão do event manager e alteração do config manager

revision 0.1  2014/nov  mlabru
initial version (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.4$"
__author__ = "mlabru, sophosoft"
__date__ = "2016/08"

# < imports >--------------------------------------------------------------------------------------

# python library
# import logging
import sys
import threading
import time

# from ..model 
import model.glb_data as gdata

# from ..control.events 
import control.events.events_manager as evtmgr
import control.events.events_basic as events

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CControlManager >------------------------------------------------------------------------

class CControlManager(threading.Thread):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    # void (str)
    def __init__(self, fs_path=None):
        """
        inicia o controle

        @param fs_path: path do arquivo de configuração
        """
        # logger
        # M_LOG.info("__init__:>>")

        # inicia a super classe
        super(CControlManager, self).__init__()

        # the application itself
        self.__app = None

        # instancia o event manager
        self.__event = evtmgr.CEventsManager()
        assert self.__event

        # registra a sí próprio como recebedor de eventos
        self.__event.register_listener(self)

        # carrega as opções de configuração
        self.__config = None

        # model manager
        self.__model = None

        # splash screen
        self.__splash = None

        # view manager
        self.__view = None

        # voip library
        self.__voip = None

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    # void (void)
    def cbk_termina(self):
        """
        termina a aplicação
        """
        # logger
        # M_LOG.info("cbk_termina:>>")

        # verifica condições de execução
        assert self.__event

        # cria um evento de quit
        l_evt = events.CQuit()
        assert l_evt

        # dissemina o evento
        self.__event.post(l_evt)

        # logger
        # M_LOG.info("cbk_termina:<<")

    # ---------------------------------------------------------------------------------------------
    @staticmethod
    def notify(f_event):
        """
        callback de tratamento de eventos recebidos.

        @param f_event: event.
        """
        # logger
        # M_LOG.info("notify:>>")

        # check input
        assert f_event

        # recebeu um aviso de término da aplicação ?
        if isinstance(f_event, events.CQuit):
            # para todos os processos
            gdata.G_KEEP_RUN = False

            # aguarda o término das tasks
            time.sleep(1)

            # termina a aplicação
            sys.exit()

        # logger
        # M_LOG.info("notify:<<")

    # ---------------------------------------------------------------------------------------------
    # void (void)
    def run(self):
        """
        executa a aplicação
        """
        # logger
        # M_LOG.info("run:><")

        # return
        return gdata.G_KEEP_RUN

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def app(self):
        """
        get application
        """
        return self.__app

    @app.setter
    def app(self, f_val):
        """
        set application
        """
        self.__app = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def config(self):
        """
        get config manager
        """
        return self.__config

    @config.setter
    def config(self, f_val):
        """
        set config manager
        """
        self.__config = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def event(self):
        """
        get event manager
        """
        return self.__event

    @event.setter
    def event(self, f_val):
        """
        set event manager
        """
        self.__event = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def model(self):
        """
        get model manager
        """
        return self.__model

    @model.setter
    def model(self, f_val):
        """
        set model manager
        """
        self.__model = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def splash(self):
        """
        get splash screen
        """
        return self.__splash

    @splash.setter
    def splash(self, f_val):
        """
        set splash screen
        """
        self.__splash = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def view(self):
        """
        get view manager
        """
        return self.__view

    @view.setter
    def view(self, f_val):
        """
        set view manager
        """
        self.__view = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def voip(self):
        """
        get voip library
        """
        return self.__voip

# < the end >--------------------------------------------------------------------------------------
