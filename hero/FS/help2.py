import binascii
import sys
import json
import datetime
import time
import random
import requests
from common import *
from buildInfo import *
service = ''
method = ''
game_version = getGameVersion()

flist = ["329190","2426488","4125379","4265183","4509838","5082962","5915645","11796750","15302521","17776767","20461833","23661798","32658681","36257998","36535035","38620902","39057925","39721922","39913577","40952738","41064410","41122706","41991450","42060268","42392799","43465163","43539460","44378967","46816137","50746419","53912829","55006117","62810212","65357737","68219862","68643636","68667021","71187603","71859984","72012183","73008830","73234077","73453170","73707564","74303058","74895385","74990087","74990161","74990385","74991442","75367792","76312315","76876470","77191158","79819505","82413437","83259333","3091478"]


person = 0
error = 0

persons = [
              {"pid":"3091478","auth":"7fb9f07a0c6156483701f8b24b79696a","gid":0,"sid":""},#corc
          ]

pid = persons[person]["pid"]
auth = persons[person]["auth"]
gid = 0
sid = ''
data = ''
actionCommand = 'Knights.doAction'

init_log("help_priority")

    
ctr = 0
def getCTR():
    global ctr
    ctr += 1
    return str(ctr)
    
def getWorld(pers):
    global sid, gid, service, method
    service = actionCommand
    method = 'friendsGetWorld'
    init_params(nsid=sid, ngid=gid, nservice=service, nmethod=method)
    dataString = '{"v":"%s","friendId":"%s","ctr":%s,"sessionKey":"%s","method":"%s"}' % (game_version, pers, getCTR(), sid, method)
    params = createData(method, dataString)
    #log("%s:%s %s" % (service, method, json.dumps(params)))
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
    init_params(nsid=sid, ngid=gid, nservice=service, nmethod=method)
    dataString = '{"friendId":"%s","list":[%s],"v":"%s","ctr":%s,"sessionKey":"%s","method":"%s"}' % (pers, hbid, game_version, getCTR(), sid, method)
    params = createData(method, dataString)
    #log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("friendHelpApply done", True)
    else:
        log(resp["data"], True)        


no_help = []
nohf = ''
pers = persons[person]
pid = pers['pid']
auth = pers['auth']
gid =  pers['gid']
sid =  pers['sid']
    
    
data, gid, sid = init(pid, auth)
print "1 friends count:", len(flist)
if data.has_key("clan") and data["clan"].has_key("roster"):
    orden = data["clan"]["roster"]
    for p in orden:
        if p in flist: continue
        flist = flist +[p]
print "2 friends count:", len(flist)

while len(flist)>0:        

    total = len(flist)
    i = 0
    left_arr = []
    while i<total:
        if len(nohf)>1: no_help = no_help + [nohf]; print "add to NO HELP arr"
        nohf = ''
        max_help = 5
        f = str(flist[i])
        nohf = f
        i += 1
        print "%d/%d (%d%%)" % (i, total, int(100*i/total))
        try: w = getWorld(f)
        except: continue
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
        if max_help>len(bk): left_arr = left_arr+[f]; print "add to left arr"
        sendHelp(f, hs)
        nohf = ''
            
    log('left_arr')
    log(','.join(str(x) for x in left_arr))
    flist = left_arr
    
if len(nohf)>1: no_help = no_help + [nohf]
for f in no_help:
    sendHelp(f, '1,2,3,4,5')
