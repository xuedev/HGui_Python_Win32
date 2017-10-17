#coding:utf-8
import StringIO
import gzip

def zip(data):
    compressedstream = StringIO.StringIO("")
    gzipper = gzip.GzipFile(filename='', mode='wr',compresslevel=9, fileobj=compressedstream)
    gzipper.write(data)
    gzipper.close()
    return compressedstream.getvalue()

def unzip(data):
    compressedstream = StringIO.StringIO(data)
    gzipper = gzip.GzipFile(fileobj=compressedstream)
    data = gzipper.read()
    gzipper.close()
    return data
