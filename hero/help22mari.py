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
              {"pid":"161702967","auth":"a5738509fb8e7486b45e8ba01436c6bb","gid":0,"sid":""},#mari kremer
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
    
    start_value = 12
    rest_value = 0
    
    lvl_need = (start_value + 1) * 5

    total = 1000
    s_i = 1
    i = 0
    while s_i<=total:
        sendHelp(str(s_i), '1,2,3,4,'+str(s_i))
        i += 5
        s_i += 1
        if i>lvl_need: lvl_need+=5;rest_value+=1;i=0
        print rest_value, i*100/lvl_need
