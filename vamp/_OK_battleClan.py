import pyamf
import sys
import json
import datetime
import time
from pyamf.remoting.client import RemotingService


#time.sleep(60*12*60)

sid = 6614
stamina = 3
bid = 1
tgt = 1
person = 'Dark'
mission = True
reenter_first = True
clanID = 1134529
targetClanID = 374242
sureClan = isFight = False
#sureClan = isFight = True
firstA = False

exceptions = []#["99373307"]

client = RemotingService('http://odnvamp.irq.ru/Gateway.aspx')
service = client.getService('MafiaAMF.AMFService')

if len(sys.argv) > 1:
    person = sys.argv[1]
if len(sys.argv) > 2:
    bid = int(sys.argv[2])
if len(sys.argv) > 3:
    tgt = int(sys.argv[3])
if len(sys.argv) > 4:
    stamina = int(sys.argv[4])
if len(sys.argv) > 5:
    mission = int(sys.argv[5]) == 1

plist = [
        {"ss":"8498TU6YQa6byTB.Idf2M281wd87xXG3x34ayTC3M73bPUkWO362y1DTR6", "u":"909428586714", "s":"65b4fe27f60a84e1789e64f2e83d7601", 'n':"Demonika"}, #zkl
        {"ss":"e4d8MRj.P9d3MRhzJ529T382Q75eL.hOOd94K.8zs422xU9QId74w0GXLb1", "u":"196891662342", "s":"5e0d81abc1a4586252630f0c1c8b76fa", 'n':"Holycrack"}, #kl
        {"ss":"0cddL3lXt479S.jUK20cu2l0L283vQiTPe84KRGTHeadKQDRJ210QTCYKc7", "u":"908125232471", "s":"83c111e36bd4047ac673cc520eb36221", 'n':"Dark"}, #me1025367
        {"ss":"c839MQGVL8f4JTl3xe6dRSFzs704zUlSw2e9yXCXvea2R1AWKce8P.G1R4b", "u":"153010015330", "s":"fc617ac75c3d51835cb205e7f66bf768", 'n':"Margaret"} #3
        ]
        
pdict = {
        "Demonika":{"ss":"8498TU6YQa6byTB.Idf2M281wd87xXG3x34ayTC3M73bPUkWO362y1DTR6", "u":"909428586714", "s":"65b4fe27f60a84e1789e64f2e83d7601", 'id':1047154}, 
        "Holycrack":{"ss":"e4d8MRj.P9d3MRhzJ529T382Q75eL.hOOd94K.8zs422xU9QId74w0GXLb1", "u":"196891662342", "s":"5e0d81abc1a4586252630f0c1c8b76fa", 'id':1035220}, 
        "Dark":{"ss":"0cddL3lXt479S.jUK20cu2l0L283vQiTPe84KRGTHeadKQDRJ210QTCYKc7", "u":"908125232471", "s":"83c111e36bd4047ac673cc520eb36221", 'id':1025367}, #me
        "Margaret":{"ss":"c839MQGVL8f4JTl3xe6dRSFzs704zUlSw2e9yXCXvea2R1AWKce8P.G1R4b", "u":"153010015330", "s":"fc617ac75c3d51835cb205e7f66bf768", 'id':912472} 
        }

