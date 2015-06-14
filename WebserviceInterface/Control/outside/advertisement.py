# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time
import pdb

from model.cmdbsearch import BasicSearch
from BaseClass.urlexplain import urlExplain

from advertisementExpand import Expand

class Advertisement:
    
    def __init__(self):
        
        self.returns = ""
    
    ''' This method used to operation url. '''    
    def getUrloperation(self, url, operation, starttime, overtime, project, pagealias):
        
        newReturnList = []
        
        # when project is none
        if type(project).__name__ == 'NoneType' or project == '0':
            # select
            project = '0'
            # decide on url variable
            if type(url).__name__ == 'NoneType' or url == 'None':
                ''' Step 1. get url list '''
                getselectofresult = BasicSearch().searchaliveinadvertising()
                if getselectofresult['Status'] != 'Success':
                    return getselectofresult
                
                ''' Step 2. check link and status. '''
                for eachurlDict in getselectofresult['list']:
                    eachurl = eachurlDict['url']
                    getcodeofurl = urlExplain().urlcheckcode(eachurl)
                    if getcodeofurl['Status'] == 'Success':
                        tmpDict = dict(eachurlDict, **dict(Status='Success'))
                        newReturnList.append(tmpDict)
                    else:
                        tmpDict = dict(eachurlDict, **dict(Status='False'))
                        newReturnList.append(tmpDict)
                        
                return dict(Status='Select', List=newReturnList)
                    
            # add or delete    
            else:
                ''' Step 1. check input Variable. '''
                getFirstStepReturn = Expand().checkadvariable(url, operation, starttime, overtime, project)
                if getFirstStepReturn['Status'] != 'Success':
                    return getFirstStepReturn
                
                ''' Step 2. check add or del. '''
                getSecondStepReturn = Expand().checkaddordel(url, operation, starttime, overtime, project, pagealias)
                if getSecondStepReturn['Status'] != 'Success':
                    return getSecondStepReturn
                
                ''' Step 3. whole action. '''
                getSecondStepReturn = Expand().wholeUsingAction(url, operation, getSecondStepReturn['starttime'], getSecondStepReturn['overtime'], getSecondStepReturn['project'], getSecondStepReturn['pagealias'])
                return getSecondStepReturn
        # When project is not None
        else:
            if type(url).__name__ == 'NoneType' or url == 'None':
                ''' Step 1. get url list '''
                getselectofproject = BasicSearch().searchaliveprojectofadvertising(project, 1)
                if getselectofproject['Status'] != 'Success':
                    return getselectofproject
                
                ''' Step 2. check link and status. '''
                for eachurlDict in getselectofproject['list']:
                    eachurl = eachurlDict['url']
                    getcodeofurl = urlExplain().urlcheckcode(eachurl)
                    if getcodeofurl['Status'] == 'Success':
                        tmpDict = dict(eachurlDict, **dict(Status='Success'))
                        newReturnList.append(tmpDict)
                    else:
                        tmpDict = dict(eachurlDict, **dict(Status='False'))
                        newReturnList.append(tmpDict)
                        
                return dict(Status='Select', List=newReturnList)
            
            else:
                ''' Step 1. check input Variable. '''
                getFirstStepReturn = Expand().checkadvariable(url, operation, starttime, overtime, project)
                if getFirstStepReturn['Status'] != 'Success':
                    return getFirstStepReturn
                
                ''' Step 2. check add or del. '''
                getSecondStepReturn = Expand().checkaddordel(url, operation, starttime, overtime, project, pagealias)
                if getSecondStepReturn['Status'] != 'Success':
                    return getSecondStepReturn
                
                ''' Step 3. whole action. '''
                getSecondStepReturn = Expand().wholeUsingAction(url, operation, getSecondStepReturn['starttime'], getSecondStepReturn['overtime'], getSecondStepReturn['project'], getSecondStepReturn['pagealias'])
                return getSecondStepReturn
    
    def decideOperationaboutAD(self, url, operation, starttime, overtime, project, pagealias):   
        
        if type(url).__name__ == 'NoneType':
            return dict(Status='False', msg='Error input url.')
        
        if type(project).__name__ == 'NoneType':
            return dict(Status='False', msg='Error input project.')
        
        if type(pagealias).__name__ == 'NoneType':
            return dict(Status='False', msg='Error input pagealias.')     
        
        ''' Step 1. check input Variable. '''
        getFirstStepReturn = Expand().checkadvariable(url, operation, starttime, overtime, project)
        if getFirstStepReturn['Status'] != 'Success':
            return getFirstStepReturn
                
        ''' Step 2. check add or del. '''
        getSecondStepReturn = Expand().checkaddordel(url, operation, starttime, overtime, project, pagealias)
        if getSecondStepReturn['Status'] != 'Success':
            return getSecondStepReturn
                
        ''' Step 3. whole action. '''
        getSecondStepReturn = Expand().wholeUsingAction(url, operation, getSecondStepReturn['starttime'], getSecondStepReturn['overtime'], getSecondStepReturn['project'], getSecondStepReturn['pagealias'])
        return getSecondStepReturn    