import binascii
import pyamf
import sys
import json
import datetime
import time
import random
from pyamf.remoting.client import RemotingService


#Knights.doBatchAction
#{"rnd":554,"batchlist":{"0":{"count":1,"method":"recipeFinish","type":"entities","index":"65574"},"1":{"count":1,"method":"recipeFinish","type":"entities","index":"65577"}}}

person = 0
phaza = 2#0 - start, #1 - speed #2 - collect#3 - sell
pids = ["124520", "160511757"]
auths = ["1e365d477c3207804013abaddbb6a0c4", "6dc2dba90c1cc9d935542aa6a60c6fb4"]
pid = pids[person]
auth = auths[person]
data = ''
actionCommand = 'Knights.doAction'
gid = 0
sid = ''
action = 'hp'
if len(sys.argv) > 1:
    action = sys.argv[1]
    
def getRandom():
    return str(int(random.random()*1000))
    
def log(s, pr=False):
    s = "[" + datetime.datetime.now().strftime('%d.%m %H:%M:%S')+"] " + s
    if pr: print s
    fatype = "hero_money_log_"+str(pid)
    try:
        tfile = open(fatype, "a")
        tfile.write(s.encode('utf-8')+'\n')
        tfile.close()
    except:
        tfile = open(fatype, "w")
        tfile.write(s.encode('utf-8')+'\n')
        tfile.close()

def sendRequest(command, params):
    client = RemotingService('http://37.200.66.212/current/gateway.php')
    service = client.getService(command)
    #resp = service.dispatch(params1,"AMFService.ClanFightInfoGet",[{"BattleDBID":bid,"IsArchive":False}],False)
    return service._call(command,pid,gid,params)
    
def getSig2(myStr):
    return binascii.crc32(myStr) & 0xffffffff
    
def getSig(data):
    return getSig2(pid+data)
    
def createData(method, data):
    o = {}
    o["data"] = data
    o["sig"] = getSig(data)
    o["method"] = method
    o["sid"] = sid
    o["auth_key"] = auth
    return o
    
def init():
    global sid, gid
    service = 'Knights.initialize'
    method = 'initialize'
    initString = '{"age":30,"gender":1,"rnd":%s,"referralType":6,"newDay":false,"owner_id":"","hash":{}}'
    sid = ''
    gid = 0
    params = createData(method, initString % getRandom())
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
        
def moveBuilding(bid, x, y):
    service = actionCommand
    method = 'entityMove'
    dataString = '{"x":%d,"y":%d,"dir":0,"sceneId":%d,"rnd":%s}' % (x, y, bid, getRandom())
    params = createData(method, dataString)
    log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("move done %d:%d" % (x, y), True)
    else:
        log(resp["data"], True)


def recipeSpeedUp(bid):
    service = actionCommand
    method = 'recipeSpeedUp'
    dataString = '{"rnd":%s,"type":"entities","collect":false,"cash":0,"index":"%d"}' % (getRandom(), bid)
    params = createData(method, dataString)
    log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("recipeSpeedUp done %d" % (bid), True)
    else:
        log(resp["data"], True)

def recipeStart(bid):
    service = actionCommand
    method = 'recipeStart'
    dataString = '{"extra":null,"rnd":%s,"rid":664621994,"type":"entities","paidStart":false,"index":"%d","count":1}' % (getRandom(), bid)
    params = createData(method, dataString)
    log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("recipeStart done %d" % (bid), True)
    else:
        log(resp["data"], True)
    
def recipeFinish(bid):
    service = actionCommand
    method = 'recipeFinish'
    dataString = '{"rnd":%s,"type":"entities","index":"%d","count":1}' % (getRandom(), bid)
    params = createData(method, dataString)
    log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("recipeFinish done %d" % (bid), True)
    else:
        log(resp["data"], True)
        
def itemSell():
    service = actionCommand
    method = 'itemSell'
    dataString = '{"id":918398820,"count":2,"rnd":%s}' % (getRandom())
    params = createData(method, dataString)
    log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("itemSell done", True)
    else:
        log(resp["data"], True)
        

bids = [65571,65588,65635,65653]
init()

while True:
    try:
        if phaza == 0:
            phaza = 1
            for b in bids:
                recipeStart(b)
            time.sleep(61)
        if phaza == 1:
            phaza = 2
            for b in bids:
                recipeSpeedUp(b)
            time.sleep(1)
        if phaza == 2:
            phaza = 3
            for b in bids:
                recipeFinish(b)
            time.sleep(1)
        if phaza == 3:
            phaza = 0
            itemSell()
            time.sleep(1)
    except:
        time.sleep(60)
        init()