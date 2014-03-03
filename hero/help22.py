import binascii
import sys
import json
import datetime
import time
import random
import requests
from common import *
service = ''
method = ''


person = 0
error = 0

persons = [
              {"pid":"124520","auth":"1e365d477c3207804013abaddbb6a0c4","gid":0,"sid":""},#corc
          ]

pid = persons[person]["pid"]
auth = persons[person]["auth"]
gid = 0
sid = ''
data = ''
actionCommand = 'Knights.doAction'

init_log("help_priority")
    
ctr = 0
def getCTR():
    global ctr
    ctr += 1
    return str(ctr)
    
def sendHelp(pers, hbid):
    global sid, gid, service, method
    service = actionCommand
    method = 'friendHelpApply'
    init_params(nsid=sid, ngid=gid, nservice=service, nmethod=method)
    dataString = '{"friendId":"%s","list":[%s],"rnd":%s,"ctr":%s,"sessionKey":"%s","method":"%s"}' % (pers, hbid, getRandom(), getCTR(), sid, method)
    params = createData(method, dataString)
    log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("friendHelpApply done " + pers, True)
    else:
        log(resp["data"], True)        


if True:
    pers = persons[person]
    pid = pers['pid']
    auth = pers['auth']
    gid =  pers['gid']
    sid =  pers['sid']
    
    data, gid, sid = init(pid, auth)

    total = 3000
    i = 0
    while i<=total:
        sendHelp(str(i), '1,2,3,4,'+str(i))
        i += 1
