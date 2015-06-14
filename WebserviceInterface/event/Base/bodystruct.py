# -*- coding: utf-8 -*-
''' @author : majian'''

import time
import os, re, sys

from BaseClass.verifityDependence import changeList

class EventBody:
    
    def __init__(self):
        
        self.eventbody = {}
        
    def bodystructs(self, templatetype, Eproject, Econtent, Elevel, Eoid, Etimestamp, Econditionid):
        
        ''' Process Inform '''
        if templatetype == 'processInform':
            ''' Eproject '''
            if type(Eproject).__name__ != 'list':
                getList = changeList().strtolist(Eproject)
                if getList['Status'] != 'Success':
                    return getList
                self.eventbody['Eproject'] = getList['List']
            else:
                self.eventbody['Eproject'] = Eproject
            
            ''' Econtent '''
            if type(Econtent).__name__ == 'str':
                self.eventbody['Econtent'] = Econtent    
            else:
                return dict(Status='False', msg='input Econtent not right. Not String.')
            
            ''' Elevel '''
            if Elevel == '' or Elevel == 'None':
                self.eventbody['Elevel'] = -1
            else:
                self.eventbody['Elevel'] = int(Elevel)
                
            ''' Eoid '''
            if Eoid == '' or Eoid == 'None':
                return dict(Status='False', msg='input Eoid not right. Not None.')
            else:
                self.eventbody['Eoid'] = Eoid
                
            ''' Etimestamp '''
            if Etimestamp == '' or Etimestamp == 'None':
                self.eventbody['Etimestamp'] = 0
            else:
                self.eventbody['Etimestamp'] = int(Etimestamp)
                
            ''' Econditionid '''
            if Econditionid == '' or Econditionid == 'None':
                self.eventbody['Econditionid'] = 1
            else:
                self.eventbody['Econditionid'] = int(Econditionid)
                
        return dict(Status='Success', eventbody=self.eventbody)

class AlarmBody:
    
    def __init__(self):
        
        self.alarmBody = {}
        
    def bodystructs(self, templatetype, Project, Eventlevel, Mbody, Timestamp):
        
        ''' Process Inform '''
        if templatetype == 'processInform':
        
            ''' Project '''
            if type(Project).__name__ == 'str':
                if Project == '' or Project == 'None':
                    return dict(Status='False', msg='Alarm Body could not None.')
                else:
                    self.alarmBody['Project'] = Project
            else:
                return dict(Status='False', msg='input Prject error.')
            
            ''' Eventlevel '''
            if Eventlevel == '' or Eventlevel == 'None':
                self.alarmBody['Eventlevel'] = -1
            else:
                self.alarmBody['Eventlevel'] = int(Eventlevel)
                
            ''' Mbody '''
            tmpMbody = {}
            tmpMbody['oc'] = Mbody
            tmpMbody['smcd'] = Mbody
            tmpMbody['mail'] = dict()
            
            self.alarmBody['Mbody'] = tmpMbody
            
            ''' Timestamp '''
            if Timestamp == '' or Timestamp == 'None':
                self.alarmBody['Timestamp'] = 0
            else:
                self.alarmBody['Timestamp'] = Timestamp
                
            return dict(Status='Success', alarmbody=self.alarmBody)