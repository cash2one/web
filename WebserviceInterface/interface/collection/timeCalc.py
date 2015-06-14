# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time

class TimePass:
    
    def __init__(self):
        
        self.timeList = []
        self.dbfileName = ""
        self.nowTime = int(round(time.time()-1*60))
    
    def TimeCalcuate(self, PassforTime, searchTime):

        if type(PassforTime) == int:
            for eachTime in range(PassforTime+1):
                searchCalc = searchTime-int((eachTime+1)*60)
                self.timeList.append(searchCalc)
        else:
            msg = 'Input Variable : Time pass error'
            return msg
        
        return dict(timeStamp=self.nowTime, timeList=self.timeList)
    
    def getNowtime(self):
        
        return dict(timeStamp=self.nowTime)
    
    def getDBfilename(self, timeStamp):
        
        # [0]: year [1]:month [3]: day
        timeText = time.localtime(timeStamp)
        newMonth = self.judgeLeastTen(timeText[1])
        newHour = self.judgeLeastTen(timeText[2])
        getDay = "%s%s%s" % (timeText[0],newMonth,newHour)
        self.dbfileName = "ONLINENUM"+str(getDay) 

        return self.dbfileName
    
    def judgeLeastTen(self, Variable):
        
        NewVariable = ""
        
        if Variable < 10:
            NewVariable = ("0"+str(Variable))
        else:
            NewVariable = str(Variable)
               
        return NewVariable