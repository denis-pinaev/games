import binascii
import pyamf
import sys
import json
import datetime
import time
import random
import requests


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
    
def log(s, pr=False):
    s = "[" + datetime.datetime.now().strftime('%d.%m %H:%M:%S')+"] " + s
    if pr: print s
    fatype = "hero_log_"+str(pid)
    try:
        tfile = open(fatype, "a")
        tfile.write(s.encode('utf-8')+'\n')
        tfile.close()
    except:
        tfile = open(fatype, "w")
        tfile.write(s.encode('utf-8')+'\n')
        tfile.close()

def sendRequest(command, params):
    url = 'http://kn-vk-sc1.playkot.com/current/json-gate.php'
    resp = requests.post(url, data=params, allow_redirects=True)
    txt = resp.text.split('!')[1].encode('utf-8')
    first = txt.find("adInfo")
    if first > 0:
        second = txt.find('}', first)
        txt = txt[:first]+"a\":\"0"+txt[second+1:]
    if txt.find("news")>0:
        txt = txt[:txt.find("news")-2]+'}}'
    txt = txt.replace('"a":"0,"', '"a":"0"},"')
    
    tfile = open('fuck', "w")
    tfile.write(txt)
    tfile.close()
    
    return {"data":txt}
    
def getSig2(myStr):
    return binascii.crc32(myStr) & 0xffffffff
    
def getSig(data):
    return getSig2(pid+service+data)
    
def createData(method, data):
    o = {}
    o["data"] = data
    o["sig"] = getSig(data)
    o["cmd"] = service
    o["gid"] = gid
    o["pid"] = pid
    return o
    
def init():
    global sid, gid, service, method
    service = 'Knights.initialize'
    method = 'initialize'
    initString = '{"age":30,"gender":1,"rnd":%s,"referralType":6,"newDay":false,"owner_id":"","hash":{},"auth_key":"%s","sid":""}'
    sid = ''
    gid = 0
    params = createData(method, initString % (getRandom(), auth))
    log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    print resp["data"][:100]
    o = json.loads(resp["data"])
    #log(json.dumps(o, indent=4))
    error = o["error"]
    if error == 0:
        sid = o["sid"]
        gid = o["player"]["player_id"]
        log("sid: %s, gid: %s" % (str(sid), str(gid)), True)
    else:
        log(resp["data"], True)
        
    return resp["data"]
        
        
def moveBuilding(bid, x, y, d):
    global sid, gid, service, method
    service = actionCommand
    method = 'entityMove'
    dataString = '{"x":%d,"y":%d,"dir":%d,"sceneId":%d,"rnd":%s,"auth_key":"%s","sid":"%s","method":"%s"}' % (x, y, d, bid, getRandom(), auth, sid, method)
    params = createData(method, dataString)
    log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("move done %d:%d" % (x, y), True)
    else:
        log(resp["data"], True)
    
def getRes():
    a=[]
    a.append({"x":4,"sceneId":66311,"y":-17,"dir":2,"auth_key":"1e365d477c3207804013abaddbb6a0c4","sid":"82654","method":"entityMove","rnd":188})
    a.append({"x":1,"sceneId":66312,"y":-16,"dir":2,"auth_key":"1e365d477c3207804013abaddbb6a0c4","sid":"82654","method":"entityMove","rnd":355})
    a.append({"x":3,"sceneId":66309,"y":-17,"dir":2,"auth_key":"1e365d477c3207804013abaddbb6a0c4","sid":"82654","method":"entityMove","rnd":814})
    a.append({"x":1,"sceneId":66310,"y":-15,"dir":2,"auth_key":"1e365d477c3207804013abaddbb6a0c4","sid":"82654","method":"entityMove","rnd":454})
    return a
    
init()

bids = getRes()

for b in bids:
    moveBuilding(b["sceneId"], b["x"], b["y"], b["dir"])
    
