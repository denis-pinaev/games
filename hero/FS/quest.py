import sys
import json
import datetime
import time

from common import *

print auth

person = 2
quest_id = '302'

if len(sys.argv) > 1:
    person = int(sys.argv[1])
else:
    raise Exception("#corc0 #vadimbot1 #polya2 #natali_vlasova3 #misha_zhukov4 #nikita5 #yura6 #lenaSv7 #VitaShani8 #mari kremer9")
    
persons = [
              {"pid":"3091478","auth":"7fb9f07a0c6156483701f8b24b79696a","gid":0,"sid":""},#corc
          ]
pid = persons[person]["pid"]
auth = persons[person]["auth"]

init_log("saveQuests")
ctr = int(random.random()*10000)
def getCTR():
    global ctr
    ctr += 1
    return str(ctr)

def saveQuest(q, restq):
    global sid, gid, service, method
    service = actionCommand
    method = 'saveQuests'
    init_params(nsid=sid, ngid=gid, nservice=service, nmethod=method)
    #{"active":{"302":null},"method":"saveQuests","ctr":42,"order":[303,269],"stat":{"exercises":[[302,0]]},"completed":{"302":1},"resources":{},"sessionKey":"535189188e4867.19491091"}
    
    dataString = '{"active":{"%s":null},"ctr":%s,"sessionKey":"%s","method":"%s","order":[%s],"stat":{"exercises":[[%s,0]]},"completed":{"%s":1},"resources":{}}' % (q,getCTR(),sid,method,restq,q,q)
    #dataString = '{"rnd":%s,"friendId":"%s","ctr":%s,"sessionKey":"%s","method":"%s"}' % (getRandom(), pers, getCTR(), sid, method)
    #print dataString
    #time.sleep(999)
    params = createData(method, dataString)
    #log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("saveQuests %s done" % q, True)
    else:
        log(resp["data"], True)
    return o

#for ddd in range(99):
if True:
    data, gid, sid = init(pid, auth)

    try:
        q_ar = []
        for q in data['quests']['active']:
            q_ar.append(q)
        
        while len(q_ar)>0:
        #if True:
            q = q_ar.pop()
            saveQuest(q, ','.join(q_ar))
    except: print 'no quests'
#    time.sleep(30)