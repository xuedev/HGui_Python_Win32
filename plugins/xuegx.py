#coding:utf-8
import hashlib
import uuid
def getMac(param):
           node = uuid.getnode()
           mac = uuid.UUID(int = node).hex[-12:]
           return mac

def getMd5(param):
           m2 = hashlib.md5()
           m2.update(param)
           return m2.hexdigest() 


def getFileCode():
    id = getMd5(getMac(""))
    rid = id[::-1]
    return rid

def getRegCode(fileCode):
    return getMd5(fileCode)[8:16]
    
def write(data):
    o = open("code.data","w")
    o.write(data)
    o.close()
def init(param):
        return "0"
