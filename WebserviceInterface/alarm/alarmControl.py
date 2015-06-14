# -*- coding: utf-8 -*-
''' @author : majian'''

import time
import os, re, sys

import pdb

from alarmScheduler import Scheduler
from alarmExplain import AlarmExplain
from broadcastControl import BroadcastMain
from ServiceConfig.config import readFromConfigFile
import simplejson as json

class AlarmControl:
    
    def __init__(self):
        
        self.oc = 0
        self.mail = 0
        self.web = 0
        self.message = 0
        self.ios = 0
        self.returns = ""
        self.userlist = []
        self.userDict = {}
        self.Inform = {}
        
    def testAlarm(self, OID):
        
        getData = {}
        changeData = {}
        getResult = Scheduler().getSearchofAlarm(OID)
        
        if getResult['Status'] == 'Success':
            
            del getResult['Status']
            
            print "#### getResult:", getResult
            
            for key,value in getResult.items():
                for keys,values in value.items():
                    if keys == 'Data':
                        getData = json.loads(values)
                        for k,v in getData.items():
                            
                            #''' This is not found filename part '''
                            if type(v).__name__ == 'str' or type(v).__name__ == 'unicode':
                                if re.search(r'Could not found', v):
                                    changeData[k] = v
                                
                            #''' This is calcuation of part '''
                            elif type(v).__name__ == 'dict':
                                tmpZone = {}
                                for zone,part in v.items():
                                    if type(part).__name__ == 'list':
                                        tmpZone[zone] = Scheduler().readlisttoMan(part)
                                        
                                changeData[k] = tmpZone

                getResult[key]['Data']=changeData
             
            getResult = json.dumps(getResult)
                        
            if self.oc == 1:
                
                getOCreturn = Scheduler().AlarmBySMCD(18017313798, getResult, 13091)
                
            else:
                return 'could not using OC pass Alarm.'
            
            return getOCreturn
        
        else:
            return getResult['msg']
    
    ''' depend OID to get detail of event '''    
    def AlarmGetdetailControl(self, OID):
        
        '''
        No.1 get OID all detail -> judge only to  Number of curves
        type : dict
        example : 3L: {'eventApart': 'event', 'Destination': 'SGZH-\xe5\x8f\x8c\xe7\xba\xbf2\xe5\x8c\xba', 'Data': 'This Zone 5 mins Lose -2000 people.', 'eventGrade': 4L}
        '''
        getalarmdetail = Scheduler().getSearchofAlarm(OID)
        if getalarmdetail['Status'] != 'Success':
            return getalarmdetail['msg']
        
        del getalarmdetail['Status']

        ''' No.2 get each of alarm '''
        for eachline, eachalarm in getalarmdetail.items():
	    if eachalarm['Data'] != '':

                tmpAlarm = []

		# eachalarm: {'eventApart': 'event', 'Destination': 'ZTII-percent', 'Data': "{'Status': 'Over', 'actualpercent': '630%', 'holdpercent': '35%', 'Time': '2013\\xe5\\xb9\\xb403\\xe6\\x9c\\x8821\\xe6\\x97\\xa5_14:54\\xe5\\x88\\x86'}", 'eventGrade': 4L}

                ''' get event level and event group '''
                tmpEventLevel = eachalarm['eventGrade']
                tmpGameName = self.GetprojectName(eachalarm['Destination'])
                ''' This part is very important : broad cast list for user '''    
                tmpEventGroup = Scheduler().getEventGroupRelation(tmpGameName['GameName'])
                ''' get people list : self.userDict '''
                for eachGroup in tmpEventGroup:
                    tmppeople = Scheduler().getPeople(tmpEventLevel, eachGroup)
                    if tmppeople['Status'] == 'Success':
                        self.userDict = dict(self.userDict, **tmppeople)
                    
                ''' Summary information and part of this '''
                GameNameCH = Scheduler().getGameNameCH(tmpGameName['GameName'])

                if GameNameCH['Status'] == 'Success':
                    GameName = GameNameCH['FullName']   # GameName Chinese
                    ZoneName = tmpGameName['ZoneName']  # ZoneName Chinese
                    TimeNow = 3
                    # [{'LosePeople': 'Over', 'Actual': 13000, 'Standard': 10000}, {'LosePercent': 'Over', 'Actual': '54%', 'Standard': '10%'}, 'None']
                    dataList = Scheduler().dataListpart(eachalarm['Data'])
		    print "######### datalist:", dataList
                    getReturnofEvent = AlarmExplain().getExplainofNumberofCurves(dataList)
		    print "############ getReturnofEvent:", getReturnofEvent
    
                    ''' Statement of Number of Curves '''
                    ActuallyHold = ""
                    ActuallyLose = ""
                    PercentHold = ""
                    PercentActually = ""
    		    WholePercent = ""
		    WholePeople = ""
                    TimeOccur = ""
    
                    for AlarmKey,AlarmValue in getReturnofEvent.items():
			print "################ AlarmKey,AlarmValue:", AlarmKey,AlarmValue,type(AlarmKey), type(AlarmValue)
                        if AlarmKey == 'ActuallyLose':
                            ActuallyLose = "实际下滑人数:%s人" % AlarmValue
                        elif AlarmKey == 'PercentActually':
                            PercentActually = "实际百分比掉率:%s" % AlarmValue
    		        elif AlarmKey == 'Wholepercentactually':
    			    WholePercent = "实际百分比掉率:%s" % AlarmValue
			elif AlarmKey == 'Wholepeopleactually':
			    WholePeople = "实际下滑人数:%s" % AlarmValue
                        elif AlarmKey == 'Time':
                            TimeOccur = "事件发生时间:%s" % AlarmValue
    
                    ''' Message header '''
                    tmpAlarm.append("【%s】" % GameName)
                    tmpAlarm.append("区名:%s" % ZoneName)
                    tmpAlarm.append("%s" % TimeOccur)
                    tmpAlarm.append("监控时间段:近%s分钟" % TimeNow)
    
                    ''' Message Body '''
                    if ActuallyLose:
                        tmpAlarm.append(ActuallyLose)
                    if PercentActually:
                        tmpAlarm.append(PercentActually)
        	    if WholePercent:
    		        tmpAlarm.append(WholePercent)
		    if WholePeople:
			tmpAlarm.append(WholePeople)
                     
                    ''' Message leg ''' 
                    tmpAlarm.append("【统一监控自动发送】")
                    
                    self.Inform[eachline] = tmpAlarm
		    print "############## self.inform:", self.Inform
                    
                    ''' Broadcast to every body '''

	            BroadcastMain().Control(self.Inform, self.userDict)
                
        
    ''' from Variable get project Name '''
    def GetprojectName(self, Destination):
        
        GameDict = {}
        
	if re.search(r'\-people', Destination):
	    GameDict['GameName'] = re.split('\-', Destination)[0]
            GameDict['ZoneName'] = '全区'
	elif re.search(r'\-percent', Destination):
	    GameDict['GameName'] = re.split('\-', Destination)[0]
            GameDict['ZoneName'] = '全区'
        elif re.search(r'\-', Destination):
            GameSimpleName = re.split('\-', Destination)[0]
            ZoneName = re.split('\-', Destination)[1]
            GameDict['GameName'] = GameSimpleName.upper()
            GameDict['ZoneName'] = ZoneName
        else:
            GameDict['GameName'] = Destination
            GameDict['ZoneName'] = '全区'
            
        return GameDict
