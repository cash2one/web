# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time

from fastregExpand import FastregExpand
from model.cmdbsearch import BasicSearch

class FastRegofPlatform:
    
    def __init__(self):
        
        self.returns = ""
        
    def testPlatformFastReg(self, type):
        
        getdnsipdict = {}
        
        # test of fastreg
        if type == 'testreg':
            
            ''' Step 1. get testreg url. '''
            geturlreturn = BasicSearch().searchunifiedurl(type)
            if geturlreturn['Status'] != 'Success':
                return geturlreturn
            
            ''' Step 2. get relation of url. '''
            getrelationreturn = BasicSearch().searchurlrelation(geturlreturn['detail']['id'])
            if getrelationreturn['Status'] != 'Success':
                return getrelationreturn
            
            ''' Step 3. get dns ip detail '''
            for eachdnsid in getrelationreturn['dnslist']:
                getdnsipdetail = BasicSearch().searchdnsipdetail(eachdnsid)
                if getdnsipdetail['Status'] == 'Success':
                    for key, value in getdnsipdetail['dnsdetail'].items():
                        getdnsipdict[key]=value
            
            ''' Step 4. judge dict null or not. '''            
            if len(getdnsipdict) == 0:
                return dict(Status='False')
            else:
                ''' Step 5. get splice detail. '''
                getexpanddetail = FastregExpand().geturlandsplice(type, getdnsipdict)
                return getexpanddetail
        else:
            return dict(Status='False')