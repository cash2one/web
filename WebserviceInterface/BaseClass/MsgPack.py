# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time
import msgpack

class MessagePack:
    
    def __init__(self):
        
        self.packed = ""
        self.unpacked = ""
        
    def packb(self, data):
        
        try:
            self.packed = msgpack.packb(data)
            
        except Exception, e:
            return str(e)
        
        return self.packed
    
    def unpackb(self, data):
        
        try:
            self.unpacked = msgpack.unpackb(data)
            
        except Exception, e:
            return str(e)
        
        return self.unpacked