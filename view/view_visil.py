#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
view_visil

DOCUMENT ME!

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "mlabru, sophosoft"
__date__ = "2015/12"

# < imports >--------------------------------------------------------------------------------------

# python library
# import logging
import os
import sys

# PyQt library
from PyQt4 import QtCore

# view
import view.color_manager as clrm
import view.view_manager as view
import view.visil.wnd_main_visil as wmain

# control
import control.events.events_basic as event

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CViewVisil >-----------------------------------------------------------------------------

class CViewVisil(view.CViewManager):
    """
    the interface to configuration visil. Handles all interaction with user
    """
    # ---------------------------------------------------------------------------------------------
    # void (void)
    def __init__(self, f_control, f_model):
        """
        initializes the display
        """
        # logger
        # M_LOG.info("__init__:>>")

        # check input
        assert f_control
        assert f_model

        # initialize super class
        super(CViewVisil, self).__init__(f_control)

        # herdados de CViewManager
        # self.app           # the application
        # self.config        # config manager
        # self.dct_config    # dicionário de configuração
        # self.control       # control manager
        # self.event         # event manager
        # self.model         # model manager

        # save model manager
        self.model = f_model

        # show message
        self.control.splash.showMessage("loading colour table...", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.white)

        # color manager 
        self.__colors = clrm.CColorManager(self.config)
                
        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    # void (???)
    def notify(self, f_evt):
        """
        events callback

        @param f_evt: event
        """
        # logger
        # M_LOG.info("notify:>>")

        # check input
        assert f_evt

        # clock tick event ?
        if isinstance(f_evt, event.CTick):
            # M_LOG.debug("event.CTick")
            pass

        # quit event ?
        elif isinstance(f_evt, event.CQuit):
            # M_LOG.debug("event.CQuit")

            # para todos os processos
            # glb_data.G_KEEP_RUN = False
            pass

        # logger
        # M_LOG.info("notify:<<")

    # ---------------------------------------------------------------------------------------------
    # void (void)
    def run(self):
        """
        exec application
        """
        # logger
        # M_LOG.info("run:>>")

        # checks
        assert self.control
        assert self.app

        # create main window
        l_wmain = wmain.CWndMainVisil(self.control)
        assert l_wmain

        # show main window
        l_wmain.show()

        # dismiss splash screen
        self.control.splash.finish(l_wmain)

        # exec application
        self.app.exec_()

        # logger
        # M_LOG.info("run:<<")

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def colors(self):
        """
        get color manager
        """
        return self.__colors

# < the end >--------------------------------------------------------------------------------------
