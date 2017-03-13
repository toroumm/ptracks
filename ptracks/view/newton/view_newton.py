#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
view_newton

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
__date__ = "2015/12"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import threading
import time

import SocketServer

# model
import ptracks.model.common.glb_data as gdata

# view
import ptracks.view.visweb.view_handler as vhnd

# < class CViewNewton >----------------------------------------------------------------------------

class CViewNewton(threading.Thread):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_model, f_control):
        """
        init newton view

        @param f_model: model
        @param f_control: control
        """
        # check input
        assert f_model
        assert f_control
                
        # init super class
        super(CViewNewton, self).__init__()

        # model
        self.__model = f_model

        # control
        self.__control = f_control

        # obtém o MPI rank
        self.__mpi_rank = f_control.mpi_rank
        assert self.__mpi_rank > -1
                                                
        # obtém o dicionário de configuração
        ldct_config = f_control.config.dct_config
        assert ldct_config is not None

        # configura a porta do servidor
        self.__i_port = int(ldct_config["srv.port"]) + self.__mpi_rank

    # ---------------------------------------------------------------------------------------------
    def run(self):
        """
        thread that runs the web server
        """
        # wait loop
        while not gdata.G_KEEP_RUN:
            # wait...
            time.sleep(1)

        try:
            # allow address reuse (avoid '[Errno 98] Address already in use')
            SocketServer.TCPServer.allow_reuse_address = True
            
            # create a web server and define the handler to manage the incoming request
            l_server = CViewServer(self.__model, self.__control, ('', self.__i_port), vhnd.CViewHandler)
            assert l_server

            # logger
            l_log = logging.getLogger("CViewNewton::run")
            l_log.setLevel(logging.INFO)
            l_log.info(u"<E01: started http server on port {}.".format(self.__i_port))

            # wait forever for incoming http requests
            l_server.serve_forever()

        # em caso de erro...
        except KeyboardInterrupt:
            # logger
            l_log = logging.getLogger("CViewNewton::run")
            l_log.setLevel(logging.WARNING)
            l_log.warning(u"<E02: ^C received, shutting down the web server.")

            # close socket
            l_server.socket.close()

        # server loop
        while gdata.G_KEEP_RUN:
            # generate aircraft JSON
            time.sleep(.5)

# < class CViewServer >----------------------------------------------------------------------------

class CViewServer(SocketServer.TCPServer):
    
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_model, f_control, f_server_address, f_handler_class=vhnd.CViewHandler):
        """
        init newton web server

        @param f_control: control manager
        """
        # check input
        assert f_model
        assert f_control
                
        # init super class
        SocketServer.TCPServer.__init__(self, f_server_address, f_handler_class)

        # save control manager
        self.__control = f_control

        # save model manager
        self.__model = f_model

        # dicionário de performances
        self.__dct_prf = f_model.dct_prf
        assert self.__dct_prf is not None                

    # ---------------------------------------------------------------------------------------------
    @property
    def control(self):
        """
        get control manager
        """
        return self.__control 
                                            
    # ---------------------------------------------------------------------------------------------
    @property
    def coords(self):
        """
        get coord system
        """
        return self.__model.coords
                                            
    # ---------------------------------------------------------------------------------------------
    @property
    def emula(self):
        """
        get emulation model
        """
        return self.__model.emula
                                            
    # ---------------------------------------------------------------------------------------------
    @property
    def model(self):
        """
        get model manager
        """
        return self.__model 
                                            
    # ---------------------------------------------------------------------------------------------
    @property
    def dct_flight(self):
        """
        get dicionário de flight engines
        """
        return self.__model.emula.dct_flight 
                                            
    # ---------------------------------------------------------------------------------------------
    @property
    def dct_prf(self):
        """
        get dicionário de performances
        """
        return self.__dct_prf 
                                            
# < the end >--------------------------------------------------------------------------------------
