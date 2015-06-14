# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time
from model.dbsearch import LogicSearch, DataSearch, TranslateSearch, EventSearch, AlarmSearch
from model.eventAlarm import EventAlarm

class searchOfevent:
    
    def __init__(self):
        
        self.returns = ""
        
    def searchOID(self, OID):
        
        searchResult = AlarmSearch().searchinAlarm(OID)
        
        return searchResult
       
        