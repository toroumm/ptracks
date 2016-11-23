#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
model manager

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

revision 0.4  2016/ago  mlabru
pequenas correções e otimização

revision 0.3  2015/nov  mlabru
pep8 style conventions

revision 0.2  2014/nov  mlabru
inclusão do event manager e config manager

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.4$"
__author__ = "Milton Abrunhosa"
__date__ = "2016/08"

# < imports >--------------------------------------------------------------------------------------

# python library
# import logging

# control
import control.events.events_manager as event
import control.config.config_manager as config

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CModelManager >--------------------------------------------------------------------------

class CModelManager(object):
    """
    main model object. Views and controllers interact with this
    """
    # ---------------------------------------------------------------------------------------------
    # void (obj)
    def __init__(self, f_control):
        """
        initializes the model manager

        @param f_control: control manager
        """
        # logger
        # M_LOG.info("__init__:>>")

        # check input
        assert f_control

        # the application
        self.__app = f_control.app

        # control manager
        self.__control = f_control

        # config manager
        self.__config = f_control.config if f_control.config is not None else config.CConfigManager()
        assert self.__config

        # event manager
        self.__event = f_control.event if f_control.event is not None else event.CEventsManager()
        assert self.__event

        # registra como recebedor de eventos
        self.__event.register_listener(self)

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    # @ abstractmethod
    def notify(self, f_event):
        """
        callback de tratamento de eventos recebidos

        @param f_event: evento recebido
        """
        # logger
        # M_LOG.info("notify:><")

        # return
        pass

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def app(self):
        """
        get the application
        """
        return self.__app

    # ---------------------------------------------------------------------------------------------
    @property
    def config(self):
        """
        get config manager
        """
        return self.__config

    # ---------------------------------------------------------------------------------------------
    @property
    def control(self):
        """
        get control manager
        """
        return self.__control

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_config(self):
        """
        get configuration dictionary
        """
        return self.__config.dct_config if self.__config is not None else {}

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
        get event manager
        """
        self.__event = f_val

# < the end >--------------------------------------------------------------------------------------
