# -*- coding: utf-8 -*-

import sys
import json
import datetime
import random
from common import *
from buildInfo import *

actionCommand = 'Knights.doAction'
gid = 0
sid = ''
init_log("getMapRect")
ctr = int(random.random()*10000)

def getCTR():
    global ctr
    ctr += 1
    return str(ctr)

def getMapRect(x1,y1,x2,y2):
    global sid, gid, service, method
    service = 'Knights.globalMap'
    method = 'queryRect'
    init_params(nsid=sid, ngid=gid, nservice=service, nmethod=method)
    dataString = '{"x1":%s,"y1":%s,"x2":%s,"y2":%s,"rx2":0,"method":"%s","sessionKey":"%s","cachedClans":{},"ctr":%s,"ry2":0,"qlevel":2,"v":"%s","rx1":0,"ry1":0}' % (x1,y1,x2,y2, method, sid, getCTR(), getGameVersion())
    params = createData(method, dataString)
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log(method + " done", False)
    else:
        log(resp["data"], False)
        time.sleep(99)
    return o
    

pid = sys.argv[1]
auth = sys.argv[2]
x = 100
y = 50
d = 50
x1 = str(int(x)-d)
x2 = str(int(x)+d)
y1 = str(int(y)-d)
y2 = str(int(y)+d)
data, gid, sid = init(pid, auth)
if data["error"] == 0:
    data = getMapRect(x1,y1,x2,y2)
print json.dumps(data, indent=4)
