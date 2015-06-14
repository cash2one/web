# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time, getopt

from ServiceConfig.config import readFromConfigFile
from BaseClass.daemon import daemonize

def usage():
    print "Usage: %s [-d] args...." % (sys.argv[0])
    
if __name__ == '__main__':
    
    scriptname = ""
    flushtime = 0
    try:
        opt, args = getopt.getopt(sys.argv[1:], 'd')
        
        if len(opt) == 0:
            print "getopt error."
            usage()
            sys.exit(0)
        else:
            if opt[0][0] == '-d':
                
                # get scriptname & flushtime
                getReturn = readFromConfigFile().get_config_xinetd()
                for eachtuple in getReturn['Xinetd']:
                    if eachtuple[0] == 'scriptname':
                        scriptname = eachtuple[1]
                    elif eachtuple[0] == 'flushtime':
                        flushtime = int(eachtuple[1])
                                        
                running = True
        
                while running:
                        
                    checkpid = "ps aux | grep -i %s | grep -v grep" % (scriptname)
                    result = os.system(checkpid)
                        
                    if result != 0:
                        daemonize(scriptname)
                    time.sleep(flushtime)
            
    except getopt.GetoptError:
        print "getopt error."
        usage()
        sys.exit(0)