# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time
import pdb

from model import DBSession
from model.dbsearch import EventTransportExpand, EventSearch, CircultSearch,\
    EventTransportSearch
from model.physicalAsset import Ethdetail, EthInfo
from model.assetforagent import AssetForAgent, AssetidtoEid

from BaseClass.verifityDependence import changeDict
from BaseClass.timeBasic import TimeBasic
from ServiceConfig.config import readFromConfigFile
from interface.collection.dbconnect import Connect

class Repeat:
    
    def __init__(self):
        
        self.returns = ""
        
    def searchindatabase(self, message):
        
        #{'Info': 'None', 'Status': 'Success', 'OID': '5.1', 'JobID': 0, 'Result': "{u'57': u'-1'}", 'Type': 'main', 'ID': '0', 'SendTime': '1390893937'}
        getSearchResult = EventSearch().SearchoidRepeat(message['Mbody'], message['Oid'], message['Timestamp'])
        
        return getSearchResult
