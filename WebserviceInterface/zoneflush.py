# encoding: utf-8
''' @author : majian'''
import sys, os
import simplejson as json
from suds.client import Client

from model.cmdbsearch import BasicSearch

reload(sys)
sys.setdefaultencoding('utf-8')

getClient = Client('http://192.168.66.196:9998/SOAP/?wsdl', cache=None)

getClient.service.autoflushServermaintian() # from auto system search zone and server maintianed or not
