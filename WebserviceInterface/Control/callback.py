# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time
import soaplib
import simplejson as json

from soaplib.core.server import wsgi
from soaplib.core.service import DefinitionBase
from soaplib.core.service import soap
from soaplib.core.model.clazz import Array
from soaplib.core.model.binary import Attachment
from soaplib.core.model.clazz import ClassModel
from soaplib.core.model.primitive import Integer,String,Boolean

from interface.mail import SendMail

class ReceivedCall:
    
    def __init__(self):
        
        self.call = {}
        
    def getReceived(self, message):
        
        if type(message).__name__ == 'NoneType' or len(message) == 0:
            message = 'Get Platform Information ERROR. <<< None >>>.'
        else:
            if type(message).__name__ != 'str':
                message = str(message)
            else:
                message = message
                
        SendMail().send_mail('8000@ztgame.com', 'lvlijun@ztgame.com', '统一监控报警', message)      