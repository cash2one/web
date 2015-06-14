# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re
import sys

from sqlalchemy import and_, or_
from model import metadata, DBSession, declarativeBase
from model.asset import ASSET
from model.translate import Translate
from model.requestobject import AgentList, SwitchList
from model.methods.getNode import calcNode
from model.methods.assignmechanism import Assign
from model.methods.connection import Connection
from interface.localAsset import AssetInformation
from Tkconstants import ALL

class allRequestObject:
    
    def __init__(self):
        
        self.Relationship = []
    
    def transportData(self, machineroomSimple, data):
        
        allAgent = DBSession.query(AgentList).all()
        allSwitch = DBSession.query(SwitchList).all()
        
        self.flushAgent(machineroomSimple)
        
    def flushAgent(self,  machineroomSimple, Agent='Agent'):
        
        try:
            getSearchAgent = DBSession.query(Translate).filter_by(simple = Agent).first()
            AgentSimple = getSearchAgent.detail
            
            getSearchMachineroom = DBSession.query(Translate).filter_by(simple = machineroomSimple).first()
            MrDetail = getSearchMachineroom.detail
            
            getAgentList = AssetInformation().searchObject(MrDetail, AgentSimple)

            print "######## LEN ", len(getAgentList['Return'])

            for key,value in getAgentList['Return'].items():
                AgentID = key
                AgentZone = machineroomSimple
                AgentName = value['hostname']
                IP = self.iprule(key, machineroomSimple, value['companyIp'], value['outIp'], value['storeIp'])
                Port = 'NULL'
                IsUse = 1
            
            
        except Exception, e:
            return e
        
        
    def iprule(self, Agentid, machineroomSimple, companyIp, outIp, storeIp):
        
        # get node detail information
        getNodeReturn = calcNode().analyNode(machineroomSimple)

        # sort of node
        getNodeReturnbySort = calcNode().sortNode(getNodeReturn)

        # get node counts
        NodeCount = len(getNodeReturnbySort)
        
        # Math node to agent
        agentTonode = Assign().Math(Agentid, NodeCount)
        
        # Relationship between agent to node
        relationship = Assign().relationship(agentTonode, getNodeReturnbySort)
        print "#### relationship", relationship

        # use node search agent connection use main (Not Fullin)
        Connection().getNodeAgent("1")
        # get result to get all search then choose one result ipaddress  -> Return
        
        
#allRequestObject().flushAgent('ZR')       
    #def flushSwitch(self, machineroomSimple, Switch='Switch'):