# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys

from model import DBSession, metadata, declarativeBase
from model.requestobject import AgentList, NodeList


class calcNode:
    
    def __init__(self):
        
        self.Nodeinform = {}
    
    def analyNode(self, AgentZone):

        try:
            getNodeInform = DBSession.query(NodeList).filter_by(NodeZone = AgentZone).all()
            if getNodeInform:
                for eachNodeInform in range(len(getNodeInform)):
                    self.Nodeinform[getNodeInform[eachNodeInform].NodeID]=dict(NodeType=getNodeInform[eachNodeInform].NodeType, NodeZone=getNodeInform[eachNodeInform].NodeZone, NodeName=getNodeInform[eachNodeInform].NodeName, IP=getNodeInform[eachNodeInform].IP, Port=getNodeInform[eachNodeInform].Port)
            else:
                msg = 'MySQLdb : select from table.nodelist error.'
                return msg
      
        except Exception, e:
            return e
        
        return self.Nodeinform
    
    def sortNode(self, nodeDict):
        
        keys = nodeDict.keys()
        keys.sort()
        
        return map(nodeDict.get,keys)