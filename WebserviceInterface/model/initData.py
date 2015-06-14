# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re
import sys
from model import metadata, DBSession, declarativeBase, thresNumber
from translate import Translate
from base import Packtype, Validate, Compress, Encrypt
from requestobject import AgentList, SwitchList, NodeList
from commandtype import CommandType, CommandTypeRelation
from curves import CURVES
from type import TypeVarify
from Eventoperation import EventOperation
from gamelist import GameList, GameListtoArea, GameGroupRelation
from oidRelation import OidRequest, OIDVariable
from template import Template
from eventRelation import EventRelation, EventInterrlated
from alarmbasic import AlarmGroup, AlarmUser
from alarmRelation import AlarmRelation, ProjecttoGroup
from thresNumber import ThresNumber, ThresRelation
from eventGraderelation import EventGradeRelation
from eventAlarm import EventAlarm, EventLevel
from Eventcircuit import EventCircultStatus
from infocheckGamename import InfoCheckGameName
from process import HostnameToProcess
from eventtransportdefine import EventTransportDefine
from responibility import ResonibilityUser, ResponibilityGroup, ResponibilityRelation

  
def initdata():
 
    # Packtype insert 
    getLength = initcheck(Packtype)
    if int(getLength) == 0:
        DBSession.add(Packtype(0,0,1,1,0))
        DBSession.add(Packtype(1,1,0,1,0))
        DBSession.add(Packtype(2,2,1,1,1))
        DBSession.add(Packtype(3,3,0,1,1))
        DBSession.add(Packtype(4,4,1,0,0))
        DBSession.add(Packtype(5,5,0,0,0))
        DBSession.add(Packtype(6,6,1,0,1))
        DBSession.add(Packtype(7,7,0,0,1))
    
    # CommandType insert
    getCommandLength = initcheck(CommandType)
    if int(getCommandLength) == 0:
        DBSession.add(CommandType(0,'10001','ClientHeartBeatCmd'))
        DBSession.add(CommandType(1,'10002','ServerHeartBeatCmd'))
        DBSession.add(CommandType(2,'11000','ClientLoginCmd'))
        DBSession.add(CommandType(3,'11001','ServerLoginCmd'))
        DBSession.add(CommandType(4,'11100','ClientAllServerInformationCmd'))
        DBSession.add(CommandType(5,'11101','ServerAllServerInformationCmd'))
        DBSession.add(CommandType(10,'11300','ClientNumberofCurves'))
        DBSession.add(CommandType(11,'11301','ServerNumberofCurves'))
        DBSession.add(CommandType(12,'11400','ClientNumberofCurvesPeople'))
        DBSession.add(CommandType(13,'11401','ServerNumberofCurvesPeople'))
        DBSession.add(CommandType(14,'11500','ClientVerifyKeyRequest'))
        DBSession.add(CommandType(15,'11501','ServerVerifyKeyRequest'))
        DBSession.add(CommandType(16,'11600','ClientHistoryofCurvesPeople'))
        DBSession.add(CommandType(17,'11601','ServerHistoryofCurvesPeople'))
        DBSession.add(CommandType(100,'19000','ClientADUserLoginCmd'))
        DBSession.add(CommandType(101,'19001','ServerADUserLoginCmd'))
        DBSession.add(CommandType(110,'19500','ClientCompanySMSCmd'))
        DBSession.add(CommandType(111,'19501','ServerCompanySMSCmd'))
        DBSession.add(CommandType(120,'19800','ClientAutoOCinform'))
        DBSession.add(CommandType(121,'19801','ServerAutoOCinform'))
        DBSession.add(CommandType(150,'20000','PassEvent'))
        DBSession.add(CommandType(151,'20001','PassEventReturn'))
        DBSession.add(CommandType(180,'21000','AlarmUnifity'))
        DBSession.add(CommandType(181,'21001','AlarmUnifityReturn'))
        DBSession.add(CommandType(182,'21100','TestAlarmUnifity'))
        DBSession.add(CommandType(183,'21101','TestAlarmUnifityReturn'))
        DBSession.add(CommandType(190,'30000','CaptureEvent'))
        DBSession.add(CommandType(191,'30001','CaptureEventReturn'))
        DBSession.add(CommandType(200,'31000','EventReceive'))
        DBSession.add(CommandType(201,'31001','EventReturn'))
        DBSession.add(CommandType(202,'31100','TestEventReceive'))
        DBSession.add(CommandType(203,'31101','TestEventReturn'))
        
        
        
    getCommandRelation = initcheck(CommandTypeRelation)
    if int(getCommandRelation) == 0:
        DBSession.add(CommandTypeRelation(0,1,0))
        DBSession.add(CommandTypeRelation(2,101,100))
        DBSession.add(CommandTypeRelation(1,3,2))
        DBSession.add(CommandTypeRelation(3,5,4))
        DBSession.add(CommandTypeRelation(4,11,10))
        DBSession.add(CommandTypeRelation(5,13,12))
        DBSession.add(CommandTypeRelation(6,15,14))
        DBSession.add(CommandTypeRelation(7,17,16))
        DBSession.add(CommandTypeRelation(10,121,120))
        DBSession.add(CommandTypeRelation(11,151,150))
        DBSession.add(CommandTypeRelation(12,111,110))
        DBSession.add(CommandTypeRelation(13,181,180))
        DBSession.add(CommandTypeRelation(14,183,182))
        DBSession.add(CommandTypeRelation(15,201,200))
        DBSession.add(CommandTypeRelation(16,203,202))
        DBSession.add(CommandTypeRelation(17,191,190))
    
    # Validate
    getValidateLength = initcheck(Validate)
    if int(getValidateLength) == 0:
        DBSession.add(Validate(0,'crc32'))
        DBSession.add(Validate(1,'md5'))
     
    # Encrypt    
    getEncryptLength = initcheck(Encrypt)
    if int(getEncryptLength) == 0:
        DBSession.add(Encrypt(0,0,'make encrypt with data'))
        DBSession.add(Encrypt(1,1,'make encrypt without data'))
    
    # Compress
    getCompressLength = initcheck(Compress)
    if int(getCompressLength) == 0:
        DBSession.add(Compress(0,0,'make Zlib with data'))
        DBSession.add(Compress(1,1,'make Zlib without data'))
    
    # Translate    
    getTranslate = initcheck(Translate)
    if int(getTranslate) == 0:
        DBSession.add(Translate(0,'ZR','真如'))
        DBSession.add(Translate(1,'NJ','南京'))
        DBSession.add(Translate(2,'TJ','天津'))
        DBSession.add(Translate(3,'WH','武汉'))
        DBSession.add(Translate(4,'BJ','北京'))
        DBSession.add(Translate(5,'LG','龙岗'))
        DBSession.add(Translate(100,'Agent','服务器'))
        DBSession.add(Translate(101,'Server','服务器'))
        DBSession.add(Translate(102,'Switch','交换机'))
    
    # NodeList
    getNodeList = initcheck(NodeList)
    if int(getNodeList) == 0:
        DBSession.add(NodeList(1,1,'ZR','ZR-Node1-Agent','192.168.82.89',16010,'',1))
        DBSession.add(NodeList(2,1,'ZR','ZR-Node2-Agent','192.168.82.89',16011,'',1))
        DBSession.add(NodeList(3,1,'ZR','ZR-Node3-Agent','192.168.82.89',16012,'',1))
     
    # Type
    getTypes = initcheck(TypeVarify)
    if int(getTypes) == 0:
        DBSession.add(TypeVarify(1,'agentClient',1,0,'from AgentClient pass DATA')) 
        DBSession.add(TypeVarify(2,'agent',1,1,'from Agent pass DATA'))
        DBSession.add(TypeVarify(3,'node',1,0,'from Node pass DATA'))
        DBSession.add(TypeVarify(4,'main',1,0,'from Main pass DATA'))
        DBSession.add(TypeVarify(5,'switch',0,1,'from switch pass DATA'))
        DBSession.add(TypeVarify(6,'interface',1,1,'from interfaceServer pass and receive DATA'))
     
    # GameList
    gameList = initcheck(GameList)
    if int(gameList) == 0:
        DBSession.add(GameList(1,'ZT','征途游戏',1))
        DBSession.add(GameList(2,'web','web社区、充值',0))
        DBSession.add(GameList(4,'JR','巨人游戏',1))
        DBSession.add(GameList(6,'ZTSJB','征途时间版',1))
        DBSession.add(GameList(7,'ZTHJB','征途怀旧版',1))
        DBSession.add(GameList(8,'JRT','巨人双版',1))
        DBSession.add(GameList(10,'WWZW3','万王之王3',1))
        DBSession.add(GameList(11,'JRDD','巨人嘟嘟',1))
        DBSession.add(GameList(12,'XJJH','仙境江湖',1))
        DBSession.add(GameList(14,'HJGD','黄金国度',1))
        DBSession.add(GameList(15,'WDXSG','我的小傻瓜',1))
        DBSession.add(GameList(16,'LH','龙魂',0))
        DBSession.add(GameList(17,'ZT2','征途2',1))
        DBSession.add(GameList(18,'LS','乱世',1))
        DBSession.add(GameList(19,'XT','仙途',1))
        DBSession.add(GameList(20,'LSZT','征途绿色版',1))
        DBSession.add(GameList(22,'JRQZ','巨人前传',0))
        DBSession.add(GameList(24,'JZWM','九州文明',0))
        DBSession.add(GameList(25,'AEZG','艾尔之光',1))
        DBSession.add(GameList(27,'PMZL','飘渺之旅',1))
        DBSession.add(GameList(28,'DDT','弹弹堂',1))
        DBSession.add(GameList(29,'HT','皇途',1))
        DBSession.add(GameList(30,'WSZN','巫师之怒',1))
        DBSession.add(GameList(31,'RXWC','热血王朝',1))
        DBSession.add(GameList(32,'SGZH','三国战魂',1))
        DBSession.add(GameList(33,'RRDZ','绒绒大战',0))
        DBSession.add(GameList(34,'HSWOL','海商王OL',1))
        DBSession.add(GameList(35,'XXSJ','仙侠世界',1))
        DBSession.add(GameList(36,'WS','万神',1))
        DBSession.add(GameList(37,'QJ','千军',1))
        DBSession.add(GameList(1026,'CSJZ','创世九州',1))
        DBSession.add(GameList(1027,'CK','苍空',1))
        DBSession.add(GameList(10000,'Unknown','未知 项目',1))
    
    # EventRelation
    relationEvent = initcheck(EventRelation)
    if int(relationEvent) == 0:
        DBSession.add(EventRelation(1,'1.1.2.2.3.3.4.6',0,'disk,memory'))
        DBSession.add(EventRelation(2,'1.1.6.0.0.1.2.34.21',1,''))
        DBSession.add(EventRelation(3,'1.1.6.0.0.1.2.34.21.1',0,'process'))
        DBSession.add(EventRelation(4,'1.1.6.0.0.1.2.34.21.2',0,'internet'))
        DBSession.add(EventRelation(5,'1.1.6.0.0.1.2.34.21.3',0,'streamlineprocess'))    
        
    # Template
    templates = initcheck(Template)
    if int(templates) == 0:
        DBSession.add(Template(10,'agent发送服务器资产信息','agent','','1.2',30,5,'agent',1))
        DBSession.add(Template(100,'人数曲线','numberofcurves','','1.1.6.0.0.1.2.34.21',30,5,'agent',1))
        DBSession.add(Template(200,'测试','test','','1.1.2.2.3.3.4.6',30,5,'agent',1))
        DBSession.add(Template(300,'进程获取及判断','processInform','','1.1.2.0.1.1.7',30,5,'agent',1))
        
    # OIDrequest
    oidget = initcheck(OidRequest)
    if int(oidget) == 0:
        DBSession.add(OidRequest('1.1.6.0.0.1.2.34.21', 'gameid', 'timepass', 'Y'))
        DBSession.add(OidRequest('1.1.6.0.0.1.2.34.22', 'gameid', 'timestamp', 'N'))
        
    # OIDvariable
    oidvarget = initcheck(OIDVariable)
    if int(oidvarget) == 0:
        DBSession.add(OIDVariable('gameid','String','list','all'))
        DBSession.add(OIDVariable('timepass','Integer','int','5'))
        DBSession.add(OIDVariable('timestamp','Integer','int','1000000000'))
        
    # CURVES 
    getCurves = initcheck(CURVES)
    if int(getCurves) == 0:
        DBSession.add(CURVES(1,'DUDU','192.168.100.171',3315,'InfoServer_DoDo'))   
        
    # alarmuser
    getAlarmuser = initcheck(AlarmUser)
    if int(getAlarmuser) == 0:
        DBSession.add(AlarmUser(0,'majian',1,'majian@ztgame.com','13817992612','majian@ztgame.com'))
        DBSession.add(AlarmUser(1,'feijun',1,'feijun@ztgame.com','18616193305','feijun@ztgame.com'))
        DBSession.add(AlarmUser(2,'jiangchao',0,'jiangchao@ztgame.com','13601674151','jiangchao@ztgame.com'))
        DBSession.add(AlarmUser(3,'zhaoyu',1,'zhaoyu@ztgame.com','13671733680','zhaoyu@ztgame.com'))
        DBSession.add(AlarmUser(4,'changzonghui',1,'changzonghui@ztgame.com','18623759189','changzonghui@ztgame.com'))
        
    # alarmgroup
    getAlarmgroup = initcheck(AlarmGroup)
    if int(getAlarmgroup) == 0:
        DBSession.add(AlarmGroup(0,'新业务',1,1))
        DBSession.add(AlarmGroup(1,'其它',-1,1))
        DBSession.add(AlarmGroup(2,'基础运维',1,0))
        DBSession.add(AlarmGroup(3,'监控值班',-1,1))
        DBSession.add(AlarmGroup(10,'征途II项目组',1,1))
        
    # projecttogroup
    getprojecttogroup = initcheck(ProjecttoGroup)
    if int(getprojecttogroup) == 0:
        DBSession.add(ProjecttoGroup(0,32,0))
        DBSession.add(ProjecttoGroup(1,14,2))
        DBSession.add(ProjecttoGroup(2,17,10))
        
    # alarmRelation
    getAlarmrelation = initcheck(AlarmRelation)
    if int(getAlarmrelation) == 0:
        DBSession.add(AlarmRelation(0,0,5,0))
        DBSession.add(AlarmRelation(1,1,1,0))
        DBSession.add(AlarmRelation(2,1,5,1))
        DBSession.add(AlarmRelation(3,2,1,2))
        DBSession.add(AlarmRelation(4,3,5,0))
        DBSession.add(AlarmRelation(5,3,1,1))
        DBSession.add(AlarmRelation(6,4,5,0))
        DBSession.add(AlarmRelation(7,0,4,10))
        DBSession.add(AlarmRelation(8,1,4,10))
        DBSession.add(AlarmRelation(9,2,4,10))
        DBSession.add(AlarmRelation(10,3,4,10))
        
    # thresRelation
    getthresRelation = initcheck(ThresRelation)
    if int(getthresRelation) == 0:
        DBSession.add(ThresRelation(0,10,'processlist',0))
        DBSession.add(ThresRelation(1,32,'numberofcurves',2))
        DBSession.add(ThresRelation(2,32,'processlist',3))
        DBSession.add(ThresRelation(3,36,'numberofcurves',4))
        DBSession.add(ThresRelation(4,36,'areajudge',5))
        DBSession.add(ThresRelation(5,32,'areajudge',6))
        DBSession.add(ThresRelation(6,17,'numberofcurves',11))
        DBSession.add(ThresRelation(7,17,'areajudge',10))

    # thresNumber
    getthresnumber = initcheck(ThresNumber)
    if int(getthresnumber) == 0:
        DBSession.add(ThresNumber(2,1,'10000','10%'))
        DBSession.add(ThresNumber(3,5,'1000','50%'))
        DBSession.add(ThresNumber(4,5,'5000','15%'))
        DBSession.add(ThresNumber(5,5,'10000','20%'))
        DBSession.add(ThresNumber(6,3,'10000','25%'))
        DBSession.add(ThresNumber(10,3,'10000','35%'))
        DBSession.add(ThresNumber(11,3,'10','0%'))
        
    # eventRelationof Grade
    geteventgrade = initcheck(EventGradeRelation)
    if int(geteventgrade) == 0:
        DBSession.add(EventGradeRelation(-1, 1, 0, 0))
        DBSession.add(EventGradeRelation(1, 1, 1, 1))
        DBSession.add(EventGradeRelation(2, 1, 1, 1))
        DBSession.add(EventGradeRelation(3, 1, 0, 1))
        DBSession.add(EventGradeRelation(4, 1, 0, 1))
        DBSession.add(EventGradeRelation(5, 1, 0, 0))
        
    # EventCircultStatus Basic
    getcircultStatus = initcheck(EventCircultStatus)
    if int(getcircultStatus) == 0:
        DBSession.add(EventCircultStatus(0,'未处理'))
        DBSession.add(EventCircultStatus(1,'已分派'))
        DBSession.add(EventCircultStatus(2,'已接手'))
        DBSession.add(EventCircultStatus(3,'已处理'))
        DBSession.add(EventCircultStatus(4,'已验收'))
        DBSession.add(EventCircultStatus(5,'已结束'))
        DBSession.add(EventCircultStatus(6,'已作废'))
        DBSession.add(EventCircultStatus(7,'已回滚'))
        DBSession.add(EventCircultStatus(10,'已归档'))
        
    # change infoserver name 
    getinfoservername = initcheck(InfoCheckGameName)
    if int(getinfoservername) == 0:
        DBSession.add(InfoCheckGameName('NULL','ZT')) 
        DBSession.add(InfoCheckGameName('JR','JR'))
        DBSession.add(InfoCheckGameName('HuaiJiu','ZTHJB'))
        DBSession.add(InfoCheckGameName('KOK3','WWZW3'))
        DBSession.add(InfoCheckGameName('XSG','WDXSG'))
        DBSession.add(InfoCheckGameName('DoDo','JRDD'))
        DBSession.add(InfoCheckGameName('HuangJin','HJGD'))
        DBSession.add(InfoCheckGameName('XT','XT'))
        DBSession.add(InfoCheckGameName('ZTLS','LSZT'))
        DBSession.add(InfoCheckGameName('XSG_ALL','XSG'))
        DBSession.add(InfoCheckGameName('LH','LH'))
        DBSession.add(InfoCheckGameName('ZTII','ZT2'))
        DBSession.add(InfoCheckGameName('LS','LS'))
        DBSession.add(InfoCheckGameName('DDT','DDT'))
        DBSession.add(InfoCheckGameName('ELS','AEZG'))
        DBSession.add(InfoCheckGameName('TKZC','XJJH'))
        DBSession.add(InfoCheckGameName('SGZH','SGZH'))
        DBSession.add(InfoCheckGameName('WSZN','WSZN'))
        DBSession.add(InfoCheckGameName('WS','WS'))
        DBSession.add(InfoCheckGameName('XXSJ','XXSJ'))
        DBSession.add(InfoCheckGameName('CSJZ','CSJZ'))
        DBSession.add(InfoCheckGameName('360','QJ'))
        DBSession.add(InfoCheckGameName('CK','CK'))
        
    # process hostname
    getprocessofhostname = initcheck(HostnameToProcess)
    if int(getprocessofhostname) == 0:
        DBSession.add(HostnameToProcess(1, 'ZR-Agent-4.x-test', 'GateServer5'))
        DBSession.add(HostnameToProcess(2, 'ZR-Agent-4.x-test', 'GateServer3'))
        DBSession.add(HostnameToProcess(3, 'ZR-Agent-4.x-test', 'GateServer2'))
        DBSession.add(HostnameToProcess(4, 'ZR-Agent-4.x-test', 'GateServer8'))
        DBSession.add(HostnameToProcess(5, 'ZR-Agent-4.x-test', 'GateServer1'))
        DBSession.add(HostnameToProcess(6, 'ZR-Agent-4.x-test', 'CharServer10'))
        DBSession.add(HostnameToProcess(7, 'ZR-Agent-4.x-test', 'CharServer11'))
        DBSession.add(HostnameToProcess(8, 'ZR-Agent-4.x-test', 'CharServer14'))
        DBSession.add(HostnameToProcess(9, 'ZR-Agent-4.x-test', 'CharServer12'))
        DBSession.add(HostnameToProcess(10, 'ZR-Agent-4.x-test', 'CharServer13'))
        DBSession.add(HostnameToProcess(11, 'ZR-Agent-4.x-test', 'LoginServer'))
        DBSession.add(HostnameToProcess(12, 'ZR-Agent-4.x-test', 'LogServer'))
        
    # Event Level
    geteventlevel = initcheck(EventLevel)
    if int(geteventlevel) == 0:
        DBSession.add(EventLevel(0, '保留位'))
        DBSession.add(EventLevel(1, '重大事件'))
        DBSession.add(EventLevel(2, '特大事件'))
        DBSession.add(EventLevel(3, '高级事件'))
        DBSession.add(EventLevel(4, '中级事件'))
        DBSession.add(EventLevel(5, '低级事件'))
        DBSession.add(EventLevel(6, '普通事件'))
        
    # Game to Group addition
    getgametogroup = initcheck(GameGroupRelation)
    if int(getgametogroup) == 0:
        DBSession.add(GameGroupRelation(1,17,0))
        DBSession.add(GameGroupRelation(2,18,1))
   
    # Event operation
    geteventoperation = initcheck(EventOperation)
    if int(geteventoperation) == 0:
        DBSession.add(EventOperation(0,'ALLControl','全部操作权限'))
        DBSession.add(EventOperation(1,'PartView','部分查看权限'))
        DBSession.add(EventOperation(2,'PartSelect','部分查询权限'))
        
    # Event transport define
    geteventtransportdefine = initcheck(EventTransportDefine)
    if int(geteventtransportdefine) == 0:
        DBSession.add(EventTransportDefine(0,0,-1,-1,1,-1))
        DBSession.add(EventTransportDefine(1,0,-1,-1,2,-1))
        DBSession.add(EventTransportDefine(2,1,2,0,3,-1))
        DBSession.add(EventTransportDefine(3,2,1,0,3,-1))
        DBSession.add(EventTransportDefine(4,3,-1,1,4,1))
        DBSession.add(EventTransportDefine(5,3,-1,1,6,1))
        DBSession.add(EventTransportDefine(6,4,-1,3,5,1))
        DBSession.add(EventTransportDefine(7,4,-1,3,6,1))
        DBSession.add(EventTransportDefine(8,5,-1,4,10,1))
        DBSession.add(EventTransportDefine(9,6,-1,3,10,-1))
        DBSession.add(EventTransportDefine(10,6,-1,4,10,-1))
        DBSession.add(EventTransportDefine(11,10,-1,5,100,-1))
        DBSession.add(EventTransportDefine(12,10,-1,6,100,-1))
        DBSession.add(EventTransportDefine(100,100,-1,-1,-1,-1))
        
    # responibility user
    getresponibilityuser = initcheck(ResonibilityUser)
    if int(getresponibilityuser) == 0:
        DBSession.add(ResonibilityUser(0,1,'jiangchao','姜超',13601674151,'jiangchao@ztgame.com','jiangchao@ztgame.com','运维负责人','True'))
        DBSession.add(ResonibilityUser(1,1,'changzonghui','常宗辉',18623759189,'changzonghui@ztgame.com','changzonghui@ztgame.com','运维人员','False'))
        DBSession.add(ResonibilityUser(2,1,'majian','赵俊杰',13817992612,'majian@ztgame.com','majian@ztgame.com','运维人员','False'))
        
    # responibility group
    getresponibilitygroup = initcheck(ResponibilityGroup)
    if int(getresponibilitygroup) == 0:
        DBSession.add(ResponibilityGroup(1,'yunwei','运维部'))

    # responibility relation
    getresponibilityrelation = initcheck(ResponibilityRelation)
    if int(getresponibilityrelation) == 0:
        DBSession.add(ResponibilityRelation(1,300,1))
        
    DBSession.commit()
    
        
# used to check instance count
def initcheck(Tableinstance):
    
    getfromSearch = DBSession.query(Tableinstance).all()
    
    return len(getfromSearch)
