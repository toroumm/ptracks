#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
prc_model

mantém os detalhes de um procedimento

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
__date__ = "2016/04"

# < class CPrcModel >------------------------------------------------------------------------------

class CPrcModel(object):
    """
    mantém as informações específicas sobre procedimento
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        # flag ok (bool)
        self.__v_prc_ok = False

        # identificação do procedimento
        self.__i_prc_id = 0

        # descrição do procedimento
        self.__s_prc_desc = ""

    # ---------------------------------------------------------------------------------------------
    def copy_prc(self, f_prc):
        """
        copy constructor
        cria um novo procedimento a partir de outro procedimento

        @param f_prc: procedimento a ser copiado
        """
        # check input
        assert f_prc

        # identificação do procedimento
        self.i_prc_id = f_prc.i_prc_id

        # descrição do procedimento
        self.s_prc_desc = f_prc.s_prc_desc

        # flag ok (bool)
        self.v_prc_ok = f_prc.v_prc_ok

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def s_prc_desc(self):
        """
        get descrição
        """
        return self.__s_prc_desc  # .decode ( "utf-8" )

    @s_prc_desc.setter
    def s_prc_desc(self, f_val):
        """
        set descrição
        """
        self.__s_prc_desc = f_val.strip()  # .encode ( "utf-8" )

    # ---------------------------------------------------------------------------------------------
    @property
    def i_prc_id(self):
        """
        get identificação do procedimento (indicativo)
        """
        return self.__i_prc_id

    @i_prc_id.setter
    def i_prc_id(self, f_val):
        """
        set identificação do procedimento (indicativo)
        """
        self.__i_prc_id = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def v_prc_ok(self):
        """
        get flag ok
        """
        return self.__v_prc_ok

    @v_prc_ok.setter
    def v_prc_ok(self, f_val):
        """
        set flag ok
        """
        self.__v_prc_ok = f_val

# < the end >--------------------------------------------------------------------------------------
