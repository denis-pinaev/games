import sys
import json
import datetime
import time

from common import *

print auth

person = 1
person_id = '124520'

if len(sys.argv) > 1:
    person_id = sys.argv[1]
if len(sys.argv) > 2:
    person = int(sys.argv[2])
    
persons = [
              {"pid":"124520","auth":"1e365d477c3207804013abaddbb6a0c4","gid":0,"sid":""},#corc
              {"pid":"102137300","auth":"e78c0aad90f427b06653067a45de6c6b","gid":0,"sid":""},#corcc
              {"pid":"160511757","auth":"6dc2dba90c1cc9d935542aa6a60c6fb4","gid":0,"sid":""},#vasya tanakan
              {"pid":"","auth":"","gid":0,"sid":""},#nononon
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










data, gid, sid = init(pid, auth)
f = getWorld(person_id)

print f["friend"]["player"]
print_user_info(get_buildings_extend(f["friend"]["entities"]))
bbb = get_buildings_ids(f["friend"]["entities"])
print get_help_string(f["friend"]["recipes"]["entities"],bbb,5)[:5]