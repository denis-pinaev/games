# -*- coding: utf-8 -*-

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


#http://vk.com/id68487257 - new
#http://vk.com/id179331321 - old

phaza = 0#0 - create, #1 - start #2 - update#3 - finish
person = 0



if len(sys.argv) > 1:
    person = int(sys.argv[1])
else:
    raise Exception("#         corc0     natali1      polya2      nikita3      ulia4      vladimir5      yura6      lenaSv7     nagaina8   tanakan 9     VitalikSha10   vladimir 11    mari kramer 12    NAZAR 13    VanyaM 14     Oleg 15   Jenya16   LenaBRED17   DimaUsmar18")

create = False
if len(sys.argv) > 2:
    phaza = int(sys.argv[2])
    create = True

energy_value = 0
#         corc0     natali1      polya2      nikita3      ulia4      vladimir5      yura6      lenaSv7     nagaina8   tanakan 9     VitalikSha10   vladimir 11    mari kramer 12
#              {"pid":"161702967","auth":"a5738509fb8e7486b45e8ba01436c6bb","gid":0,"sid":""},#mari kremer
#74163736,"group_id":0,"is_app_user":1,"auth_key":"8943b2c7e241b1a97342d3c87346de23
pids = ["124520", "29431585", "144536559", '218661879', '56518190', '217858589', '179499220', "169768611", "68487257", "160511757", "73940623", '93902559', '161702967', '74163736', '114233049', '11305565', '692795', '65706308', '202787673', '20633660']
auths = ["1e365d477c3207804013abaddbb6a0c4", "55f56ea187574da9b2ed69474db78ac0", "731331d4e19d1f5483acd67abf424b58", "4a7a2ac0efcadd1a42499e34ed217e8b", "22f411e60eebd913b689b19705900ab2", '8b9107a32674785b79463d5585ec4918', '49e1540eb72f701a7c0924054ef10fc1', '9bc9bdd4929458a2108f1ae419906f66', "4f66fe9422f3b5f17ab1e90ce34a42d3", "6dc2dba90c1cc9d935542aa6a60c6fb4", "9ba0d48c2a9b701ffa031504b5232451", 'd40ce5e63d99e92fd57859c7be81729c', 'a5738509fb8e7486b45e8ba01436c6bb','8943b2c7e241b1a97342d3c87346de23', 'b2c5894ec83e287b4c2563402b064248', '40328e38ddaac299a62bafe98d4cfaac', '77107b46d764d40148b967deaa8cd474', 'a889a08c37aa0430b62ae6a5928e6950', '03bda5b072c520d2fc767c708979ad00', '587e50e0738885a44b37faee0f214aa6']
start_hero = ''
pid = pids[person]
auth = auths[person]
data = ''
actionCommand = 'Knights.doAction'
gid = 0
sid = ''
action = 'hp'
init_info = None
killFriend = False;
select_stage = True

# corc0     natali1      polya2      nikita3      ulia4      vladimir5      yura6      lenaSv7     nagaina8   tanakan 9     VitalikSha10
# vladimir 11    mari kramer 12    NAZAR 13    VanyaM 14     Oleg 15   Jenya16   LenaBRED17

orden_Dark = [
                 {'name':u'темный культ'}
]

user_not_attack = [
                 {'id':'132569016','name':'Svetlana Vostokova'},
                 {'id':'9644769','name':'Andrew Ann'},
                 #{'id':'185957394','name':'Ilnar Galiullin'},
                 {'id':'151757834','name':'Maksim Muljavka'},
                 {'id':'139046492','name':'Aleksej Mihajlichenko'},
                 #{'id':'45991619','name':'Sergej Vasilkovskij'},
                 #{'id':'43522563','name':'Evgenij Blinov'},
                 {'id':'166076867','name':'Mihail Smirnov'},
                 {'id':'132287081','name':'Natalia Shirokih'},
                 {'id':'186282895','name':'Mrachnii Tip'}
             ]
             
not_attack = {"user":[user_not_attack], "orden":[orden_Dark]}

if person in [8,9,11,13]:
    not_attack = {"user":[], "orden":[orden_Dark]}
    
if person in [2,3,4]:
    not_attack = {"user":[user_not_attack], "orden":[orden_Dark, [{'name':u'Лемберг'}]]}

if person in [5,17]:
    not_attack = {"user":[], "orden":[orden_Dark, [{'name':u'Анархия тьмы'},{'name':u'Элита Медведей'},{'name':u'МЕДВЕДИ'},{'name':u'Академия Медведей'},{'name':u'Сильные Медведи'},{'name':u'Легион Медведей'},{'name':u'Конкистадоры'}]]}

if person in [6]:
    not_attack = {"user":[], "orden":[orden_Dark, [{'name':u'Украина'}]]}


def read(fname):
    fatype = fname
    tfile = open(fatype, "r")
    d = tfile.read()
    tfile.close()
    return d

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
        time.sleep(999999)
        
    return resp["data"]
        

def killEnemy(dataj2, create, first=False):
    global select_stage

    # mission => pvpInfo => clanInfo(?) + id + power + epower + level + powerlevel => name
    if create and dataj2.has_key("mission") and dataj2["mission"].has_key("pvpInfo"):
        info = dataj2["mission"]["pvpInfo"]
        clanName = info['clanInfo']['name'] if info.has_key("clanInfo") else 'no clan'
        ratingPlace = info['clanInfo']['ratingPlace'] if info.has_key("clanInfo") else '0'
        fid = str(info['id']) if info.has_key("id") else ''
        level = str(info['level']) if info.has_key("level") else ''
        power = str(info['power']) if info.has_key("power") else ''
        epower = str(info['epower']) if info.has_key("epower") else ''
        powerlevel = str(info['powerlevel']) if info.has_key("powerlevel") else ''
        
        try:
            if first: log("TRY: id:%s, level:%s, clan:%s, epower:%s, power:%s, powerlevel:%s" % (fid,level,clanName,epower,power,powerlevel), True, True)
        except:
            if first: log("TRY: id:%s, level:%s, clan:%s, epower:%s, power:%s, powerlevel:%s" % (fid,level,ratingPlace,epower,power,powerlevel), True, True)
        
        na_user = not_attack['user']
        for uarr in na_user:
            for naid in uarr:
                if fid == naid["id"]:
                    print "WARNING! Try to kill friend: "+naid["name"]+" id: "+naid["id"]
                    if not killFriend: return ''
        na_orden = not_attack['orden']
        for oarr in na_orden:
            for orden in oarr:
                if clanName == orden["name"]:
                    print "WARNING! Try to kill orden: "+orden["name"]
                    if not killFriend: return ''
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



while True:
    init_person()
    
    print "energy_value = "+str(energy_value)
    gogo = energy_value>0 or not create or phaza>0
    
    cycle = 1
    if len(sys.argv) > 3:
        cycle = min(int(sys.argv[3]),energy_value)
        
    if len(sys.argv) > 4: killFriend = True
        
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
    
    if person in (0,5):
        init_person()
        if init_info.has_key("modules") and init_info["modules"].has_key("PvpChests") and init_info["modules"]["PvpChests"].has_key("keys"):
            print "Morgeina keys: " + str(init_info["modules"]["PvpChests"]["keys"])
    time.sleep(20*60)