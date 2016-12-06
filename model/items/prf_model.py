#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
prf_model

mantém os detalhes de uma família de performance

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

# < class CPrfModel >------------------------------------------------------------------------------

class CPrfModel(object):
    """
    mantém as informações específicas sobre performance
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        # flag ok (bool)
        self.__v_prf_ok = False

        # identificação da performance
        self.__s_prf_id = ""

        # descrição da performance
        self.__s_prf_desc = ""

    # ---------------------------------------------------------------------------------------------
    def copy_prf(self, f_prf):
        """
        copy constructor
        cria uma nova performance a partir de uma outra performance

        @param f_prf: performance a ser copiada
        """
        # check input
        assert f_prf

        # identificação da performance
        self.__s_prf_id = f_prf.s_prf_id

        # descrição da performance
        self.__s_prf_desc = f_prf.s_prf_desc

        # flag ok (bool)
        self.__v_prf_ok = f_prf.v_prf_ok

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def s_prf_desc(self):
        """
        get descrição
        """
        return self.__s_prf_desc.strip()

    @s_prf_desc.setter
    def s_prf_desc(self, f_val):
        """
        set descrição
        """
        self.__s_prf_desc = f_val.strip()

    # ---------------------------------------------------------------------------------------------
    @property
    def s_prf_id(self):
        """
        get ID
        """
        return self.__s_prf_id.strip()

    @s_prf_id.setter
    def s_prf_id(self, f_val):
        """
        set ID
        """
        self.__s_prf_id = f_val.strip().upper()

    # ---------------------------------------------------------------------------------------------
    @property
    def v_prf_ok(self):
        """
        get flag ok
        """
        return self.__v_prf_ok

    @v_prf_ok.setter
    def v_prf_ok(self, f_val):
        """
        set flag ok
        """
        self.__v_prf_ok = f_val

# < the end >--------------------------------------------------------------------------------------
