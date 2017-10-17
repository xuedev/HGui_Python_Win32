import ConfigParser
import os
import comm

config = ConfigParser.ConfigParser()
path = os.getcwd()+'\\set.ini'

def run(code):
        exec code
        return "ok"

def runJs(js):
        comm.browser.GetMainFrame().ExecuteJavascript(js)
        del js
        return "ok"
        
def getAppCfg(key):
        config.readfp(open(path))
        return config.get("app",key)
def setAppCfg(key,value):
        config.readfp(open(path))
        print config.set("app",key,value)
        config.write(open(path,"w"))

def getUiCfg(key):
        config.readfp(open(path))
        return config.get("ui",key)
def setUiCfg(key,value):
        config.readfp(open(path))
        print config.set("ui",key,value)
        config.write(open(path,"w"))
