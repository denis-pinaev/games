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
from common import get_buildings_ids, get_help_string


flist = ["144536559", "9894033", "106358745", "49809104"]


person = 0#old!
error = 0
start_p = 1
end_p = 999
if len(sys.argv) > 1:
    start_p = int(sys.argv[1])
if len(sys.argv) > 2:
    end_p = int(sys.argv[2])


persons = [
              {"pid":"124520","auth":"1e365d477c3207804013abaddbb6a0c4","gid":0,"sid":""},#corc
              {"pid":"102137300","auth":"e78c0aad90f427b06653067a45de6c6b","gid":0,"sid":""},#corcc
              {"pid":"160511757","auth":"6dc2dba90c1cc9d935542aa6a60c6fb4","gid":0,"sid":""},#vasya tanakan
              #{"pid":"","auth":"","gid":0,"sid":""},#nononon
              {"pid":"155908147","auth":"38e6c4c6f1a3ca43a78a6c499879ba7e","gid":0,"sid":""},#margo
              {"pid":"49809104","auth":"faeaec9d6c41db027a1f8a2dc7244c38","gid":0,"sid":""},#misha_zhukov
              #{"pid":"124678851","auth":"f659c32017ecad7b4d36b862f68351ef","gid":0,"sid":""},#misha_zhukov5
              {"pid":"182933786","auth":"662b4add4856bc946f65e70d9254c862","gid":0,"sid":""},#misha_zhukov4
              {"pid":"209559126","auth":"02e68b3110fbeac985c6846649e3cee2","gid":0,"sid":""},#misha_zhukov3
              {"pid":"200139667","auth":"0be685ed1b3787bc144ef88cf0d2de1d","gid":0,"sid":""},#misha_zhukov2
              {"pid":"199648989","auth":"14279d90af4c929b3f645e777e6b30fb","gid":0,"sid":""},#misha_zhukov1
              {"pid":"233828632","auth":"3cf7aac00f56163404482ed0550eb1dc","gid":0,"sid":""},#misha_zhukov7
              {"pid":"101053386","auth":"77a9e62eed9e7d25866efd2c8aeef30e","gid":0,"sid":""}#misha_zhukov6
          ]
start_hero = ['{"rnd":%s,"units":[{"home":0,"x":1,"sceneId":68402,"y":14,"id":364860972,"owner":1,"type":"hero","dir":4}],"index":"default"}',
              '{"units":[{"owner":1,"id":437216723,"type":null,"sceneId":66087,"x":1,"home":65599,"y":14,"dir":4}],"rnd":%s,"index":"default"}',
              '{"rnd":%s,"index":"default","units":[{"id":364860972,"type":"hero","y":14,"owner":1,"x":1,"dir":4,"home":0,"sceneId":69228}]}',
              '']
pid = persons[person]["pid"]
auth = persons[person]["auth"]
gid = 0
sid = ''
data = ''
actionCommand = 'Knights.doAction'
action = 'hp'
    
def getRandom():
    return str(int(random.random()*1000))
    
def log(s, pr=False):
    s = "[" + datetime.datetime.now().strftime('%d.%m %H:%M:%S')+"] " + s
    if pr: print s
    fatype = "hero_helpmisha_log"
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
    txt = resp.text.split('!')[1].encode('utf-8')
    first = txt.find("adInfo")
    if first > 0:
        second = txt.find('}', first)
        txt = txt[:first]+"a\":\"0"+txt[second+1:]
    if txt.find("news")>0:
        txt = txt[:txt.find("news")-2]+'}}'
    txt = txt.replace('"a":"0,"', '"a":"0"},"')
    
    try: json.loads(txt)
    except: txt = txt[:-1]
    
    tfile = open('fuck', "w")
    tfile.write(txt)
    tfile.close()
    
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
    global sid, gid, service, method
    service = 'Knights.initialize'
    method = 'initialize'
    initString = '{"age":30,"gender":1,"rnd":%s,"referralType":6,"newDay":false,"owner_id":"","hash":{},"auth_key":"%s","sid":""}'
    sid = ''
    gid = 0
    params = createData(method, initString % (getRandom(), auth))
    log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    print resp["data"][:100]
    #if auth == "" : resp["data"] = resp["data"][:-1]
    o = json.loads(resp["data"])
    #log(json.dumps(o, indent=4))
    error = o["error"]
    if error == 0:
        sid = o["sid"]
        gid = o["player"]["player_id"]
        log("sid: %s, gid: %s" % (str(sid), str(gid)), True)
    else:
        log(resp["data"], True)
        
    return resp["data"]
        

def getWorld(pers):
    global sid, gid, service, method
    service = actionCommand
    method = 'friendsGetWorld'
    dataString = '{"rnd":%s,"friendId":"%s","auth_key":"%s","sid":"%s","method":"%s"}' % (getRandom(), pers, auth, sid, method)
    params = createData(method, dataString)
    log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("getWorld %s done" % pers, True)
    else:
        log(resp["data"], True)
    return o

def sendHelp(pers, hbid):
    global sid, gid, service, method
    service = actionCommand
    method = 'friendHelpApply'
    dataString = '{"friendId":"%s","list":[%s],"rnd":%s,"auth_key":"%s","sid":"%s","method":"%s"}' % (pers, hbid, getRandom(), auth, sid, method)
    params = createData(method, dataString)
    log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("friendHelpApply done", True)
    else:
        log(resp["data"], True)
         

#'103'#altar
#'83'#hram
#'69113'#kuz 4go
#'65600'#ars
#65584,65724#zhelezo
#70081#runa

            #misha
flist = ["49809104"]
person = 0
sendSTR = ''
#persons = persons[3:33]

if True:
    i = 0
    total = len(persons)
    while i<total:
        pers = persons[i]
        pid = pers['pid']
        auth = pers['auth']
        gid =  pers['gid']
        sid =  pers['sid']
        init()

        f = flist[person]
        i += 1
        print "%d/%d (%d%%)" % (i, total, int(100*i/total))
        
        if len(sendSTR)>1:
            sendHelp(f, sendSTR)
            continue
        
        w = getWorld(f)
        max_help = 5
        if w["friend"].has_key("currentBuildingHelp"):
            ll = 5 - len(w["friend"]["currentBuildingHelp"])
            if ll<=0: nohf = '';continue
            max_help = ll
            try:
                qqq = ''
                for p in w["interaction"]: qqq = p;break
                ll = 5 - w["interaction"][qqq]["help"]
                if ll<=0: nohf = '';continue
                max_help = ll
            except: log("fail get count "+str(f))
        bbb = get_buildings_ids(w["friend"]["entities"])
        bk = []
        if w["friend"].has_key("recipes") and len(w["friend"]["recipes"])>0 and w["friend"]["recipes"].has_key("entities"):
            bk=get_help_string(w["friend"]["recipes"]["entities"],bbb,5)[:max_help]
        if len(bk) == 0: continue
        hs = ','.join(str(x) for x in bk)
        print hs
        sendHelp(f, hs)
    
