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


person = 3
error = 0
total = 1

if len(sys.argv) > 1:
    total = int(sys.argv[1])


persons = [
              {"pid":"124520","auth":"1e365d477c3207804013abaddbb6a0c4","gid":0,"sid":""},#corc
              {"pid":"102137300","auth":"e78c0aad90f427b06653067a45de6c6b","gid":0,"sid":""},#corcc
              {"pid":"155908147","auth":"38e6c4c6f1a3ca43a78a6c499879ba7e","gid":0,"sid":""},#margo
              {"pid":"160511757","auth":"6dc2dba90c1cc9d935542aa6a60c6fb4","gid":0,"sid":""},#vasya tanakan
              {"pid":"","auth":"","gid":0,"sid":""},#nononon
              {"pid":"144536559","auth":"731331d4e19d1f5483acd67abf424b58","gid":0,"sid":""},#polya
              {"pid":"47654405","auth":"8868f86742f95fe034b6b04da48f5ac4","gid":0,"sid":""},#tregub
              {"pid":"107402663","auth":"81ac464a55f116dcd1c0441c4e11cb49","gid":0,"sid":""},#alex black
              {"pid":"156721888","auth":"fd0f8ffff11ba378e7bdae6a64e2bb1b","gid":0,"sid":""},#podolskaya irina
              {"pid":"108534050","auth":"be89b8b65bf6faea7d8a1a679f9b05db","gid":0,"sid":""},#vlad
              {"pid":"120865611","auth":"ae8affc607866e40cd1f1b312bb69fda","gid":0,"sid":""},#elina-zp
              {"pid":"151977002","auth":"8fd177f25f5bd712eec60421deab2899","gid":0,"sid":""},#anna-maria
              {"pid":"329928","auth":"3537936f4b228959fa759ce2508574fd","gid":0,"sid":""},#sveta
              {"pid":"218661879","auth":"4a7a2ac0efcadd1a42499e34ed217e8b","gid":0,"sid":""}#nikita
              
          ]

pid = persons[person]["pid"]
auth = persons[person]["auth"]
gid = 0
sid = ''
data = ''
actionCommand = 'Knights.doAction'
batchCommand = 'Knights.doBatchAction'
action = 'hp'
    
def getRandom():
    return str(int(random.random()*1000))
    
def log(s, pr=False):
    s = "[" + datetime.datetime.now().strftime('%d.%m %H:%M:%S')+"] " + s
    if pr: print s
    fatype = "hero_speedup_log"
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
    txtar = resp.text.split('!')
    txtar[0] = ''
    txt = "!".join(str(x) for x in txtar)[1:]
    #txt = resp.text.split('!')[1].encode('utf-8')
    first = txt.find("adInfo")
    if first > 0:
        second = txt.find('}', first)
        txt = txt[:first]+"a\":\"0"+txt[second+1:]
    #if txt.find("news")>0:
    #    txt = txt[:txt.find("news")-2]+'}}'
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
        
def sendHelpSpeed(hbids):
    global sid, gid, service, method
    service = batchCommand
    method = 'recipeSpeedupHelp'
    #dataString = '{"friendId":"%s","list":[%s],"rnd":%s,"auth_key":"%s","sid":"%s","method":"%s"}' % (pers, hbid, getRandom(), auth, sid, method)
    #dataString = '{"type":"entities","index":"%s","rnd":%s,"auth_key":"%s","sid":"%s","method":"%s"}' % (hbid, getRandom(), auth, sid, method)
    blist = []
    j = 0
    for hbid in hbids:
        blist = blist + ['"%d":{"method":"recipeSpeedupHelp","index":"%s","type":"entities"}'%(j,str(hbid))]
        j = j + 1
    blists = ",".join(str(x) for x in blist)
    dataString = '{"rnd":%s,"batchlist":{%s},"auth_key":"%s","sid":"%s"}' % (getRandom(), blists, auth, sid)
    params = createData(method, dataString)
    log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("recipeSpeedupHelp done "+hbid, True)
    else:
        log(resp["data"], True)        

def getHelpSpeed(hbid):
    global sid, gid, service, method
    service = actionCommand
    method = 'recipeFinish'
    #data	{"count":33,"type":"entities","method":"recipeFinish","index":"65540"}
    dataString = '{"count":5,"type":"entities","method":"recipeFinish","index":"%s","rnd":%s,"auth_key":"%s","sid":"%s"}' % (hbid, getRandom(), auth, sid)
    params = createData(method, dataString)
    log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("recipeFinish done "+hbid, True)
    else:
        log(resp["data"], True)        

def getHelpSpeeds(hbids):
    for hbid in hbids:
        getHelpSpeed(str(hbid))



'''
67002 - elka
ars:
   65570 x=14,y=-1
hram:
   83 x=2,y=10
altar:
   103 x=2,y=6
runa:
   66765 x=18,y=-4
main:
   828 x=8,y=-10
gnom:
   66766 x=9,y=-6
plav:
   65651 x=12,y=-12
   65652 x=12,y=-8
   65596 x=12,y=-10
   '65651','65596','65652'
kuzn:
   65653 x=12,y=-15
   65571 x=6,y=-15
   65588 x=9,y=-15
   65635 x=3,y=-15
   '65635','65571','65588','65653'
rist:
   66752 x=27,y=-16
wood:
   66751 x=36,y=18
stone:
   65554 x=36,y=18
iron:
   65562 x=36,y=18
sklad:
   66541 x=36,y=18
   65593 x=3,y=-12
   65569 x=3,y=-9
   65616 x=6,y=-6
gold:
   66750 x=3,y=-6
'''
#CorC
pid = "124520"
auth = "1e365d477c3207804013abaddbb6a0c4"
gid =  999038
sid =  "77275"
#           wood    iron    stone   gold    stone2  iron2         3plavi             ars
#sendSTR = ['66751','65562','65554','66750','66912','66913','65652','65596','65651','65570']
sendSTR = ['65570']

#

if len(sys.argv) > 2:
    sendSTR = [sys.argv[2]]

if True:
    
    #init()

    i = 0
    cnt = 0
    while i<total:
        sendHelpSpeed(sendSTR)
        #getHelpSpeeds(sendSTR)
        i = i + 1
        cnt = cnt + len(sendSTR)
        print cnt
        
