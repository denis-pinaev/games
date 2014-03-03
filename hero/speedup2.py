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

from common import *

person = 0#old!
persons = [
              {"pid":"124520","auth":"1e365d477c3207804013abaddbb6a0c4","gid":0,"sid":""},#corc
          ]
          
pid = persons[person]["pid"]
auth = persons[person]["auth"]

gid = 0
sid = ''
data = ''
actionCommand = 'Knights.doAction'
init_log("hero_help2_log")
ctr = int(random.random()*10000)
def getCTR():
    global ctr
    ctr += 1
    return str(ctr)
 
def getHelpSpeed(hbid):
    global sid, gid, service, method
    service = actionCommand
    method = 'recipeFinish'
    init_params(nsid=sid, ngid=gid, nservice=service, nmethod=method)
    #data	{"count":33,"type":"entities","method":"recipeFinish","index":"65540"}
    dataString = '{"count":5,"type":"entities","method":"recipeFinish","index":"%s","rnd":%s,"ctr":%s,"sessionKey":"%s"}' % (hbid, getRandom(), getCTR(), sid)
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
sendSTR = ['67002']

data, gid, sid = init(pid, auth)
getHelpSpeeds(sendSTR)        
