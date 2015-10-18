# -*- coding: utf-8 -*-

import sys
import json
import random
from common import *
from buildInfo import *

actionCommand = 'Knights.doAction'
gid = 0
sid = ''
init_log("healObject")
ctr = int(random.random()*10000)

def getCTR():
    global ctr
    ctr += 1
    return str(ctr)

def battleHeal(sity):
    global sid, gid, service, method
    service = 'Knights.globalMap'
    method = 'healObject'
    init_params(nsid=sid, ngid=gid, nservice=service, nmethod=method)
    dataString = '{"id":%s,"v":"%s","ctr":%s,"sessionKey":"%s","method":"%s"}' % (str(sity), getGameVersion(), getCTR(), sid, method)
    params = createData(method, dataString)
    #log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log(method+" done", False)
    else:
        log(resp["data"], False)
    return o
    

pid = sys.argv[1]
auth = sys.argv[2]
sity = sys.argv[3]
data, gid, sid = init(pid, auth)
res = data
if data["error"] == 0:
    data_map = battleHeal(sity)
    data_map["initInfo"] = data
    res = data_map
print json.dumps(res, indent=4)
