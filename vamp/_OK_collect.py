import pyamf
import sys
import json
import datetime
import time
from pyamf.remoting.client import RemotingService

sid = 20049
plist = [
        {"ss":"8498TU6YQa6byTB.Idf2M281wd87xXG3x34ayTC3M73bPUkWO362y1DTR6", "u":"909428586714", "s":"65b4fe27f60a84e1789e64f2e83d7601", 'n':"Demonika"}, #me
        {"ss":"e4d8MRj.P9d3MRhzJ529T382Q75eL.hOOd94K.8zs422xU9QId74w0GXLb1", "u":"196891662342", "s":"5e0d81abc1a4586252630f0c1c8b76fa", 'n':"Holycrack"}, #me
        {"ss":"0cddL3lXt479S.jUK20cu2l0L283vQiTPe84KRGTHeadKQDRJ210QTCYKc7", "u":"908125232471", "s":"83c111e36bd4047ac673cc520eb36221", 'n':"Dark"} #me1025367
        #{"ss":"c839MQGVL8f4JTl3xe6dRSFzs704zUlSw2e9yXCXvea2R1AWKce8P.G1R4b", "u":"153010015330", "s":"fc617ac75c3d51835cb205e7f66bf768", 'n':"Margaret"} #me
        #{"u":"34688001", "s":"a08e48565ce2bbb87ead6ce014016a0e", 'n':"magistra", "no_missions":True, "no_chest":True} #magistra
        ]

client = RemotingService('http://odnvamp.irq.ru/Gateway.aspx')
service = client.getService('MafiaAMF.AMFService')
    
def log(s):
    s = "[" + datetime.datetime.now().strftime('%d.%m %H:%M:%S')+"] " + s
    fatype = "_OK_collect_log_"+str(sid)
    try:
        tfile = open(fatype, "a")
        tfile.write(s.encode('utf-8')+'\n')
        tfile.close()
    except:
        tfile = open(fatype, "w")
        tfile.write(s.encode('utf-8')+'\n')
        tfile.close()

def sendRequest(params1, command, params2):
    client = RemotingService('http://odnvamp.irq.ru/Gateway.aspx')
    service = client.getService('MafiaAMF.AMFService')
    #resp = service.dispatch(params1,"AMFService.ClanFightInfoGet",[{"BattleDBID":bid,"IsArchive":False}],False)
    return service.dispatch(params1,command,params2,False)
    #data = resp["data"]["Answer"]["OtherData"]

def main():
    print datetime.datetime.now().strftime('%H:%M:%S')
    for person in plist:
        params1 = {
            "userId":person['u'],
            "ServerVersion":sid,
            "SystemID":"4",
            "sig":person['s'],
            "session":person['ss'],
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