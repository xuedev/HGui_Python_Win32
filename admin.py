#coding:utf-8
import hashlib
import uuid
import sys
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
    o = open("register.data","w")
    o.write(data)
    o.close()

if __name__ == '__main__':
        mac = None
        if len(sys.argv)>1:
            mac = sys.argv[1]
            
        if mac == None:
            print u"请输入Code"
        else:
            write(getRegCode(mac))
            print u"成功生成注册文件"
