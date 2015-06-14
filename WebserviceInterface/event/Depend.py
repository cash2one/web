# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time
from BaseClass.verifityDependence import changeDict

class Dependence:
    
    def __init__(self):
        
        self.count = 0
        self.returns = ""
        
    ''' This method use to check message body '''    
    def CheckBody(self, body):

        for key,value in body.items():
            if key == 'Status':
                self.count += 1
            elif key == 'Type':
                self.count += 1
            elif key == 'Result':
                self.count += 1
            elif key == 'Info':
                self.count += 1
            elif key == 'ID':
                self.count += 1
            elif key == 'OID':
                self.count += 1
            elif key == 'JobID':
                self.count += 1
            elif key == 'SendTime':
                self.count += 1
        
        if self.count == 8:
            return dict(Status="Success")
        else:
            return dict(Status="False", msg="check message body failed. Not eight Variable.")
        
    ''' This method use to check message body correct.'''
    def checkBodydata(self, body):
        
        newBody = {}
        
        for key,value in body.items():
            if key == 'Status':
                if value == ''  or value == 'None':
                    return dict(Status='False', msg='check message body data <Status> Failed.')
                else:
                    newBody[key] = value
            elif key == 'Type':
                if value == ''  or value == 'None':
                    return dict(Status='False', msg='check message body data <Type> Failed.')
                else:
                    newBody[key] = value
            elif key == 'ID':
                if value == ''  or value == 'None':
                    return dict(Status='False', msg='check message body data <ID> Failed.')
                else:
                    newBody[key] = value
            elif key == 'OID':
                if value == ''  or value == 'None':
                    return dict(Status='False', msg='check message body data <Status> Failed.')
                else:
                    newBody[key] = value
            elif key == 'JobID':
                if value == '' or int(value) == 0:
                    newBody[key] = 0
                else:
                    newBody[key] = value
            elif key == 'SendTime':
                if value == '' or int(value) == 0:
                    newBody[key] = 0
                else:
                    newBody[key] = value
            elif key == 'Result':
                if value == '' or value == 'None':
                    newBody[key] = 'None'
                else:
                    newBody[key] = value
            elif key == 'Info':
                if value == '' or value == 'None':
                    newBody[key] = 'None'
                else:
                    newBody[key] = value   
                    
        return dict(Status='Success', message=newBody)
       
    
     
    ''' This method use to check struct of data '''    
    def SearchStep(self, message):
        
        count = 0
        
        try:
            for key,value in message.items():

                if key == 'Eproject':
                    if type(value).__name__ == 'list' or type(value).__name__ == 'str':
                        count += 1
                elif key == 'Econtent':
                    if type(value).__name__ == 'str':
                        count += 1
                elif key == 'Elevel':
                    if type(value).__name__ == 'str' or type(value).__name__ == 'int':
                        count += 1
                elif key == 'Eoid':
                    if type(value).__name__ == 'str':
                        count += 1
                elif key == 'Etimestamp':
                    if type(value).__name__ == 'str' or type(value).__name__ == 'int':
                        count += 1
                elif key == 'Econditionid':
                    if type(value).__name__ == 'str' or type(value).__name__ == 'int':
                        count += 1  
                                         
            if count == 6:
                return dict(Status='Success')
            else:
                return dict(Status='False', msg='Received Message Struct Error.')
                
        except Exception, e:
            return dict(Status='False', msg=str(e))
     
    ''' This method use to check data '''    
    def Checkdata(self, message):
        
        newDict = {}
        
        for key, value in message.items():
            
            if key == 'Eproject':
                if type(value).__name__ == 'str':
                    value = eval(value)
                    newDict[key] = value
                elif value == '':
                    return dict(Status='False', msg='Eproject Variable Error.')
                else:
                    newDict[key] = value
            
            elif key == 'Econtent':
                if value == '':
                    return dict(Status='False', msg='Econtent Variable Error.')
                else:         
                    newDict[key] = value
                
            elif key == 'Elevel':
                if value == '':
                    newDict[key] = -1
                else:
                    newDict[key] = int(value)
            
            elif key == 'Eoid':
                if value == '':
                    return dict(Status='False', msg='Eoid Variable Error.')
                else:         
                    newDict[key] = value
                
            elif key == 'Etimestamp':
                if value == '' or value == 'None':
                    newDict[key] = 0
                else:
                    newDict[key] = int(value)
                
            elif key == 'Econditionid':
                if value == '' or value == 'None':
                    newDict[key] = 1
                else:
                    newDict[key] = int(value)
                
        return dict(Status='Success', message=newDict)
    
    def checkFirstdisconnbody(self, body):
        
        try:
            if type(body).__name__ != 'dict':
                body = changeDict().strtodict(body)
                
            if body['Type'] != 'main':
                return dict(Status='False', msg='input Body has not correct Type.')
            
            if body['OID'] != '5.1':
                return dict(Status='False', msg='input Body has not correct Oid.')
            
        except Exception, e:
            return dict(Status='False', msg=str(e))
        
        return dict(Status='Success')