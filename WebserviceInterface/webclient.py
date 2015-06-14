# encoding: utf-8
''' @author : majian'''
import chardet
import sys, os
import simplejson as json
import chardet
import urllib2
from suds.client import Client

'''
解决了suds支持中文字符集的问题
使用suds的时候，必须要记得将www.w3.org网站的80端口打开，以便可以访问
才能读取到/usr/local/python2.6/lib/python2.6/site-packages/suds/reader.py中的url : http://www.w3.org/2001/XMLSchema.org
所以需要在本地起nginx做www.w3.org源站并且启动在80端口上
'''
reload(sys)
sys.setdefaultencoding('utf-8')

game = 'wuxiaoping'
zone = 'ztgame%123'
game = urllib2.quote(game)
zone = urllib2.quote(zone)

getClient = Client('http://192.168.66.196:9998/SOAP/?wsdl', cache=None)
#result = getClient.service.searchzonemaintianed(game,zone)
result = getClient.service.searchDesignUser('changzonghui')
print result



#'AgentList','CustomExecList','ExceptionLogic','ExecGroup','GameList','NodeList','ProcList','SwitchList','Template'
