# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time

from BaseClass.calcpercent import percentCalc

class Depend:
    
    def __init__(self):
        
        self.returns = ""
    
    def CurvesManage(self, Dict):
        
        ResultManage = {}
        
        ''' 
        No.1 get Max People 
        example : {u'\u53cc\u7ebf1\u533a(\u53cc\u7ebf)': 27222, u'\u53cc\u7ebf2\u533a': 11111}
        '''
        MaxPeople = self.MaxOfPeople(Dict)
        
        ''' 
        No.2 get Lose People 
        example : {u'\u53cc\u7ebf1\u533a(\u53cc\u7ebf)': 3000, u'\u53cc\u7ebf2\u533a': 2000}
        '''
        LosePeople = self.CurvesofCalc(Dict)
        
        '''
        No.3 get Percent Lose
        example : {u'\u53cc\u7ebf1\u533a(\u53cc\u7ebf)': '0%', u'\u53cc\u7ebf2\u533a': '18%'}
        '''
        PercentPeople = self.PercentLose(MaxPeople, LosePeople)
        
        ''' 
        No.4 be part of whole result
        example : {u'\u53cc\u7ebf1\u533a(\u53cc\u7ebf)': [{'Allcount': 27222}, {'Losecount': 0}, {'Percent': '0%'}], u'\u53cc\u7ebf2\u533a': [{'Allcount': 11111}, {'Losecount': -2000}, {'Percent': '18%'}]}
        '''
        for key,value in MaxPeople.items():
            ResultManage[key]= [] 
            ResultManage[key].append(dict(Allcount=value))
        
        for key,value in LosePeople.items():
            for Rkey,Rvalue in ResultManage.items():
                if key == Rkey:
                    ResultManage[key].append(dict(Losecount = value))
                    
        for key,value in PercentPeople.items():
            for Rkey,Rvalue in ResultManage.items():
                if key == Rkey:
                    ResultManage[key].append(dict(Percent = value))

        return ResultManage
        
    ''' FOR each game calc Curves '''
    def CurvesofCalc(self, Dict):
        
        newDict = {}
        
        for key,value in Dict.items():
            newDict[key] = ""
            tmpList = []
            for eachVar in range(len(value)):
                if eachVar != 0:
                    getCheck = int( int(value[eachVar]) - int(value[eachVar-1]) )
                    tmpList.append(getCheck)
                    newDict[key] = min(tmpList)

        return newDict
    
    ''' For each game calc Max people '''
    def MaxOfPeople(self, Dict):
        
        newMax = {}
        
        for key,value in Dict.items():
            newMax[key] = ""
            for eachVar in range(len(value)):
                if eachVar != 0:
                    newMax[key] = max(value)
            
        return newMax
    
    ''' For each Zone calcaulation Lose people percent '''
    def PercentLose(self, MaxDict, LoseDict):
        
        newPercent = {}
        
        for Losekey,Losevalue in LoseDict.items():
            for Maxkey,Maxvalue in MaxDict.items():
                if Losekey == Maxkey:
                    if int(Losevalue) >= 0:
                        newPercent[Losekey] = '0%'
                    if int(Losevalue) < 0:
                        newPercent[Losekey] = percentCalc().percent(abs(Losevalue), abs(Maxvalue))
                        
        return newPercent