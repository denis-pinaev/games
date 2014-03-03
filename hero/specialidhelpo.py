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
              {"pid":"144536559","auth":"731331d4e19d1f5483acd67abf424b58","gid":0,"sid":""},#polya
              {"pid":"107402663","auth":"81ac464a55f116dcd1c0441c4e11cb49","gid":0,"sid":""},#alex black
              {"pid":"155908147","auth":"38e6c4c6f1a3ca43a78a6c499879ba7e","gid":0,"sid":""},#margo
              {"pid":"156721888","auth":"fd0f8ffff11ba378e7bdae6a64e2bb1b","gid":0,"sid":""},#podolskaya irina
              {"pid":"108534050","auth":"be89b8b65bf6faea7d8a1a679f9b05db","gid":0,"sid":""},#vlad
              {"pid":"120865611","auth":"ae8affc607866e40cd1f1b312bb69fda","gid":0,"sid":""},#elina-zp
              {"pid":"151977002","auth":"8fd177f25f5bd712eec60421deab2899","gid":0,"sid":""},#anna-maria
              {"pid":"329928","auth":"3537936f4b228959fa759ce2508574fd","gid":0,"sid":""},#sveta
              {"pid":"102137300","auth":"e78c0aad90f427b06653067a45de6c6b","gid":0,"sid":""},#corcc
              {"pid":"47654405","auth":"8868f86742f95fe034b6b04da48f5ac4","gid":0,"sid":""},#tregub
              {"pid":"160511757","auth":"6dc2dba90c1cc9d935542aa6a60c6fb4","gid":0,"sid":""},#vasya tanakan
              {"pid":"163834109","auth":"36a870e45af6041189b3e6905945d6e7","gid":0,"sid":""},#bot1
              {"pid":"153969376","auth":"9707e9bc5f45e2bd45d5d73dfbb768db","gid":0,"sid":""},#bot1
              {"pid":"84324359","auth":"b61b0e2d2757946edcca304e6bdc853b","gid":0,"sid":""},#bot1
              {"pid":"173550501","auth":"5ca7913de53548ac794d541672ce9e8b","gid":0,"sid":""},#bot1
              {"pid":"34688001","auth":"fc8c2f798036ef2af8bbd6fbc312f7fb","gid":0,"sid":""},#bot1
              {"pid":"218661879","auth":"4a7a2ac0efcadd1a42499e34ed217e8b","gid":0,"sid":""},#nikita
              {"pid":"124520","auth":"1e365d477c3207804013abaddbb6a0c4","gid":0,"sid":""},#corc
              {"pid":"233828632","auth":"3cf7aac00f56163404482ed0550eb1dc","gid":0,"sid":""},#misha_zhukov7
              {"pid":"101053386","auth":"77a9e62eed9e7d25866efd2c8aeef30e","gid":0,"sid":""},#misha_zhukov6
              {"pid":"124678851","auth":"f659c32017ecad7b4d36b862f68351ef","gid":0,"sid":""},#misha_zhukov5
              {"pid":"182933786","auth":"662b4add4856bc946f65e70d9254c862","gid":0,"sid":""},#misha_zhukov4
              {"pid":"209559126","auth":"02e68b3110fbeac985c6846649e3cee2","gid":0,"sid":""},#misha_zhukov3
              {"pid":"200139667","auth":"0be685ed1b3787bc144ef88cf0d2de1d","gid":0,"sid":""},#misha_zhukov2
              {"pid":"199648989","auth":"14279d90af4c929b3f645e777e6b30fb","gid":0,"sid":""},#misha_zhukov1
              {"pid":"49809104","auth":"faeaec9d6c41db027a1f8a2dc7244c38","gid":0,"sid":""},#misha_zhukov
              {"pid":"56518190","auth":"22f411e60eebd913b689b19705900ab2","gid":0,"sid":""},#ulia
              {"pid":"93902559","auth":"d40ce5e63d99e92fd57859c7be81729c","gid":0,"sid":""},#vadimbot0
              {"pid":"217858589","auth":"8b9107a32674785b79463d5585ec4918","gid":0,"sid":""},#vadimbot1
              {"pid":"65706308","auth":"a889a08c37aa0430b62ae6a5928e6950","gid":0,"sid":""},#vadimbot2
              {"pid":"217752865","auth":"bc8251178d92e9f671d7f23f19fbb4a7","gid":0,"sid":""},#vadimbot3
              {"pid":"107564843","auth":"81af0508db36b84e869e2b77a9b4a142","gid":0,"sid":""},#vadimbot4
              {"pid":"107738176","auth":"3194740fd9573509f0d3c523be6e4541","gid":0,"sid":""},#vadimbot5
              {"pid":"6432236","auth":"f51966179add0bc14b234ca5d7de9211","gid":0,"sid":""},#KUUSAMO
              {"pid":"29431585","auth":"55f56ea187574da9b2ed69474db78ac0","gid":0,"sid":""}#natali vlasova
              
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
    txt = resp.text.split('!',1)[1].encode('utf-8')
    first = txt.find("adInfo")
    if first > 0:
        second = txt.find('}', first)
        txt = txt[:first]+"a\":\"0"+txt[second+1:]
    txt = txt.replace('"a":"0,"', '"a":"0"},"')
    
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
persons = persons[10:]

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
    
