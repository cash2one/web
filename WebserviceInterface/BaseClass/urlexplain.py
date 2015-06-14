# -*- coding: utf-8 -*-
''' @author : majian'''

import sys, re, os
import urllib2
import pdb

class urlExplain:
    
    def __init__(self):
        
        self.returns = ""
        
    def urlcheckcode(self, url):
        
        try:
            
            if re.search(r'http', url):
                code = urllib2.urlopen(url).getcode()
                if code == 200:
                    return dict(Status='Success')
                else:
                    return dict(Status='False', msg='check url failed.')
            else:
                return dict(Status='False', msg='input variable:url Error.')
        
        except Exception, e:
            return dict(Status='False', msg='url could not be found: 404.')
        
    def urlforfastreg(self, url):
        
        try:
            if re.search(r'http', url):
                getreturn = urllib2.urlopen(url)
                html = getreturn.readline()
                
                return dict(Status='Success', result=html)
                
            else:
                return dict(Status='False', msg='input variable:url Error.')
            
        except Exception, e:
            return dict(Status='False', msg='url could not be found: 404.')