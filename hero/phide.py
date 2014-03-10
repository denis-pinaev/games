import sys
import json
import datetime
import time

from common import *

print auth

person = 2
hide = True

if len(sys.argv) > 1:
    person = int(sys.argv[1])
if len(sys.argv) > 2:
    hide = False
    
persons = [
              {"pid":"124520","auth":"1e365d477c3207804013abaddbb6a0c4","gid":0,"sid":""},#corc
              {"pid":"102137300","auth":"e78c0aad90f427b06653067a45de6c6b","gid":0,"sid":""},#corcc
              {"pid":"160511757","auth":"6dc2dba90c1cc9d935542aa6a60c6fb4","gid":0,"sid":""},#vasya tanakan
              {"pid":"155908147","auth":"38e6c4c6f1a3ca43a78a6c499879ba7e","gid":0,"sid":""}#margo
              
          ]
pid = persons[person]["pid"]
auth = persons[person]["auth"]

init_log("playerinfo")
ctr = int(random.random()*10000)
def getCTR():
    global ctr
    ctr += 1
    return str(ctr)

def moveBuilding(bid, x, y, d):
    global sid, gid, service, method
    service = actionCommand
    method = 'entityMove'
    init_params(nsid=sid, ngid=gid, nservice=service, nmethod=method)
    dataString = '{"x":%d,"y":%d,"dir":%d,"sceneId":%s,"rnd":%s,"ctr":%s,"sessionKey":"%s","method":"%s"}' % (x, y, d, bid, getRandom(), getCTR(), sid, method)
    params = createData(method, dataString)
    log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("move done %d:%d dir:%d for %s" % (x, y, d, bid), True)
    else:
        log(resp["data"], True)

def getWorld(pers):
    global sid, gid, service, method
    service = actionCommand
    method = 'friendsGetWorld'
    init_params(nsid=sid, ngid=gid, nservice=service, nmethod=method)
    dataString = '{"rnd":%s,"friendId":"%s","ctr":%s,"sessionKey":"%s","method":"%s"}' % (getRandom(), pers, getCTR(), sid, method)
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
    
def readFile(logFile):
    tfile = open(logFile, "r")
    lines = tfile.read()
    tfile.close()
    lines = lines.split('\n')
    papa = {}
    for line in lines:
        linea = line.split()
        if len(linea)<5: continue
        o = {'sceneId':linea[2],'x':float(linea[3]),'y':float(linea[4]),'dir':float(linea[5])}
        if o['dir']>8: o['dir'] = 0
        papa[linea[2]] = o
    return papa








d = 9
x = 36
y = 18
if not hide:
    logdata = readFile('old_dirs_'+pid)
    
    
data, gid, sid = init(pid, auth)
for e in data['entities']:
    ent = data['entities'][e]
    if ent.has_key('dir') and ent.has_key('x') and ent.has_key('y') and ent.has_key('sceneId'):
        if hide:
            if ent['x']!=36: log(e+' '+str(ent['x'])+' '+str(ent['y'])+' '+str(ent['dir']), False, 'old_dirs_'+pid)
            if ent['x']!=36: moveBuilding(e,x,y,d)#ent['dir'])
        else:
            if logdata.has_key(e):
                moveBuilding(e,logdata[e]['x'],logdata[e]['y'],logdata[e]['dir'])
    else: print 'strange sid = '+str(e)
        
    