# -*- coding: utf-8 -*-
# CEF Python 3 example application.
#coding:utf-8
# Checking whether python architecture and version are valid, otherwise an obfuscated error
# will be thrown when trying to load cefpython.pyd with a message "DLL load failed".
import platform
if platform.architecture()[0] != "32bit":
    raise Exception("Architecture not supported: %s" % platform.architecture()[0])
import proxy
import sys
import os
def GetApplicationPath(file=None):
    import re, os
    # If file is None return current directory without trailing slash.
    if file is None:
        file = ""
    # Only when relative path.
    if not file.startswith("/") and not file.startswith("\\") and (
            not re.search(r"^[\w-]+:", file)):
        if hasattr(sys, "frozen"):
            path = os.path.dirname(sys.executable)
        elif "__file__" in globals():
            path = os.path.dirname(os.path.realpath(__file__))
        else:
            path = os.getcwd()
        path = path + os.sep + file
        path = re.sub(r"[/\\]+", re.escape(os.sep), path)
        path = re.sub(r"[/\\]+$", "", path)
        return path
    return str(file)

def GetParentPath(file=None):
    if file is None:
        file = ""
        
    global currpath
    if hasattr(sys, "frozen"):
            currpath = os.path.dirname(sys.executable)
    elif "__file__" in globals():
            currpath = os.path.dirname(os.path.realpath(__file__))
    else:
            currpath = os.getcwd()
    #print path[0:path.rfind("base")]
    return currpath[0:currpath.rfind("base")]+file


import json
from sys import path
path.append(r"%s" % GetParentPath())
path.append(r"%splugins" % GetParentPath())
print path

from plugins import *
import comm

import codecs
from cefpython3 import cefpython
#import cefpython_py27 as cefpython
import base as cefwindow
import win32con
import win32gui
import win32api
import time

DEBUG = True

def GetErrorStr():
    (ErrorType, ErrorValue, ErrorTB) = sys.exc_info()
    return "%s" % ErrorValue

def ExceptHook(excType, excValue, traceObject):
    import traceback, os, time, codecs
    # This hook does the following: in case of exception write it to
    # the "error.log" file, display it to the console, shutdown CEF
    # and exit application immediately by ignoring "finally" (_exit()).
    errorMsg = "\n".join(traceback.format_exception(excType, excValue,
            traceObject))
    errorFile = GetParentPath("error.log")
    try:
        appEncoding = cefpython.g_applicationSettings["string_encoding"]
    except:
        appEncoding = "utf-8"
    if type(errorMsg) == bytes:
        errorMsg = errorMsg.decode(encoding=appEncoding, errors="replace")
    try:
        with codecs.open(errorFile, mode="a", encoding=appEncoding) as fp:
            fp.write("\n[%s] %s\n" % (
                    time.strftime("%Y-%m-%d %H:%M:%S"), errorMsg))
    except:
        print("cefpython: WARNING: failed writing to error file: %s" % (
                errorFile))
    # Convert error message to ascii before printing, otherwise
    # you may get error like this:
    # | UnicodeEncodeError: 'charmap' codec can't encode characters
    errorMsg = errorMsg.encode("ascii", errors="replace")
    errorMsg = errorMsg.decode("ascii", errors="replace")
    print("\n"+errorMsg+"\n")
    cefpython.QuitMessageLoop()
    cefpython.Shutdown()
    os._exit(1)

def InitCefApp():
    appSettings = dict()
    if DEBUG:
        # cefpython debug messages in console and in log_file
        appSettings["debug"] = False
        cefwindow.g_debug = True
    appSettings["log_file"] = GetApplicationPath("HGui.log")
    appSettings["log_severity"] = cefpython.LOGSEVERITY_ERROR
    appSettings["release_dcheck_enabled"] = True # Enable only when debugging
    appSettings["browser_subprocess_path"] = "%s/%s" % (
            cefpython.GetModuleDirectory(), "subprocess")
    cefpython.Initialize(appSettings)

def InitBrowserSettings():
    browserSettings = dict()
    browserSettings["universal_access_from_file_urls_allowed"] = True
    browserSettings["file_access_from_file_urls_allowed"] = True
    browserSettings["web_security_disabled"] = True
    return browserSettings

def readJs(jsName):
    f = open(GetParentPath("\\js\\"+jsName),"r")
    s = f.read()
    return s

def getJsName(i):
    global menuData
    for d in menuData:
        if(d["id"] == str(i)):
            global browser
            browser.GetMainFrame().ExecuteJavascript("top.menuName = '"+d["title"]+"';")
            return d["js"]

    return ""

