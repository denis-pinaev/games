import binascii
import pyamf
import sys
import json
import datetime
import time
import random
import requests
from common import *


person = 0
pids = ["124520", "160511757"]
auths = ["1e365d477c3207804013abaddbb6a0c4", "6dc2dba90c1cc9d935542aa6a60c6fb4"]
pid = pids[person]
auth = auths[person]
data = ''
actionCommand = 'Knights.doAction'
gid = 0
sid = ''
service = ''
method = ''

action = 'hp'
if len(sys.argv) > 1:
    action = sys.argv[1]
    
isHide = action[0] == 'h'
isKuz = action[1] == 'k'
isSkl = action[1] == 's'
isRes = action[1] == 'r'

def getRandom():
    return str(int(random.random()*1000))
    
init_log("move")
ctr = int(random.random()*10000)
def getCTR():
    global ctr
    ctr += 1
    return str(ctr)

def moveBuilding(bid, x, y, d):
    global sid, gid, service, method
    service = actionCommand
    method = 'entityMove'
    init_params(nsid=sid, ngid=gid, nservice=service, nmethod=method)
    dataString = '{"x":%d,"y":%d,"dir":%d,"sceneId":%s,"rnd":%s,"ctr":%s,"sessionKey":"%s","method":"%s"}' % (x, y, d, bid, getRandom(), getCTR(), sid, method)
    params = createData(method, dataString)
    log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("move done %d:%d dir:%d for %s" % (x, y, d, bid), True)
    else:
        log(resp["data"], True)    
        
def getSklad():
    a=[]
    a.append({"x":26,"dir":4,"rnd":834,"sceneId":66541,"y":-14})
    return a
    
#wood:
#   66751 x=1,y=9
#stone:
#   65554 x=3,y=11
#iron:
#   65562 x=1,y=11

data, gid, sid = init(pid, auth)

def getRes():
    a=[]
    a.append({"x":1,"dir":4,"rnd":1,"sceneId":66751,"y":9})
    a.append({"x":2,"dir":4,"rnd":2,"sceneId":65554,"y":11})
    a.append({"x":1,"dir":4,"rnd":3,"sceneId":65562,"y":11})
    return a
    
def getKuz():
    a=[]
    a.append({"x":22,"dir":2,"rnd":655,"sceneId":65571,"y":-11})
    a.append({"x":25,"dir":2,"rnd":239,"sceneId":65588,"y":-11})
    a.append({"x":28,"dir":2,"rnd":26,"sceneId":65635,"y":-11})
    #a.append({"x":26,"dir":4,"rnd":834,"sceneId":66541,"y":-11}) #65653
    return a

def getPalat():
    a=[]
    a.append({"x":15,"dir":4,"rnd":22,"sceneId":65629,"y":-5})
    a.append({"x":17,"dir":0,"rnd":48,"sceneId":65557,"y":-6})
    a.append({"x":19,"dir":4,"rnd":515,"sceneId":65553,"y":-6})
    a.append({"x":23,"dir":4,"rnd":299,"sceneId":66478,"y":-5})
    a.append({"x":23,"dir":2,"rnd":694,"sceneId":65597,"y":-3})
    a.append({"x":23,"dir":2,"rnd":376,"sceneId":65615,"y":-1})
    a.append({"x":23,"dir":0,"rnd":456,"sceneId":65598,"y":1})
    a.append({"x":21,"dir":2,"rnd":631,"sceneId":66499,"y":2})
    a.append({"x":19,"dir":2,"rnd":886,"sceneId":65649,"y":2})
    a.append({"x":17,"dir":2,"rnd":669,"sceneId":65538,"y":2})
    return a
    
    
#bids = [[65577, 20, -11], [65586,10,-7]]

if isKuz:
    bids = getKuz()
elif isSkl:
    bids = getSklad()
elif isRes:
    bids = getRes()

if isHide:
    for b in bids:
        moveBuilding(b["sceneId"], 36, 18, b["dir"])
else:
    for b in bids:
        moveBuilding(b["sceneId"], b["x"], b["y"], b["dir"])
    
