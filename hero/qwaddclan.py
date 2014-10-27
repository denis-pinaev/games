import sys
import json
import datetime
import time

from common import *

print auth

person = 11
quest_id = '302'

if len(sys.argv) > 1:
    person = int(sys.argv[2])
if len(sys.argv) > 2:
    person = int(sys.argv[2])
    
persons = [
              {"pid":"124520","auth":"1e365d477c3207804013abaddbb6a0c4","gid":0,"sid":""},#corc0
              {"pid":"217858589","auth":"8b9107a32674785b79463d5585ec4918","gid":0,"sid":""},#vadimbot1
              {"pid":"144536559","auth":"731331d4e19d1f5483acd67abf424b58","gid":0,"sid":""},#polya2
              {"pid":"29431585","auth":"55f56ea187574da9b2ed69474db78ac0","gid":0,"sid":""},#natali_vlasova3
              {"pid":"49809104","auth":"faeaec9d6c41db027a1f8a2dc7244c38","gid":0,"sid":""},#misha_zhukov4
              {"pid":"218661879","auth":"4a7a2ac0efcadd1a42499e34ed217e8b","gid":0,"sid":""},#nikita5
              {"pid":"179499220","auth":"49e1540eb72f701a7c0924054ef10fc1","gid":0,"sid":""},#yura6
              {"pid":"169768611","auth":"9bc9bdd4929458a2108f1ae419906f66","gid":0,"sid":""},#lenaSv7
              {"pid":"73940623","auth":"9ba0d48c2a9b701ffa031504b5232451","gid":0,"sid":""},#VitaShani8
              {"pid":"161702967","auth":"a5738509fb8e7486b45e8ba01436c6bb","gid":0,"sid":""},#mari kremer9
              {"pid":"68487257","auth":"4f66fe9422f3b5f17ab1e90ce34a42d3","gid":0,"sid":""},#Nagaina 10
              {"pid":"202787673","auth":"03bda5b072c520d2fc767c708979ad00","gid":0,"sid":""},#DimaUsmar 11
              
          ]
pid = persons[person]["pid"]
auth = persons[person]["auth"]

init_log("saveQuests")
ctr = int(random.random()*10000)
def getCTR():
    global ctr
    ctr += 1
    return str(ctr)

def addUser():
    global sid, gid, service, method
    service = 'Knights.doClanAction'
    method = 'addUserApplication'
    
    init_params(nsid=sid, ngid=gid, nservice=service, nmethod=method)
    
    dataString = '{"message":"1","clan":11,"ctr":%s,"sessionKey":"%s","method":"%s"}' % (getCTR(),sid,method)
    params = createData(method, dataString)
    log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("%s %s done" % (method, q), True)
    else:
        log(resp["data"], True)
    return o

def getUser():
    global sid, gid, service, method
    service = 'Knights.doClanAction'
    method = 'getUserApplications'
    
    init_params(nsid=sid, ngid=gid, nservice=service, nmethod=method)
    
    dataString = '{"message":"1","clan":11,"ctr":%s,"sessionKey":"%s","method":"%s"}' % (getCTR(),sid,method)
    params = createData(method, dataString)
    log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("%s %s done" % (method, q), True)
    else:
        log(resp["data"], True)
    return o

def cancelUser():
    global sid, gid, service, method
    service = 'Knights.doClanAction'
    method = 'cancelUserApplication'
    
    init_params(nsid=sid, ngid=gid, nservice=service, nmethod=method)
    
    dataString = '{"message":"1","id":304109,"ctr":%s,"sessionKey":"%s","method":"%s"}' % (getCTR(),sid,method)
    params = createData(method, dataString)
    log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("%s %s done" % (method, q), True)
    else:
        log(resp["data"], True)
    return o


data, gid, sid = init(pid, auth)

try:
    addUser()
except: print 'no quests'