def RunJs(jsName):
    try:
        js = readJs(jsName)
        global browser
        browser.GetMainFrame().ExecuteJavascript(js)
    except:
        browser.GetMainFrame().ExecuteJavascript("alert('Failed to execute "+jsName+"')")

def OnCommand(hwnd,msg,wParam,lParam):
    
    #执行菜单js
    if(msg == 273):
        RunJs(getJsName(wParam))
    

def InitMenu(hwnd):
   try:
        #初始化菜单
        f = open(GetParentPath("\\menu\\menus_map.json"),"r")
        s = f.read()
        j = json.loads(s)
        
        if(getAppCfg("is_show_menu") == "0"):
            return
        
        global menuData 
        menuData =  j["menus"]

        menus = win32gui.CreateMenu()
        for d in menuData:
            #print d["id"]
            #print d["title"]
            win32gui.AppendMenu(menus,win32con.MF_STRING|win32con.MF_ENABLED,int(d["id"]),d["title"])

        win32gui.SetMenu(hwnd,menus)
   except:
        win32gui.MessageBox(None,u"初始化菜单失败",u"错误",0)
        #pass

import ConfigParser
config = ConfigParser.ConfigParser()
path = os.getcwd()+'\\set.ini'
def getAppCfg(key):
        config.readfp(open(path))
        return config.get("app",key)
def setAppCfg(key,value):
        config.readfp(open(path))
        print config.set("app",key,value)
        config.write(open(path,"w"));
        
def InitBrowser():
    wndproc = {
        win32con.WM_COMMAND:OnCommand,
        win32con.WM_CLOSE: CloseWindow,
        win32con.WM_DESTROY: QuitApplication,
        win32con.WM_SIZE: cefpython.WindowUtils.OnSize,
        win32con.WM_SETFOCUS: cefpython.WindowUtils.OnSetFocus,
        win32con.WM_ERASEBKGND: cefpython.WindowUtils.OnEraseBackground
    }

    windowHandle = cefwindow.CreateWindow(title=getAppCfg("title"),
            className="class_hgui", width=int(getAppCfg("width")), height=int(getAppCfg("height")),
            icon="icon.ico", windowProc=wndproc)

    #显示模式
    show = getAppCfg("show")
    if show == "hide":
        win32gui.ShowWindow(windowHandle,win32con.SW_HIDE)
    if show == "min":
        win32gui.ShowWindow(windowHandle,win32con.SW_MINIMIZE)
    if show == "max":
        win32gui.ShowWindow(windowHandle,win32con.SW_SHOWMAXIMIZED)
    
    #初始化菜单
    InitMenu(windowHandle)


    windowInfo = cefpython.WindowInfo()
    windowInfo.SetAsChild(windowHandle)

    global browser
    browser = cefpython.CreateBrowserSync(windowInfo, InitBrowserSettings(),
            navigateUrl=GetParentPath(getAppCfg("start_url")))


def BindJavascipt():
    global browser
    jsBindings = cefpython.JavascriptBindings(
                bindToFrames=False, bindToPopups=True)
    jsBindings.SetProperty("currdir", GetParentPath(""))
    jsBindings.SetObject("app", JavascriptApp(browser))
    browser.SetJavascriptBindings(jsBindings)

def handleProxy(request):
    url = request.GetUrl()[:70]
    keys = proxy.url_url.keys()
    for d in keys:
        if url.find(d)>-1:
            request.SetUrl(proxy.url_url[d])
def Main():
    sys.excepthook = ExceptHook
    
    #初始化CEFApp
    InitCefApp()

    #加密代码
    m = __import__("xuegx")
    f = getattr(m,"init")
    ret = f("")
    if ret !="0":
        win32api.MessageBox(win32con.NULL,u"请把注册文件放到软件目录下！\n 您可以把目录下的code.data发送给软件维护人员，以获得注册文件！", u'本软件未注册', win32con.MB_OK)
        exit()
    
    #初始化browser
    global browser
    InitBrowser()

    #绑定浏览器handler
    clientHandler = ClientHandler()
    browser.SetClientHandler(clientHandler)

    #绑定Js对象
    BindJavascipt()

    #赋值到comm
    comm.browser = browser
    comm.currdir = GetParentPath()+"\\"
    #Quit
    cefpython.MessageLoop()
    cefpython.Shutdown()

