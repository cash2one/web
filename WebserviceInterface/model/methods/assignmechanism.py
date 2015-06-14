# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys

class Assign:
    
    def __init__(self):
        
        self.agentid = ""
        self.nodeIndex = ""        
        self.belong = {}
        self.getRelation = {}
    
    def Math(self, Agentid, Nodecount):
        
        NodeIndex = int(Agentid) % int(Nodecount)

        self.belong[NodeIndex] = int(Agentid)
        
        return self.belong
    
    def relationship(self, agentTonode, nodeSort):
        
        # analyst agent and node relation
        getAnalyst = self.analystAgentidandNodeIndex(agentTonode)
        Agentid = getAnalyst['agentid']
        NodeIndex = getAnalyst['nodeindex']
        
        # write agent to node detail
        self.getRelation[Agentid] = nodeSort[NodeIndex]
        
        return self.getRelation
        
            
    def analystAgentidandNodeIndex(self, agentTonode):
        
        for key,value in agentTonode.items():
            self.nodeIndex = key
            self.agentid = value
            
        return dict(agentid = self.agentid, nodeindex = self.nodeIndex)