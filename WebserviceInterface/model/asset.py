# -*- coding: utf-8 -*-
''' @author : majian'''

import os
import sys
from model import metadata, DBSession, declarativeBase
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Boolean
from sqlalchemy.orm import relation, synonym
from sqlalchemy.schema import Index

__all__ = ['ASSET']

class ASSET(declarativeBase):
    __tablename__ = 'asset'
    
    # Columns
    #id               配置编号                               分类号                              资产编号                          使用属性                            核算项目                            主机名                                   内网                                    外网                                      存储网                                    使用人                                    机架位置                         zcbm                 使用人id            所属机房                            用途                                 是否使用中（Y/N）
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, default=0)   # id
    confNum = Column(Integer, nullable=False, default=0)                       # 配置编号
    partNum = Column(Unicode(50), nullable=True, default=u'None')                           # 分类号
    serialNum = Column(String(50), nullable=True, default=u'None')                          # 资产编号
    useProperty = Column(Unicode(50), nullable=False, default=u'None')                      # 使用属性
    conProject = Column(Unicode(255), nullable=False, default=u'None')                       # 核算项目
    hostname = Column(String(50), nullable=False, default=u'localhost')                     # 主机名
    companyIp = Column(String(32), nullable=False, default=u'None')                         # 内网
    outIp = Column(String(32), nullable=False, default=u'None')                             # 外网
    storeIp = Column(String(32), nullable=False, default=u'None')                           # 存储网
    username = Column(String(20), nullable=False, default=u'None')                          # 使用人
    rackPosition = Column(Unicode(50), nullable=False, default=u'None')                     # 机架位置
    zcbm = Column(Integer, nullable=True)                                                   # ZCBM
    userId = Column(Unicode(20), nullable=True)                                                 # 使用人工号
    machineRoom = Column(Unicode(50), nullable=False, default=u'None')                      # 机房
    usage = Column(Unicode(50), nullable=False, default=u'None')                            # 用途
    useNow = Column(String(2), nullable=False, default=u'N')                                # 是否在使用中
    
    def __init__(self, id, confNum, partNum, serialNum, useProperty, conProject, hostname, companyIp, outIp, storeIp, username, rackPostion, zcbm, userId, machineRoom, usage, useNow):
        
        self.id = id
        self.confNum = confNum
        self.partNum = partNum
        self.serialNum = serialNum
        self.useProperty = useProperty
        self.conProject = conProject
        self.hostname = hostname
        self.companyIp = companyIp
        self.outIp = outIp
        self.storeIp = storeIp
        self.username = username
        self.rackPosition = rackPostion
        self.zcbm = zcbm
        self.userId = userId
        self.machineRoom = machineRoom
        self.usage = usage
        self.useNow = useNow
        
    def __repr__(self):
        
        return '<ASSET: id="%s", confNum="%s", partNum="%s", serialNum="%s", useProperty="%s", conProject="%s", hostname="%s", companyIp="%s", outIp="%s", storeIp="%s", username="%s", rackPosition="%s", zcbm="%s", userId="%s", machineRoom="%s", usage="%s", useNow="%s">' % (self.id, self.confNum, self.partNum, self.serialNum, self.useProperty, self.conProject, self.hostname, self.companyIp, self.outIp, self.storeIp, self.username, self.rackPosition, self.zcbm, self.userId, self.machineRoom, self.usage, self.useNow)
    