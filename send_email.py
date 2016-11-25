import smtplib
import sys
from email.mime.text import MIMEText

mailto_list = ['815666124@qq.com',]
mail_host = 'smtp.163.com'
mail_user = '15626453394@163.com'
mail_pass = 'czh123'
mail_postfix = '163.com'

def send_mail(to_list,sub,content):
    me = 'alexanda<%s@%s>' % (mail_user,mail_postfix)
    msg = MIMEText(content,_subtype='plain')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ';'.join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user,mail_pass)
        server.sendmail(me,to_list,msg.as_string())
        server.close()
        return True
    except Exception as e:
        print(str(e))
        return False

for i in range(1):
    if send_mail(mailto_list,'千里之外','送你离开,千里之外你是否还在，沉默年代是否不该，太遥远的相爱'):
        print('done!')
    else:
        print('failed!')