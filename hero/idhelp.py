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


flist = ["144536559", "9894033", "106358745", "49809104"]


person = 0#old!
error = 0
start_p = 0
end_p = 999
person_id = ''
sendSTR = ''
needCorC = True
if len(sys.argv) > 2:
    sendSTR = sys.argv[2]
    person_id = sys.argv[1]
elif len(sys.argv) > 1:
    needCorC = False
    ss = sys.argv[1]
    ss = ss.replace(':[','JOPA',1)
    ss = ss.replace(':','":"',10)
    ss = ss.replace(',','","',10)
    ss = ss.replace('{','{"',1)
    ss = ss.replace(']}','"]}',1)
    ss = ss.replace('JOPA','":["',1)
    inobj = json.loads(ss)
    if inobj.has_key('friendId') and inobj.has_key('list'):
        person_id = str(inobj['friendId'])
        sendSTR = ','.join(str(x) for x in inobj['list'])
        print person_id, sendSTR


persons = [
              {"pid":"124520","auth":"1e365d477c3207804013abaddbb6a0c4","gid":0,"sid":""},#corc
              {"pid":"102137300","auth":"e78c0aad90f427b06653067a45de6c6b","gid":0,"sid":""},#corcc
              {"pid":"160511757","auth":"6dc2dba90c1cc9d935542aa6a60c6fb4","gid":0,"sid":""},#vasya tanakan
              #{"pid":"","auth":"","gid":0,"sid":""},#nononon
              {"pid":"155908147","auth":"38e6c4c6f1a3ca43a78a6c499879ba7e","gid":0,"sid":""}#margo
              
          ]
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
    fatype = "hero_help2_log"
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
    
    
    #tfile = open('fuck', "w")
    #tfile.write(txt)
    #tfile.close()
    
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
    if auth == "" : resp["data"] = resp["data"][:-1]
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
#'65555'#natars
flist = [person_id]
person = 0
#if len(sendSTR)<1: sendSTR = '83'

if True:
    i = 0 if needCorC else 1
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
        
        if w.has_key("friend"):
            
            if w["friend"].has_key("currentBuildingHelp"): continue
            if w["friend"].has_key("recipes") and len(w["friend"]["recipes"])>0 and w["friend"]["recipes"].has_key("entities"):
                bk = w["friend"]["recipes"]["entities"]
                if len(bk)>0:
                    kset = bk.keys()
                    for k in kset:
                        if bk[k].has_key("ready"): del bk[k]
                if len(bk)<1: continue
                try:
                    bk = sorted(bk, key=lambda x : bk[x]['start'], reverse=True)[:5]
                    hs = ','.join(str(x) for x in bk)
                    sendHelp(f, hs)
                except:
                    print w["friend"]["recipes"]["entities"]
                    i = total
    