def CloseWindow(windowHandle, message, wparam, lparam):
    #browser = cefpython.GetBrowserByWindowHandle(windowHandle)
    #browser.CloseBrowser()
    return win32gui.DefWindowProc(windowHandle, message, wparam, lparam)

def QuitApplication(windowHandle, message, wparam, lparam):
    win32gui.PostQuitMessage(0)
    return 0

#--------------------------ClientHandler----------------------------------------
class ClientHandler:

    # -------------------------------------------------------------------------
    # DisplayHandler
    # -------------------------------------------------------------------------

    def OnLoadingStateChange(self, browser,is_loading, can_go_back,
            can_go_forward):
        print("DisplayHandler::OnLoadingStateChange()")
        print("  isLoading = %s, canGoBack = %s, canGoForward = %s" \
                % (is_loading, can_go_back, can_go_forward))

    def OnAddressChange(self, browser, frame, url):
        print("DisplayHandler::OnAddressChange()")
        print("  url = %s" % url)

    def OnTitleChange(self, browser, title):
        print("DisplayHandler::OnTitleChange()")
        print("  title = %s" % title)

    def OnTooltip(self, browser, text_out):
        # OnTooltip not yet implemented (both Linux and Windows),
        # will be fixed in next CEF release, see Issue 783:
        # https://code.google.com/p/chromiumembedded/issues/detail?id=783
        print("DisplayHandler::OnTooltip()")
        print("  text = %s" % text_out[0])

    statusMessageCount = 0
    def OnStatusMessage(self, browser, value):
        if not value:
            # Do not notify in the console about empty statuses.
            return
        self.statusMessageCount += 1
        if self.statusMessageCount > 3:
            # Do not spam too much.
            return
        print("DisplayHandler::OnStatusMessage()")
        print("  value = %s" % value)

    def OnConsoleMessage(self, browser, message, source, line):
        print("DisplayHandler::OnConsoleMessage()")
        print("  message = %s" % message)
        print("  source = %s" % source)
        print("  line = %s" % line)

    # -------------------------------------------------------------------------
    # KeyboardHandler
    # -------------------------------------------------------------------------

    def OnPreKeyEvent(self, browser, event, event_handle,
            is_keyboard_shortcut_out):
        #print("KeyboardHandler::OnPreKeyEvent()")
		pass

    def OnKeyEvent(self, browser, event, event_handle):
        #print("KeyboardHandler::OnKeyEvent()")
        if platform.system() == "Linux":
            print("  native_key_code = %s" % event["native_key_code"])
            # F5 = 71
            if event["native_key_code"] == 71:
                print("  F5 pressed! Reloading page..")
                browser.ReloadIgnoreCache()
        elif platform.system() == "Windows":
            #print("  windows_key_code = %s" % event["windows_key_code"])
            # F5 = VK_F5
            if event["windows_key_code"] == cefpython.VK_F5:
                print("  F5 pressed! Reloading page..")
                browser.ReloadIgnoreCache()

    # -------------------------------------------------------------------------
    # RequestHandler
    # -------------------------------------------------------------------------

    def OnBeforeBrowse(self, browser, frame, request, is_redirect):
        print("RequestHandler::OnBeforeBrowse()")
        print("  url = %s" % request.GetUrl()[:70])
        handleProxy(request)
        return False

    def OnBeforeResourceLoad(self, browser, frame, request):
        print("RequestHandler::OnBeforeResourceLoad()")
        print("  url = %s" % request.GetUrl()[:70])
        handleProxy(request)
        return False

    def OnResourceRedirect(self, browser, frame, old_url, new_url_out,request,response):
        print("RequestHandler::OnResourceRedirect()")
        print("  old url = %s" % old_url[:70])
        print("  new url = %s" % new_url_out[0][:70])

    def GetAuthCredentials(self, browser, frame, is_proxy, host, port, realm,
            scheme, callback):
        print("RequestHandler::GetAuthCredentials()")
        print("  host = %s" % host)
        print("  realm = %s" % realm)
        callback.Continue(username="test", password="test")
        return True

    def OnQuotaRequest(self, browser, origin_url, new_size, callback):
        print("RequestHandler::OnQuotaRequest()")
        print("  origin url = %s" % origin_url)
        print("  new size = %s" % new_size)
        callback.Continue(True)
        return True

    def GetCookieManager(self, browser, main_url):
        # Create unique cookie manager for each browser.
        # --
        # Buggy implementation in CEF, reported here:
        # https://code.google.com/p/chromiumembedded/issues/detail?id=1043
        cookieManager = browser.GetUserData("cookieManager")
        if cookieManager:
            return cookieManager
        else:
            cookieManager = cefpython.CookieManager.CreateManager("")
            browser.SetUserData("cookieManager", cookieManager)
            return cookieManager

    def OnProtocolExecution(self, browser, url, allow_execution_out):
        # There's no default implementation for OnProtocolExecution on Linux,
        # you have to make OS system call on your own. You probably also need
        # to use LoadHandler::OnLoadError() when implementing this on Linux.
        print("RequestHandler::OnProtocolExecution()")
        print("  url = %s" % url)
        if url.startswith("magnet:"):
            print("  Magnet link allowed!")
            allow_execution_out[0] = True

    def _OnBeforePluginLoad(self, browser, url, policy_url, info):
        # Plugins are loaded on demand, only when website requires it,
        # the same plugin may be called multiple times.
        print("RequestHandler::OnBeforePluginLoad()")
        print("  url = %s" % url)
        print("  policy url = %s" % policy_url)
        print("  info.GetName() = %s" % info.GetName())
        print("  info.GetPath() = %s" % info.GetPath())
        print("  info.GetVersion() = %s" % info.GetVersion())
        print("  info.GetDescription() = %s" % info.GetDescription())
        # False to allow, True to block plugin.
        return False

    def _OnCertificateError(self, cert_error, request_url, callback):
        print("RequestHandler::OnCertificateError()")
        print("  certError = %s" % cert_error)
        print("  requestUrl = %s" % request_url)
        if request_url.startswith(
                "https://sage.math.washington.edu:8091/do-not-allow"):
            print("  Not allowed!")
            return False
        if request_url.startswith(
                "https://sage.math.washington.edu:8091/hudson/job/"):
            print("  Allowed!")
            callback.Continue(True)
            return True
        return False

    # -------------------------------------------------------------------------
    # LoadHandler
    # -------------------------------------------------------------------------

    def OnLoadStart(self, browser, frame):
        print("LoadHandler::OnLoadStart()")
        print("  frame url = %s" % frame.GetUrl()[:70])

    def OnLoadEnd(self, browser, frame,http_code):
        print("LoadHandler::OnLoadEnd()")
        print("  frame url = %s" % frame.GetUrl()[:70])
        # For file:// urls the status code = 0
        print("  http status code = %s" % http_code)

        RunJs("on_load.js")


    def OnLoadError(self, browser, frame, error_code, error_text_out, failed_url):
        print("LoadHandler::OnLoadError()")
        print("  frame url = %s" % frame.GetUrl()[:70])
        print("  error code = %s" % error_code)
        print("  error text = %s" % error_text_out[0])
        print("  failed url = %s" % failed_url)
        customErrorMessage = "My custom error message!"
        frame.LoadUrl("data:text/html,Failed to load url [%s]" % failed_url)

    def OnRendererProcessTerminated(self, browser, status):
        print("LoadHandler::OnRendererProcessTerminated()")
        statuses = {
            cefpython.TS_ABNORMAL_TERMINATION: "TS_ABNORMAL_TERMINATION",
            cefpython.TS_PROCESS_WAS_KILLED: "TS_PROCESS_WAS_KILLED",
            cefpython.TS_PROCESS_CRASHED: "TS_PROCESS_CRASHED"
        }
        statusName = "Unknown"
        if status in statuses:
            statusName = statuses[status]
        print("  status = %s" % statusName)

    def OnPluginCrashed(self, browser, plugin_ath):
        print("LoadHandler::OnPluginCrashed()")
        print("  plugin path = %s" % plugin_ath)

    # -------------------------------------------------------------------------
    # LifespanHandler
    # -------------------------------------------------------------------------

    # Empty place-holders: popupFeatures, windowInfo, client, browserSettings.
    #def OnBeforePopup(self, browser, frame, target_url, target_frame_name,
     #       popup_features, window_info, client, browser_settings_out, no_javascript_access):
     #   print("LifespanHandler::OnBeforePopup()")
     #   print("  targetUrl = %s" % target_url)
     #   allowPopups = True
     #   return allowPopups

