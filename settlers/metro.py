import urllib
import json
import sys
import datetime

f = open('metro', 'r')
data = f.read()
f.close()
jdata = json.loads(data)
data = json.dumps(jdata, indent=4)
f = open('metro_out', 'w')
f.write(data)
f.close()
