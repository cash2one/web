# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re
import sys
import zlib
import base64
import simplejson as json
from pyDes import *

null = ''

class dataCompress:
    
    def compress(self, data):
        
        becomp = zlib.compress(data, zlib.Z_BEST_COMPRESSION)

        return becomp
    
    def uncompress(self, data):
        
        uncomp = zlib.decompress(data)
        
        return uncomp

class Encryption:
    
    def __init__(self, key='_interf_', Model=1, iv='12345678', pad=None, padmode=2):
        self.key = key
        self.Model = Model
        self.iv = iv
        self.pad = pad
        self.padmode = padmode
        self.useKey = des(self.key, self.Model, self.iv, self.pad, self.padmode)
        
    def enEncrypt(self, data):
        
        keyPlusData = self.useKey.encrypt(data)
        
        return keyPlusData
    
    def deEncrypt(self, data):
        
        resourceData = self.useKey.decrypt(data)
        
        return resourceData
    
class base64Data:
    
    def encode64(self, data):
        
        encover = base64.encodestring(data)
        encovery = encover.replace("\n",'')

        return encovery
    
    def decode64(self, data):
        
        decover = base64.decodestring(data)
        
        return decover

class changeDict:

    global null
    
    def dicttostr(self, data):
        
        # solve chinese unicode
        reload(sys)
        sys.setdefaultencoding('utf8')
        
        # Dict to str
        newData = ''
        _tempBuff, dictToStr = '',''
        
        for key,value in data.items():
            _tempBuff = "\"%s\":\"%s\"," % (key, value)
            dictToStr = dictToStr + _tempBuff
              
        newData = dictToStr[:-1]
        
        if re.search(r'^{|}$', newData):
            newData = newData
        else:
            newData = "{"+newData+"}"
            
        # sure newData is str
        newData = newData.encode('utf8')
        
        return newData
    
    def strtodict(self, data):
        
        self.newDict = {}
        newData = ""
        
        reload(sys)
        sys.setdefaultencoding('utf8')

        if re.search(r'{|}',data):
            newData = data
        else:
            newData = "{"+data+"}"

        self.newDict = eval(newData)
        
        return self.newDict
    
class changeList:
    
    def listtostr(self, list):
        
        if type(list).__name__ == 'list':
            
            newStr = ','.join(list)
            
            return dict(Status='Success', String=newStr)
        else:
            return dict(Status='False', msg='type of input error: not LIST.')

    def strtolist(self, string):
        
        if type(string).__name__ == 'str':
            
            newList = [i for i in string.split(',')]
            
            return dict(Status='Success', List=newList)
        else:
            return dict(Status='False', msg='type of input error: not STRING.')
        
class ListCount:
    
    def __init__(self):
        
        self.Dict = {}
    
    def base(self, listinput):
            
        for eachitem in set(listinput):
            if type(eachitem).__name__ == 'unicode':
                self.Dict[eachitem.encode()] = listinput.count(eachitem)
            else:
                self.Dict[eachitem] = listinput.count(eachitem)
          
        return self.Dict