#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
aer_model

mantém os detalhes de um aeródromo

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

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CAerModel >------------------------------------------------------------------------------

class CAerModel(object):
    """
    mantém as informações específicas sobre aeródromo
    """
    # ---------------------------------------------------------------------------------------------
    # void (void)
    def __init__(self):

        # logger
        # M_LOG.info("__init__:>>")

        # flag ok (bool)
        self.__v_aer_ok = False

        # identificação do aeródromo (indicativo)
        self.__s_aer_indc = ""

        # descrição do aeródromo (nome)
        self.__s_aer_desc = ""

        # elevação do aeródromo (m)
        self.__f_aer_elev = 0

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    # void (?)
    def copy_aer(self, f_aer):
        """
        copy constructor
        cria um novo aeródromo a partir de um outro aeródromo

        @param f_aer: aeródromo a ser copiado
        """
        # logger
        # M_LOG.info("copy_aer:>>")

        # check input
        assert f_aer

        # identificação do aeródromo
        self.__s_aer_indc = f_aer.s_aer_indc

        # descrição do aeródromo
        self.__s_aer_desc = f_aer.s_aer_desc

        # elevação (m)
        self.__f_aer_elev = f_aer.f_aer_elev

        # flag ok (bool)
        self.__v_aer_ok = f_aer.v_aer_ok

        # logger
        # M_LOG.info("copy_aer:<<")

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def f_aer_elev(self):
        """
        get elevação
        """
        return self.__f_aer_elev

    @f_aer_elev.setter
    def f_aer_elev(self, f_val):
        """
        set elevação
        """
        self.__f_aer_elev = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def s_aer_indc(self):
        """
        get identificação do aeródromo (indicativo)
        """
        return self.__s_aer_indc  # .decode ( "utf-8" )

    @s_aer_indc.setter
    def s_aer_indc(self, f_val):
        """
        set identificação do aeródromo (indicativo)
        """
        self.__s_aer_indc = f_val.strip().upper()  # .encode ( "utf-8" )

    # ---------------------------------------------------------------------------------------------
    @property
    def s_aer_desc(self):
        """
        get descrição
        """
        return self.__s_aer_desc  # .decode ( "utf-8" )

    @s_aer_desc.setter
    def s_aer_desc(self, f_val):
        """
        set descrição
        """
        self.__s_aer_desc = f_val.strip()  # .encode ( "utf-8" )

    # ---------------------------------------------------------------------------------------------
    @property
    def v_aer_ok(self):
        """
        get flag ok
        """
        return self.__v_aer_ok

    @v_aer_ok.setter
    def v_aer_ok(self, f_val):
        """
        set flag ok
        """
        self.__v_aer_ok = f_val

# < the end >--------------------------------------------------------------------------------------
