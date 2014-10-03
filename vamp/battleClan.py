import pyamf
import sys
import json
import datetime
import time
from pyamf.remoting.client import RemotingService


#time.sleep(60*12*60)

sid = 11329
stamina = 3
bid = 1
tgt = 1
person = 'gludia4'#'none'
mission = True
reenter_first = True
clanID = 2305215
targetClanID = 1220531#1349474
sureClan = isFight = False
#sureClan = isFight = True
firstA = False

exceptions = ["1349474", "888882", "2316470", "2305215"]

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

client = RemotingService('http://dracula.irq.ru/Gateway.aspx')
service = client.getService('MafiaAMF.AMFService')

plist = [
        {"u":"107564843", "s":"f14ee2e6686a3a1ed382c9cbd2197543", 'n':"holy"}, #Holy 644957
        {"u":"107738176", "s":"846a794ee3ae0c1b068635fdf315d90c", 'n':"isi"}, #Gabr 1211600
        {"u":"217858589", "s":"61ad63f2daa8afe9c0ea07d14a273064", 'n':"gabr"}, #Isi
        {"u":"217752865", "s":"464118e98f82e3c85665566cb02ae04d", 'n':"tor"}, #Tor
        {"u":"163834109", "s":"2145e7542c750385d38675b9f8f648d7", 'n':"gludia4"}, #Gludiya4
        {"u":"65706308", "s":"f4451c1962ffdaf519e86961cf0f1dfb", 'n':"gludia4"}, #newgirl
        {"u":"160511757", "s":"fdb5b7a95c9fe6aa5399ad4346799011", 'n':"tanazia"} #Tanazia
        ]
        
pdict = {
        "holy":{"u":"107564843", "s":"f14ee2e6686a3a1ed382c9cbd2197543", 'id':644957}, #Holy 644957
        "isi":{"u":"107738176", "s":"846a794ee3ae0c1b068635fdf315d90c", 'id':1211600}, #Gabr 1211600
        "gabr":{"u":"217858589", "s":"61ad63f2daa8afe9c0ea07d14a273064", "id":2302559}, 
        "gludia4":{"u":"163834109", "s":"2145e7542c750385d38675b9f8f648d7", "id":1764862},
        "tor":{"u":"217752865", "s":"464118e98f82e3c85665566cb02ae04d", "id":2302307},
        "newgirl":{"u":"65706308", "s":"f4451c1962ffdaf519e86961cf0f1dfb", 'id':2137438}, #newgirl
        "tanazia":{"u":"160511757", "s":"fdb5b7a95c9fe6aa5399ad4346799011", "id":2303868}
        }

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
        
def log(s, final=False):
    global log_all
    s = "[" + datetime.datetime.now().strftime('%d.%m %H:%M:%S')+"] " + s
    log_all += s + "\n"
    print s
    if final: log_end()

def log_end():
    global log_all
    fatype = "battle_clan_log_"+str(bid)
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
    zam_clan("holy","gabr")
    exit_clan("holy")
    exit_clan("holy")
    enter_clan("holy")
    accept_clan("gabr","holy")
    zam_clan("gabr","holy")

    exit_clan("gabr")
    exit_clan("gabr")
    enter_clan("gabr")
    accept_clan("holy","gabr")
    zam_clan("holy","gabr")
    
    exit_clan("gludia4")
    enter_clan("gludia4")
    accept_clan("holy","gludia4")
    
    exit_clan("newgirl")
    enter_clan("newgirl")
    accept_clan("holy","newgirl")
    

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
        getTargetClan("holy", cl)
        #time.sleep(5000)
        fight_clan("holy")
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

def exit_clan(name):
    if name:
        if pdict.has_key(name):
            command = "AMFService.ClanLeave"
            params2 = [{}]
            try:
                params = get_params1(pdict[name]['u'], pdict[name]['s'])
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
                params = get_params1(pdict[name]['u'], pdict[name]['s'])
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
                params = get_params1(pdict[name]['u'], pdict[name]['s'])
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
                params = get_params1(pdict[name]['u'], pdict[name]['s'])
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
                params = get_params1(pdict[name]['u'], pdict[name]['s'])
                resp = sendRequest(params,command,params2)
                code = resp["data"]["Answer"]["Code"]
                log("User: %s, Command: %s, Code: %s"%(person['n'],command,code))
            except:
                log("User: %s, Command: %s, ERROR!"%(person['n'],command))
                
def getTargetClan(name, cl):
    global targetClanID
    #return targetClanID
    clist = getClanList(name)
    if clist:
        clist.sort(key=lambda x: x['Rang'], reverse=True)
        for c in clist:
            print c["ClanDBID"], c["Level"]
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
                params = get_params1(pdict[name]['u'], pdict[name]['s'])
                resp = sendRequest(params,command,params2)
                code = resp["data"]["Answer"]["Code"]
                log("User: %s, Command: %s, Code: %s"%(person['n'],command,code))
                return resp["data"]["Answer"]["OtherData"]["ClanList"]
            except:
                log("User: %s, Command: %s, ERROR!"%(person['n'],command))
                


error = 1
while True:
    try:
        main()
        log_end()
        sureClan = isFight = False
        error = 1
        targetClanID = 2331404
        #main()
        #log_end()
        if firstA:
            time.sleep(3*60*60)
            firstA = False
    except:
        error += 1
        log(str(sys.exc_info()), True)
        print sys.exc_info()
        time.sleep(error)
        sureClan = isFight = True