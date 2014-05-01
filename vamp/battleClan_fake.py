import pyamf
import sys
import json
import datetime
import time
from pyamf.remoting.client import RemotingService


sid = 11329
stamina = 3
bid = 1
tgt = 1
person = 'margo'
mission = True
reenter_first = False
clanID = 888882
targetClanID = 1
sureClan = isFight = True
firstA = False

plist = [
        {"u":"34688001", "s":"a08e48565ce2bbb87ead6ce014016a0e", 'n':"magistra", 'no_missions':True},
        {"u":"155908147", "s":"27318498bd78868465f331f3c5c45fcd", 'n':"margo"}, 
        {"u":"108534050", "s":"ab40269dcbfb1374c7590050ae3b242c", 'n':"vlad"}
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
        
client = RemotingService('http://dracula.irq.ru/Gateway.aspx')
service = client.getService('MafiaAMF.AMFService')

def log(s, final=False):
    global log_all
    s = "[" + datetime.datetime.now().strftime('%d.%m %H:%M:%S')+"] " + s
    log_all += s + "\n"
    print s
    if final: log_end()

def log_end():
    global log_all
    fatype = "battle_clan_fake_log_"+str(bid)
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
    return service.dispatch(params1,command,params2,False)

def main():
    global bid, tgt, targetClanID, stamina
    print datetime.datetime.now().strftime('%H:%M:%S')
    cl = getBattlesData()

    rest = 999
    if len(cl)>0:
        c = cl[0]
        if c["Winner"] != 0: return True
        targetClanID = c["EnemyDBID"]
        bid = c["BattleDBID"]
        log_all = ""
        log("bid: %s, clan: %s" % (str(bid), str(targetClanID)))
        #s = json.dumps(getBattlesData(), indent=4)
        #log(s, True)
    else: return True
    fight = get_fight()
    a = fight["data"]["Answer"]["OtherData"]["ClanFightInfo"]["ActorPlayers"]
    if (len(a)>0):
        tgt = a[0]["FighterDBID"]
    log("bid: %s, clan: %s, tgt: %s" % (str(bid), str(targetClanID), str(tgt)))
    was_heal = False
    while rest>5:
        fight = get_fight()
        rest = fight["data"]["Answer"]["OtherData"]["ClanFightInfo"]["SecondsToEnd"]
        log("Left time " + str(rest), True)
        a = fight["data"]["Answer"]["OtherData"]["ClanFightInfo"]["ActorPlayers"]
        if (len(a)>0):
            tgt = a[0]["FighterDBID"]
            rest = 0
        time.sleep(min(60*30, rest/2))
        print datetime.datetime.now().strftime('%H:%M:%S')
        if rest<15 and not was_heal:
            log("start heal_up", True)
            user_init()
            healup_person()
            was_heal = True

    stamina = 55
    while stamina > 0:
        stamina -= 1
        if not was_heal:
            healup_person()
            was_heal = True
        log('attack ready')
        #code = 1123
        #stamina = 0
        fight = get_fight()
        a = fight["data"]["Answer"]["OtherData"]["ClanFightInfo"]["ActorPlayers"]
        if (len(a)>0):
            tgt = a[0]["FighterDBID"]
        log("bid: %s, clan: %s, tgt: %s"% (str(bid), str(targetClanID), str(tgt)))
        code = attack_target(bid, tgt)
        
        if code == 1123: stamina = 0
        if code == 501: healup_person()
        
    log('start missions', True)
    reduce_HP()
    print datetime.datetime.now().strftime('%H:%M:%S')
    return False

def healup_person():
    global person, params1
    for p in plist:
        person = p
        params1 = get_params1(person['u'], person['s'])
        healup_person2()

def healup_person2():
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
            log("Not enoufh slaves blood")
            #time.sleep(1)
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
    for person in plist:
        if not person.has_key("no_missions"):
            for i in range(10):
                command = "AMFService.DoMission"
                params1 = get_params1(person['u'], person['s'])
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
    command = "AMFService.ClanFightAttack"
    params2 = [{"BattleDBID":bid,"TargetDBID":tgt}]
    code = -1
    for person in plist:
        if person:
            try:
                params1 = get_params1(person['u'], person['s'])
                resp = sendRequest(params1,command,params2)
                code = resp["data"]["Answer"]["Code"]
                log("User: %s, Command: %s, Code: %s"%(person['n'],command,code))
            except:
                log("User: %s, Command: %s, ERROR!"%(person['n'],command))
    return code

def user_init():
    for person in plist:
        if person:
            command = "AMFService.UserInit"
            params1 = get_params1(person['u'], person['s'])
            params2 = [{"SocialIsGirl":False,"SocialSurname":"Bot","SocialName":"Bot","friends":[],"SocialNick":"Bot","SocialAvatarUrl":""}]
            try:
                resp = sendRequest(params1,command,params2)
                code = resp["data"]["Answer"]["Code"]
                log("User: %s, Command: %s, Code: %s"%(person['n'],command,code))
            except:
                log("User: %s, Command: %s, ERROR!"%(person['n'],command))
           
                


while True:
    try:
        longTime = main()
        log_end()
        if longTime: time.sleep(23*60*60)
    except:
        log(str(sys.exc_info()), True)
        print sys.exc_info()