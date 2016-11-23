#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
exe_model

mantém as informações comuns sobre os exercícios

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
# import logging

# model
import model.glb_defs as gdefs

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CExeModel >------------------------------------------------------------------------------

class CExeModel(object):
    """
    mantém as informações comuns sobre os exercícios
    """
    # ---------------------------------------------------------------------------------------------
    # void (?)
    def __init__(self):

        # logger
        # M_LOG.info("__init__:>>")

        # flag ok (bool)
        self.__v_exe_ok = False

        # identificação
        self.__s_exe_id = ""

        # descrição
        self.__s_exe_desc = ""

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    # void (?)
    def copy_exe(self, f_exe):
        """
        copy constructor
        cria um novo exercício a partir de um outro exercício

        @param f_exe: exercício a ser copiado

        @return flag e mensagem
        """
        # logger
        # M_LOG.info("copy_exe:>>")

        # identificação
        self.__s_exe_id = f_exe.s_exe_id

        # descrição
        self.__s_exe_desc = f_exe.s_exe_desc

        # flag ok (bool)
        self.__v_exe_ok = f_exe.v_exe_ok

        # logger
        # M_LOG.info("copy_exe:<<")

    # ---------------------------------------------------------------------------------------------
    # void (?)
    def send_exe(self, f_sender):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("send_exe:>>")

        # envia os dados de configuração
        f_sender.send_data(str(gdefs.D_MSG_VRS) + gdefs.D_MSG_SEP +
                           str(gdefs.D_MSG_EXE) + gdefs.D_MSG_SEP + self.__s_exe_id)

        # logger
        # M_LOG.info("send_exe:<<")

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def s_exe_desc(self):
        """
        get descrição do exercício
        """
        # return self.__s_exe_desc.decode("utf-8")
        return self.__s_exe_desc

    @s_exe_desc.setter
    def s_exe_desc(self, f_val):
        """
        set descrição do exercício
        """
        self.__s_exe_desc = f_val.strip()  # encode("utf-8").strip()

    # ---------------------------------------------------------------------------------------------
    @property
    def s_exe_id(self):
        """
        get ID do exercício
        """
        # return self.__s_exe_id.decode("utf-8")
        return self.__s_exe_id

    @s_exe_id.setter
    def s_exe_id(self, f_val):
        """
        set ID do exercício
        """
        self.__s_exe_id = f_val.strip().upper()  # encode("utf-8").strip().upper()

    # ---------------------------------------------------------------------------------------------
    @property
    def v_exe_ok(self):
        """
        get flag ok
        """
        return self.__v_exe_ok

    @v_exe_ok.setter
    def v_exe_ok(self, f_val):
        """
        set flag ok
        """
        self.__v_exe_ok = f_val

# < the end >--------------------------------------------------------------------------------------
