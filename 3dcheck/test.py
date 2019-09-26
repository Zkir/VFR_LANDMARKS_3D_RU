#!c:\Program Files\Python37\python.exe
import urllib.parse as urlparse
import os
import sys
import codecs
from mdlMisc import *
import cgi



sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

print ("Content-Type: text/html; charset=utf-8 \n\n")
print

url = os.environ.get("REQUEST_URI","") 
parsed = urlparse.urlparse(url) 
strParam=urlparse.parse_qs(parsed.query).get('param','')
strQuadrantName=url[1:-5]



param = cgi.FieldStorage().getvalue('param')

print (strQuadrantName+'\n')
print (param)