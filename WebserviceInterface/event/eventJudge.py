# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time

from EventScheduler import MainScheduler

class EventJudge:
    
    def __init__(self):
        
        self.returns = ""
        
        ''' This method used to judge Event threshold 
        import : thresNumber : {'thresLevel': 1L, 'thresValueTwo': '10%', 'thresValueOne': '10000'}
        import : getDict :  {u'\u53cc\u7ebf1\u533a(\u53cc\u7ebf)': [{'Allcount': 27222}, {'Losecount': 0}, {'Percent': '0%'}], u'\u53cc\u7ebf2\u533a': [{'Allcount': 11111}, {'Losecount': -2000}, {'Percent': '18%'}]}
        '''
    def EventJudge(self, GameName, Timestamp, ThresNumber, getDict):
        
        newGroupDict = {}
        
        ''' Judge lost people '''
        if ThresNumber['thresValueOne'] != '':
            
            for key,value in getDict.items():
                newGroupDict[key] = []
                if type(value).__name__ == 'list':
                    for eachvalue in value:
                        for keys,values in eachvalue.items():
                            if keys == 'Losecount':
                                if int(abs(values)) > int(ThresNumber['thresValueOne']):
                                    newGroupDict[key].append(dict(LosePeople='Over', Standard=int(ThresNumber['thresValueOne']), Actual=int(abs(values)), TimeOccur=Timestamp))
                                elif int(abs(values)) <= int(ThresNumber['thresValueOne']):
                                    newGroupDict[key].append(dict(LosePeople='NotOver', Standard=int(ThresNumber['thresValueOne']), Actual=int(abs(values)), TimeOccur=Timestamp))
        
        ''' Judge Lost Percent '''
        if ThresNumber['thresValueTwo'] != '':
                
            for key,value in getDict.items():
                if type(value).__name__ == 'list':
                    for eachvalue in value:
                        for keys,values in eachvalue.items():
                            if keys == 'Percent':
                                if int(int(values[:-1] >= ThresNumber['thresValueTwo'][:-1])):
                                    newGroupDict[key].append(dict(LosePercent='Over', Standard=ThresNumber['thresValueTwo'], Actual=values, TimeOccur=Timestamp))
                                elif int(int(values[:-1] < ThresNumber['thresValueTwo'][:-1])):
                                    newGroupDict[key].append(dict(LosePercent='NotOver', Standard=ThresNumber['thresValueTwo'], Actual=values, TimeOccur=Timestamp))
                                    
        return newGroupDict
    
    ''' This is part of area contain '''
    def EventOfArea(self, gameID, eventtype, formattime, getJudgeDict):
        
        '''
        Step Explain:
        1. from thresRelation get ThresNumberID
        2. from thresNumber get thresHold
        3. from Dict to count data
        4. Result :  SureResult
        '''
        
        SureResult = {}
        # Step 1 -> ThresNumberID = getsearchOfareaThres['ThresNumberID']
        getsearchOfareaThres = MainScheduler().searchThresNumberID(gameID, eventtype)
        if getsearchOfareaThres['Status'] == 'Success':
            # Step 2 -> Detail of example : 
            getsearchOfareaDetail = MainScheduler().searchThresDetail(getsearchOfareaThres['ThresNumberID'])
            if getsearchOfareaDetail['Status'] == 'Success':
                areaCount = 0
                ActuralPeople = 0
                ActuralPercent = 0
                for key,value in getJudgeDict.items():
                    
                    if type(value).__name__ == 'list':
                        for eachP in value:
                            count = 0
                            print "##### value:", eachP
                            for eachZone, ZoneDetail in eachP.items():
                                if eachZone == 'LosePeople':
                                    if ZoneDetail == 'Over':
                                        count = count + 1
                                        ActuralPeople = ActuralPeople + int(eachP['Actual']) 
                                elif eachZone == 'LosePercent':
                                    if ZoneDetail == 'Over':
                                        count = count + 1
                                        ActuralPercent = ActuralPercent + int(eachP['Actual'][:-1])
                                            
                        if count < 2:
                            areaCount += 1
                            
                if areaCount >= 5:
                    if int(ActuralPeople) > int(getsearchOfareaDetail['thresValueOne']):
                        tmpResult = {}
                        tmpResult['Status'] = 'Over'
                        tmpResult['holdpeople'] = getsearchOfareaDetail['thresValueOne']
                        tmpResult['actualpeople'] = ActuralPeople
			tmpResult['Time'] = formattime
                        SureResult['people'] = tmpResult  
                    
		    ''' Calcualtion about percent '''
		    newPercent = int(float(int(ActuralPeople)) / float(int(getsearchOfareaDetail['thresValueOne'])) * 100)
		
                    if int(newPercent) > int(getsearchOfareaDetail['thresValueTwo'][:-1]):
                        tmpResult = {}
                        tmpResult['Status'] = 'Over'
                        tmpResult['holdpercent'] = str(getsearchOfareaDetail['thresValueTwo'][:-1])+"%"
                        tmpResult['actualpercent'] = str(newPercent)+"%"
			tmpResult['Time'] = formattime
                        SureResult['percent'] = tmpResult 
                
                else:
                    return dict(Status='False', msg='Not fillin 5 area lose.')
            else:
                return dict(Status='False', msg=getsearchOfareaDetail['msg'])
        else:
            return dict(Status='False', msg=getsearchOfareaThres['msg'])
        
	if len(SureResult) == 0:
	        return dict(Status='False', ReturnValue='')
	else:
		return dict(Status='Success', ReturnValue=SureResult)
