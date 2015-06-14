# -*- coding: utf-8 -*-
''' @author : majian'''

import time
import datetime

class TimeBasic:
    
    def __init__(self):
        
        self.nowtime = 0
        self.timeFormat = {}
    
    ''' This method used to get local timestamp '''    
    def nowtime(self):

        self.nowtime = int(round(time.time()))
        
        return self.nowtime
    
    ''' 
    Time Control method 
    method : 1 : 2013年03月25日_19:25分
    method : 2 : 2013_03_25_19:25
    method : 3 : 2013-03-25_11:30:53
    method : 4 : 20130412_14
    method : 5 : 2013.03.25_11:30:53
    '''
    def timeControl(self, Timestamp, method):

        newFormat = ""
        formatTime = self.formatTimeasDict(Timestamp)

        if formatTime:
            if method == 1:
                newFormat = "%s年%s月%s日_%s:%s分" % (formatTime['year'], formatTime['month'], formatTime['day'], formatTime['hour'], formatTime['minute'])
            elif method == 2:
                newFormat = "%s_%s_%s_%s:%s" % (formatTime['year'], formatTime['month'], formatTime['day'], formatTime['hour'], formatTime['minute'])
            elif method == 3:
                dt = datetime.datetime.fromtimestamp(Timestamp)
                newFormat = dt.strftime("%Y-%m-%d_%H:%M:%S")
            elif method == 4:
                dt = datetime.datetime.fromtimestamp(Timestamp)
                newFormat = dt.strftime("%Y%m%d_%H")  
            elif method == 5:
                dt = datetime.datetime.fromtimestamp(Timestamp)
                newFormat = dt.strftime("%Y.%m.%d_%H:%M:%S")
                      
            return newFormat
        else:
            return 'input Timestamp ERROR.'
    
        return newFormat
    
    '''
    Time Recontrol => 2013-04-13_19:55:58 into timestamp
    '''
    def timeRecontrol(self, TimeNow):
        
        newTime = int(time.mktime(time.strptime(TimeNow, '%Y-%m-%d_%H:%M:%S')))
        
        return newTime
    
    def timeADcontrol(self, timeNow):
        
        newsTime = int(time.mktime(time.strptime(timeNow, '%Y.%m.%d_%H:%M:%S')))
        
        return newsTime
    
    def TimeMinus(self, starttime, overtime):
        
        if type(overtime).__name__ != 'int':
            overtime = int(overtime)
        else:
            overtime = overtime
            
        if type(starttime).__name__ != 'int':
            starttime = int(starttime)
        else:
            starttime = starttime
        
        result = str(int(int(overtime - starttime) / 3600))+" Hour"  
        
        return result
    
    ''' 
    This method used to get Local timestamp format after.
    output format: {'year':4bit, 'month':2bit, 'day':2bit, 'hour':2bit, 'minute':2bit, 'second':2bit}
    '''
    def formatTimeasDict(self, timeStamp):
        
        try:
            newLocaltime = time.localtime(int(timeStamp))
            
            self.timeFormat['year'] = self.judgeTime(newLocaltime[0])
            self.timeFormat['month'] = self.judgeTime(newLocaltime[1])
            self.timeFormat['day'] = self.judgeTime(newLocaltime[2])
            self.timeFormat['hour'] = self.judgeTime(newLocaltime[3])
            self.timeFormat['minute'] = self.judgeTime(newLocaltime[4])
            self.timeFormat['second'] = self.judgeTime(newLocaltime[5])
    
        except Exception, e:
            return e

        return self.timeFormat
    
    ''' This method used to get 1bit became 2bit '''
    def judgeTime(self, onebit):
        
        if len(str(onebit)) == 1:
            return "0"+str(onebit)
        else:   
            return str(onebit)     