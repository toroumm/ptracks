#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
generate_status_json

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
__date__ = "2016/04"

# < imports >--------------------------------------------------------------------------------------

# python library
import json
import logging
import time

# model
import model.newton.defs_newton as ldefs

# ------------------------------------------------------------------------------------------------
def generate_status_json(fdct_flight, fs_callsign):
    """
    DOCUMENT ME!

    @param fdct_flight: dicionário de flight engines
    @param fs_callsign: aircraft callsign
    """
    # check input
    assert fdct_flight is not None
    assert fs_callsign

    # aeronave existe ?
    l_anv = fdct_flight.get(fs_callsign, None)

    if l_anv is None:
        # logger
        l_log = logging.getLogger("generate_status_json")
        l_log.setLevel(logging.ERROR)
        l_log.error(u"<E01: aeronave {} não existe.".format(fs_callsign))
                                                
        # return
        return None

    # procedimento
    li_prc_id = 0

    # em procedimento ?
    if l_anv.ptr_trf_prc is not None:
        # procedimento
        li_prc_id = l_anv.ptr_trf_prc.i_prc_id

    # monta um dicionário com o status
    ldct_status = { "fnc_ope": ldefs.DCT_FNC_OPE[l_anv.en_trf_fnc_ope],
                    "prc_id": li_prc_id,
                  }

    # return
    return json.dumps(ldct_status)

# < the end >--------------------------------------------------------------------------------------
