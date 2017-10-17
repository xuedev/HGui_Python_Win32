#coding:utf-8
import urllib
import urllib2
import sys
import json
import os
import base64
import zlib
from PIL import  Image
from PIL import  ImageGrab

def post(url,param):
        #try:
                req = urllib2.Request(url,param)
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
                response = opener.open(req)
                js = "top.connectLog('%s%s')" % ("发送图片完毕,图片大小:",str(len(param)))
                print js
                return response.read()
        #except:
         #       js = "top.connectLog('%s')" % (u"无法连接到服务器")
         #       print js
        
def readFile(filename):
        file = open(filename,"rb")
        return file.read()

def sendFile(filename,url):
        data = readFile(filename)
        tmp = base64.b64encode(data)
        tmp = zlib.compress(tmp)
        post(url,tmp)

def grab():
        im = ImageGrab.grab()
        im.save("tmp.jpeg",'jpeg')

def startGrab(url):
        #grab()
        sendFile("tmp.jpeg",url)
        return "ok"
if __name__ == '__main__':
        startGrab("http://127.0.0.1:8000")
