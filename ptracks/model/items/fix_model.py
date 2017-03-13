#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
fix_model

mantém os detalhes de um fixo

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

# model
import ptracks.model.newton.defs_newton as ldefs

# < class CFixModel >------------------------------------------------------------------------------

class CFixModel(object):
    """
    mantém as informações específicas sobre fixo
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        # flag ok (bool)
        self.__v_fix_ok = False

        # identificação do fixo
        self.__i_fix_id = -1
        # indicativo do fixo
        self.__s_fix_indc = ""
        # descriçao do fixo
        self.__s_fix_desc = ""

        # tipo do fixo (VOR, NDB, DME ou " ")
        self.__en_fix_tipo = ldefs.E_BRANCO

        # X
        self.__f_fix_x = 0.
        # Y
        self.__f_fix_y = 0.
        # Z
        self.__f_fix_z = 0.

    # ---------------------------------------------------------------------------------------------
    def copy_fix(self, f_fix):
        """
        copy constructor. Copia para este fixo os dados de um outro fixo

        @param f_fix: fixo a ser copiado
        """
        # check input
        assert f_fix

        # identificação do fixo
        self.__i_fix_id = f_fix.i_fix_id
        # indicativo do fixo
        self.__s_fix_indc = f_fix.s_fix_indc
        # descrição do fixo
        self.__s_fix_desc = f_fix.s_fix_desc
        # tipo do fixo
        self.__en_fix_tipo = f_fix.en_fix_tipo

        # X
        self.__f_fix_x = f_fix.f_fix_x
        # Y
        self.__f_fix_y = f_fix.f_fix_y
        # Z
        self.__f_fix_z = f_fix.f_fix_z

        # flag ok (bool)
        self.__v_fix_ok = f_fix.v_fix_ok

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def s_fix_desc(self):
        """
        get descrição
        """
        return self.__s_fix_desc

    @s_fix_desc.setter
    def s_fix_desc(self, f_val):
        """
        set descrição
        """
        self.__s_fix_desc = f_val.strip()
        
    # ---------------------------------------------------------------------------------------------
    @property
    def v_fix_dme(self):
        """
        get flag DME
        """
        return ldefs.E_DME == self.__en_fix_tipo

    # ---------------------------------------------------------------------------------------------
    @property
    def i_fix_id(self):
        """
        get ID
        """
        return self.__i_fix_id

    @i_fix_id.setter
    def i_fix_id(self, f_val):
        """
        set ID
        """
        self.__i_fix_id = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def s_fix_indc(self):
        """
        get indicativo
        """
        return self.__s_fix_indc

    @s_fix_indc.setter
    def s_fix_indc(self, f_val):
        """
        set indicativo
        """
        self.__s_fix_indc = f_val.strip()

    # ---------------------------------------------------------------------------------------------
    @property
    def v_fix_ndb(self):
        """
        get flag NDB
        """
        return ldefs.E_NDB == self.__en_fix_tipo

    # ---------------------------------------------------------------------------------------------
    @property
    def v_fix_ok(self):
        """
        get flag Ok
        """
        return self.__v_fix_ok

    @v_fix_ok.setter
    def v_fix_ok(self, f_val):
        """
        set flag Ok
        """
        self.__v_fix_ok = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def en_fix_tipo(self):
        """
        get tipo de fixo
        """
        return self.__en_fix_tipo

    @en_fix_tipo.setter
    def en_fix_tipo(self, f_val):
        """
        set tipo de fixo
        """
        # check input
        assert f_val in ldefs.SET_TIPOS_FIXOS

        # salva tipo de fixo
        self.__en_fix_tipo = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def v_fix_vor(self):
        """
        get flag VOR
        """
        return ldefs.E_VOR == self.__en_fix_tipo

    # ---------------------------------------------------------------------------------------------
    @property
    def f_fix_x(self):
        """
        get X
        """
        return self.__f_fix_x

    @f_fix_x.setter
    def f_fix_x(self, f_val):
        """
        set X
        """
        self.__f_fix_x = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_fix_y(self):
        """
        get Y
        """
        return self.__f_fix_y

    @f_fix_y.setter
    def f_fix_y(self, f_val):
        """
        set Y
        """
        self.__f_fix_y = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_fix_z(self):
        """
        get Z
        """
        return self.__f_fix_z

    @f_fix_z.setter
    def f_fix_z(self, f_val):
        """
        set Z
        """
        self.__f_fix_z = f_val

# < the end >--------------------------------------------------------------------------------------
