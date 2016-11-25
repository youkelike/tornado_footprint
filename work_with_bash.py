import smtplib
import sys
from optparse import OptionParser

mailto_list = ['815666124@qq.com',]
mail_host = 'smtp.163.com'
mail_user = '15626453394@163.com'
mail_pass = 'czh123'
mail_postfix = '163.com'

def initialize_smtp_server(smtpserver,email,pwd):
    server = smtplib.SMTP()
    server.connect(smtpserver)
    server.login(email,pwd)
    return server

def send_mail(email,smtpserver):
    to_email = email
    from_email = 'alexanda<%s>' % mail_user
    subj = 'Thanks for being an active commenter!'
    header = 'To:%s\nFrom:%s\nSubject:%s' % (to_email,from_email,subj)
    msg_body = """
    Hi friend,

    Thank you very much for your repeated comments on our service.
    The interaction is much appreciated.

    Thank You."""
    content = '%s\n%s' % (header,msg_body)
    print(content)
    smtpserver.sendmail(from_email,to_email,content)

if __name__ == '__main__':
    usage = 'usage: %prog [options]'
    parser = OptionParser(usage=usage)
    parser.add_option('--email',dest='email',help='email to login to smtp server',default='15626453394@163.com')
    parser.add_option('--pwd',dest='pwd',help='password to login to smtp server',default='czh123')
    parser.add_option('--smtp-server',dest='smtpserver',help='smtp server url',default='smtp.163.com')
    options,args = parser.parse_args()
    print(options)
    try:
        smtpserver = initialize_smtp_server(options.smtpserver,options.email,options.pwd)
        for email in sys.stdin.readlines():
            send_mail(email,smtpserver)
        # print(smtpserver)
        # send_mail('815666124@qq.com', smtpserver)
    except Exception as e:
        print(str(e))

    smtpserver.close()