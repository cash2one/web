# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time

from EventScheduler import EventScheduler
from model.dbsearch import EventTransportExpand, EventSearch

class EventProcessStep:
    
    def __init__(self):
        
        self.processCalc = {}
        
    def processStep(self, templatetype, ipaddress, timestamp):
        
        ''' This is process part '''
        if templatetype == 'processInform':
            
            # list of ipaddress in template from web 
            # {'Status': 'Success', 'processinfo': {'ScenServer': 5L, 'GatewayServer': 6L}}
            gethostnameReturn = EventScheduler().searchprocessinfo(ipaddress)
            print "####### gethostnameReturn:", gethostnameReturn
            if gethostnameReturn['Status'] != 'Success':
                return gethostnameReturn
        
            # list of tempprocess
            # {'Status': 'Success', 'Return': {'Status': 'Success', 'process': "{u'ScenServer': 5, u'GatewayServer': 6}"}}
            getSearchHostname = EventScheduler().searchintempprocess(ipaddress)
            print "####### getSearchHostname:", getSearchHostname
            if getSearchHostname['Status'] != 'Success':
                return getSearchHostname
            
            # compare of each process
            # ProcessStandard : gethostnameReturn['Return']['processlist']
            # ProcessTemp : getSearchHostname['Return']['processlist']
            webinputprocesslist = gethostnameReturn['processinfo']
            agentinputprocesslist = eval(getSearchHostname['Return']['process'])

            for key,value in webinputprocesslist.items():
                if key in agentinputprocesslist.keys():
                    if type(value).__name__ == 'long':
                        value = int(value)

                    if value != agentinputprocesslist[key]:
                        self.processCalc[key] = value-agentinputprocesslist[key]
                else:
                    self.processCalc[key] = value
                        
            return dict(Status='Success', compare=self.processCalc)
    
    ''' This method used to change hostname from localhost to localhost_[ipaddress] '''
    def HostnameJudge(self, templatetype, hostname, ipaddress):
        
        newhostname = ""
        
        if templatetype == 'processInform':
            
            if type(hostname).__name__ == 'str' or type(hostname).__name__ == 'unicode':
                if hostname == 'localhost':
                    newhostname = hostname+str(ipaddress)
                else:
                    newhostname = hostname
            else:
                return dict(Status='False', hostname='Hostname must be String.')
        
            return dict(Status='Success', hostname=newhostname, ipaddress=ipaddress)
        
    ''' This method used to get GameID in relation table.'''
    def getGameID(self, ipaddress):
        
        # get Eid
        getEid = EventTransportExpand().searchethdetailfromethdetail(ipaddress)
        if getEid['Status'] != 'Success':
            return getEid
        tmpEid = getEid['eid']
        
        # getEidforall
        getEidforall = EventTransportExpand().searchethinformfromethinform('eth0', tmpEid)
        if getEidforall['Status'] != 'Success':
            return getEidforall
        tmpEidforuse = getEidforall['eid']
        
        # get pserver from eid
        getHid = EventTransportExpand().searchhidfromeid(tmpEidforuse)
        if getHid['Status'] != 'Success':
            return getHid
        tmpHid = getHid['assetid']
        
        # get pserver detail
        getDetailforhid = EventTransportExpand().searchProjectfromHid(tmpHid)
        if getDetailforhid['Status'] != 'Success':
            return getDetailforhid
        tmpProject = getDetailforhid['Project']
        tmpHostName = getDetailforhid['HostName']
        
        # get game detail
        getGamedetail = EventSearch().searchGameIDbyGamename(tmpProject)
        if getGamedetail['Status'] != 'Success':
            return getGamedetail
        tmpGameID = getGamedetail['GameID']
        tmpGamePYname = getGamedetail['GameFullName']
        
        return dict(Status='Success', GameID=tmpGameID, GameName=tmpGamePYname)        
        
        # get ZoneID -> zonetohost
#        getZoneID = EventScheduler().searchzonetohost(hostname)
#        if getZoneID['Status'] != 'Success':
#            return getZoneID
#        zoneID = getZoneID['zoneID']
#        
#        # get GameID -> gamelisttoarea
#        getGameID = EventScheduler().searchgamelisttoarea(zoneID)
#        if getGameID['Status'] != 'Success':
#            return getGameID
#        GameID = getGameID['GameID']
#        
#        # get GameNamae -> GameList
#        getGameName = EventScheduler().searchgameNamebygameID(GameID)
#        if getGameName['Status'] != 'Success':
#            return getGameName
#        GameName = getGameName['Name']
#        
