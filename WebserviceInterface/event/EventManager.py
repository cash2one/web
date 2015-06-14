# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time
import pdb

from ServiceConfig.config import readFromConfigFile
from interface.collection.dbconnect import Connect 
from BaseClass.verifityDependence import changeDict, ListCount

from EventScheduler import EventScheduler

class Manager:
    
    def __init__(self):
        
        self.Return = {}
        self.Returnlist = []
        self.mainserver = {}
        
    def ManagerDecide(self, message, oidName):
        
        count = 0
        ''' Process monitor 
        message input : {
                 'Info': 'None', 
                 'Status': 'Success', 
                 'OID': '1.1.2.0.1.1.7', 
                 'JobID': '5', 
                 'Result': "{u'GateServer5': u'GateServer5', u'GateServer3': u'GateServer3', 
                             u'GateServer2': u'GateServer2', u'CharServer10': u'CharServer10', 
                             u'CharServer11': u'CharServer11', u'GateServer1': u'GateServer1', 
                             u'CharServer14': u'CharServer14', u'LogServer': u'LogServer', 
                             u'GateServer8': u'GateServer8', u'LoginServer': u'LoginServer', 
                             u'CharServer12': u'CharServer12', u'CharServer13': u'CharServer13'
                            }", 
                'Type': 'agent', 
                'ID': '1', 
                'SendTime': '1363848874'
                }
        Step 1. get connect with MainServer Database
        Step 2. search in eachTable
        Step 3. get each Result
        Step 4. judge host is used in table 
        Step 5. insert into Temp table
        '''
        if oidName == 'processInform':
            # Step 1. 
            getMainServerconfig = readFromConfigFile().get_config_mainserver()
            for key,value in getMainServerconfig.items():
                if key == 'MainServer':
                    for eachElement in value:
                        if eachElement[0] == 'username':
                            self.mainserver['username'] = eachElement[1]
                        elif eachElement[0] == 'ip':
                            self.mainserver['ipaddress'] = eachElement[1]
                        elif eachElement[0] == 'port':
                            self.mainserver['port'] = int(eachElement[1])
                        elif eachElement[0] == 'password':
                            self.mainserver['password'] = eachElement[1]
                        elif eachElement[0] == 'dbname':
                            self.mainserver['dbname'] = eachElement[1]
        
            (mainConnect, mainCursor) = Connect().create(self.mainserver)
        
            # Step 2.
            for eachKey,eachValue in message.items():
                if eachKey == 'Type':
                    if eachValue == 'agent':
                        self.tablename = 'AgentList'
                        self.columname = 'AgentID'
                    elif eachValue == 'switch':
                        self.tablename = 'SwitchList'
                        self.columname = 'SwitchID'
                    elif eachValue == 'Node':
                        self.tablename = 'NodeList'
                        self.columname = 'NodeID'
             
            # Step 3. 
            try:
                cmd = "select * from %s where %s = %s" % (self.tablename, self.columname, message['ID'])
                mainCursor.execute(cmd)
                searchResult = mainCursor.fetchone()
            
            # Step 4.
                if int(searchResult[6]) == 1:
                    self.Return['MachineRoom'] = searchResult[1]
                    self.Return['Hostname'] = searchResult[2]
                    self.Return['Ipaddress'] = searchResult[3]
                
                elif int(searchResult[6]) == 0:
                    msg = "%s is Unused." % searchResult[3]
                    return dict(Status='False', msg=msg)
        
            except Exception, e:
                return dict(Status='False', msg=str(e))

            # Step 5. 
            if type(message['Result']).__name__ != 'dict':
                body = changeDict().strtodict(message['Result'])
            else:
                body = message['Result']
            
            if len(body['Process']) != 0:
                for key,value in body.items():
                    if key and key != '':
                        context = ListCount().base(value)
                        getSearchofEvent = EventScheduler().Searchinformintempprocess(self.Return['Ipaddress'], str(context), message['SendTime'])
                        count += 1
                
                if count == int(len(body)):
                    return dict(Status='Success', Return=self.Return)
                else:
                    msg = 'insert into temptable.tempprocess failed.'
                    return dict(Status='False', msg=msg)
            else:
                msg = 'body is None. Exit.'
                return dict(Status='False', msg=msg)
            
    def getfromMain(self, message):
        
        # Step 1. 
        getMainServerconfig = readFromConfigFile().get_config_mainserver()
        for key,value in getMainServerconfig.items():
            if key == 'MainServer':
                for eachElement in value:
                    if eachElement[0] == 'username':
                        self.mainserver['username'] = eachElement[1]
                    elif eachElement[0] == 'ip':
                        self.mainserver['ipaddress'] = eachElement[1]
                    elif eachElement[0] == 'port':
                        self.mainserver['port'] = int(eachElement[1])
                    elif eachElement[0] == 'password':
                        self.mainserver['password'] = eachElement[1]
                    elif eachElement[0] == 'dbname':
                        self.mainserver['dbname'] = eachElement[1]
        
        (mainConnect, mainCursor) = Connect().create(self.mainserver)
        
        # Step 2. create define
        Tablename = 'AgentList'
        Columname = 'AgentID'
        
        # Step 3. try to get ipdetail
        try:
            tmpcount = 0
            
            if type(message['Result']).__name__ != 'dict':
                newbody = changeDict().strtodict(message['Result'])
            else:
                newbody = message['Result']
            
            for keys,values in newbody.items():
                
                if type(keys).__name__ != 'int':
                    keys = int(keys)
                
                cmd = "select * from %s where %s = %s" % (Tablename, Columname, keys)
                mainCursor.execute(cmd)
                searchResult = mainCursor.fetchone()
                
                if int(searchResult[6]) == 1:
                    self.Returnlist.append(searchResult[3])
                    tmpcount += 1
                   
            if tmpcount != len(self.Returnlist):
                Connect().drop(mainConnect, mainCursor)
                return dict(Status='False', msg='mainserver passed Data Error.')
            else:
                Connect().drop(mainConnect, mainCursor)
                return dict(Status='Success', iplist=self.Returnlist)
            
        except Exception, e:
            Connect().drop(mainConnect, mainCursor)
            return dict(Status='False',msg='mainserver passed Data Error.') 
        