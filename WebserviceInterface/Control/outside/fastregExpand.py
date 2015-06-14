# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time

from BaseClass.randomnum import RandomNum
from BaseClass.urlexplain import urlExplain
from BaseClass.verifityDependence import changeDict

from model.__cmdbinit__ import CMDBSession
from model.cmdbsearch import BasicSearch

class FastregExpand:
    
    def __init__(self):
        
        self.returns = ""
        
    def geturlandsplice(self, category, arrayDict):
        
        count = 0
        Errormessage = []
        
        try:
            if category == 'testreg':
                ''' Step 1. get variable. '''
                getSearchofspliceurl = BasicSearch().searchspliceurl(category)
                if getSearchofspliceurl['Status'] != 'Success':
                    return getSearchofspliceurl
            
                ''' Step 2. combination. '''
                for key,value in arrayDict.items():
                    tmpip = value['ipaddress']
                    tmpusername = "test00"+str(int(time.time()))
                    sourceDict = getSearchofspliceurl['categoryinform']
                    for k,v in sourceDict.items():
                        urlfirst = re.sub(r'\(%s\)', tmpip, v, 1)
                        urlsecond = re.sub(r'\(%s\)', tmpusername, urlfirst, 1)
                        
                        ''' Step 3. judge success. '''
                        getReturnofurl = urlExplain().urlforfastreg(urlsecond)
                        if getReturnofurl['Status'] == 'Success':
                            tmpDict = changeDict().strtodict(getReturnofurl['result'])
                            time.sleep(1)
                            if len(tmpDict) == 4:
                                count += 1
                            elif len(tmpDict) == 3:
                                getreturnvaluedefine = BasicSearch().searchreturnvaluedefine(tmpDict['code'], 'testreg')
                                if getreturnvaluedefine['Status'] == 'Success':
                                    #Errormessage.append(tmpip+" : check failed. BY: "+getreturnvaluedefine['zhdefine'])
                                    Errormessage.append(tmpip+" : check failed.")
                if count == len(arrayDict):
                    return dict(Status='Success')
                elif count < len(arrayDict):
                    return dict(Status='Warning', msg=Errormessage)
                elif count == 0:
                    return dict(Status='False', msg='Fast Register broken down.')
        
        except Exception, e:
            return dict(Status='False', msg=str(e))