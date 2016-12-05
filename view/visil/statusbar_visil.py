#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
statusbar_visil

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

# view
import view.common.statusbar_basic as sbb

# < class CStatusBarVisil >------------------------------------------------------------------------

class CStatusBarVisil(sbb.CStatusBarBasic):
    """
    used to display the Current Working Position, the Independant/Dependant mode, radar and weather
    services used, filters and coordinates of the mouse pointer on the status bar of a radar window
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_parent=None):
        """
        constructor
        """
        # check input
        assert f_parent

        # init super class
        super(CStatusBarVisil, self).__init__(f_parent)

    # =============================================================================================
    # dados
    # =============================================================================================

# < the end >--------------------------------------------------------------------------------------
