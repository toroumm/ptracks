#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------------------------
control_debug

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

revision 0.2  2016/oct  mlabru
pep8 style conventions

revision 0.1  2015/nov  mlabru
initial version (Linux/Python)
-------------------------------------------------------------------------------------------------- 
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2016/10"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < the end >--------------------------------------------------------------------------------------
