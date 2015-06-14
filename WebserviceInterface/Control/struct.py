# -*- coding: utf-8 -*-
''' @author : majian'''

import soaplib

from soaplib.core.server import wsgi
from soaplib.core.service import DefinitionBase
from soaplib.core.service import soap
from soaplib.core.model.clazz import Array
from soaplib.core.model.binary import Attachment
from soaplib.core.model.clazz import ClassModel
from soaplib.core.model.primitive import Integer,String,Boolean

class C_test(ClassModel):
    __namespace__ = "C_test"
    TestResult = String

class C_loginReback(ClassModel):
    __namespace__ = "C_loginReback"
    Status = String
    ValidateTime = Integer
    
class C_loginInformationReback(ClassModel):
    __namespace__ = "C_loginInformationReback"
    Status = String
    Mail = String
    StaffNum = Integer
    
class C_NowNumberCurves(ClassModel):
    __namespace__ = "C_NowNumberCurves"
    Name = String
    JsonChar = String
    
class C_HistoryofCurves(ClassModel):
    __namespace__ = "C_HistoryofCurves"
    Name = String
    JsonChar = String
    
class C_EventSearch(ClassModel):
    __namespace__ = 'C_EventSearch'
    JsonChar = String

###########################################################    
############### This part used by Event ###################
########################################################### 
class C_EventBasicStatus(ClassModel):
    __namespace__ = 'C_EventBasicStatus'
    JsonChar = String
    
class C_EventGameList(ClassModel):
    __namespace__ = 'C_EventGameList'
    JsonChar = String
    
class C_EventLevel(ClassModel):
    __namespace__ = 'C_EventLevel'
    JsonChar = String
    
class C_EventfromEventAlarm(ClassModel):
    __namespace__ = 'C_EventfromEventAlarm'
    Status = String
    Jsonchar = String
    
class C_UserBelong(ClassModel):
    __namespace__= 'C_UserBelong'
    Status = String
    Char = String
    
class C_WholeUsing(ClassModel):
    __namespace__ = 'C_WholeUsing'
    Status = String
    JsonChar = String
    
class C_userSelect(ClassModel):
    __namespace__ = 'C_userSelect'
    Status = String
    JsonChar = String
    
class C_TransportMain(ClassModel):
    __namespace__ = 'C_TransportMain'
    Status = String
    SourceStep = Integer
    CompleteStep = String
    Remark = String
    
class C_RecentlyTenEvent(ClassModel):
    __namespace__ = 'C_RecentlyTenEvent'
#    Status = String
    Recently = String
    
class C_designPeople(ClassModel):
    __namespace__ = 'C_designPeople'
    Status = String
    Char = String
    
class C_designsearch(ClassModel):
    __namespace__ = 'C_designsearch'
    #Status = String
    JsonChar = String
    
class C_EventDetailSearch(ClassModel):
    __namespace__ = 'C_EventDetailSearch'
    Status = String
    JsonChar = String
    
###########################
#### Part of pass store ###
###########################
class C_TestMainserverDatabase(ClassModel):
    __namespace__ = 'C_TestMainserverDatabase'
    Status = String
    Char = String
    
class C_testMainServerTable(ClassModel):
    __namespace__ = 'C_testMainServerTable'
    Status = String
    JsonChar = String
    
class C_insertJudge(ClassModel):
    __namespace__ = 'C_insertJudge'
    Status = String
    JsonChar = String
    
class C_searchMaxLine(ClassModel):
    __namespace__ = 'C_searchMaxLine'
    Status = String
    Count = Integer
    
##############################
#### part of alarm module ####
##############################
class C_AlarmModuleTest(ClassModel):
    __namespace__ = 'C_AlarmModuleTest'
    Status = String
    Info = String
    
class C_AlarmModule(ClassModel):
    __namespace__ = 'C_AlarmModule'
    Status = String
    Info = String  
    
##############################
#### part of event module ####
##############################
class C_EventModuleTest(ClassModel):
    __namespace__ = 'C_EventModuleTest'
    Status = String
    Info = String  
    
class C_EventModule(ClassModel):
    __namespace__ = 'C_EventModule'
    Status = String
    Info = String 
    
class C_inMaximo(ClassModel):
    __namespace__ = 'C_inMaximo'
    Status = String
    JsonChar = String
    
class C_careCount(ClassModel):
    __namespace__ = 'C_careCount'
    Status = String
    Char = String
    
class C_EventSearchofDoing(ClassModel):
    __namespace__ = 'C_EventSearchofDoing'
    Status = String
    JsonChar = String

class C_ReadfromEventTrace(ClassModel):
    __namespace__ = 'C_ReadfromEventTrace'
    #Status = String
    JsonChar = String
    
class C_RestoreResultofEasy(ClassModel):
    __namespace__ = 'C_RestoreResultofEasy'
    Status = String
    Char = String
    
class C_counterStatus(ClassModel):
    __namespace__ = 'C_counterStatus'
    Status = String
    Char = String
    SolvePerson = String
    
class C_testUserRegistered(ClassModel):
    __namespace__ = 'C_testUserRegistered'
    Status = String
    Char = String
    SolvePerson = String
    
class C_webadvertising(ClassModel):
    __namespace__ = 'C_webadvertising'
    Status = String
    JsonChar = String
    
class C_fastRegtest(ClassModel):
    __namespace__ = 'C_fastRegtest'
    Status = String
    JsonChar = String
    SolvePerson = String
    
class C_EasyNamefromFullName(ClassModel):
    __namespace__ = 'C_EasyNamefromFullName'
    Status = String
    JsonChar = String
    
class C_eventfinishedsearch(ClassModel):
    __namespace__ = 'C_eventfinishedsearch'
    Status = String
    JsonChar = String

class C_eventdoingsearchByCombinationParameter(ClassModel):
    __namespace__ = 'C_eventdoingsearchByCombinationParameter'
    Status = String
    JsonChar = String
    
class C_eventdoingsearchByCombinationParameterweb(ClassModel):
    __namespace__ = 'C_eventdoingsearchByCombinationParameterweb'
    Status = String
    JsonChar = String
    
class C_eventfinishedByCombinationParameter(ClassModel):
    __namespace__ = 'C_eventfinishedByCombinationParameter'
    Status = String
    JsonChar = String
    
class C_eventfinishedByCombinationParameterweb(ClassModel):
    __namespace__ = 'C_eventfinishedByCombinationParameterweb'
    Status = String
    JsonChar = String
    
class C_Cachecounterstatus(ClassModel):
    __namespace__ = 'C_Cachecounterstatus'
    Status = String
    Char = String
    SolvePerson = String
    
class C_Cachefastreg(ClassModel):
    __namespace__ = 'C_Cachefastreg'
    Status = String
    Char = String
    SolvePerson = String
    
class C_CacheofAdvertising(ClassModel):
    __namespace__ = 'C_CacheofAdvertising'
    Status = String
    JsonChar = String
    
class C_operationADurl(ClassModel):
    __namespace__= 'C_operationADurl'
    Status = String
    Char = String
    
class C_ServerMaintain(ClassModel):
    __namespace__ = 'C_ServerMaintain'
    Status = String
    
class C_ServerhasbeenMaintain(ClassModel):
    __namespace__ = 'C_ServerhasbeenMaintain'
    Status = String
    Char = String
    
class C_curvesofnumberperson(ClassModel):
    __namespace__ = 'C_curvesofnumberperson'
    Status = String
    Char = String
    
class C_getRecentlyEvent(ClassModel):
    __namespace__ = 'C_getRecentlyEvent'
    Status = String
    JsonChar = String