import pyamf
import sys
import json
import datetime
import time
from pyamf.remoting.client import RemotingService

sid = 11329
bid = 1
tgt = 1
person = 'gludia4'
mission = True
reenter_first = True
clanID = 888882#2287459
targetClanID = 2132983

plist = [
        {"u":"93902559", "s":"e365fb4b1f20c6289e2df08b101e8cb7", 'n':"gludia4"} #Gludiya
        ]
        
def get_params1(name, pid):
    global sid
    params1 = {
        "userId":name,
        "ServerVersion":sid,
        "SystemID":"1",
        "sig":pid
    }
    return params1

if person:
    for p in plist:
        found = False
        if p['n'] == person:
            found = True
            person = p
            break
    if found:
        params1 = get_params1(person['u'], person['s'])
    else:
        print "Unknown person"
        time.sleep(99999)
else:
    print "No person"
    time.sleep(99999)
    
log_all = ""
        
def log(s, final=False, data=True):
    global log_all
    ds = ""
    if data:
        ds = "[" + datetime.datetime.now().strftime('%d.%m %H:%M:%S')+"] "
    s = ds + s
    log_all += s + "\n"
    print s
    if final: log_end()

def log_end():
    global log_all
    fatype = "battle_clan_get_log_"+str(bid)
    try:
        tfile = open(fatype, "a")
        tfile.write(log_all.encode('utf-8')+'\n')
        tfile.close()
    except:
        tfile = open(fatype, "w")
        tfile.write(log_all.encode('utf-8')+'\n')
        tfile.close()
    log_all = ""

def sendRequest(params1, command, params2):
    client = RemotingService('http://dracula.irq.ru/Gateway.aspx')
    service = client.getService('MafiaAMF.AMFService')
    return service.dispatch(params1,command,params2,False)


def main():
    global bid, tgt
    global stamina
    print datetime.datetime.now().strftime('%H:%M:%S')
    rest = 999
    if bid<1000:
        cl = getBattlesData()
        for c in cl:
            if c["EnemyDBID"] == targetClanID:
                bid = c["BattleDBID"]
                break
    fight = get_fight()
    ta = fight["data"]["Answer"]["OtherData"]["ClanFightInfo"]["TargetPlayers"]
    at = fight["data"]["Answer"]["OtherData"]["ClanFightInfo"]["ActorPlayers"]
    if not fight["data"]["Answer"]["OtherData"]["ClanFightInfo"]["TargetClanDBID"] == clanID:
        at = fight["data"]["Answer"]["OtherData"]["ClanFightInfo"]["TargetPlayers"]
        ta = fight["data"]["Answer"]["OtherData"]["ClanFightInfo"]["ActorPlayers"]
    at.sort(key=lambda x: x["HealthMax"], reverse=True)
    ta.sort(key=lambda x: x["Ladder"], reverse=True)
    log("ATTACKER", True)
    for p in at:
        Name = p["PlayerName"]#.encode('utf-8')
        DBID = str(p["FighterDBID"])
        Stamina = str(p["Stamina"])
        Ladder = str(p["Ladder"])
        Health  = "%.2f" % (float(p["HealthCur"])/float(p["HealthMax"]))
        log("N: %s, DBID: %s, H: %s, S: %s, L:%s" % (Name, DBID, Health, Stamina, Ladder), True)
    log("DEFENDER", True)
    for p in ta:
        Name = p["PlayerName"]#.encode('utf-8')
        DBID = str(p["FighterDBID"])
        Stamina = str(p["Stamina"])
        Ladder = str(p["Ladder"])
        Health  = "%.2f" % (float(p["HealthCur"])/float(p["HealthMax"]))
        log("N: %s, DBID: %s, H: %s, S: %s, L:%s" % (Name, DBID, Health, Stamina, Ladder), True)
    print datetime.datetime.now().strftime('%H:%M:%S')
    log("DEFENDER-ATTACKER", True)
    ati = 0
    nta = 0
    ia = 0
    na = ""
    for p in ta:
        n = p["PlayerName"]
        s = int(p["Stamina"])
        while s>0:
            if nta > 0:
                #log("%s %s, %s, NA:%s, S:%s" % (n, str(ia), na, str(nta), str(s)), True)
                log("d:\srv\python27\python.exe d:/srv/vamp/battle.py %s %s %s 1 0" % (n, str(bid), str(ia)), True, False)
                s = s - 1
                nta = nta - 1
                continue
            ia = 0
            while True:
                if ati >= len(at):
                    ia = 0
                    break
                an = at[ati]["PlayerName"]
                ah = float(at[ati]["HealthCur"])/float(at[ati]["HealthMax"])
                ia = at[ati]["FighterDBID"]
                na = at[ati]["PlayerName"]
                ati = ati + 1
                if ah>0.9:
                    nta = 3
                    break
                if ah>0.6:
                    nta = 2
                    break
                if ah>0.3:
                    nta = 1
                    break
            if ia == 0: print("EOL");return
            #log("%s %s, %s, NA:%s, S:%s" % (n, str(ia), na, str(nta), str(s)), True)
            log("d:\srv\python27\python.exe d:/srv/vamp/battle.py %s %s %s 1 0" % (n, str(bid), str(ia)), True, False)
            #d:\srv\python27\python.exe d:\srv\games\vamp\battle.py margo 46589 380224 1 1
            s = s - 1
            nta = nta - 1

