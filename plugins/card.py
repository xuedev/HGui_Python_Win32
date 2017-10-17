import ctypes
from ctypes import *
dll = ctypes.windll.LoadLibrary( 'Mifare Reader.dll' )
def WriteCard(param):
        pStr = ctypes.c_char_p()
        pStr.value = param
        nRst = dll.WriteCard(pStr)
        return str(nRst)

def ReadCard(param):
        pStr = ctypes.create_string_buffer('\0'*100)
        nRst = dll.ReadCard(byref(pStr))
        return str(nRst)+","+str(pStr.value)

def SendKeys(param):
        return
