# -*- coding: utf-8 -*-

import sys
import json
import datetime
import random
import requests

from buildInfo import *
from common import *
from common_head import *


pid = sys.argv[1]
auth = loadPlayer(pid)["auth"]
phaza = int(sys.argv[2])
cycle = int(sys.argv[3])
battle_type = sys.argv[4]
sity = sys.argv[5]

print "pid: %s, auth: %s, phaza: %s, cycle: %s, battle: %s, sity: %s" % (pid, auth, phaza, cycle, battle_type, sity)

service = ''
method = ''
phaza = 0#0 - create, #1 - start #2 - update#3 - finish
create = True
energy_value = 0
start_hero = ''
data = ''
actionCommand = 'Knights.doAction'
gid = 0
sid = ''
init_info = None
killFriend = False;
select_stage = True
game_version = getGameVersion()
init_log("fight")

def getGlobalEnergy(timestamp):
    td = (datetime.datetime.now() - datetime.datetime.fromtimestamp(int(timestamp)-60*60)).total_seconds()
    s = int(td)
    m = s/60
    h = m/60
    energy_value = min(6,h/4)
    rh = h-energy_value*4
    rm = m-h*60
    rs = s-m*60
    tsl4 = 4*60*60
    tsl = tsl4 if energy_value>5 else rs + rm*60 + rh*60*60
    td = str(datetime.datetime.fromtimestamp(tsl4) - datetime.datetime.fromtimestamp(tsl))
    return int(energy_value), td

def loadignores():
    try:
        return json.loads(read("tmp/ignores"))
    except Exception as ex:
        return {"players":[],"orden":[]}

ignores = loadignores()
not_attack = {"user":[ignores["players"]], "orden":[ignores["orden"], [{"name":u"темный культ"}]]}

ctr = int(random.random()*10000)
def getCTR():
    global ctr
    ctr += 1
    return str(ctr)
    
def getRandom():
    return str(int(random.random()*1000))
    
def killEnemy(dataj2, create, first=False):
    global select_stage, bot_fight

    # mission => pvpInfo => clanInfo(?) + id + power + epower + level + powerlevel => name
    if create and dataj2.has_key("mission") and dataj2["mission"].has_key("pvpInfo"):
        info = dataj2["mission"]["pvpInfo"]
        clanName = u_(info['clanInfo']['name']) if info.has_key("clanInfo") else 'no clan'
        #??? ratingPlace = info['clanInfo']['ratingPlace'] if info.has_key("clanInfo") else '0'
        fid = str(info['id']) if info.has_key("id") else ''
        level = str(info['level']) if info.has_key("level") else ''
        power = str(info['power']) if info.has_key("power") else ''
        epower = str(info['epower']) if info.has_key("epower") else ''
        powerlevel = str(info['powerlevel']) if info.has_key("powerlevel") else ''
        try:
            if fid == "BOT": bot_fight = int(info['stage'])
        except:
            print "ERROR: fight = BOT but stage not found"
            bot_fight = 2
        try:
            if first: log("TRY: id:%s, level:%s, clan:%s" % (fid,level,u_(clanName)), True)
        except Exception as ex:
            print ex
            print "Unexpected error2323:\n", sys.exc_info()
            #if first: log("TRY: id:%s, level:%s, clan:%s, epower:%s, power:%s, powerlevel:%s" % (fid,level,ratingPlace,epower,power,powerlevel), True, True)
        na_user = not_attack['user']
        for uarr in na_user:
            for naid in uarr:
                if fid == naid["pid"]:
                    print "WARNING! Try to kill friend: "+u_(naid["name"])+" id: "+naid["pid"]
                    if not killFriend: return ''
        na_orden = not_attack['orden']
        for oarr in na_orden:
            for orden in oarr:
                if u_(clanName) == u_(orden["name"]):
                    print "WARNING! Try to kill orden: "+u_(orden["name"])
                    if not killFriend: return ''
        if first: log("FIGHT ID: vk.com/id"+fid, True)
    method = 'battleUpdate'
    new_cheat = 0
    #dataj2 = json.loads(data)
    sunits = ''
    if dataj2.has_key("mission") and dataj2["mission"].has_key("entities"):
        dataj = dataj2["mission"]["entities"]
        
        for e in dataj:
            if dataj[e].has_key('owner') and str(dataj[e]['owner']) == '1': select_stage = False
        
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
        if dataj2["mission"]["missionTargets"].has_key("list"):
            kset = dataj2["mission"]["missionTargets"]["list"]
            for i2 in kset:
                i = str(i2)
                o = dataj[i]
                if o.has_key("dead"): continue
                if len(sunits)>0:
                    sunits = '%s,"%s":{"dmg":1000,"dead":1}' % (sunits, i)
                else: sunits = '%s"%s":{"dmg":1000,"dead":1}' % (sunits, i)

    sline = '{"entities":{%s},"v":"%s","config":{},"globalSpells":null,"turn":0,"index":"default","aid":%d,"ctr":%s,"sessionKey":"%s","method":"%s"}' % (sunits, game_version, new_cheat, getCTR(), sid, method)
    return sline
        
