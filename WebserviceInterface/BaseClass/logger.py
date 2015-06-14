# -*- coding: utf-8 -*-
''' @author : majian'''
import logging

from ServiceConfig.config import readFromConfigFile
from twisted.application import internet, service, app
from twisted.python import logfile

class LoggerRecord:
    
    def __init__(self):
        
        self.Level = ""
        self.Filename = ""
        
        getReturnofconfiglog = readFromConfigFile().get_config_Log()
        for eachtuple in getReturnofconfiglog['Log']:
            if eachtuple[0] == 'level':
                self.Level = "logging."+eachtuple[1]
            elif eachtuple[0] == 'filename':
                self.Filename = eachtuple[1]

    def initlog(self):

        logfile = self.Filename

        logger = logging.getLogger()
        hdlr = logging.FileHandler(logfile)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.NOTSET)
        
        return logger