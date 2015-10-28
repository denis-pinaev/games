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
init_log("saveQuest")
ctr = int(random.random()*10000)

def getCTR():
    global ctr
    ctr += 1
    return str(ctr)

def saveQuest(q, restq):
    global sid, gid, service, method
    service = actionCommand
    method = 'saveQuests'
    init_params(nsid=sid, ngid=gid, nservice=service, nmethod=method)
    dataString = '{"active":{"%s":null},"ctr":%s,"sessionKey":"%s","method":"%s","order":[%s],"stat":{"exercises":[[%s,0]]},"completed":{"%s":1},"resources":{},"v":"%s"}' % (q,getCTR(),sid,method,restq,q,q, getGameVersion())
    params = createData(method, dataString)
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("saveQuests %s done" % q, False)
    else:
        log(resp["data"], False)
    return o

def battleSay():
    global sid, gid, service, method
    service = actionCommand
    method = 'createPost'
    init_params(nsid=sid, ngid=gid, nservice=service, nmethod=method)
    dataString = '{"image":"levelup","postAward":1,"locKey":"#OG_LEVEL_DESC","userLocale":"russian","sessionKey":"%s","cdn":"http://kn-cdn.playkot.com/vk/content/","imgTemplate":"levelup","ctr":%s,"storyId":"10","method":"%s","text":"!","storyType":"level","v":"%s","storyAction":"reach"}' % (sid, getCTR(), method, getGameVersion())
    params = createData(method, dataString)
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("battleSay done", False)
    else:
        log(resp["data"], False)
        time.sleep(99)
    return o
    

pid = sys.argv[1]
auth = sys.argv[2]
data, gid, sid = init(pid, auth)
q_done = []
if data["error"] == 0:
    try:
        q_ar = []
        for q in data['quests']['active']:
            q_ar.append(q)
        while len(q_ar)>0:
            q = q_ar.pop()
            saveQuest(q, ','.join(q_ar))
            q_done.append(q)
    except: None
data["questsDone"] = q_done
print json.dumps(data, indent=4)
