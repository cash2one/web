# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time
import chardet
import urllib2, urllib
import simplejson as json

from BaseClass.verifityDependence import base64Data
from ServiceConfig.config import readFromConfigFile

class linkAuto:
    
    def __init__(self):
        
        self.autokey = ""
        self.officalurl = ""
        
        getReturn = readFromConfigFile().get_config_giantauto()
        for eachline in getReturn['GiantAuto']:
            if eachline[0] == 'autokey':
                self.autokey = eachline[1]
            if eachline[0] == 'officalurl':
                self.officalurl = eachline[1]

    # Base64（AUTO_KEY+gameName+gameZone）
    def linkwithzonedetail(self, gamename, gamezone):
        
        dataDict = {}
        ''' Step 1. create new Verifty Key. '''
        newLinkchar = "%s%s%s" % (self.autokey, gamename, gamezone)
        newbase64 = base64Data().encode64(newLinkchar)[0:4]
        
        ''' Step 2. gamename & gamezone charset. '''
        urlgamename = urllib2.quote(gamename)
        urlgamezone = urllib2.quote(gamezone)

        ''' Step 3. post data with auto api. '''
        dataDict['gameName'] = urlgamename
        dataDict['gameZone'] = urlgamezone
        dataDict['X'] = newbase64

        newautoapi = urllib2.urlopen(url     = self.officalurl,\
                                     data    = urllib.urlencode(dataDict))
        
        ''' Step 4. judge decide by using. '''
        for eachurlline in newautoapi.readlines():
            eachResult = json.loads(eachurlline)
            # using Error By Url
            if eachResult['code'] == 500:
                return dict(Status='False', msg=eachResult['message'])
            # right url using.
            elif eachResult['code'] == 200:
                if eachResult['data'] != 'ing':
                    return dict(Status='Success', maintain=0)
                else:
                    return dict(Status='Success', maintain=1)