def healup_person():
    info = get_slaves_and_info()
    info['hp_fight'] = hp_fight = info['hp_max']/5 + 1
    log('user info got')
    if info['hp'] < info['hp_fight']:
        info['hp_need'] = hp_need = hp_fight - info['hp']
        log('need heal '+str(hp_need))
        sum_slaves = 0
        for slave in info['slaves']:
            sum_slaves += slave['count']
        if sum_slaves < hp_need:
            log("Not enoufh slaves blood", True)
            time.sleep(1)
        info['sum_slaves'] = sum_slaves
        for slave in info['slaves']:
            if hp_need <= 0:
                slave['count'] = 0
                continue
            if hp_need < slave['count']:
                slave['count'] = hp_need
                hp_need = 0
            else:
                hp_need -= slave['count']
        log('start heal')
        heal_person(info['slaves'])

    
def getBattlesData():
    data = []
    client = RemotingService('http://dracula.irq.ru/Gateway.aspx')
    service = client.getService('MafiaAMF.AMFService')
    resp = service.dispatch(params1,"AMFService.ClanFightListGet",[{}],False)
    if resp.has_key("data"):
        data = resp["data"]
    if data.has_key("Answer"):
        data = data["Answer"]
    if data.has_key("OtherData"):
        data = data["OtherData"]
    if data.has_key("ClanWarsList"):
        data = data["ClanWarsList"]
    return data
    
def reduce_HP():
    if mission:
        if not person.has_key("no_missions"):
            for i in range(10):
                command = "AMFService.DoMission"
                params2 = [{"missionId":687+i}]
                try:
                    resp = sendRequest(params1,command,params2)
                    code = resp["data"]["Answer"]["Code"]
                    log("User: %s, Command: %s, Code: %s"%(person['n'],command,code))
                except:
                    log("User: %s, Command: %s, ERROR!"%(person['n'],command))
                    time.sleep(1)
                
def get_slaves_and_info():
    if person:
        if person:
            command = "AMFService.Hospital"
            params2 = [{"SlaveId":1, "Blood":1}]
            #command = "AMFService.UserInit"
            #params2 = [{"SocialIsGirl":Flase, "friends":[], "SocialAvatarUrl":"", "SocialName":"1", "SocialSurname":"1", "SocialNick":"1",}]
            try:
                resp = sendRequest(params1,command,params2)
                code = resp["data"]["Answer"]["Code"]
                log("User: %s, Command: %s, Code: %s"%(person['n'],command,code))
                user = {}
                user["name"] = resp["data"]["UserInfo"]["Name"].encode('utf-8')
                user["hp"] = int(resp["data"]["UserInfo"]["Health"]["Value"])
                user["hp_max"] = int(resp["data"]["UserInfo"]["Health"]["MaxValue"])
                user["slaves"] = []
                slaves = resp["data"]["Answer"]["OtherData"]["Business"]
                for slave in slaves:
                    user["slaves"].append({'id':int(slave["DBID"]), 'count':int(slave["NowMoney"])})
                return user
            except:
                log("User: %s, Command: %s, ERROR!"%(person['n'],command))
    return None
                
def heal_person(slaves):
    if person:
        for slave in slaves:
            if not slave['count']: return
            command = "AMFService.Hospital"
            params2 = [{"SlaveId":slave['id'], "Blood":slave['count']}]
            try:
                resp = sendRequest(params1,command,params2)
                code = resp["data"]["Answer"]["Code"]
                log("User: %s, Command: %s, Code: %s"%(person['n'],command,code))
            except:
                log("User: %s, Command: %s, ERROR!"%(person['n'],command))
                
def get_fight():
    if person:
        if person:
            command = "AMFService.ClanFightInfoGet"
            params2 = [{"BattleDBID":bid,"IsArchive":False}]
            try:
                resp = sendRequest(params1,command,params2)
                code = resp["data"]["Answer"]["Code"]
                log("User: %s, Command: %s, Code: %s"%(person['n'],command,code))
                return resp
            except:
                log("User: %s, Command: %s, ERROR!"%(person['n'],command))
                return None

def attack_target(bid, tgt):
    if person:
        if person:
            command = "AMFService.ClanFightAttack"
            params2 = [{"BattleDBID":bid,"TargetDBID":tgt}]
            code = -1
            try:
                resp = sendRequest(params1,command,params2)
                code = resp["data"]["Answer"]["Code"]
                log("User: %s, Command: %s, Code: %s"%(person['n'],command,code))
            except:
                log("User: %s, Command: %s, ERROR!"%(person['n'],command))
    return code

def user_init():
    if person:
        if person:
            command = "AMFService.UserInit"
            params2 = [{"SocialIsGirl":False,"SocialSurname":"Bot","SocialName":"Bot","friends":[],"SocialNick":"Bot","SocialAvatarUrl":""}]
            try:
                resp = sendRequest(params1,command,params2)
                code = resp["data"]["Answer"]["Code"]
                log("User: %s, Command: %s, Code: %s"%(person['n'],command,code))
            except:
                log("User: %s, Command: %s, ERROR!"%(person['n'],command))

def fight_clan(name):
    if name:
        if pdict.has_key(name):
            command = "AMFService.ClanFightDeclare"
            params2 = [{"EnemyDBID":targetClanID}]
            try:
                params = get_params1(pdict[name]['u'], pdict[name]['s'])
                resp = sendRequest(params,command,params2)
                code = resp["data"]["Answer"]["Code"]
                log("User: %s, Command: %s, Code: %s"%(person['n'],command,code))
            except:
                log("User: %s, Command: %s, ERROR!"%(person['n'],command))
                
                
                
cl = getBattlesData()
for c in cl:
   if c["Winner"] == 0:
       bid = c["BattleDBID"]
       print bid
       main()
       
log_end()