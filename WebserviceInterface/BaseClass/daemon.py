# -*- coding: utf-8 -*-
''' @author : majian'''

import os, sys
import time

def daemonize(pname=None,stdout='/dev/null', stderr=None, stdin='/dev/null', pidfile=None, startmsg = 'started with pid %s' ):

    # flush io buffer
    sys.stdout.flush()
    sys.stderr.flush()
    # Do first fork.  
    try:
        pid = os.fork()
        if pid > 0: sys.exit(0) # Exit first parent.
    except OSError, e:
        sys.stderr.write("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)
    # Decouple from parent environment.  
    os.chdir("/")
    #os.umask()->Set the current numeric umask and return the previous umask. Availability: Unix, Windows
    os.umask(022)
    # os.setsid()->Call the system call setsid(). See the Unix manual for the semantics. Availability: Unix.
    os.setsid()

    # Do second fork.  
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0) # Exit second parent.  
    except OSError, e:
        sys.stderr.write("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)
    # Open file descriptors and print start message  
    if not stderr:
        stderr = stdout
        si = file(stdin, 'r')
        so = file(stdout, 'a+')
        se = file(stderr, 'a+',0)  #unbuffered  
        # os.getpid()->Return the current process id. Availability: Unix, Windows.
        pid = str(os.getpid())
        sys.stderr.write("\n%s\n" % startmsg % pid)
        sys.stderr.flush()
    if pidfile:
        file(pidfile,'w+').write("%s\n" % pid)
    # Redirect standard file descriptors.  
    # file.fileno()->Return the integer “file descriptor” that is used by the underlying implementation to request I/O operations from the operating system
    # os.dup2(fd,fd2)->Duplicate file descriptor fd to fd2, closing the latter first if necessary. Availability: Unix, Windows
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())
    os.system("/usr/bin/python %s" % (pname))