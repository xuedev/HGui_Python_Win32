import ctypes
import win32api
import win32con
import win32gui

def MinWindow(param):
        hn=win32gui.FindWindow('CEFCLIENT',None)
        win32gui.ShowWindow(hn,win32con.SW_MINIMIZE)
        return str("0")
