#coding:utf-8
import urllib
import urllib2
import sys
import json
import os
import base64
import ziputils
from PIL import  Image
from PIL import  ImageGrab
import core

def post(url,param):
        try:
                param = ziputils.zip(param)
                ilen = str(len(param))
                req = urllib2.Request(url,param)
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
                response = opener.open(req)
                js = "top.connectLog('%s%s')" % ("发送图片完毕,图片大小:",ilen)
                core.runJs(js)
                print js
                return response.read()
        except:
                js = "top.connectLog('%s')" % "无法连接到服务器"
                core.runJs(js)
                print js
        
def readFile(filename):
        try:
                file = open(filename,"rb")
                return file.read()
        except:
                js = "top.connectLog('%s')" % "读取图片文件失败"
                print js
                core.runJs(js)
                
                
def sendFile(filename,url):
        try:
                data = readFile(filename)
                tmp = base64.b64encode(data)
                post(url,tmp)
        except:
                js = "top.connectLog('%s')" % "发送文件失败"
                print js
                core.runJs(js)

def grab():
        try:
                im = ImageGrab.grab()
                im.save("tmp.png",'png')
        except:
                js = "top.connectLog('%s')" % "截图失败"
                print js
                core.runJs(js)
                
def startGrab(url):
        grab()
        sendFile("tmp.png",url)
        return "ok"
if __name__ == '__main__':
        import time
        while True:
                startGrab("http://127.0.0.1:8000")
                time.sleep(1)