def battleInit():
    global sid, gid, service, method
    service = actionCommand
    method = 'battleInit'
    init_params(nsid=sid, ngid=gid, nservice=service, nmethod=method)
    #dataString = '{"v":"%s","index":"default"}' % (game_version)
    dataString = '{"v":"%s","index":"default","ctr":%s,"sessionKey":"%s","method":"%s"}' % (game_version, getCTR(), sid, method)
    params = createData(method, dataString)
    #log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("battleInit done", True)
    else:
        log(resp["data"], True)
        global gogo
        gogo = False
    return o
    
def battleUpdate(killstring):
    if select_stage: print "ERROR IN battleUpdate!!! select_stage = "+str(select_stage) ;return False
    global sid, gid, service, method
    service = actionCommand
    method = 'battleUpdate'
    init_params(nsid=sid, ngid=gid, nservice=service, nmethod=method)
    params = createData(method, killstring)
    #log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("battleUpdate done", True)
    else:
        log(resp["data"], True)
        global gogo
        gogo = False
    return o

def battleSwitch():
    global sid, gid, service, method
    service = actionCommand
    method = 'battleSwitchMap'
    init_params(nsid=sid, ngid=gid, nservice=service, nmethod=method)
    dataString = '{"alias":null,"index":"default","ctr":%s,"sessionKey":"%s","method":"%s"}' % (getCTR(), sid, method)
    #{"alias":null,"method":"battleSwitchMap","sessionKey":"546cec1f907638.67715772","ctr":24,"index":"default"}
    params = createData(method, dataString)
    #log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("battleSwitchMap done", True)
    else:
        log(resp["data"], True)
        global gogo
        gogo = False
    return o

def battleCreate():
    global sid, gid, service, method
    service = actionCommand
    method = 'battleCreate'
    init_params(nsid=sid, ngid=gid, nservice=service, nmethod=method)
    #{"reason":"pvp","debug":false,"data":null,"v":"%s","index":"default","ctr":%s,"sessionKey":"%s","method":"%s"}
    #{"reason":"gwAttack","debug":false,"data":%s,"v":"%s","index":"default","ctr":%s,"sessionKey":"%s","method":"%s"}
    battleData = "null" if battle_type == "pvp" else sity
    dataString = '{"reason":"%s","debug":false,"data":%s,"v":"%s","index":"default","ctr":%s,"sessionKey":"%s","method":"%s"}' % (battle_type, battleData, game_version, getCTR(), sid, method)
    log(dataString, True)
    params = createData(method, dataString)
    #log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("battleCreate done", True)
    else:
        log(resp["data"], True)
        global gogo
        gogo = False
    return o

def loadPerson(initdata):
    global start_hero, energy_value
    if True:
        ts = '{"units":[{"owner":1,"id":%d,"type":null,"sceneId":99999,"x":1,"home":%d,"y":14,"dir":4}],"v":"%s","index":"default"}'
        #print initdata["player"]
        if battle_type == "pvp":
            energy_value = int(initdata["player"]["energy"])
        else:
            energy_value, td = getGlobalEnergy(int(initdata["playerStats"]["gwAttacks"]))
        for e in initdata["entities"]:
            ee = initdata["entities"][e]
            if ee.has_key("subtype") and ee["subtype"] == "unit":
                pid = ee["id"]
                sid = ee["sceneId"]
                dataString = ts % (pid, sid, game_version)
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
    init_params(nsid=sid, ngid=gid, nservice=service, nmethod=method)
    #print start_hero[person]
    dataString = start_hero[:-1]+',"ctr":%s,"sessionKey":"%s","method":"%s"}'
    dataString = dataString % (getCTR(), sid, method)
    params = createData(method, dataString)
    #log("%s:%s %s" % (service, method, json.dumps(params)))
    
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("battleStart done", True)
    else:
        log(resp["data"], True)
        global gogo
        gogo = False
    return o

def battleFinish():
    if select_stage: print "ERROR IN battleFinish!!! select_stage = "+str(select_stage) ;return False
    global sid, gid, service, method
    service = actionCommand
    method = 'battleFinish'
    init_params(nsid=sid, ngid=gid, nservice=service, nmethod=method)
    #dataString = '{"reason":"win","index":"default","v":"%s"}' % (game_version)
    dataString = '{"reason":"win","index":"default","v":"%s","ctr":%s,"sessionKey":"%s","method":"%s"}' % (game_version, getCTR(), sid, method)
    params = createData(method, dataString)
    #log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        printResults(o)
        log("battleFinish done", True)
    else:
        log(resp["data"], True)
        global gogo
        gogo = False
    return o
    
