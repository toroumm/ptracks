#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
landscape_visil

DOCUMENT ME!

revision 0.2  2015/dez  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "mlabru, sophosoft"
__date__ = "2016/01"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import os
import sys

# PyQt4 library
from PyQt4 import QtCore
from PyQt4 import QtXml

# model
import model.coords.pos_lat_lng as pll

import model.stock.landscape_basic as land
import model.stock.fix as cfix

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < class CLandscapeVisil >------------------------------------------------------------------------

class CLandscapeVisil(land.CLandscapeBasic):
    """
    represent an landscape
    """
    # ---------------------------------------------------------------------------------------------
    # void (???)
    def __init__(self, f_model, fs_dir, fs_location):
        """
        read datafile for specified location (airport)
        """
        # logger
        # M_LOG.info("__init__:>>")

        # check input
        assert f_model
        assert fs_dir
        assert fs_location

        # init super class
        super(CLandscapeVisil, self).__init__(f_model)

        # herdados de CLandscapeBase
        # self.config         # config manager
        # self.dct_config     # dicionário de configuração
        # self.event          # event manager
        # self.model          # model manager
        # self.dct_aer        # dicionário de aeródromos
        # self.dct_fix        # dicionário de fixos
        # self.dct_fix_indc   # dicionário de indicativos

        # dicionários locais
        self.__dct_dme = {}
        self.__dct_ndb = {}
        self.__dct_vor = {}
        self.__dct_wpt = {}

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    # void (???)
    def dme(self, fi_ndx):
        """
        return a pointer to the DME with specified index
        """
        # logger
        # M_LOG.info("dme:><")

        # check input
        # assert f_model

        if fi_ndx >= len(self.__dct_dme):
            return None

        # return
        return self.__dct_dme[fi_ndx]

    # ---------------------------------------------------------------------------------------------
    # void (???)
    def getPosition(self, fs_indc):
        """
        get position of a waypoint/vor/ndb/... named as specified
        """
        # logger
        # M_LOG.info("getPosition:>>")

        # check input
        # assert f_model

        # pesquisa aeródromos
        l_aer = self.dct_aer.get(fs_indc, None)
        M_LOG.debug("getPosition:aer:[{}]".format(l_aer))

        if l_aer is not None:

            M_LOG.debug("getPosition:aer:[{}]/[{}]".format(l_aer.f_aer_lat, l_aer.f_aer_lng))

            # logger
            # M_LOG.info("getPosition:<E01")

            # return
            return pll.CPosLatLng(l_aer.f_aer_lat, l_aer.f_aer_lng)

        # pesquisa fixos
        l_key = self.dct_fix_indc.get(fs_indc, None)

        if l_key is not None:

            # acessa o fixo pela key
            l_fix = self.dct_fix[l_key]
            assert l_fix

            # logger
            # M_LOG.info("getPosition:<E02")

            # return
            return pll.CPosLatLng(l_fix.f_fix_lat, l_fix.f_fix_lng)

        # logger
        # M_LOG.info("getPosition:<<")

        # return
        return None

    # ---------------------------------------------------------------------------------------------
    # void (???)
    def load_dicts(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("load_dicts:>>")

        # pathname of holding procedures table
        # ls_path = os.path.join(self.dct_config["dir.prc"], self.dct_config["tab.esp"])

        # load holding procedures table in dictionary
        # self.__dct_esp = espdata.CEspData(self.model, ls_path)
        # assert self.__dct_esp is not None

        # logger
        # M_LOG.info("load_dicts:<<")

    # ---------------------------------------------------------------------------------------------
    # void (???)
    def load_xml(self, fs_filename):
        """
        load xml landscape file
        """
        # logger
        # M_LOG.info("load_xml:>>")

        # check input
        # assert f_model

        # read coordinates
        ls_filename = ":/data/" + fs_filename + ".xml"
        M_LOG.debug("ls_filename: " + str(ls_filename))

        l_data_file = QtCore.QFile(ls_filename)
        assert l_data_file is not None

        l_data_file.open(QtCore.QIODevice.ReadOnly)

        if not l_data_file.isOpen():
            # logger
            l_log = logging.getLogger("landscape::load_xml")
            l_log.setLevel(logging.NOTSET)
            l_log.fatal("<E01: failed to open {}".format(ls_filename))

            # abend
            sys.exit(1)

        l_xml_doc = QtXml.QDomDocument("landscape")
        assert l_xml_doc is not None

        if not l_xml_doc.setContent(l_data_file):
            l_data_file.close()

            # logger
            l_log = logging.getLogger("landscape::load_xml")
            l_log.setLevel(logging.NOTSET)
            l_log.fatal("<E02: failed to parse {}".format(ls_filename))

            # abend
            sys.exit(1)

        l_data_file.close()

        l_doc_elem = l_xml_doc.documentElement()
        assert l_doc_elem is not None

        self.__f_variation, lv_ok = l_doc_elem.attribute(QtCore.QString("variation"), QtCore.QString("0")).toDouble()
        self.__f_elevation, lv_ok = l_doc_elem.attribute(QtCore.QString("elevation"), QtCore.QString("0")).toDouble()

        l_node = l_doc_elem.firstChild()
        assert l_node is not None

        while not l_node.isNull():
            l_element = l_node.toElement()
            assert l_element is not None

            if not l_element.isNull():
                self.__parse_dom_element(l_element)

            l_node = l_node.nextSibling()
            assert l_node is not None

        # logger
        # M_LOG.info("load_xml:<<")

    # ---------------------------------------------------------------------------------------------
    # void (???)
    def ndb(self, fi_ndx):
        """
        return a pointer to the NDB with specified index
        """
        # logger
        # M_LOG.info("ndb:><")

        # check input
        # assert f_model

        if fi_ndx >= len(self.__dct_ndb):
            return None

        # return
        return self.__dct_ndb[fi_ndx]

    # ---------------------------------------------------------------------------------------------
    # void (???)
    def __parse_dom_element(self, f_element):
        """
        helper function to the constructor, parses xml entries
        """
        # logger
        # M_LOG.info("__parse_dom_element:>>")

        # check input
        # assert f_model

        lv_ok = False

        lf_lat = 0
        lf_lng = 0

        ls_indc = f_element.text().toLocal8Bit().data()  # constData ()
        # M_LOG.info("ls_indc: %s" % ls_indc)

        # read coordinates if available
        if f_element.hasAttribute(QtCore.QString("longitude")) and \
           f_element.hasAttribute(QtCore.QString("latitude")):
            lf_lat, lv_ok = f_element.attribute(QtCore.QString("latitude"), QtCore.QString("0")).toDouble()
            lf_lng, lv_ok = f_element.attribute(QtCore.QString("longitude"), QtCore.QString("0")).toDouble()

        # handle case of ARP
        if f_element.tagName() == QtCore.QString("ARP"):
            self.__arp = cfix.CFix(ls_indc, lf_lat, lf_lng)
            assert self.__arp

        # handle case of VOR
        elif f_element.tagName() == QtCore.QString("VOR"):
            l_fix = cfix.CFix(ls_indc, lf_lat, lf_lng)
            assert l_fix

            self.__dct_vor.append(l_fix)

        # handle case of DME
        elif f_element.tagName() == QtCore.QString("DME"):
            l_fix = cfix.CFix(ls_indc, lf_lat, lf_lng)
            assert l_fix

            self.__dct_dme.append(l_fix)

        # handle case of NDB
        elif f_element.tagName() == QtCore.QString("NDB"):
            l_fix = cfix.CFix(ls_indc, lf_lat, lf_lng)
            assert l_fix

            self.__dct_ndb.append(l_fix)

        # handle case of WPT
        elif f_element.tagName() == QtCore.QString("WPT"):
            l_fix = cfix.CFix(ls_indc, lf_lat, lf_lng)
            assert l_fix

            self.__dct_wpt.append(l_fix)

        # logger
        # M_LOG.info("__parse_dom_element:<<")

    # ---------------------------------------------------------------------------------------------
    # void (???)
    def vor(self, fi_ndx):
        """
        return a pointer to the VOR with specified index
        """
        # logger
        # M_LOG.info("vor:><")

        # check input
        # assert f_model

        if fi_ndx >= len(self.__dct_vor):
            return None

        # return
        return self.__dct_vor[fi_ndx]

    # ---------------------------------------------------------------------------------------------
    # void (???)
    def waypoint(self, fi_ndx):
        """
        return a pointer to the waypoint with specified index
        """
        # logger
        # M_LOG.info("waypoint:><")

        # check input
        # assert f_model

        if fi_ndx >= len(self.__dct_wpt):
            return None

        # return
        return self.__dct_wpt[fi_ndx]

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def airport(self):
        """
        pointer to the aerodrome reference point
        """
        return self.__arp

    # ---------------------------------------------------------------------------------------------
    @property
    def f_elevation(self):
        """
        get aerodrome elevation
        """
        return self.__f_elevation
                                            
    # @f_elevation.setter
    # def f_elevation(self, f_val):
        # """
        # set aerodrome elevation
        # """
        # self.__f_elevation = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_variation(self):
        """
        get magnetic variation
        """
        return self.__f_variation
                                            
    # @f_variation.setter
    # def f_variation(self, f_val):
        # """
        # set magnetic variation
        # """
        # self.__f_variation = f_val

# < the end >--------------------------------------------------------------------------------------
