#-------------------------------------------------------------------------------
# Name:        Send Mail
# Purpose:     This module is used to send Email with the parameters sent to
#               sendMail function
# Author:      Akhila Vasanth
#
# Created:     16/05/2012
# Copyright:   (c) McAfee Inc
#-------------------------------------------------------------------------------

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email import Encoders
import mimetypes

class SendMail(object):

    def sendEmail(self, hostName, toList, fromAdd, subject, content, \
                    attachmentsList = None):
        """This method takes as input sender,list of recipients,subject,content,
        attachments (if any) and composes and sends a mail to the recipients"""
        #initialising the variables
        host = hostName
        #composing the mail
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = fromAdd
        msg['To'] = ','.join(toList)
        msg.attach(MIMEText(content,'html'))
        #The attachments
        if attachmentsList:
            for fname in attachmentsList:
                #print fname
                ctype, encoding = mimetypes.guess_type(fname)
                if ctype is None or encoding is not None:
                    # No guess could be made so use a binary type.
                    ctype = 'application/octet-stream'
                maintype, subtype = ctype.split('/', 1)
                if maintype == 'text':
                    fp = open(fname)
                    attach = MIMEText(fp.read(), _subtype=subtype)
                    fp.close()
                elif maintype == 'html':
                    fp = open(fname)
                    attach = MIMEText(fp.read(), _subtype=subtype)
                    fp.close()
                elif maintype == 'image':
                    fp = open(fname, 'rb')
                    attach = MIMEImage(fp.read(), _subtype=subtype)
                    fp.close()
                elif maintype == 'audio':
                    fp = open(fname, 'rb')
                    attach = MIMEAudio(fp.read(), _subtype=subtype)
                    fp.close()
                else:
                    fp = open(fname, 'rb')
                    attach = MIMEBase(maintype, subtype)
                    attach.set_payload(fp.read())
                    fp.close()
                    # Encode the payload using Base64
                    Encoders.encode_base64(attach)
                # Set the filename parameter
                filename = os.path.basename(fname)
                attach.add_header('Content-Disposition', 'attachment', \
                                    filename = filename)
                msg.attach(attach)
        try:
           #sending the mail
            server = smtplib.SMTP(host)
            server.sendmail(fromAdd,toList,msg.as_string())
            server.quit()
            return True
        except Exception as e:
            print "Mail Exception::%s" % (str(e))
            return False