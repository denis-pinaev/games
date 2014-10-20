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


#Knights.doBatchAction
#{"rnd":554,"batchlist":{"0":{"count":1,"method":"recipeFinish","type":"entities","index":"65574"},"1":{"count":1,"method":"recipeFinish","type":"entities","index":"65577"}}}

phaza = 0#0 - create, #1 - start #2 - update#3 - finnish
person = 0
if len(sys.argv) > 1:
    person = int(sys.argv[1])
else:
    raise Exception("#         corc0     natali1      polya2      nikita3      ulia4      vladimir5      yura6      lenaSv7     nagaina8   tanakan 9     VitalikSha10   vladimir 11    mari kramer 12    NAZAR 13    VanyaM 14     Oleg 15   Jenya16   LenaBRED17   DimaUsmar18")

create = True
if len(sys.argv) > 2:
    phaza = int(sys.argv[2])
    create = True

#         corc0     natali1      polya2      nikita3      ulia4      vladimir5      yura6      lenaSv7     nagaina8        ? 9     VitalikSha10   ? 11          mari         nazar      vanyam
pids = ["124520", "29431585", "144536559", '218661879', '56518190', '217858589', '179499220', "169768611", "68487257", "160511757", "73940623", '93902559', '161702967', '74163736', '114233049', '11305565', '692795', '65706308', '202787673']
auths = ["1e365d477c3207804013abaddbb6a0c4", "55f56ea187574da9b2ed69474db78ac0", "731331d4e19d1f5483acd67abf424b58", "4a7a2ac0efcadd1a42499e34ed217e8b", "22f411e60eebd913b689b19705900ab2", '8b9107a32674785b79463d5585ec4918', '49e1540eb72f701a7c0924054ef10fc1', '9bc9bdd4929458a2108f1ae419906f66', "4f66fe9422f3b5f17ab1e90ce34a42d3", "6dc2dba90c1cc9d935542aa6a60c6fb4", "9ba0d48c2a9b701ffa031504b5232451", 'd40ce5e63d99e92fd57859c7be81729c', 'a5738509fb8e7486b45e8ba01436c6bb','8943b2c7e241b1a97342d3c87346de23', 'b2c5894ec83e287b4c2563402b064248', '40328e38ddaac299a62bafe98d4cfaac', '77107b46d764d40148b967deaa8cd474', 'a889a08c37aa0430b62ae6a5928e6950', '03bda5b072c520d2fc767c708979ad00']

start_hero = ''
attak_arr = []
pid = pids[person]
auth = auths[person]
data = ''
actionCommand = 'Knights.doAction'
gid = 0
sid = ''
action = 'hp'
# 
not_attack = [
                 {'id':'159662551','name':'ORDEN'},
                 {'id':'73940623','name':'ORDEN'},
                 {'id':'114233049','name':'ORDEN'},
                 {'id':'161702967','name':'ORDEN'},
                 {'id':'170312666','name':'ORDEN'},
                 {'id':'179331321','name':'ORDEN'},
                 {'id':'31568442','name':'ORDEN'},
                 {'id':'13721794','name':'ORDEN'},
                 {'id':'52437466','name':'ORDEN'},
                 {'id':'35006200','name':'ORDEN'},
                 {'id':'20633660','name':'ORDEN'},#Sergey Udov
                 #{'id':'179499220','name':'ORDEN'},Yura
                 {'id':'130161945','name':'ORDEN'},
                 {'id':'79670506','name':'ORDEN'},
                 {'id':'203263126','name':'ORDEN'},
                 {'id':'196086079','name':'ORDEN'},
                 {'id':'11305565','name':'ORDEN'},
                 {'id':'202787673','name':'ORDEN'},
                 {'id':'169768611','name':'ORDEN'},
                 {'id':'98890676','name':'ORDEN'},
                 #{'id':'9499004','name':'ORDEN'},
                 {'id':'29431585','name':'ORDEN'},
                 {'id':'144536559','name':'Polina'},
                 {'id':'124520','name':'CorC'}
             ]
ctr = 0
def getCTR():
    global ctr
    ctr += 1
    return str(ctr)
    
def getRandom():
    return str(int(random.random()*1000))
    
def log(s, pr=False, new_file=False, file_name="hero_fights_log_"):
    s = "[" + datetime.datetime.now().strftime('%d.%m %H:%M:%S')+"] " + s
    if pr: print s
    fatype = "hero_mfight_log_"+str(pid)
    if new_file: fatype = file_name+str(pid)
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
    txt = resp.text.split('!',1)[1].encode('utf-8')
    first = txt.find("adInfo")
    if txt.find('"adInfo":"[]"')>0: first = -1
    if first > 0:
        second = txt.find('}', first)
        txt = txt[:first]+"a\":\"0"+txt[second+1:]
    txt = txt.replace('"a":"0,"', '"a":"0"},"')
    
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
#,"auth_key":"%s","ctr":%s,"sessionKey":"%s","method":"%s"}' % (getRandom(), auth, getCTR(), sid, method)
    global sid, gid, service, method
    service = 'Knights.initialize'
    method = 'initialize'
    initString = '{"age":30,"gender":1,"rnd":%s,"referralType":6,"newDay":false,"owner_id":"","hash":{},"auth_key":"%s","sessionKey":"","ctr":0}'
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
        sid = o["sessionKey"]
        gid = o["player"]["player_id"]
        log("sid: %s, gid: %s" % (str(sid), str(gid)), True)
    else:
        log(resp["data"], True)
        
    return resp["data"]
        

