# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time

from oidDetail import OidDetail

class OidDecide:
    
    def __init__(self):
        
        self.returns = ""
        
    def OidCharge(self, Oid, message):
        
        # insert into database about asset 
        if Oid == '1.1':
            name = 'insert'
            getReturnofDetail = OidDetail().DetailforEachOid(name, message) 
            return getReturnofDetail
    
        # Threshold judge    
        elif Oid == '1.2':
            name = 'disk'
            getReturnofDetail = OidDetail().DetailforEachOid(name, message)
            if getReturnofDetail['Status'] != 'Success':
                if re.search(r'IntegrityError', getReturnofDetail['msg']):
                    getReturnofDetail['msg'] = 'MySQL could not insert same Data in table.'
            
            return getReturnofDetail
        
        # else
        elif Oid == '1.3' or Oid == '1.4' or Oid == '1.5':
            print Oid
            return dict(Status='Success')
        # ethernet judge
        elif Oid == '1.6':
            print Oid
            return dict(Status='Success')
        # Process Monitor
        elif Oid == '1.7':
            name = 'processInform'
            getReturnofDetail = OidDetail().DetailforEachOid(name, message)
            return getReturnofDetail
        
        elif Oid == '5.1':
            name = 'serveralive'
            getReturnDetail = OidDetail().DetailforEachOid(name, message)
            
        
        elif Oid == '8.0':
            print "#### get from platform:", Oid
            return dict(Status='Success')
        
        else:
            msg="Oid could not be used."
            return dict(Status='False', msg=msg)
            
            
            
        
        
        