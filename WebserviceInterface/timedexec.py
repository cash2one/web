# encoding: utf-8
''' @author : majian'''
import sys, os
import simplejson as json
from suds.client import Client

from model.cmdbsearch import BasicSearch

reload(sys)
sys.setdefaultencoding('utf-8')

        getClient = Client('http://192.168.66.196:9998/SOAP/?wsdl', cache=None)

curvesresult = getClient.service.flushcurvesofnumber("", "1.1.6.0.0.1.2.34.21", "5") # from curvesofnumber flush table
result = getClient.service.CounterStatus() # platform counter status search
regresult = getClient.service.testPlatformFastReg() # platform fastreg status search
flushservermaintian = getClient.service.autoflushServermaintian() # from auto system search zone and server maintianed or not

BasicSearch().addintoresultofcounterstatus(result.Status, result.Char, result.SolvePerson)
BasicSearch().addintoresultoffastreg(regresult.Status, regresult.JsonChar, regresult.SolvePerson)