def killEnemy(dataj2, create, first=False):
    
    if create and dataj2.has_key("mission") and dataj2["mission"].has_key("pvpInfo"):
        fid = str(dataj2["mission"]["pvpInfo"]["id"])
        for naid in not_attack:
            if fid == naid["id"]:
                print "WARNING! Try to kill friend: "+naid["name"]+ "id: "+fid
                return ''
        if first: log("FIGHT ID: vk.com/id"+fid, True, True)
    method = 'battleUpdate'
    new_cheat = 0
    #dataj2 = json.loads(data)
    sunits = ''
    if dataj2.has_key("mission") and dataj2["mission"].has_key("entities"):
        dataj = dataj2["mission"]["entities"]
        
        new_cheat2 = int(dataj2["mission"]["actionId"])
        if new_cheat2 > new_cheat: new_cheat = new_cheat2

        kset = dataj2["mission"]["missionTargets"]["units"]
        for i2 in kset:
            i = str(i2)
            o = dataj[i]
            if o.has_key("dead"): continue
            if len(sunits)>0:
                sunits = '%s,"%s":{"dmg":1000,"dead":1}' % (sunits, i)
            else: sunits = '%s"%s":{"dmg":1000,"dead":1}' % (sunits, i)
            
        kset = dataj2["mission"]["missionTargets"]["list"]
        for i2 in kset:
            i = str(i2)
            o = dataj[i]
            if o.has_key("dead"): continue
            if len(sunits)>0:
                sunits = '%s,"%s":{"dmg":1000,"dead":1}' % (sunits, i)
            else: sunits = '%s"%s":{"dmg":1000,"dead":1}' % (sunits, i)

    sline = '{"entities":{%s},"rnd":%s,"config":{},"globalSpells":null,"turn":0,"index":"default","aid":%d,"ctr":%s,"sessionKey":"%s","method":"%s"}' % (sunits, getRandom(), new_cheat, getCTR(), sid, method)
    return sline
        
def battleInit():
    global sid, gid, service, method
    service = actionCommand
    method = 'battleInit'
    #dataString = '{"rnd":%s,"index":"default"}' % (getRandom())
    #data	{"auth_key":"1e365d477c3207804013abaddbb6a0c4""ctr":%s,"sessionKey":"4639","method":"battleInit","index":"default","rnd":109}
    dataString = '{"rnd":%s,"index":"default","ctr":%s,"sessionKey":"%s","method":"%s"}' % (getRandom(), getCTR(), sid, method)
    params = createData(method, dataString)
    log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("battleInit done", True)
    else:
        log(resp["data"], True)
    return o
    
def battleUpdate(killstring):
    global sid, gid, service, method
    service = actionCommand
    method = 'battleUpdate'
    params = createData(method, killstring)
    log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("battleUpdate done", True)
    else:
        log(resp["data"], True)
    return o

def battleCreate(attaker):
    global sid, gid, service, method
    service = actionCommand
    method = 'battleCreate'
    #dataString = '{"reason":"pvp","debug":false,"data":null,"rnd":%s,"index":"default"}' % (getRandom())
    
    #{"debug":false,"auth_key":"731331d4e19d1f5483acd67abf424b58","reason":"revenge","sid":"13507","data":"40786581","method":"battleCreate","rnd":82,"index":"default"}
    
    dataString = '{"reason":"revenge","debug":false,"data":"%s","rnd":%s,"index":"default","ctr":%s,"sessionKey":"%s","method":"%s"}' % (attaker, getRandom(), getCTR(), sid, method)
    #{"auth_key":"1e365d477c3207804013abaddbb6a0c4","sid":"4639","method":"battleCreate"}
    params = createData(method, dataString)
    log("%s:%s %s" % (service, method, json.dumps(params)))
    
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("battleCreate done", True)
    else:
        log(resp["data"], True)
    return o

