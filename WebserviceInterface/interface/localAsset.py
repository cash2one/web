# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys

from model.asset import ASSET
from model import metadata, DBSession, declarativeBase
from sqlalchemy import and_

class AssetInformation:
    
    def __init__(self):
        
        self.allLineofConfnum = ""
        self.allLineofCompany = ""
        self.allLineofZcbm = ""
        self.reBack = {}
        self.assetBack = {}
    
    def FromConfNum(self, confNum):
        
        Attitude = ""
        ServerInform = {}
        Internet = {}
        Device = {}
        
        try:
            self.allLineofConfnum = DBSession.query(ASSET).filter_by(confNum = confNum).first()
            print self.allLineofConfnum
            
            if self.allLineofConfnum:
                
                # All information collect
                Attitude = self.allLineofConfnum.useNow
                      
                Device['confNum'] = self.allLineofConfnum.confNum
                Device['partNum'] = self.allLineofConfnum.partNum
                Device['serialNum'] = self.allLineofConfnum.serialNum
                Device['zcbm'] = self.allLineofConfnum.zcbm
                Device['machineRoom'] = self.allLineofConfnum.machineRoom
                
                ServerInform['useProperty'] = self.allLineofConfnum.useProperty
                ServerInform['conProject'] = self.allLineofConfnum.conProject
                ServerInform['username'] = self.allLineofConfnum.username
                ServerInform['userId'] = self.allLineofConfnum.userId
                ServerInform['usage'] = self.allLineofConfnum.usage
                
                Internet['hostname'] = self.allLineofConfnum.hostname
                Internet['companyIp'] = self.allLineofConfnum.companyIp
                Internet['outIp'] = self.allLineofConfnum.outIp
                Internet['storeIp'] = self.allLineofConfnum.storeIp
                
                return dict(State=Attitude, Device=Device, ServerInform=ServerInform, Internet=Internet)
                
            else:
                msg = 'MySQLdb : could not found any confNum.'
                return msg
        
        except Exception, e:
            msg = e
            return msg

    def FromCompanyIp(self, companyIp):
        
        Attitude = ""
        ServerInform = {}
        Internet = {}
        Device = {}
        
        try:
            self.allLineofCompany = DBSession.query(ASSET).filter_by(companyIp = companyIp).first()
            
            if self.allLineofCompany:
                
                # All information collect
                Attitude = self.allLineofCompany.useNow
                      
                Device['confNum'] = self.allLineofCompany.confNum
                Device['partNum'] = self.allLineofCompany.partNum
                Device['serialNum'] = self.allLineofCompany.serialNum
                Device['zcbm'] = self.allLineofCompany.zcbm
                Device['machineRoom'] = self.allLineofCompany.machineRoom
                
                ServerInform['useProperty'] = self.allLineofCompany.useProperty
                ServerInform['conProject'] = self.allLineofCompany.conProject
                ServerInform['username'] = self.allLineofCompany.username
                ServerInform['userId'] = self.allLineofCompany.userId
                ServerInform['usage'] = self.allLineofCompany.usage
                
                Internet['hostname'] = self.allLineofCompany.hostname
                Internet['companyIp'] = self.allLineofCompany.companyIp
                Internet['outIp'] = self.allLineofCompany.outIp
                Internet['storeIp'] = self.allLineofCompany.storeIp
                
                return dict(State=Attitude, Device=Device, ServerInform=ServerInform, Internet=Internet)
                
            else:
                msg = 'MySQLdb : could not found any confNum.'
                return msg
        
        except Exception, e:
            msg = e
            return msg
        
    def Fromzcbm(self, zcbm):
        
        Attitude = ""
        ServerInform = {}
        Internet = {}
        Device = {}
        
        try:
            self.allLineofZcbm = DBSession.query(ASSET).filter_by(zcbm = zcbm).first()
            
            if self.allLineofZcbm:
                
                # All information collect
                Attitude = self.allLineofZcbm.useNow
                      
                Device['confNum'] = self.allLineofZcbm.confNum
                Device['partNum'] = self.allLineofZcbm.partNum
                Device['serialNum'] = self.allLineofZcbm.serialNum
                Device['zcbm'] = self.allLineofZcbm.zcbm
                Device['machineRoom'] = self.allLineofZcbm.machineRoom
                
                ServerInform['useProperty'] = self.allLineofZcbm.useProperty
                ServerInform['conProject'] = self.allLineofZcbm.conProject
                ServerInform['username'] = self.allLineofZcbm.username
                ServerInform['userId'] = self.allLineofZcbm.userId
                ServerInform['usage'] = self.allLineofZcbm.usage
                
                Internet['hostname'] = self.allLineofZcbm.hostname
                Internet['companyIp'] = self.allLineofZcbm.companyIp
                Internet['outIp'] = self.allLineofZcbm.outIp
                Internet['storeIp'] = self.allLineofZcbm.storeIp
                
                return dict(State=Attitude, Device=Device, ServerInform=ServerInform, Internet=Internet)
                
            else:
                msg = 'MySQLdb : could not found any confNum.'
                return msg
        
        except Exception, e:
            msg = e
            return msg
        
    def searchObject(self, machineroom, requestobject):
        
        try:
            allsearch = DBSession.query(ASSET).filter(and_(ASSET.partNum.like("%"+requestobject+"%"), ASSET.machineRoom.like("%"+machineroom+"%"), ASSET.useNow == 'Y')).all()

            for eachAsset in range(len(allsearch)):
                self.assetBack[allsearch[eachAsset].id] = dict(confNum=allsearch[eachAsset].confNum, serialNum=allsearch[eachAsset].serialNum, hostname=allsearch[eachAsset].hostname, companyIp=allsearch[eachAsset].companyIp, outIp=allsearch[eachAsset].outIp, storeIp=allsearch[eachAsset].storeIp, zcbm=allsearch[eachAsset].zcbm)
             
        except Exception, e:
            return dict(Status='false', Return=e)
        
        return dict(Status='success', Return=self.assetBack)    
        