def get_params1(name, pid, session):
    global sid
    params1 = {
        "session":session,
        "userId":name,
        "ServerVersion":sid,
        "SystemID":"4",
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
        params1 = get_params1(person['u'], person['s'], person['ss'])
    else:
        print "Unknown person"
        time.sleep(99999)
else:
    print "No person"
    time.sleep(99999)
    
log_all = ""
        
def log(s, final=False):
    global log_all
    s = "[" + datetime.datetime.now().strftime('%d.%m %H:%M:%S')+"] " + s
    log_all += s + "\n"
    print s
    if final: log_end()

def log_end():
    global log_all
    fatype = "_OK_battle_clan_log_"+str(bid)
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

def reenter():
    zam_clan("Holycrack","Demonika")
    exit_clan("Holycrack")
    exit_clan("Holycrack")
    enter_clan("Holycrack")
    accept_clan("Demonika","Holycrack")
    zam_clan("Demonika","Holycrack")

    exit_clan("Demonika")
    exit_clan("Demonika")
    enter_clan("Demonika")
    accept_clan("Holycrack","Demonika")
    zam_clan("Holycrack","Demonika")
    
    #exit_clan("Margaret")
    
    exit_clan("Dark")
    enter_clan("Dark")
    accept_clan("Holycrack","Dark")
    

def get_targets():
    global tgt, bid
    f = open("battleClan", "r")
    s = f.read()
    f.close()
    a = s.split()
    bid = int(a[0])
    tgt = int(a[1])
    print bid, tgt

def main():
    global bid, tgt
    global stamina
    print datetime.datetime.now().strftime('%H:%M:%S')
    cl = getBattlesData()
    if not isFight:
        log("WARNING! REENTER!!!")
        #time.sleep(5)
        if reenter_first: reenter()
        getTargetClan("Holycrack", cl)
        fight_clan("Holycrack")
        print datetime.datetime.now().strftime('%H:%M:%S')
    rest = 999
    if True:
        for c in cl:
            if c["EnemyDBID"] == targetClanID:
                bid = c["BattleDBID"]
                break
        log_all = ""
        log(str(bid))
        s = json.dumps(getBattlesData(), indent=4)
        log(s, True)
    fight = get_fight()
    a = fight["data"]["Answer"]["OtherData"]["ClanFightInfo"]["TargetPlayers"]
    if len(a) < 1:
        a = fight["data"]["Answer"]["OtherData"]["ClanFightInfo"]["ActorPlayers"]
    a.sort(key=lambda x: x["HealthMax"])
    tgt = a[0]["FighterDBID"]
    print bid, tgt
    was_heal = False
    while rest>2:
        fight = get_fight()
        rest = fight["data"]["Answer"]["OtherData"]["ClanFightInfo"]["SecondsToEnd"]
        log("Left time " + str(rest), True)
        time.sleep(min(60*30, rest/2))
        print datetime.datetime.now().strftime('%H:%M:%S')
        if rest<15 and not was_heal:
            log("start heal_up", True)
            healup_person()
            was_heal = True
    #get_targets()
    stamina = 100
    while stamina > 0:
        stamina -= 1
        if not was_heal:
            healup_person()
            was_heal = True
        #info = get_slaves_and_info()
        log('attack ready')
        user_init()
        

        #code = 1123
        #stamina = 0
        code = attack_target(bid, tgt)
        
        
        
        if code == 1123: stamina = 0
        if code == 501: healup_person()
        
    log('start missions', True)
    reduce_HP()
    reenter()
    print datetime.datetime.now().strftime('%H:%M:%S')

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
    resp = sendRequest(params1,"AMFService.ClanFightListGet",[{}])
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

def exit_clan(name):
    if name:
        if pdict.has_key(name):
            command = "AMFService.ClanLeave"
            params2 = [{}]
            try:
                params = get_params1(pdict[name]['u'], pdict[name]['s'], pdict[name]['ss'])
                resp = sendRequest(params,command,params2)
                code = resp["data"]["Answer"]["Code"]
                log("User: %s, Command: %s, Code: %s"%(person['n'],command,code))
            except:
                log("User: %s, Command: %s, ERROR!"%(person['n'],command))
                
def enter_clan(name):
    if name:
        if pdict.has_key(name):
            command = "AMFService.ClanJoin"
            params2 = [{"Reason":"Bot", "ClanDBID":clanID}]
            try:
                params = get_params1(pdict[name]['u'], pdict[name]['s'], pdict[name]['ss'])
                resp = sendRequest(params,command,params2)
                code = resp["data"]["Answer"]["Code"]
                log("User: %s, Command: %s, Code: %s"%(person['n'],command,code))
            except:
                log("User: %s, Command: %s, ERROR!"%(person['n'],command))
                
def accept_clan(name, name2):
    if name:
        if pdict.has_key(name) and pdict.has_key(name2):
            command = "AMFService.ClanAccept"
            params2 = [{"UserDBID":pdict[name2]['id']}]
            try:
                params = get_params1(pdict[name]['u'], pdict[name]['s'], pdict[name]['ss'])
                resp = sendRequest(params,command,params2)
                code = resp["data"]["Answer"]["Code"]
                log("User: %s, Command: %s, Code: %s"%(person['n'],command,code))
            except:
                log("User: %s, Command: %s, ERROR!"%(person['n'],command))
                
def zam_clan(name, name2):
    if name:
        if pdict.has_key(name) and pdict.has_key(name2):
            command = "AMFService.ClanOfficerSet"
            params2 = [{"UserDBID":pdict[name2]['id']}]
            try:
                params = get_params1(pdict[name]['u'], pdict[name]['s'], pdict[name]['ss'])
                resp = sendRequest(params,command,params2)
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
                params = get_params1(pdict[name]['u'], pdict[name]['s'], pdict[name]['ss'])
                resp = sendRequest(params,command,params2)
                code = resp["data"]["Answer"]["Code"]
                log("User: %s, Command: %s, Code: %s"%(person['n'],command,code))
            except:
                log("User: %s, Command: %s, ERROR!"%(person['n'],command))
                
def getTargetClan(name, cl):
    global targetClanID
    clist = getClanList(name)
    if clist:
        clist.sort(key=lambda x: x['Rang'], reverse=True)
        for c in clist:
            if c["Level"]>1 and not (str(c["ClanDBID"]) in exceptions):
                targetClanID = c["ClanDBID"]
                wasC = True
                for clan in cl:
                    if clan["Winner"] == 0 and clan["EnemyDBID"] == targetClanID: wasC = False
                if wasC: break
    else:
        log("ERROR: no clans found")

def getClanList(name):
    if name:
        if pdict.has_key(name):
            command = "AMFService.ClanListGet"
            params2 = [{"IsFight":False}]
            try:
                params = get_params1(pdict[name]['u'], pdict[name]['s'], pdict[name]['ss'])
                resp = sendRequest(params,command,params2)
                code = resp["data"]["Answer"]["Code"]
                log("User: %s, Command: %s, Code: %s"%(person['n'],command,code))
                return resp["data"]["Answer"]["OtherData"]["ClanList"]
            except:
                log("User: %s, Command: %s, ERROR!"%(person['n'],command))
                


while True:
    try:
        main()
        log_end()
        sureClan = isFight = False
        
        targetClanID = 889390#889390
        #main()
        #log_end()
        if firstA:
            time.sleep(0*60*60)
            firstA = False
    except:
        log(str(sys.exc_info()), True)
        print sys.exc_info()
        sureClan = isFight = True
        time.sleep(1*60*60)