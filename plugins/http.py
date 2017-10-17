import urllib
import urllib2
import sys
import json
import os
import core

def test(param):
	import _imaging
	return "ok"

def tojson(param):
        return json.loads(param)
        
def get(param):
        j = tojson(param)
        f = urllib.urlopen(j["url"]).read()   
        return f
def post(param):
        j = tojson(param)
        req = urllib2.Request(j["url"])  
        post = j["data"] 
        #enable cookie  
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())  
        response = opener.open(req, post)  
        return response.read()

def download(param):
        j = tojson(param)
        path = os.getcwd()+"\\"+j["name"]
        file_object = open(path, 'w')
        file_object.writelines(get(param))
        file_object.close()
        return path

def runHttpFile(url):
        f = urllib.urlopen(url).read()
        core.run(f)
        return f
