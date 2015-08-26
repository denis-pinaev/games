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
from buildInfo import *
service = ''
method = ''


person = 1
pids = ["124520", "102137300"]
auths = ["1e365d477c3207804013abaddbb6a0c4", "e78c0aad90f427b06653067a45de6c6b"]
#              {"pid":"102137300","auth":"e78c0aad90f427b06653067a45de6c6b","gid":0,"sid":""},#corcc

start_hero = ''
pid = pids[person]
auth = auths[person]
data = ''
actionCommand = 'Knights.doAction'
gid = 0
sid = ''

init_log("hero_lvl_log")

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
    #dataString ='{"image":"default","userLocale":"russian","imgTemplate":"","storyAction":"beat","cdn":"","storyId":"1","locKey":"#OG_PVP_WIN_DESC","text":"!","storyType":"profile","ctr":%s,"sessionKey":"%s","method":"%s"}' % (getCTR(), sid, method)
    params = createData(method, dataString)
    #log("%s:%s %s" % (service, method, json.dumps(params)))
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
    log(sss+hashStr, True, "+hero_lvl", False)
    #data, gid, sid = init(pid, auth, hashStr)