#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
wizard_page_model.
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
# import logging

# PyQt library
from PyQt4 import QtGui

# < module data >----------------------------------------------------------------------------------

# logging level
# M_LOG_LVL = logging.DEBUG

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(M_LOG_LVL)

# < class CWizardPageModel >-----------------------------------------------------------------------


class CWizardPageModel(QtGui.QWidget):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, fdlg_wizard=None):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__init__:>>")

        # inicia a super classe
        super(CWizardPageModel, self).__init__(fdlg_wizard)

        # salva a 'dialog wizard' localmente
        self.__dlg_wizard = fdlg_wizard

        # dicionário de configuração
        self.__dct_config = {}

        # oculta a página
        self.hide()

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def is_complete(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("is_complete:><")

        # return
        return True

    # ---------------------------------------------------------------------------------------------

    def is_last_page(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("is_last_page:><")

        # return
        return False

    # ---------------------------------------------------------------------------------------------

    def next_page(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("next_page:><")

        # return
        return None

    # ---------------------------------------------------------------------------------------------

    def reset_page(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("reset_page:><")

        # return
        return

    # ---------------------------------------------------------------------------------------------

    @property
    def dct_config(self):
        """
        get dicionário de configuração
        """
        return self.__dct_config

    @dct_config.setter
    def dct_config(self, f_val):
        """
        set dicionário de configuração
        """
        # verifica parâmetros de entrada
        assert f_val

        # dicionário de configuração
        self.__dct_config = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def dlg_wizard(self):
        """
        get dialog wizard
        """
        return self.__dlg_wizard

    @dlg_wizard.setter
    def dlg_wizard(self, f_val):
        """
        set dialog wizard
        """
        # verifica parâmetros de entrada
        assert f_val

        # save dialog wizard
        self.__dlg_wizard = f_val

# < the end >--------------------------------------------------------------------------------------
