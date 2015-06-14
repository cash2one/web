# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time

from EventScheduler import MainScheduler
from eventJudge import EventJudge

class EventDefine:
    
    def __init__(self):
        
        self.returns = ""
        
    def defineManager(self, eventtype, timestamp, dataDict):
        
        newDict = {}
        
        ''' format timestamp to chinese '''
        formattime = MainScheduler().timeBasicCalc(timestamp, 1)
        
        ''' The part of number of curves method '''   
        if eventtype == 'numberofcurves':

            ''' 
            No.1 judge Game Zone
                Step 1. from gamelist to get gameid 
                step 2. add white list ignore gameid
                Step 3. from thresRelation to get tNumberID -> mul
                step 4. get each threshold
                step 5. judge five area
            '''
            for key,value in dataDict.items():
                if type(key).__name__ == 'str' or type(key).__name__ == 'unicode':
                    # step 1
                    getGameIDdict = MainScheduler().searchGameID(key)
		    print "####### getGameIDdict:", getGameIDdict
                    if getGameIDdict['Status'] == 'Success':
                    # step 2
                        getWhiteList = MainScheduler().searchIgnoreType(eventtype, getGameIDdict['GameID'])
                        if getWhiteList['Status'] == 'Success':    
                    # step 3
                            getThresID = MainScheduler().searchThresNumberID(getGameIDdict['GameID'], eventtype)
			    print "####### getThresID:", getThresID
                            if getThresID['Status'] == 'Success':
                    # step 4
                                getThresDetail = MainScheduler().searchThresDetail(getThresID['ThresNumberID'])
                                del getThresDetail['Status']
                                getJudgeReturn = EventJudge().EventJudge(key, formattime, getThresDetail, dataDict[key])
                                print "##### getJudageReturn:", getJudgeReturn
                    # step 5
		    # success : {'Status': 'Success', 'ReturnValue': {'percent': {'Status': 'Over', 'hold': '2', 'actual': 3}}}
		    # falied : {'Status': 'False', 'ReturnValue': ''}
                                getJudgeOfArea = EventJudge().EventOfArea(getGameIDdict['GameID'], 'areajudge', formattime, getJudgeReturn)
				print "######################### getJudgeofArea:", getJudgeOfArea
                                if getJudgeOfArea['Status'] == 'Success': 
                                    del getJudgeOfArea['Status']            
                                    newDict[key] = getJudgeOfArea
                                else:
                                    newDict[key] = getJudgeReturn
                        else:
                            newDict[key] = 'this game %s could not be allowed.' % eventtype
                    else:
                        newDict[key]=value
             
            ''' No.2 judge Agent -> Server '''            
            
            ''' No.3 judge Switch '''
            
            ''' No.4 judge Machineroom '''
                        
            return newDict
