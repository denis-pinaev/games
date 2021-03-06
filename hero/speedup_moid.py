import binascii
import pyamf
import sys
import json
import datetime
import time
import random
import requests
service = ''
method = ''

from common import *

persons = [
              {"pid":"124520","auth":"1e365d477c3207804013abaddbb6a0c4","gid":0,"sid":""},#corc
              {"pid":"144536559","auth":"731331d4e19d1f5483acd67abf424b58","gid":0,"sid":""},#poly
              {"pid":"160511757","auth":"6dc2dba90c1cc9d935542aa6a60c6fb4","gid":0,"sid":""},#vasya tanakan
              {"pid":"161702967","auth":"a5738509fb8e7486b45e8ba01436c6bb","gid":0,"sid":""},#mari kremer
          ]
          

actionCommand = 'Knights.doAction'
data = ''
init_log("hero_help2_log")
ctr = int(random.random()*10000)
def getCTR():
    global ctr
    ctr += 1
    return str(ctr)
 
def getHelpSpeed(hbid):
    global sid, gid, service, method
    service = actionCommand
    method = 'recipeFinish'
    init_params(nsid=sid, ngid=gid, nservice=service, nmethod=method)
    #data	{"count":33,"type":"entities","method":"recipeFinish","index":"65540"}
    dataString = '{"count":5,"type":"entities","method":"recipeFinish","index":"%s","rnd":%s,"ctr":%s,"sessionKey":"%s"}' % (hbid, getRandom(), getCTR(), sid)
    params = createData(method, dataString)
    log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("recipeFinish done "+hbid, True)
    else:
        log(resp["data"], True)        

def hide(hbids):
    for hbid in hbids:
        hideOne(str(hbid))

def hideOne(hbid):
    global sid, gid, service, method
    service = actionCommand
    method = 'entityStore'
    init_params(nsid=sid, ngid=gid, nservice=service, nmethod=method)
    #dataString = '{"count":5,"type":"entities","method":"recipeFinish","index":"%s","rnd":%s,"ctr":%s,"sessionKey":"%s"}' % (hbid, getRandom(), getCTR(), sid)
    dataString = '{"method":"entityStore","sceneId":"%s","rnd":%s,"ctr":%s,"sessionKey":"%s"}' % (hbid, getRandom(), getCTR(), sid)
    params = createData(method, dataString)
    log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("entityStore done "+hbid, True)
    else:
        log(resp["data"], True)        

def getHelpSpeeds(hbids):
    for hbid in hbids:
        getHelpSpeed(str(hbid))

def getWorld(pers):
    global sid, gid, service, method
    service = actionCommand
    method = 'friendsGetWorld'
    init_params(nsid=sid, ngid=gid, nservice=service, nmethod=method)
    dataString = '{"rnd":%s,"friendId":"%s","ctr":%s,"sessionKey":"%s","method":"%s"}' % (getRandom(), pers, getCTR(), sid, method)
    params = createData(method, dataString)
    log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("getWorld %s done" % pers, True)
    else:
        log(resp["data"], True)
    return o
    
    
def showOne(hbid):#frozen!
    global sid, gid, service, method
    service = actionCommand
    method = 'entityRestore'
    init_params(nsid=sid, ngid=gid, nservice=service, nmethod=method)
    dataString = '{"x":22,"y":-6,"dir":0,"method":"entityRestore","id":733825800,"sceneId":%d,"rnd":%s,"ctr":%s,"sessionKey":"%s","level":3}' % (hbid, getRandom(), getCTR(), sid)
    params = createData(method, dataString)
    log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("entityRestore done", True)
    else:
        log(resp["data"], True)
        
def moveBuilding(bid, x, y, d):
    global sid, gid, service, method
    service = actionCommand
    method = 'entityMove'
    dataString = '{"x":%d,"y":%d,"dir":%d,"sceneId":%s,"rnd":%s,"ctr":%s,"sessionKey":"%s","method":"%s"}' % (x, y, d, bid, getRandom(), getCTR(), sid, method)
    print dataString
    params = createData(method, dataString)
    log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("move done %d:%d" % (x, y), True)
    else:
        log(resp["data"], True)



sendSTR = [76854,77729,77239]

person = 1
gid = 0
sid = ''
pid = persons[person]["pid"]
auth = persons[person]["auth"]
data, gid, sid = init(pid, auth)

person_id = persons[person]["pid"]

print sendSTR
if len(sendSTR)>0:
    hide(sendSTR)
    #moveBuilding(sendSTR[0], x, y, 8)
