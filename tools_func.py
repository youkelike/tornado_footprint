import socket


def ping_port(ip,port):
    '''可用于监测服务器运行状态'''
    sk = socket.socket()
    sk.settimeout(0.2)
    address = (str(ip),int(port))
    try:
        sk.connect((address))
    except socket.error as e:
        print(e)
        return 1
    sk.close()
    return 0

import os,json
import pycurl
from io import BytesIO

class Curl(object):
    def __init__(self,curl):
        self.__curl__ = curl

    def get_value(self):
        d_url = pycurl.Curl()
        url_buf = BytesIO()
        d_url.setopt(d_url.URL,self.__curl__)
        try:
            d_url.setopt(d_url.WRITEFUNCTION,url_buf.write)
            d_url.perform()
        except pycurl.error as e:
            errno,errstr = e
            print('An error occured:',errstr)
        ret_json = json.loads(url_buf.getvalue())
        return ret_json

    def post_value(self,action,param):
        pass