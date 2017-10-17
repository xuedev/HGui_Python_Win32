#coding: utf-8
# Written by xuegx
# A messy HTTP server based on TCP socket 

import BaseHTTPServer
import SimpleHTTPServer
import urllib
import io,shutil
import core
import ziputils
import json
import base64
import threading

global callback
global serverThread

def transDicts(params):
    dicts={}
    if len(params)==0:
        return
    params = params.split('&')
    for param in params:
        dicts[param.split('=')[0]]=param.split('=')[1]
    return dicts

class ImageHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
        def do_POST(self):
                try:
                    ip = self.client_address
                    datas = self.rfile.read(int(self.headers['content-length']))
                    buf = ziputils.unzip(datas)
                    buf = base64.b64decode(buf)
                    #buf = datas
                
                    #param = "%02d%s%s" % (len(ip[0]),ip[0],buf)
                    f = open("./ui/tmp/"+ip[0]+".png","wb")
                    f.write(buf)
                    #print len(ip[0])
                    
                    self.wfile.write("1")
                    self.wfile.close()
                    core.runJs(callback+"('"+ip[0]+"');")
                
                    del datas
                    del buf
                except:
                    self.wfile.write("0")
                    self.wfile.close()
                    core.runJs("console.log('出现异常');")

class ServerThread(threading.Thread):
    __host = None
    __port = None
    __server = None
    
    def __init__(self,host,port):
        threading.Thread.__init__(self)
        self.__host = host
        self.__port = port
        self.__server = BaseHTTPServer.HTTPServer((self.__host, self.__port), ImageHandler)

    def run(self):
        self.__server.serve_forever()

    def stop(self):
        pass
        
def flisten(param):
        global callback
        callback = param
        
        HOST = ''
        PORT = 8000
        global serverThread
        
        #serverThread = ServerThread(HOST,PORT)
        #serverThread.start()
        
        # Create the server, CGIHTTPRequestHandler is pre-defined handler
        server = BaseHTTPServer.HTTPServer((HOST, PORT), ImageHandler)
        # Start the server
        server.serve_forever()

        return "ok"
    
if __name__ == '__main__':
        flisten("top.recvImg")
