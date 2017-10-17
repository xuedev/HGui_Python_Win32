import ctypes
import win32api
import win32con
import time
dll = ctypes.cdll.LoadLibrary( 'AutoUtils.dll' )
def SendString(param):
        pStr = ctypes.c_char_p()
        pStr.value = param
        nRst = dll.SendString(pStr)
        return str(nRst)

def PressEnterKey(param):
        win32api.keybd_event(13,0,0,0)
        win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
        time.sleep(0.01)
        return str("011")
