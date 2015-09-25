import binascii
import sys
import json
import datetime
import time
import random
import requests
from common import *
from buildInfo import *
service = ''
method = ''
game_version = getGameVersion()



person = 0

persons = [
              {"pid":"124520","auth":"1e365d477c3207804013abaddbb6a0c4","gid":0,"sid":""},#corc
          ]

pid = persons[person]["pid"]
auth = persons[person]["auth"]
gid = 0
sid = ''
data = ''
actionCommand = 'Knights.doAction'
globalCommand = 'Knights.globalMap'

init_log("requests")

ctr = 0
def getCTR():
    global ctr
    ctr += 1
    return str(ctr)

def write(data, fn):
    f = open(fn,"wb")
    f.write(data)
    f.close()

def getVillage(vid):
    global sid, gid, service, method
    service = globalCommand
    method = 'getObjectInfo'
    init_params(nsid=sid, ngid=gid, nservice=service, nmethod=method)
    dataString = '{"v":"%s","id":"%s","ctr":%s,"sessionKey":"%s","method":"%s"}' % (game_version, vid, getCTR(), sid, method)
    params = createData(method, dataString)
    #log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("%s done" % method, True)
    else:
        log(resp["data"], True)
    return o


pers = persons[person]
pid = pers['pid']
auth = pers['auth']
gid =  pers['gid']
sid =  pers['sid']
    
    
data, gid, sid = init(pid, auth)


resp = getVillage(79)
write(json.dumps(resp, indent=4), 'gwReq79')
