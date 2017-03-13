#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
generate_prf_json

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

# < imports >--------------------------------------------------------------------------------------

# python library
import json
import logging

# libs
import ptracks.libs.coords.coord_defs as cdefs

# ------------------------------------------------------------------------------------------------
def generate_prf_json(fdct_prf, fs_prf):
    """
    DOCUMENT ME!
    """
    # performance existe no dicionário ?
    l_prf = fdct_prf.get(fs_prf, None)

    if l_prf is None:
        # logger
        l_log = logging.getLogger("generate_prf_json")
        l_log.setLevel(logging.ERROR)
        l_log.error(u"<E01: performance {} não existe no dicionário.".format(fs_prf))
                                                
        # return
        return None

    # monta um dicionário com a performance
    ldct_prf = { "teto_sv": int(l_prf.f_prf_teto_sv * cdefs.D_CNV_M2FT),                      # (m -> ft)
                 "vel_max_crz": int(l_prf.f_prf_vel_max_crz * cdefs.D_CNV_MS2KT),             # (m/s -> kt)
                 "raz_max_sub_crz": int(l_prf.f_prf_raz_max_sub_crz * cdefs.D_CNV_MS2FTMIN),  # (m/s -> ft/min)
                 "raz_max_des_crz": int(l_prf.f_prf_raz_max_des_crz * cdefs.D_CNV_MS2FTMIN),  # (m/s -> ft/min)
                 "raz_crv_rot": round(l_prf.f_prf_raz_crv_rot, 1),
               }
 
    # return
    return json.dumps(ldct_prf)

# < the end >--------------------------------------------------------------------------------------