#----------------------------JavascriptApp------------------------------------
import thread
def threadproc(module,func,param,callback):
    try:
        m = __import__(module)
        f = getattr(m,func)
        ret = f(param);
        callback.Call("".join(ret))
    except:
        print sys.exc_info()
        callback.Call("\"%s\"" % GetErrorStr())
        
class JavascriptApp:
    mainBrowser = None
    stringVisitor = None
    currdir = GetParentPath("")

    def __init__(self, mainBrowser):
        self.mainBrowser = mainBrowser
    def CurrDir(self):
        self.mainBrowser.GetMainFrame().ExecuteJavascript(
                "console.log(\"%s\")" % sys.path)

    def PythonAsync(self,module,func,param,callback):
        thread.start_new_thread(threadproc,(module,func,param,callback))
            
    def Python(self,module,func,param,callback):
        try:
            m = __import__(module)
            f = getattr(m,func)
            ret = f(param);
            callback.Call("".join(ret))
        except:
            print sys.exc_info()
            callback.Call("\"%s\"" % GetErrorStr())
        
    def ExecuteFunction(self, *args):
        self.mainBrowser.GetMainFrame().ExecuteFunction(*args)

    def TestJSCallback(self, jsCallback):
        print("jsCallback.GetFunctionName() = %s" % jsCallback.GetFunctionName())
        print("jsCallback.GetFrame().GetIdentifier() = %s" % \
                jsCallback.GetFrame().GetIdentifier())
        jsCallback.Call("This message was sent from python using js callback")

    def TestJSCallbackComplexArguments(self, jsObject):
        jsCallback = jsObject["myCallback"];
        jsCallback.Call(1, None, 2.14, "string", ["list", ["nested list", \
                {"nested object":None}]], \
                {"nested list next":[{"deeply nested object":1}]})

    def TestPythonCallback(self, jsCallback):
        jsCallback.Call(self.PyCallback)

    def PyCallback(self, *args):
        message = "PyCallback() was executed successfully! Arguments: %s" \
                % str(args)
        print(message)
        self.mainBrowser.GetMainFrame().ExecuteJavascript(
                "window.alert(\"%s\")" % message)

    def GetSource(self):
        # Must keep a strong reference to the StringVisitor object
        # during the visit.
        self.stringVisitor = StringVisitor()
        self.mainBrowser.GetMainFrame().GetSource(self.stringVisitor)

    def GetText(self):
        # Must keep a strong reference to the StringVisitor object
        # during the visit.
        self.stringVisitor = StringVisitor()
        self.mainBrowser.GetMainFrame().GetText(self.stringVisitor)

    def NewWindow(self):
        frame = MainFrame()
        frame.Show()

    # -------------------------------------------------------------------------
    # Cookies
    # -------------------------------------------------------------------------
    cookieVisitor = None

    def VisitAllCookies(self):
        # Need to keep the reference alive.
        self.cookieVisitor = CookieVisitor()
        cookieManager = self.mainBrowser.GetUserData("cookieManager")
        if not cookieManager:
            print("\nCookie manager not yet created! Visit http website first")
            return
        cookieManager.VisitAllCookies(self.cookieVisitor)

    def VisitUrlCookies(self):
        # Need to keep the reference alive.
        self.cookieVisitor = CookieVisitor()
        cookieManager = self.mainBrowser.GetUserData("cookieManager")
        if not cookieManager:
            print("\nCookie manager not yet created! Visit http website first")
            return
        cookieManager.VisitUrlCookies(
            "http://www.html-kit.com/tools/cookietester/",
            False, self.cookieVisitor)
        # .www.html-kit.com

    def SetCookie(self):
        cookieManager = self.mainBrowser.GetUserData("cookieManager")
        if not cookieManager:
            print("\nCookie manager not yet created! Visit http website first")
            return
        cookie = cefpython.Cookie()
        cookie.SetName("Created_Via_Python")
        cookie.SetValue("yeah really")
        cookieManager.SetCookie("http://www.html-kit.com/tools/cookietester/",
                cookie)
        print("\nCookie created! Visit html-kit cookietester to see it")

    def DeleteCookies(self):
        cookieManager = self.mainBrowser.GetUserData("cookieManager")
        if not cookieManager:
            print("\nCookie manager not yet created! Visit http website first")
            return
        cookieManager.DeleteCookies(
                "http://www.html-kit.com/tools/cookietester/",
                "Created_Via_Python")
        print("\nCookie deleted! Visit html-kit cookietester to see the result")

class StringVisitor:
    def Visit(self, string):
        print("\nStringVisitor.Visit(): string:")
        print("--------------------------------")
        print(string)
        print("--------------------------------")

class CookieVisitor:
    def Visit(self, cookie, count, total, deleteCookie):
        if count == 0:
            print("\nCookieVisitor.Visit(): total cookies: %s" % total)
        print("\nCookieVisitor.Visit(): cookie:")
        print(cookie.Get())
        # True to continue visiting cookies
        return True


            
if __name__ == "__main__":
    Main()
