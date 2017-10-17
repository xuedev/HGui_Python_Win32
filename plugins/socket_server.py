#coding: utf-8
from socket import *
import os
import sys
import struct
import zlib
import base64
import time
import core
addr = ('',8000)
buf_size = 1024*1024*10
recvSock = None
start = True

#file_size = struct.calcsize

callback = ""
def handleConn(conn):
        try:
                buf = ""
                while True:
                        tmp =  conn.recv(buf_size)
                        if(len(tmp)>0):
                                buf += tmp
                        else:
                                break
        
                print len(buf)


                #print tmp

                buf = zlib.decompress(buf)
                core.runJs(callback+"('"+buf+"');")
                info = "接收到图片,大小为:%s" % str(len(buf))
                js = "top.recvLog('%s')" % info;
                core.runJs(js)
                
                
        except:
                (ErrorType, ErrorValue, ErrorTB) = sys.exc_info()
                (errno, err_msg) = ErrorValue
                error = "程序出现异常: %s, errno=%d" % (err_msg, errno)
                js = "top.recvLog('%s')" % error;
                core.runJs(js)
                pass

def flisten(param):
        global addr
        global callback
        global recvSock
        global start

        callback  = param

        recvSock = socket(AF_INET,SOCK_STREAM)
        recvSock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        recvSock.bind(addr)
        recvSock.listen(True)
        #core.runJs("top.log('等待连接');")
        while start:
                conn,addr = recvSock.accept()
                handleConn(conn)
        

if __name__ == '__main__':
        flisten("")

