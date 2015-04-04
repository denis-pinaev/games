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
#49e1540eb72f701a7c0924054ef10fc1 179499220


#13721794
#65857702

phaza = 0#0 - create, #1 - start #2 - update#3 - finish
person = 0



if len(sys.argv) > 1:
    person = int(sys.argv[1])
else:
    raise Exception("#         corc0     natali1      polya2      nikita3      ulia4      vladimir5      yura6      lenaSv7     nagaina8   tanakan 9     VitalikSha10   vladimir 11    mari kramer 12    NAZAR 13    VanyaM 14")

create = False
if len(sys.argv) > 2:
    phaza = int(sys.argv[2])
    create = True

energy_value = 0
pids = ["3091478"]
auths = ["7fb9f07a0c6156483701f8b24b79696a"]
start_hero = ''
pid = pids[person]
auth = auths[person]
data = ''
actionCommand = 'Knights.doAction'
gid = 0
sid = ''
action = 'hp'
init_info = None

select_stage = True

# 
not_attack = [
                 {'id':'159662551','name':'ORDEN'},
                 {'id':'73940623','name':'ORDEN'},
                 {'id':'114233049','name':'ORDEN'},
                 {'id':'161702967','name':'ORDEN'},
                 {'id':'170312666','name':'ORDEN'},
                 {'id':'23594947','name':'ORDEN'},
                 {'id':'68487257','name':'ORDEN'},
                 {'id':'692795','name':'ORDEN'},
                 {'id':'50958901','name':'ORDEN'},
                 {'id':'116189705','name':'ORDEN'},
                 {'id':'65857702','name':'ORDEN'},
                 {'id':'179499220','name':'ORDEN'},
                 {'id':'130161945','name':'ORDEN'},
                 {'id':'79670506','name':'ORDEN'},
                 {'id':'203263126','name':'ORDEN'},#was! Ruslan
                 {'id':'196086079','name':'ORDEN'},
                 {'id':'11305565','name':'ORDEN'},
                 {'id':'202787673','name':'ORDEN'},
                 {'id':'169768611','name':'ORDEN'},
                 {'id':'98890676','name':'ORDEN'},
                 {'id':'9499004','name':'ORDEN'},
                 {'id':'29431585','name':'ORDEN'},
                 
                 {'id':'9894033','name':'Vadim Tuma'},
                 {'id':'9644769','name':'Andrew Ann'},
                 {'id':'25497481','name':'Plolin drug'},
                 {'id':'144536559','name':'Polina'},
                 {'id':'124520','name':'CorC'},
                 {'id':'197305999','name':'Julija Belinskaja'},
                 {'id':'185957394','name':'Ilnar Galiullin'},
                 {'id':'151757834','name':'Maksim Muljavka'},
                 {'id':'139046492','name':'Aleksej Mihajlichenko'},
                 {'id':'45991619','name':'Sergej Vasilkovskij'},
                 {'id':'43522563','name':'Evgenij Blinov'},
                 {'id':'166076867','name':'Mihail Smirnov'},
                 {'id':'132287081','name':'Natalia Shirokih'},
                 {'id':'186282895','name':'Mrachnii Tip'},
                 {'id':'166924744','name':'Vifur Tverdolobii'}
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
    fatype = "hero_fight_log_"+str(pid)
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
    url = 'http://188.93.20.156/current/json-gate.php'
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
        time.sleep(999999)
        
    return resp["data"]
        

def killEnemy(dataj2, create, first=False):
    global select_stage
    
    if create and dataj2.has_key("mission") and dataj2["mission"].has_key("pvpInfo"):
        fid = str(dataj2["mission"]["pvpInfo"]["id"])
        for naid in not_attack:
            if fid == naid["id"]:
                print "WARNING! Try to kill friend: "+naid["name"]
                return ''
        if first: log("FIGHT ID: vk.com/id"+fid, True, True)
    method = 'battleUpdate'
    new_cheat = 0
    #dataj2 = json.loads(data)
    sunits = ''
    if dataj2.has_key("mission") and dataj2["mission"].has_key("entities"):
        dataj = dataj2["mission"]["entities"]
        
        for e in dataj:
            if str(dataj[e]['owner']) == '1': select_stage = False
        
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
        time.sleep(999999)
    return o
    
def battleUpdate(killstring):
    if select_stage: print "ERROR IN battleUpdate!!! select_stage = "+str(select_stage) ;return False
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
        time.sleep(999999)
    return o

def battleCreate():
    global sid, gid, service, method
    service = actionCommand
    method = 'battleCreate'
    dataString = '{"reason":"pvp","debug":false,"data":null,"rnd":%s,"index":"default","ctr":%s,"sessionKey":"%s","method":"%s"}' % (getRandom(), getCTR(), sid, method)
    #{"auth_key":"1e365d477c3207804013abaddbb6a0c4""ctr":%s,"sessionKey":"4639","method":"battleCreate"}
    params = createData(method, dataString)
    log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("battleCreate done", True)
    else:
        log(resp["data"], True)
        time.sleep(999999)
    return o

def loadPerson(initdata):
    global start_hero, energy_value
    if True:
        ts = '{"units":[{"owner":1,"id":%d,"type":null,"sceneId":99999,"x":1,"home":%d,"y":14,"dir":4}],"rnd":%s,"index":"default"}'
        #print initdata["player"]
        energy_value = int(initdata["player"]["energy"])
        for e in initdata["entities"]:
            ee = initdata["entities"][e]
            if ee.has_key("subtype") and ee["subtype"] == "unit":
                pid = ee["id"]
                sid = ee["sceneId"]
                dataString = ts % (pid, sid, getRandom())
                start_hero = dataString
                print "taking person done"
                break
    #except:
    #    print "error taking person"

def battleStart():
    if not select_stage: print "ERROR IN battleStart!!! select_stage = "+str(select_stage) ;return False
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
        time.sleep(999999)
    return o

def battleFinish():
    if select_stage: print "ERROR IN battleFinish!!! select_stage = "+str(select_stage) ;return False
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
        time.sleep(999999)
    return o
    
    
def printResults(o):
    s = ''
    if o.has_key('honorValue'): s = '%s Rang:%s' % (s, str(o['honorValue']))
    if o.has_key('player') and o.has_key('awards'):
        ss = ["cash","epower","money","wood","stone","iron","experience"]
        for i in range(len(ss)):
            res = ss[i]
            s = '%s %s:' % (s, res)
            if o['player'].has_key(res): s = '%s %s' % (s, str(o['player'][res]))
            for e in o['awards']:
                if e.has_key('type') and e['type'] == res:
                    s = '%s(%s)' % (s, str(e['count']))
                    break
    log(s, True, True, "hero_final_info_")


def cycle_proc():
    global select_stage
    isBattle = False
    try:
        if gogo: mission = init_info["missions"]["default"]["id"]; isBattle = True; init_info["missions"] = None; print "mission = " + str(mission)
    except:
        print "no mission found"
        if not create:
            return False
            
    if create:
        try:
            if gogo and phaza==0 and not isBattle: o = battleCreate(); print "battleCreate ok"
            isBattle = False
            #if phaza==0 and o["success"] == False: print "battleCreate - not energy!"; gogo = False
        except:
            print "Unexpected error:\n", sys.exc_info()
            print "error in battleCreate"
            return False
        try: 
            if gogo: inito = battleInit(); print "battleInit ok"
        except:
            print "error in battleInit"
            return False
        try:
            if gogo: killsting = killEnemy(inito, create, True); print "killEnemy done"
            if len(killsting)<1: return False
        except:
            print "error in killEnemy"
            return False
        try:
            if gogo and phaza<=1: battleStart(); print "battleStart ok"
            select_stage = False
        except:
            print "error in battleStart"
            return False
    
    try:
        if gogo: inito = battleInit(); print "battleInit done"
    except:
        print "error in battleInit"
        return False
    try:
        if gogo: killsting = killEnemy(inito, create); print "killEnemy done"
        if len(killsting)<1: return False
    except:
        print "error in killEnemy"
        return False
    try:
        if gogo: battleUpdate(killsting); print "battleUpdate done"
    except:
        print "error in battleUpdate"
        return False
    if create or phaza>2:
        try:
            if gogo: battleFinish(); print "battleFinish done"
        except:
            print "Unexpected error:\n", sys.exc_info()
            print "error in battleFinish"
    
    select_stage = True

    return True
    

def init_person():
    global init_info
    initdata = init()
    init_info = json.loads(initdata)
    loadPerson(init_info)




init_person()

print "energy_value = "+str(energy_value)
gogo = energy_value>0 or not create or phaza>0

cycle = 1
if len(sys.argv) > 3:
    cycle = min(int(sys.argv[3]),energy_value)
    
if not gogo: cycle = 0

for i_cycle in range(cycle):
    res = cycle_proc()
    if cycle>1:
        if not res:
            phaza = 1
            init_person()
            res = cycle_proc()
            if res: phaza = 0
            else: break
    
    if phaza == 0: energy_value = energy_value - 1
    if create: print "energy_value = "+str(energy_value)
    