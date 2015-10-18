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
init_log("getPresentEnergy")
ctr = int(random.random()*10000)

def getCTR():
    global ctr
    ctr += 1
    return str(ctr)

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
sss = "https://vk.com/app3289256#post="
data, gid, sid = init(pid, auth)
hashStr = None
if data["error"] == 0:
    data = battleSay()
    if data["error"] == 0:
        hashStr = data['hash']
        log(sss+hashStr)
        data, gid, sid = init(pid, auth, hashStr)
if hashStr: data["presentURL"] = sss+hashStr
print json.dumps(data, indent=4)
