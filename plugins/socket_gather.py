#coding:utf-8
from socket import *
import os
import struct
import base64
import zlib
import json
import sys
from PIL import  Image
from PIL import  ImageGrab
import core

filename = 'test.txt'

#file_size = struct.calcsize

def startSend(data,param):
        j = json.loads(param)
        tmp = base64.b64encode(data)
        tmp = zlib.compress(tmp)
        addr = (j["ip"],int(j["port"]))
        try:
                sendSock = socket(AF_INET,SOCK_STREAM)
                sendSock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
                sendSock.connect(addr)
                sendSock.send(tmp)
                sendSock.close()
                js = "top.connectLog('%s')" % "发送完毕";
                core.runJs(js)
        except:
                (ErrorType, ErrorValue, ErrorTB) = sys.exc_info()
                (errno, err_msg) = ErrorValue
                error = "连接服务器失败: %s, errno=%d" % (err_msg, errno)
                js = "top.connectLog('%s')" % error;
                core.runJs(js)

def readFile(filename):
        file = open(filename,"rb")
        return file.read()

def sendFile(filename,param):
        data = readFile(filename)
        startSend(data,param)

def grab():
        im = ImageGrab.grab()
        im.save("tmp.jpeg",'jpeg')

def startGrab(param):
        grab()
        sendFile("tmp.jpeg",param)
        return "ok"
if __name__ == '__main__':
        startGrab("{\"ip\":\"127.0.0.1\",\"port\":\"8000\"")

