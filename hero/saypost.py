# -*- coding: utf-8 -*-

import binascii
import pyamf
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
pids = ["124520"]
auths = ["1e365d477c3207804013abaddbb6a0c4"]
start_hero = ''
pid = pids[person]
auth = auths[person]
data = ''
actionCommand = 'Knights.doAction'
gid = 0
sid = ''

init_log("hero_say_log")

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
    dataString = '{"image":"default","userLocale":"russian","imgTemplate":"","storyAction":"beat","cdn":"","storyId":"1","locKey":"#OG_PVP_WIN_DESC","text":"!","storyType":"profile","ctr":%s,"sessionKey":"%s","method":"%s"}' % (getCTR(), sid, method)
    params = createData(method, dataString)
    log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("battleSay done", True)
    else:
        log(resp["data"], True)
        time.sleep(99)
    return o
    

sss = "vk.com/app3289256#post="
data, gid, sid = init(pid, auth)

for i in range(5):
    o = battleSay()
    hashStr = o['hash']
    log(sss+hashStr, True, "+hero_post", False)
    data, gid, sid = init(pid, auth, hashStr)

