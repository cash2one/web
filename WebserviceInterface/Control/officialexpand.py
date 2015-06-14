# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys

from Expand import ExpandStep
from model.cmdbsearch import BasicSearch
from BaseClass.urlexplain import urlExplain

class OfficialExpand(ExpandStep):
    
    def __init__(self):
        
        self.returns = ""
        
    def Part_counter(self):
        
        allcount = 0
        count = 0
        
        getResultofcountersearch = BasicSearch().counterSearch()
        if getResultofcountersearch['Status'] != 'Success':
            return getResultofcountersearch
        
        allcount = len(getResultofcountersearch['counterlist'])
        
        for eachline in getResultofcountersearch['counterlist']:
            newurl = 'http://'+eachline+'/ref.php?ref=tttttt'
            getReturns = urlExplain().urlcheckcode(newurl)
            if getReturns['Status'] == 'Success':
                count += 1
        
        if count == allcount:
            return dict(Status='Success')
        elif count < allcount:
            return dict(Status='Warning', count=count)
        elif count == 0:
            return dict(Status='False')
            