def loadPerson(initdata):
    global start_hero, attak_arr
    try:
        ts = '{"units":[{"owner":1,"id":%d,"type":null,"sceneId":99999,"x":1,"home":%d,"y":14,"dir":4}],"rnd":%s,"index":"default"}'
        for e in initdata["entities"]:
            ee = initdata["entities"][e]
            if ee.has_key("subtype") and ee["subtype"] == "unit":
                pid = ee["id"]
                sid = ee["sceneId"]
                dataString = ts % (pid, sid, getRandom())
                start_hero = dataString
                print "taking person done"
                break
                
        if initdata.has_key("messages") and len(initdata["messages"])>0:
            for mess in initdata["messages"]:
                if initdata["messages"][mess].has_key("type") and initdata["messages"][mess]["type"] == "attack":
                    at_id = str(mess)
                    at_win = "none"
                    at_att = "none"
                    at_gold = "none"
                    at_wood = "none"
                    at_iron = "none"
                    at_rang = "none"
                    try:
                        at_win = str(initdata["messages"][mess]["data"]["win"])
                    except: None
                    try:
                        at_gold = str(initdata["messages"][mess]["data"]["looting"]["money"])
                    except: None
                    try:
                        at_att = str(initdata["messages"][mess]["sender"])
                    except: None
                    try:
                        at_wood = str(initdata["messages"][mess]["data"]["looting"]["wood"])
                    except: None
                    try:
                        at_iron = str(initdata["messages"][mess]["data"]["looting"]["iron"])
                    except: None
                    try:
                        at_rang = str(initdata["messages"][mess]["data"]["honorValue"])
                    except: None
                    attak_arr.append([at_id, at_att, at_win, at_rang, at_gold, at_wood, at_iron])
                    log("ATTAKER ID: vk.com/id%s win: %s, rang: %s, gold: %s, wood: %s, iron: %s" % (at_att, at_win, at_rang, at_gold, at_wood, at_iron))
                
    except:
        print "error taking person"
        
def get_attak_person(attak_arr):
    ret = ""
    min_att = 999999
    for p in attak_arr:
        if p[3] != "none":
            if int(p[3])<min_att: min_att = int(p[3]); ret = p[0]
    return ret
    

def battleStart():
    global sid, gid, service, method
    service = actionCommand
    method = 'battleStart'
    #print start_hero[person]
    dataString = start_hero[:-1]+',"ctr":%s,"sessionKey":"%s","method":"%s"}'
    dataString = dataString % (getCTR(), sid, method)
    params = createData(method, dataString)
    log("%s:%s %s" % (service, method, json.dumps(params)))
    
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("battleStart done", True)
    else:
        log(resp["data"], True)
    return o

def battleFinish():
    global sid, gid, service, method
    service = actionCommand
    method = 'battleFinish'
    #dataString = '{"reason":"win","index":"default","rnd":%s}' % (getRandom())
    #{"reason":"win","rnd":700,"auth_key":"1e365d477c3207804013abaddbb6a0c4""ctr":%s,"sessionKey":"4639","method":"battleFinish","index":"default"}
    dataString = '{"reason":"win","index":"default","rnd":%s,"ctr":%s,"sessionKey":"%s","method":"%s"}' % (getRandom(), getCTR(), sid, method)
    params = createData(method, dataString)
    log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        printResults(o)
        log("battleFinish done", True)
    else:
        log(resp["data"], True)
    return o
    
    
def printResults(o):
    s = ''
    if o.has_key('honorValue'): s = '%s Rang:%s' % (s, str(o['honorValue']))
    if o.has_key('player') and o.has_key('awards'):
        ss = ["cash","epower","money","wood","stone","iron"]
        for i in range(len(ss)):
            res = ss[i]
            s = '%s %s:' % (s, res)
            if o['player'].has_key(res): s = '%s %s' % (s, str(o['player'][res]))
            for e in o['awards']:
                if e.has_key('type') and e['type'] == res:
                    s = '%s(%s)' % (s, str(e['count']))
                    break
    log(s, True, True, "hero_final_info_")


initdata = init()
o = json.loads(initdata)
loadPerson(o)

attak_id = get_attak_person(attak_arr)

if len(attak_id)>0:

    gogo = True
    
    if create:
        try:
            if gogo and phaza==0: o = battleCreate(attak_id); print "battleCreate ok"
            if phaza==0 and o["success"] == False: print "battleCreate - not energy!"; gogo = False
        except:
            print "error in battleCreate"
            gogo = False
        try: 
            if gogo: inito = battleInit(); print "battleInit ok"
        except:
            print "error in battleInit"
            gogo = False
        try:
            if gogo: killsting = killEnemy(inito, create, True); print "killEnemy done"
            if len(killsting)<1: gogo = False
        except:
            print "error in killEnemy"
            gogo = False
        try:
            if gogo and phaza<=1: battleStart(); print "battleStart ok"
        except:
            print "error in battleStart"
            gogo = False
    
    try:
        if gogo: mission = o["missions"]["default"]["id"]; print "mission = " + str(mission)
    except:
        print "error in missions get"
        gogo = False
    try:
        if gogo: inito = battleInit(); print "battleInit done"
    except:
        print "error in battleInit"
        gogo = False
    try:
        if gogo: killsting = killEnemy(inito, create); print "killEnemy done"
        if len(killsting)<1: gogo = False
    except:
        print "error in killEnemy"
        gogo = False
    try:
        if gogo: battleUpdate(killsting); print "battleUpdate done"
    except:
        print "error in battleUpdate"
        gogo = False
    if create or phaza>2:
        try:
            if gogo: battleFinish(); print "battleFinish done"
        except:
            print "error in battleFinish"
    
    
    