def battleFinishTimeout():
    global sid, gid, service, method
    service = actionCommand
    method = 'battleFinish'
    init_params(nsid=sid, ngid=gid, nservice=service, nmethod=method)
    dataString = '{"reason":"timeout","index":"default","v":"%s","ctr":%s,"sessionKey":"%s","method":"%s"}' % (game_version, getCTR(), sid, method)
    params = createData(method, dataString)
    #log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        printResults(o)
        log("battleFinishTimeout done", True)
    else:
        log(resp["data"], True)
    return o
    
def battleFinishRetreat():
    global sid, gid, service, method
    service = actionCommand
    method = 'battleFinish'
    init_params(nsid=sid, ngid=gid, nservice=service, nmethod=method)
    dataString = '{"reason":"retreat","index":"default","v":"%s","ctr":%s,"sessionKey":"%s","method":"%s"}' % (game_version, getCTR(), sid, method)
    params = createData(method, dataString)
    #log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        printResults(o)
        log("battleFinishRetreat done", True)
    else:
        log(resp["data"], True)
        global gogo
        gogo = False
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
    log(s, True)


def cycle_proc():
    global select_stage, bot_fight, gogo
    isBattle = False
    bot_fight = 2
    try:
        if gogo:
            mission = init_info["missions"]["default"]["id"]
            mission_time = int(init_info["missions"]["default"]["time"])
            loose = False if str(mission) == "0" else (datetime.datetime.now() - datetime.datetime.fromtimestamp(mission_time)).total_seconds()>0
            if loose:
                print "mission LOOSE timeout = " + str(mission)
                battleFinishTimeout()
            else:
                isBattle = True
                print "mission ACTIVE = " + str(mission)
            init_info["missions"] = None
    except Exception as ex:
        print ex
        print "no mission found"
        if not create:
            return False
            
    if create:
        try:
            if gogo and phaza==0 and not isBattle: o = battleCreate(); print "battleCreate ok"
            isBattle = False
            #if phaza==0 and o["success"] == False: print "battleCreate - not energy!"; gogo = False
        except Exception as ex:
            print ex
            print "Unexpected error:\n", sys.exc_info()
            print "error in battleCreate"
            return False
        try: 
            if gogo: inito = battleInit(); print "battleInit ok"
        except Exception as ex:
            print ex
            print "error in battleInit"
            return False
        try:
            if gogo: killsting = killEnemy(inito, create, True); print "killEnemy done"
            if gogo and len(killsting)<1: battleFinishRetreat(); select_stage = True; return True
        except Exception as ex:
            print ex
            print "error in killEnemy"
            return False
        try:
            if gogo and phaza<=1: battleStart(); print "battleStart ok"
            select_stage = False
        except Exception as ex:
            print ex
            print "error in battleStart"
            return False
    
    try:
        if gogo: inito = battleInit(); print "battleInit done"
    except Exception as ex:
        print ex
        print "error in battleInit"
        return False
    try:
        if gogo: killsting = killEnemy(inito, create); print "killEnemy done"
        if gogo and len(killsting)<1: battleFinishRetreat(); select_stage = True; return True
    except Exception as ex:
        print ex
        print "error in killEnemy"
        return False
    try:
        if gogo: battleUpdate(killsting); print "battleUpdate done"
    except Exception as ex:
        print ex
        print "error in battleUpdate"
        return False
        
    while bot_fight<2:
        if gogo: battleSwitch(); print "battleSwitch ok"
        if gogo: inito = battleInit(); print "battleInit ok"
        if gogo: killsting = killEnemy(inito, create, True); print "killEnemy done"
        if len(killsting)<1: return False
        if gogo: battleUpdate(killsting); print "battleUpdate done"
        
    if create or phaza>2:
        try:
            if gogo: battleFinish(); print "battleFinish done"
        except Exception as ex:
            print ex
            print "Unexpected error:\n", sys.exc_info()
            print "error in battleFinish"
    
    select_stage = True
    bot_fight = 2

    return True
    

def init_person():
    global init_info, gid, sid
    init_info, gid, sid = init(pid, auth)
    loadPerson(init_info)

init_person()

if battle_type == '': energy_value = 0

print "START ENERGY = "+str(energy_value)
gogo = energy_value>0 or not create or phaza>0

cycle = min(int(cycle),energy_value)

if not gogo: cycle = 0
bot_fight = 2
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
    if create: print "END ENERGY = "+str(energy_value)
