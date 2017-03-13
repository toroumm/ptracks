#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
pst_model

mantém os detalhes de um pista

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

# < class CPstModel >------------------------------------------------------------------------------

class CPstModel(object):
    """
    mantém as informações específicas sobre pista
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        # flag ok (bool)
        self.__v_pst_ok = False
        # identificação do pista (indicativo)
        self.__s_pst_indc = ""

        # proa em relação ao norte magnético
        self.__f_pst_rumo = 0.
                
        # proa em relação ao norte verdadeiro
        self.__f_pst_true = 0.

        # X (m)
        self.__f_pst_x = 0.
        # Y (m)
        self.__f_pst_y = 0.
        # Z (m)
        self.__f_pst_z = 0.

    # ---------------------------------------------------------------------------------------------
    def copy_pst(self, f_pst):
        """
        copy constructor
        cria uma nova pista a partir de uma outra pista

        @param f_pst: pista a ser copiada
        """
        # check input
        assert f_pst

        # identificação da pista
        self.__s_pst_indc = f_pst.s_pst_indc
        # rumo magnético
        self.__f_pst_rumo = f_pst.f_pst_rumo
        # rumo verdadeiro
        self.__f_pst_true = f_pst.f_pst_true

        # X
        self.__f_pst_x = f_pst.f_pst_x
        # Y
        self.__f_pst_y = f_pst.f_pst_y
        # Z
        self.__f_pst_z = f_pst.f_pst_z

        # flag ok (bool)
        self.__v_pst_ok = f_pst.v_pst_ok

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def s_pst_indc(self):
        """
        get identificação da pista (indicativo)
        """
        return self.__s_pst_indc

    @s_pst_indc.setter
    def s_pst_indc(self, f_val):
        """
        set identificação da pista (indicativo)
        """
        self.__s_pst_indc = f_val.strip().upper()

    # ---------------------------------------------------------------------------------------------
    @property
    def v_pst_ok(self):
        """
        get flag pista ok
        """
        return self.__v_pst_ok

    @v_pst_ok.setter
    def v_pst_ok(self, f_val):
        """
        set flag pista ok
        """
        self.__v_pst_ok = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_pst_rumo(self):
        """
        get rumo magnético da pista
        """
        return self.__f_pst_rumo

    @f_pst_rumo.setter
    def f_pst_rumo(self, f_val):
        """
        set rumo magnético da pista
        """
        self.__f_pst_rumo = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_pst_true(self):
        """
        get rumo verdadeiro da pista
        """
        return self.__f_pst_true

    @f_pst_true.setter
    def f_pst_true(self, f_val):
        """
        set rumo verdadeiro da pista
        """
        self.__f_pst_true = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_pst_x(self):
        """
        get X
        """
        return self.__f_pst_x

    @f_pst_x.setter
    def f_pst_x(self, f_val):
        """
        set X
        """
        self.__f_pst_x = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_pst_y(self):
        """
        get Y
        """
        return self.__f_pst_y

    @f_pst_y.setter
    def f_pst_y(self, f_val):
        """
        set Y
        """
        self.__f_pst_y = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_pst_z(self):
        """
        get Z
        """
        return self.__f_pst_z

    @f_pst_z.setter
    def f_pst_z(self, f_val):
        """
        set Z
        """
        self.__f_pst_z = f_val

# < the end >--------------------------------------------------------------------------------------
