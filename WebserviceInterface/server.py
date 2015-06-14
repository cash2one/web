# -*- coding: utf-8 -*-
''' 
@author : majian 
Webservice start : run_twisted(((wsgi_app, "SOAP"),), 9998) 
'''

''' Global Statement '''
import os, sys
import struct

''' webservice statement'''
import getopt
import logging
import soaplib
from soaplib.core.util.wsgi_wrapper import run_twisted
from soaplib.core.server import wsgi
from soaplib.core.service import DefinitionBase
from soaplib.core.service import soap
from soaplib.core.model.clazz import Array
from soaplib.core.model.binary import Attachment
from soaplib.core.model.clazz import ClassModel
from soaplib.core.model.primitive import Integer,String,Boolean

from twisted.application import internet, service
from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor

''' write for using webservice '''
from Control.main import externalWebservice, OfficialWebservice

''' All server Initialization''' 
from model import init_model
from model.__cmdbinit__ import cmdbinit_model
from model.initData import initdata
from model.cminitData import cminitdata

from BaseClass.logger import LoggerRecord
logger = LoggerRecord().initlog()
        
if __name__ == '__main__':

    init_model() # init all tables 
    cmdbinit_model() # init cmdb all tables 
    initdata()   # init all data  
    cminitdata() # init cmdb all data
    
    # starting tcpserver
    factory = Factory()

    # starting webservice
    soap_app=soaplib.core.Application([externalWebservice, OfficialWebservice], 'tns')
    wsgi_app=wsgi.Application(soap_app)
    
    # outside Statement
    logger.debug('* Webservice started on port:7789... ')
    logger.debug('* wsdl AT: http://192.168.82.89:7789/SOAP/?wsdl')
    logger.debug('* wsdl AT: http://222.73.33.131:7789/SOAP/?wsdl')

    
    ''' webservice start'''
    run_twisted(((wsgi_app, "SOAP"),), 9998)
