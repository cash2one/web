# -*- coding: utf-8 -*-
''' @author : majian'''
import chardet

from sqlalchemy import and_, or_, desc
from BaseClass.timeBasic import TimeBasic

from model.__cmdbinit__ import cmetadata, CMDBSession, cmdeclarativeBase

from model.Practicalusing.UnifiedURL import UnifiedURL
from model.Practicalusing.unifiedDnsIp import UnifiedDNSIP
from model.Practicalusing.URLtoDNS import URLtoDNS
from model.Practicalusing.SplicingURL import SpliceURL
from model.Practicalusing.counterlist import CounterList
from model.advertising.tmpSolvePerson import TmpSolvePerson
from model.advertising.Returnvaluedefine import ReturnValuedefine
from model.advertising.URL_advertisingarrival import AdvertisingArrival
from model.advertising.result import ResultADUrl, ResultFastReg, ResultCounterStatus

class BasicSearch:
    
    def __init__(self):
        
        self.returns = ""
        
    def searchaliveinadvertising(self, Status=1):
        
        tmplist = []
        
        try:
            getSearchinadvertising = CMDBSession.query(AdvertisingArrival).filter_by(Status=Status).all()

            if getSearchinadvertising:
                for eachline in getSearchinadvertising:
                    starttime = TimeBasic().timeControl(eachline.StartTimestamp, 5)
                    overtime = TimeBasic().timeControl(eachline.OverTimestamp, 5)
                    tmplist.append(dict(url=eachline.url, starttime=starttime, overtime=overtime, project=eachline.Project, pagealias=eachline.pagealias))
                    
                return dict(Status='Success', list=tmplist)
                
            else:
                msg = 'MySQL could not found any information in database.'
                CMDBSession.rollback()
                return dict(Status='False', msg=msg)
            
        except Exception, e:
            CMDBSession.rollback()
            return dict(Status='False', msg=str(e))
        
    def searchaliveprojectofadvertising(self, project, Status=1):
        
        tmplist = []
        
        try:
            getSearchofadveristingofproject = CMDBSession.query(AdvertisingArrival).filter(and_(AdvertisingArrival.Project == project, AdvertisingArrival.Status == 1)).all()
            
            if getSearchofadveristingofproject:
                for eachline in getSearchofadveristingofproject:
                    starttime = TimeBasic().timeControl(eachline.StartTimestamp, 5)
                    overtime = TimeBasic().timeControl(eachline.OverTimestamp, 5)
                    tmplist.append(dict(url=eachline.url, starttime=starttime, overtime=overtime, project=eachline.Project, pagealias=eachline.pagealias))
                    
                return dict(Status='Success', list=tmplist)
            else:
                msg = 'MySQL could not found any information in database about project %s.' % (project)
                CMDBSession.rollback()
                return dict(Status='False', msg=msg)
            
        except Exception, e:
            CMDBSession.rollback()
            return dict(Status='False', msg=str(e))
        
    def addintoadurl(self, url, starttime, overtime, status, project, pagealias):
        
        try:
            getSearchinexist = CMDBSession.query(AdvertisingArrival).filter_by(url = url).first()
            
            if getSearchinexist:
                getSearchinexist.StartTimestamp = starttime
                getSearchinexist.OverTimestamp = overtime
                getSearchinexist.Status = status
                getSearchinexist.Project = project
                getSearchinexist.pagealias = pagealias
            else:
                CMDBSession.add(AdvertisingArrival(url, starttime, overtime, status, project, pagealias))
            
        except Exception, e:
            CMDBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        CMDBSession.commit()
        return dict(Status='Success')
    
    def deladurl(self, url):
        
        try:
            ''' 1. del url & starttime '''
            getdeladurl = CMDBSession.query(AdvertisingArrival).filter(AdvertisingArrival.url == url).first()
            
            if getdeladurl:
                getdeladurl.Status = 0
            else:
                CMDBSession.rollback()
                return dict(Status='False', msg='Input url and starttime is not Exist. Please check.')
            
            ''' 2. del url in table.resultadurl. '''
            getdelseultadurl = self.delresultadurl(url)
            if getdelseultadurl['Status'] != 'Success':
                return getdelseultadurl
                        
        except Exception, e:
            CMDBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        CMDBSession.commit()
        return dict(Status='Success')
    
    def hideadurl(self, starttime):
        
        try:
            gethideurl = CMDBSession.query(AdvertisingArrival).filter(AdvertisingArrival.OverTimestamp < starttime).all()
            
            if gethideurl:
                for eachline in gethideurl:
                    eachline.Status = 0
            else:
                return dict(Status='Success')
            
        except Exception, e:
            CMDBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        CMDBSession.commit()
        return dict(Status='Success')
    
    def delresultadurl(self, url):
        
        try:
            getresultadurl = CMDBSession.query(ResultADUrl).filter_by(url = url).first()
            
            if getresultadurl:
                CMDBSession.delete(getresultadurl)
            else:
                return dict(Status='False', msg='MySQL could not found any detail in table.resultadurl.')
            
        except Exception, e:
            CMDBSession.rollback()
            return dict(Status='False', msg=str(e))

        CMDBSession.commit()
        return dict(Status='Success')
    
    def searchunifiedurl(self, category):
        
        tmpDict = {}
        
        try:
            getsearchofunifiedurl = CMDBSession.query(UnifiedURL).filter_by(Category=category).first()
            
            if getsearchofunifiedurl:
                if getsearchofunifiedurl.Status != 0:
                    tmpDict['id'] = getsearchofunifiedurl.id
                    tmpDict['Url'] = getsearchofunifiedurl.Url
                    tmpDict['Urlexplain'] = getsearchofunifiedurl.Urlexplain
                else:
                    msg = 'The URL: %s is not used Now.' % (getsearchofunifiedurl.Url)
                    return dict(Status='False', msg=msg)
                
                return dict(Status='Success', detail=tmpDict)
            else:
                return dict(Status='False', msg='MySQL could not found any detail of unified url.')
            
        except Exception, e:
            CMDBSession.rollback()
            return dict(Status='False', msg=str(e))
            
    def searchurlrelation(self, urlid):
        
        tmplist = []
        
        try:
            getsearchofrelation = CMDBSession.query(URLtoDNS).filter_by(urlid = urlid).all()
            
            if getsearchofrelation:
                for eachline in getsearchofrelation:
                    tmplist.append(eachline.dnsid)
                
                return dict(Status='Success', dnslist=tmplist)
            else:
                return dict(Status='False', msg='MySQL could not found any detailf of url relation to dns.')
            
        except Exception, e:
            CMDBSession.rollback()
            return dict(Status='False', msg=str(e))

    def searchdnsipdetail(self, dnsid):
        
        tmplist = {}
        
        try:
            getsearchofdnsipdetail = CMDBSession.query(UnifiedDNSIP).filter_by(id = dnsid).first()
            
            if getsearchofdnsipdetail:
                if getsearchofdnsipdetail.Status != 0:
                    tmplist[dnsid] = dict(ipaddress=getsearchofdnsipdetail.Ipaddress)
                    
                    return dict(Status='Success', dnsdetail=tmplist)
                else:
                    return dict(Status='False', msg='MySQL could not found any detail of dns ip.')
            else:
                return dict(Status='False', msg='MySQL could not found dns ip detail.')
            
        except Exception, e:
            CMDBSession.rollback()
            return dict(Status='False', msg=str(e))
        
    def searchspliceurl(self, category):
        
        tmpDict = {}
        try:
            getsearchofspliceurl = CMDBSession.query(SpliceURL).filter_by(Category = category).first()
            
            if getsearchofspliceurl:
                tmpDict[getsearchofspliceurl.partipofurl] = getsearchofspliceurl.example
                
                return dict(Status='Success', categoryinform = tmpDict)
                
            else:
                msg = 'MySQL Category of %s could not be found.'
                return dict(Status='False', msg=msg)
            
            
        except Exception, e:
            CMDBSession.rollback()
            return dict(Status='False', msg=str(e))
        
    def searchreturnvaluedefine(self, code, types):
        
        try:
            getsearchofreturnvaluedefine = CMDBSession.query(ReturnValuedefine).filter(and_(ReturnValuedefine.value == code, ReturnValuedefine.Type == types)).first()
            
            if getsearchofreturnvaluedefine:
                return dict(Status='Success', zhdefine=getsearchofreturnvaluedefine.ZHdefine)
            else:
                return dict(Status='False', msg='MySQL could not found detail in database.')
            
        except Exception, e:
            CMDBSession.rollback()
            return dict(Status='False', msg=str(e))
        
    def counterSearch(self):
        
        tmplist = []
                
        try:
            getSearchofCounter = CMDBSession.query(CounterList).all()
            
            if getSearchofCounter:

                for eachline in getSearchofCounter:
                    tmplist.append(eachline.ipaddress)
            else:
                msg = 'Could not found any detail about counter list.'
                return dict(Status='False', msg=msg)
            
        except Exception, e:
            return dict(Status='False', msg=str(e))
        
        return dict(Status='Success', counterlist=tmplist)
    
    def addintoresultofcounterstatus(self, status, char, solveperson):
        
        try:
            getsearchofaddintoresult = CMDBSession.query(ResultCounterStatus).first()
            
            if getsearchofaddintoresult:
                getsearchofaddintoresult.Status = status
                getsearchofaddintoresult.Char = char
                getsearchofaddintoresult.SolvePerson = solveperson
                
            else:
                CMDBSession.add(ResultCounterStatus(status, char, solveperson))
        
        except Exception, e:
            CMDBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        CMDBSession.commit()
        return dict(Status='Success')
    
    def addintoresultoffastreg(self, status, char, solveperson):
        
        try:
            getsearchofaddintoffastreg = CMDBSession.query(ResultFastReg).first()
            
            if getsearchofaddintoffastreg:
                getsearchofaddintoffastreg.Status = status
                getsearchofaddintoffastreg.Char = char
                getsearchofaddintoffastreg.SolvePerson = solveperson
                
            else:
                CMDBSession.add(ResultFastReg(status, char, solveperson))
        
        except Exception, e:
            CMDBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        CMDBSession.commit()
        return dict(Status='Success')
    
    def addintoresultofadvert(self, project, overtime, starttime, url, pagealias, status):

        if type(pagealias).__name__ == 'unicode':
            pagealias = pagealias.encode('utf8') 
                       
        try:
            getsearchofadvert = CMDBSession.query(ResultADUrl).filter(and_(ResultADUrl.project == project, ResultADUrl.url == url, ResultADUrl.pagealias == pagealias)).first()
            
            if getsearchofadvert:
                getsearchofadvert.project = project
                getsearchofadvert.overtime = overtime
                getsearchofadvert.starttime = starttime
                getsearchofadvert.url = url
                getsearchofadvert.pagealias = pagealias
                getsearchofadvert.status = status
                
            else:
                CMDBSession.add(ResultADUrl(project, overtime, starttime, url, pagealias, status))
            
        except Exception, e:
            CMDBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        CMDBSession.commit()
        return dict(Status='Success')
    
    def searchCacheofCounterStatus(self):
        
        try:
            getsearchofcachrofcounter = CMDBSession.query(ResultCounterStatus).first()
            
            if getsearchofcachrofcounter:
                tmpDict = {}
                tmpDict['Status'] = getsearchofcachrofcounter.Status
                tmpDict['Char'] = getsearchofcachrofcounter.Char
                tmpDict['SolvePerson'] = getsearchofcachrofcounter.SolvePerson
                return dict(Status='Success', Dict=tmpDict)
            else:
                return dict(Status='False', msg='MySQL could not found any result in counter Status.')
            
        except Exception, e:
            CMDBSession.rollback()
            return dict(Status='False', msg=str(e))
        
    def searchCacheofFastReg(self):
        
        try:
            getsearchofcachroffastreg = CMDBSession.query(ResultFastReg).first()
            
            if getsearchofcachroffastreg:
                tmpDict = {}
                tmpDict['Status'] = getsearchofcachroffastreg.Status
                tmpDict['Char'] = getsearchofcachroffastreg.Char
                tmpDict['SolvePerson'] = getsearchofcachroffastreg.SolvePerson
                return dict(Status='Success', Dict=tmpDict)
            else:
                return dict(Status='False', msg='MySQL could not found any result in counter Status.')
            
        except Exception, e:
            CMDBSession.rollback()
            return dict(Status='False', msg=str(e))
        
    def searchurlinad(self, url, nowtimestamp):
        
        allist = []
        
        try:
            ''' 1. del all < starttime line. '''
            gethideadurl = self.hideadurl(nowtimestamp)
            if gethideadurl['Status'] != 'Success':
                CMDBSession.rollback()
                return dict(Status='False', msg='Flush starttime beforetime Failed.')
            
            getsearchofurlad = CMDBSession.query(ResultADUrl).filter_by(url = url).all()
            
            ''' 2. search url in ad. '''
            if getsearchofurlad:
                for eachline in getsearchofurlad:
                    tmpDict = {}
                    tmpDict['project'] = eachline.project
                    tmpDict['overtime'] = eachline.overtime
                    tmpDict['starttime'] = eachline.starttime
                    tmpDict['url'] = eachline.url
                    tmpDict['pagealias'] = eachline.pagealias
                    tmpDict['Status'] = eachline.Status
                    allist.append(tmpDict)
    
                return dict(Status='Success', newlist=allist)
            else:
                return dict(Status='False', msg='MySQL could not found this url in database.')
            
        except Exception, e:
            CMDBSession.rollback()
            return dict(Status='False', msg=str(e))
        
    def searchprojectinad(self, project, nowtimestamp):
        
        allist = []
        
        try:
            ''' 1. del all < starttime line. '''
            gethideadurl = self.hideadurl(nowtimestamp)
            if gethideadurl['Status'] != 'Success':
                CMDBSession.rollback()
                return dict(Status='False', msg='Flush starttime beforetime Failed.')
            
            getsearchofprojectad = CMDBSession.query(ResultADUrl).filter_by(project = project).all()
            
            if getsearchofprojectad:
                for eachline in getsearchofprojectad:
                    tmpDict = {}
                    tmpDict['project'] = eachline.project
                    tmpDict['overtime'] = eachline.overtime
                    tmpDict['starttime'] = eachline.starttime
                    tmpDict['url'] = eachline.url
                    tmpDict['pagealias'] = eachline.pagealias
                    tmpDict['Status'] = eachline.Status
                    allist.append(tmpDict)
                    
                return dict(Status='Success', newlist=allist)
            else:
                return dict(Status='False', msg='MySQL could not found this url in database.')
            
        except Exception, e:
            CMDBSession.rollback()
            return dict(Status='False', msg=str(e))
        
    def searchprojectandurlinad(self, project, url, nowtimestamp):
        
        allist = []
        
        try:
            ''' 1. del all < starttime line. '''
            gethideadurl = self.hideadurl(nowtimestamp)
            if gethideadurl['Status'] != 'Success':
                CMDBSession.rollback()
                return dict(Status='False', msg='Flush starttime beforetime Failed.')
            
            getsearchofprojectandurlad = CMDBSession.query(ResultADUrl).filter(and_(ResultADUrl.project == project, ResultADUrl.url == url)).all()
            
            if getsearchofprojectandurlad:
                for eachline in getsearchofprojectandurlad:
                    tmpDict = {}
                    tmpDict['project'] = eachline.project
                    tmpDict['overtime'] = eachline.overtime
                    tmpDict['starttime'] = eachline.starttime
                    tmpDict['url'] = eachline.url
                    tmpDict['pagealias'] = eachline.pagealias
                    tmpDict['Status'] = eachline.Status
                    allist.append(tmpDict)
                    
                return dict(Status='Success', newlist=allist)
            else:
                return dict(Status='False', msg='MySQL could not found this url in database.')
            
        except Exception, e:
            CMDBSession.rollback()
            return dict(Status='False', msg=str(e))
        
    def searchUserdetailfortemp(self, uid=1):
        
        tmpDict = {}
        
        try:
            getsearchofuserdetail = CMDBSession.query(TmpSolvePerson).filter_by(id = uid).first()
            
            if getsearchofuserdetail:
                tmpDict['username'] = getsearchofuserdetail.Username
                tmpDict['phonenum'] = getsearchofuserdetail.PhoneNum
                return dict(Status='Success', Dict=tmpDict)
            else:
                return dict(Status='False', msg='MySQL could not found any detail information about user.')
            
        except Exception, e:
            CMDBSession.rollback()
            return dict(Status='False', msg=str(e))