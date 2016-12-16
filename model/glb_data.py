#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
glb_data

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
__date__ = "2015/11"

# < global data >----------------------------------------------------------------------------------

# canal de comunicação
G_CANAL = 4

# trava da lista de vôos
G_LCK_FLIGHT = None

# keep things running
G_KEEP_RUN = False

# map limits
G_MIN_LAT = 91.
G_MAX_LAT = -91.

G_MIN_LNG = 181.
G_MAX_LNG = -181.

# colour dictionary
G_DCT_COLORS = {}

# < the end >--------------------------------------------------------------------------------------
