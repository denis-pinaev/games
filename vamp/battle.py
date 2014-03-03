import pyamf
import sys
import json
import datetime
import time
from pyamf.remoting.client import RemotingService

#usage: PERSON BID TARGET STAMINA MISSIONS
'''
d:\srv\python27\python.exe d:\srv\vamp\battle.py vasilisk 46589 1108736 3 0
d:\srv\python27\python.exe d:\srv\vamp\battle.py lucky 46589 693482 3 0
'''


sid = 22442
stamina = 3
bid = 1
tgt = 1
person = 'corc'#'none'
mission = True
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
#G2 f14ee2e6686a3a1ed382c9cbd2197543 107564843
plist = [
        {"u":"124520", "s":"d6b9ab24005cf6447de56d505f09b9a9", 'n':"corc"}, #me
        {"u":"155908147", "s":"27318498bd78868465f331f3c5c45fcd", 'n':"margo"}, #margo
        {"u":"13200983", "s":"e2cffa0c183f41194776e5b48bf3e460", 'n':"noname1"}, #no name 1
        {"u":"56433778", "s":"1214f5cc84b0de0188e214c139a2f7d9", 'n':"noname2"}, #no name 2
        {"u":"16843363", "s":"72f0196726e1eb959166e8b524b49dfa", 'n':"frier"}, #frier
        {"u":"9602055", "s":"1882652382ae743634e8a9a7a3f71001", 'n':"demoniex", "no_missions":True}, #Demoniex
        {"u":"111562663", "s":"65d32fa6d170d1ff100c38c073b306c1", 'n':"lucky", "no_missions":True}, #LuckyRU
        {"u":"44419226", "s":"a0b1d67c2388ae8f53a15f3f5de5067c", 'n':"vasilisk", "no_missions":True}, #Vasilisk
        {"u":"2959909", "s":"3b3c9c202351991b0de294584bfc2507", 'n':"di", "no_missions":True}, #Diana
        {"u":"93902559", "s":"e365fb4b1f20c6289e2df08b101e8cb7", 'n':"gludia"}, #Gludiya
        {"u":"47654405", "s":"5b58a05fa548b92ddc318a574ca44a2a", 'n':"luska"}, #Luska
        {"u":"120865611", "s":"a1d8f762dc70137348d2031a493b0e5b", 'n':"ladivictori"}, #LadyVictory
        {"u":"153969376", "s":"51b28aa0e28b9e1c78681c1b4edb92ff", 'n':"nemesis"}, #Nemesis
        {"u":"84324359", "s":"2e04ff007aa66f86827a68a9a566889a", 'n':"venom"}, #VictoriaVenom
        {"u":"156721888", "s":"627c9ff59bed2df10f1b8e9a5d2398bc", 'n':"anger"}, #Goddess of Anger
        {"u":"108534050", "s":"ab40269dcbfb1374c7590050ae3b242c", 'n':"vlad"}, #Vlad Hunter
        {"u":"34688001", "s":"a08e48565ce2bbb87ead6ce014016a0e", 'n':"magistra", "no_missions":True} #magistra
        #{"u":"18742782", "s":"37b2f9d03330b64531f3d665e50a72b9", 'n':"freez"} #freezze!
        ]

if person:
    for p in plist:
        found = False
        if p['n'] == person:
            found = True
            person = p
            break
    if found:
        params1 = {
            "userId":person['u'],
            "ServerVersion":sid,
            "SystemID":"1",
            "sig":person['s']
        }
    else:
        print "Unknown person"
        time.sleep(99999)
else:
    print "No person"
    time.sleep(99999)
        
def log(s):
    s = "[" + datetime.datetime.now().strftime('%d.%m %H:%M:%S')+"] " + s
    print s
    return
    fatype = "battle_log_"+str(sid)
    try:
        tfile = open(fatype, "a")
        tfile.write(s.encode('utf-8')+'\n')
        tfile.close()
    except:
        tfile = open(fatype, "w")
        tfile.write(s.encode('utf-8')+'\n')
        tfile.close()

def sendRequest(params1, command, params2):
    client = RemotingService('http://dracula.irq.ru/Gateway.aspx')
    service = client.getService('MafiaAMF.AMFService')
    return service.dispatch(params1,command,params2,False)

def main():
    global stamina
    print datetime.datetime.now().strftime('%H:%M:%S')
    user_init()
    while stamina > 0:
        stamina -= 1
        info = get_slaves_and_info()
        info['hp_fight'] = hp_fight = info['hp_max']/5 + 1
        print 'user info got', stamina
        if info['hp'] < info['hp_fight']:
            info['hp_need'] = hp_need = hp_fight - info['hp']
            print 'need heal', hp_need
            sum_slaves = 0
            for slave in info['slaves']:
                sum_slaves += slave['count']
            if sum_slaves < hp_need:
                print "Not enoufh slaves blood"
                time.sleep(99999)
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
            print 'start heal'
            heal_person(info['slaves'])
            
        #info = get_slaves_and_info()
        print 'attack ready'
        attack_target(bid, tgt)
        
    print 'start missions', mission
    reduce_HP()
        
    print datetime.datetime.now().strftime('%H:%M:%S')
    #time.sleep(9999)
    
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
                
def attack_target(bid, tgt):
    if person:
        if person:
            command = "AMFService.ClanFightAttack"
            params2 = [{"BattleDBID":bid,"TargetDBID":tgt}]
            try:
                resp = sendRequest(params1,command,params2)
                code = resp["data"]["Answer"]["Code"]
                log("User: %s, Command: %s, Code: %s"%(person['n'],command,code))
            except:
                log("User: %s, Command: %s, ERROR!"%(person['n'],command))

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
                
if True:
    try:
        main()
        time.sleep(1)
    except:
        log(str(sys.exc_info()))
        print sys.exc_info()