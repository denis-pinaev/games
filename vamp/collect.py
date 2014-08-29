import pyamf
import sys
import json
import datetime
import time
from pyamf.remoting.client import RemotingService

client = RemotingService('http://dracula.irq.ru/Gateway.aspx')
service = client.getService('MafiaAMF.AMFService')
sid = 11329
plist = [
        {"u":"124520", "s":"d6b9ab24005cf6447de56d505f09b9a9", 'n':"CorC"}, #me
        {"u":"155908147", "s":"27318498bd78868465f331f3c5c45fcd", 'n':"margo", "no_chest":True}, #margo
        #{"u":"13200983", "s":"e2cffa0c183f41194776e5b48bf3e460", 'n':"noname 1"}, #no name 1
        #{"u":"56433778", "s":"1214f5cc84b0de0188e214c139a2f7d9", 'n':"noname 2"}, #no name 2
        #{"u":"16843363", "s":"72f0196726e1eb959166e8b524b49dfa", 'n':"frier"}, #frier
        {"u":"47654405", "s":"5b58a05fa548b92ddc318a574ca44a2a", 'n':"luska", "no_chest":True}, #Luska
        {"u":"120865611", "s":"a1d8f762dc70137348d2031a493b0e5b", 'n':"ladivictori"}, #LadyVictory
        {"u":"153969376", "s":"51b28aa0e28b9e1c78681c1b4edb92ff", 'n':"nemesis"}, #Nemesis
        {"u":"84324359", "s":"2e04ff007aa66f86827a68a9a566889a", 'n':"venom"}, #VictoriaVenom
        {"u":"156721888", "s":"627c9ff59bed2df10f1b8e9a5d2398bc", 'n':"anger"}, #Goddess of Anger
        {"u":"108534050", "s":"ab40269dcbfb1374c7590050ae3b242c", 'n':"vlad"}, #Vlad Hunter
        {"u":"93902559", "s":"e365fb4b1f20c6289e2df08b101e8cb7", 'n':"gludia", "no_chest":True}, #Gludiya
        {"u":"107564843", "s":"f14ee2e6686a3a1ed382c9cbd2197543", 'n':"gludia2"}, #Gludiya2
        {"u":"107738176", "s":"846a794ee3ae0c1b068635fdf315d90c", 'n':"gludia3"}, #Gludiya3
        {"u":"163834109", "s":"2145e7542c750385d38675b9f8f648d7", 'n':"gludia4"}, #Gludiya4
        {"u":"217858589", "s":"61ad63f2daa8afe9c0ea07d14a273064", 'n':"isida"}, #Isi
        {"u":"217752865", "s":"464118e98f82e3c85665566cb02ae04d", 'n':"tor"}, #Tor
        {"u":"160511757", "s":"fdb5b7a95c9fe6aa5399ad4346799011", 'n':"tanazia", "no_chest":True}, #Tanazia
        {"u":"9602055", "s":"1882652382ae743634e8a9a7a3f71001", 'n':"demoniex", "no_chest":True, "no_chest":True}, #Demoniex
        {"u":"111562663", "s":"65d32fa6d170d1ff100c38c073b306c1", 'n':"lucky", "no_chest":True}, #LuckyRU
        {"u":"44419226", "s":"a0b1d67c2388ae8f53a15f3f5de5067c", 'n':"vasilisk", "no_chest":True}, #Vasilisk
        {"u":"2959909", "s":"3b3c9c202351991b0de294584bfc2507", 'n':"di", "no_missions":True, "no_chest":True}, #Diana
        {"u":"34688001", "s":"a08e48565ce2bbb87ead6ce014016a0e", 'n':"magistra", "no_chest":True} #magistra
        #{"u":"18742782", "s":"37b2f9d03330b64531f3d665e50a72b9", 'n':"freez"} #freezze!	

        ]

def log(s):
    s = "[" + datetime.datetime.now().strftime('%d.%m %H:%M:%S')+"] " + s
    fatype = "collect_log_"+str(sid)
    try:
        tfile = open(fatype, "a")
        tfile.write(s.encode('utf-8')+'\n')
        tfile.close()
    except:
        tfile = open(fatype, "w")
        tfile.write(s.encode('utf-8')+'\n')
        tfile.close()

def sendRequest(params1, command, params2):
    #resp = service.dispatch(params1,"AMFService.ClanFightInfoGet",[{"BattleDBID":bid,"IsArchive":False}],False)
    return service.dispatch(params1,command,params2,False)
    #data = resp["data"]["Answer"]["OtherData"]

def main():
    print datetime.datetime.now().strftime('%H:%M:%S')
    for person in plist:
        params1 = {
            "userId":person['u'],
            "ServerVersion":sid,
            "SystemID":"1",
            "sig":person['s']
        }
        
        if not person.has_key("no_missions"):
            for i in range(10):
                command = "AMFService.DoMission"
                params2 = [{"missionId":687+i}]
                try:
                    resp = sendRequest(params1,command,params2)
                    code = resp["data"]["Answer"]["Code"]
                    #log("User: %s, Command: %s, Code: %s"%(person['n'],command,code))
                except:
                    log("User: %s, Command: %s, ERROR!"%(person['n'],command))
                
        if not person.has_key("no_hunt"):
            for i in range(5):
                command = "AMFService.Hunt"
                params2 = [{"Target":i}]
                try:
                    resp = sendRequest(params1,command,params2)
                    code = resp["data"]["Answer"]["Code"]
                    #log("User: %s, Command: %s, Code: %s"%(person['n'],command,code))
                except:
                    log("User: %s, Command: %s, ERROR!"%(person['n'],command))
    
        if not person.has_key("no_slaves"):
            command = "AMFService.TakeBlood"
            params2 = [{"SlaveId":-1}]
            try:
                resp = sendRequest(params1,command,params2)
                code = resp["data"]["Answer"]["Code"]
                #log("User: %s, Command: %s, Code: %s"%(person['n'],command,code))
            except:
                log("User: %s, Command: %s, ERROR!"%(person['n'],command))
                
        if not person.has_key("no_chest"):
            command = "AMFService.ElderChest"
            params2 = []
            try:
                resp = sendRequest(params1,command,params2)
                code = resp["data"]["Answer"]["Code"]
                #log("User: %s, Command: %s, Code: %s"%(person['n'],command,code))
            except:
                log("User: %s, Command: %s, ERROR!"%(person['n'],command))
    
            command = "AMFService.UseObject"
            params2 = [{"ObjId":468,"Selection":0}]
            try:
                resp = sendRequest(params1,command,params2)
                code = resp["data"]["Answer"]["Code"]
                #log("User: %s, Command: %s, Code: %s"%(person['n'],command,code))
            except:
                log("User: %s, Command: %s, ERROR!"%(person['n'],command))

while True:
    pause = 5*60
    try:
        main()
    except:
        log(str(sys.exc_info()))
        print sys.exc_info()
    time.sleep(pause)