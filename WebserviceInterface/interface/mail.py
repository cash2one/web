# -*- coding: utf-8 -*-
''' @author : majian'''

import smtplib
from email.mime.text import MIMEText

class SendMail:

    def __init__(self):
        
        self.returns = ""
        self.host = '192.168.66.74'
        self.port = 25
        
    def send_mail(self, fromUser, toUser, sub, content):
        '''
        to_list: to the mailto_list
        sub:  subscribe
        content: detail of content
        usage: send_mail("touser","sub","content")
        '''

        msg = MIMEText(content)
        msg['Subject'] = sub
        msg['From'] = fromUser
        msg['To'] = toUser

        try:
            s = smtplib.SMTP()
            s.connect(self.host, self.port)
            s.sendmail(fromUser, toUser, msg.as_string())
            s.close()
            return True
        
        except Exception, e:
            print str(e)
            return False