#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
holding

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

revision 0.2  2015/dez  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2016/01"

# < class CHolding >----------------------------------------------------------------------------

class CHolding(object):

    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_fixo=None, ff_entrada=None, fc_dir=None):
        """
        constructor
        """
        # check input
        assert fc_dir in ['l', 'r']

        self._sWaypoint = fs_fixo

        self._fInbound = ff_entrada

        # sentido da espera 
        self._cDirection = fc_dir

# < the end >--------------------------------------------------------------------------------------
