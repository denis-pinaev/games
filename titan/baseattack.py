# -*- coding: utf-8 -*-

import binascii
import pyamf
import sys
import json
import datetime
import time
import random
import requests
import urllib
import base64
import zlib
import hashlib

#               CorC      VladKsu      EErem     Mrachnii       Yarik    Kulich
exceptions = ['124520', '217858589', '132632', '186282895', '6514823', '221870455']

def log(s, pr=True, filename="attacks", needTime=True):
    if needTime:
        s = "[" + datetime.datetime.now().strftime('%d.%m %H:%M:%S')+"] " + s
    if pr: print s
    fatype = filename
    try:
        tfile = open(fatype, "a")
        tfile.write(s.encode('utf-8')+'\n')
        tfile.close()
    except:
        tfile = open(fatype, "w")
        tfile.write(s.encode('utf-8')+'\n')
        tfile.close()

def getRandom():
    s = ''
    for i in range(9):
        c = str(int(random.random()*9)+1)
        s+=str(c)
    return s
    
def getTime():
    return str(int(time.time()))

def sendRequest(params):
    url = 'http://tt-vk-sc.playkot.com/current/server.php?'
    ppp = urllib.urlencode(params)
    url+=ppp
    resp = requests.get(url)
    txt = resp.text
    return txt
    
    
unit_type = 15
unit_hp = 5700
    
resultBase = {
  "enemy": {
    "buildings": []
  },
  "f2": 0,
  "f1": 4696722.395209581,
  "ts": 1414766004,
  "units": [
    {
      "typeId": unit_type,
      "capacity": 13000,
      "level": 0,
      "arm": [
        {
          "id": 0,
          "level": 4
        },
        {
          "id": 1,
          "level": 4
        },
        {
          "id": 2,
          "level": 4
        }
      ],
      "bonus_hp": [
        {
          "id": 3,
          "level": 4
        },
        {
          "id": 3,
          "level": 4
        },
        {
          "id": 3,
          "level": 4
        }
      ],
      "health": unit_hp,
      "wp": [
        {
          "id": 8,
          "level": 4
        },
        {
          "id": 8,
          "level": 4
        },
        {
          "id": 8,
          "level": 4
        },
        {
          "id": 8,
          "level": 4
        },
        {
          "id": 8,
          "level": 4
        }
      ],
      "spec": [
        {
          "id": 0,
          "level": 4
        },
        {
          "id": 0,
          "level": 4
        },
        {
          "id": 0,
          "level": 4
        },
        {
          "id": 0,
          "level": 4
        },
        {
          "id": 0,
          "level": 4
        }
      ],
      "y": 22,
      "x": 10,
      "id": 0
    },
    
    {
      "typeId": unit_type,
      "capacity": 93000,
      "level": 0,
      "arm": [
        {
          "id": 0,
          "level": 4
        },
        {
          "id": 1,
          "level": 4
        },
        {
          "id": 2,
          "level": 4
        }
      ],
      "bonus_hp": [
        {
          "id": 3,
          "level": 4
        },
        {
          "id": 3,
          "level": 4
        },
        {
          "id": 3,
          "level": 4
        }
      ],
      "health": unit_hp,
      "wp": [
        {
          "id": 8,
          "level": 4
        },
        {
          "id": 8,
          "level": 4
        },
        {
          "id": 8,
          "level": 4
        },
        {
          "id": 8,
          "level": 4
        },
        {
          "id": 8,
          "level": 4
        }
      ],
      "spec": [
        {
          "id": 0,
          "level": 4
        },
        {
          "id": 0,
          "level": 4
        },
        {
          "id": 0,
          "level": 4
        },
        {
          "id": 0,
          "level": 4
        },
        {
          "id": 0,
          "level": 4
        }
      ],
      "y": 23,
      "x": 8,
      "id": 1
    },
    {
      "typeId": unit_type,
      "capacity": 93000,
      "level": 0,
      "arm": [
        {
          "id": 0,
          "level": 4
        },
        {
          "id": 1,
          "level": 4
        },
        {
          "id": 2,
          "level": 4
        }
      ],
      "bonus_hp": [
        {
          "id": 3,
          "level": 4
        },
        {
          "id": 3,
          "level": 4
        },
        {
          "id": 3,
          "level": 4
        }
      ],
      "health": unit_hp,
      "wp": [
        {
          "id": 8,
          "level": 4
        },
        {
          "id": 8,
          "level": 4
        },
        {
          "id": 8,
          "level": 4
        },
        {
          "id": 8,
          "level": 4
        },
        {
          "id": 8,
          "level": 4
        }
      ],
      "spec": [
        {
          "id": 0,
          "level": 4
        },
        {
          "id": 0,
          "level": 4
        },
        {
          "id": 0,
          "level": 4
        },
        {
          "id": 0,
          "level": 4
        },
        {
          "id": 0,
          "level": 4
        }
      ],
      "y": 23,
      "x": 12,
      "id": 2
    },
    {
      "typeId": unit_type,
      "capacity": 93000,
      "level": 0,
      "arm": [
        {
          "id": 0,
          "level": 4
        },
        {
          "id": 1,
          "level": 4
        },
        {
          "id": 2,
          "level": 4
        }
      ],
      "bonus_hp": [
        {
          "id": 3,
          "level": 4
        },
        {
          "id": 3,
          "level": 4
        },
        {
          "id": 3,
          "level": 4
        }
      ],
      "health": unit_hp,
      "wp": [
        {
          "id": 8,
          "level": 4
        },
        {
          "id": 8,
          "level": 4
        },
        {
          "id": 8,
          "level": 4
        },
        {
          "id": 8,
          "level": 4
        },
        {
          "id": 8,
          "level": 4
        }
      ],
      "spec": [
        {
          "id": 0,
          "level": 4
        },
        {
          "id": 0,
          "level": 4
        },
        {
          "id": 0,
          "level": 4
        },
        {
          "id": 0,
          "level": 4
        },
        {
          "id": 0,
          "level": 4
        }
      ],
      "x": 6,
      "y": 24,
      "id": 3
    },
    {
      "typeId": unit_type,
      "capacity": 93000,
      "level": 0,
      "arm": [
        {
          "id": 0,
          "level": 4
        },
        {
          "id": 1,
          "level": 4
        },
        {
          "id": 2,
          "level": 4
        }
      ],
      "bonus_hp": [
        {
          "id": 3,
          "level": 4
        },
        {
          "id": 3,
          "level": 4
        },
        {
          "id": 3,
          "level": 4
        }
      ],
      "health": unit_hp,
      "wp": [
        {
          "id": 8,
          "level": 4
        },
        {
          "id": 8,
          "level": 4
        },
        {
          "id": 8,
          "level": 4
        },
        {
          "id": 8,
          "level": 4
        },
        {
          "id": 8,
          "level": 4
        }
      ],
      "spec": [
        {
          "id": 0,
          "level": 4
        },
        {
          "id": 0,
          "level": 4
        },
        {
          "id": 0,
          "level": 4
        },
        {
          "id": 0,
          "level": 4
        },
        {
          "id": 0,
          "level": 4
        }
      ],
      "x": 10,
      "y": 24,
      "id": 4
    },
    {
      "typeId": unit_type,
      "capacity": 93000,
      "level": 0,
      "arm": [
        {
          "id": 0,
          "level": 4
        },
        {
          "id": 1,
          "level": 4
        },
        {
          "id": 2,
          "level": 4
        }
      ],
      "bonus_hp": [
        {
          "id": 3,
          "level": 4
        },
        {
          "id": 3,
          "level": 4
        },
        {
          "id": 3,
          "level": 4
        }
      ],
      "health": unit_hp,
      "wp": [
        {
          "id": 8,
          "level": 4
        },
        {
          "id": 8,
          "level": 4
        },
        {
          "id": 8,
          "level": 4
        },
        {
          "id": 8,
          "level": 4
        },
        {
          "id": 8,
          "level": 4
        }
      ],
      "spec": [
        {
          "id": 0,
          "level": 4
        },
        {
          "id": 0,
          "level": 4
        },
        {
          "id": 0,
          "level": 4
        },
        {
          "id": 0,
          "level": 4
        },
        {
          "id": 0,
          "level": 4
        }
      ],
      "x": 14,
      "y": 24,
      "id": 5
    }
  ],
  "id": 0
}


def decode(s):
    s = base64.decodestring(s)
    s = zlib.decompress(s)
    return s
    
def encode(s):
    s = zlib.compress(s)
    s = base64.encodestring(s)
    return s
    
def getMap():
    request = {
        "request":"getUserMap"
    }
        
    resp_txt = sendRequest(genReq(request))
    try:
        resp = json.loads(resp_txt)
        if resp.has_key("result") and resp["result"] == "ok":
            print "Map loaded"
            return resp["userMap"]
        else:
            print resp_txt
    except:
        print "Load JSON Error: "+resp_txt
        
    return None;
    
def loadBase(p):
    request = {
        "id":p['userId'],
        "squad_id":squad_id,
        "request":"loadBase"
        }
        
    resp_txt = sendRequest(genReq(request))
    try:
        resp = json.loads(resp_txt)
        if resp.has_key("result") and resp["result"] == "ok":
            log("Base loaded "+str(p['userId']))
            return resp['base']
        else:
            print resp_txt
    except:
        print "Load JSON Error: "+resp_txt
        
    return None;
    
def attackBase(base):
    request = {
        "params":{
            "state": 3,
            "id": squad_id,
            "ts": getTime(),
            "trgUser": base
        },
        "request":"startBattleVsBase"
        }
        
    request["params"] = encode(json.dumps(request["params"]))
    resp_txt = sendRequest(genReq(request))
    try:
        resp = json.loads(resp_txt)
        if resp.has_key("result") and resp["result"] == "ok":
            print "startBattleVsBase: "+str(base)
            return resp
        else:
            print resp_txt
    except:
        print "Load JSON Error: "+resp_txt
        
    return None

def resultBaseFight(builds):

    resultBase['ts'] = getTime()
    resultBase['enemy']['buildings'] = builds
    
    request = {
        "params":resultBase,
        "request":"battleResults"
        }
        
    
    request["params"] = encode(json.dumps(request["params"]))
    resp_txt = sendRequest(genReq(request))
    try:
        resp = json.loads(resp_txt)
        if resp.has_key("result") and resp["result"] == "ok":
            print "battle done!"
            return resp
        else:
            print resp_txt
    except:
        print "Load JSON Error: "+resp_txt
        
    return None
def killBase(base):
    res = []
    if base.has_key("buildings"):
        for b in base["buildings"]:
            if int(b['typeId']) != 12:
                res.append({'id':b['id'],'health':0})
    return res
    
def enemyToString(p, first=True, pos="0"):
            s = "["+pos+"] "
            if len(pos)<2: s+=" "
            s += str(p['userId'])
            while len(s)<15: s+=" "
            if p.has_key('firstName'):
                if first:
                    s+=p['firstName']+u" "+p['lastName']
                else:
                    s+=u"STRANGE NAME"
                while len(s)<40: s+=" "
            if p.has_key('level'):
                s+=u"level:"+str(p['level'])
                while len(s)<50: s+=" "
            if p.has_key('rating'):
                s+=u"\tRate:"+str(p['rating'])
            return s
            
def printEnemyToString(p, pos="0"):
    try:
        print enemyToString(p, True, str(pos))
    except:
        print enemyToString(p, False, str(pos))
    
    
def getEnemy(m):
    global enemyId
    min_lvl = 999
    enemy = None
    enemy_pos = 0
    ai = 0
    for p in m:
        if p.has_key('userId'):
            printEnemyToString(p, ai)
            if str(enemyId) == str(p["userId"]) or (ai>0 and str(enemyId) == str(ai)):
                enemy = p
                enemy_pos = ai
                print "REVENGE: " + str(p["userId"])
                break
            if (str(p["userId"]) in exceptions):
                print "EXCEPT: "; printEnemyToString(p, ai)
            if int(p['level'])<min_lvl and p["userId"] != pid and not str(p["userId"]) in exceptions:
                min_lvl = int(p['level'])
                enemy = p
                enemy_pos = ai
            ai+=1
    if enemy:
        print 'ATTACK: '; printEnemyToString(enemy, enemy_pos)
    return enemy

def exitBase():
    request = {
        "params":{
            "state": 1,
            "id": squad_id,
            "ts": getTime()
        },
        "request":"changeSquadState"
        }
        
    request["params"] = encode(json.dumps(request["params"]))
    resp_txt = sendRequest(genReq(request))
    try:
        resp = json.loads(resp_txt)
        if resp.has_key("result") and resp["result"] == "ok":
            print "Squad exit base, id: "+str(squad_id)
        else:
            print resp_txt
    except:
        print "Load JSON Error: "+resp_txt

def enterBase():
    request = {
        "params":{
            "state": 0,
            "id": squad_id,
            "ts": getTime()
        },
        "request":"changeSquadState"
        }
        
    request["params"] = encode(json.dumps(request["params"]))
    resp_txt = sendRequest(genReq(request))
    try:
        resp = json.loads(resp_txt)
        if resp.has_key("result") and resp["result"] == "ok":
            print "Squad enter base, id: "+str(squad_id)
        else:
            print resp_txt
    except:
        print "Load JSON Error: "+resp_txt

def move(x1,y1,x2,y2):
    base_x = -7.5
    base_y = 2.5
    if not x1: x1 = base_x; y1 = base_y;
    if not x2: x2 = base_x; y2 = base_y;
    request = {
        "params":{
            "tx": x2,
            "ty": y2,
            "ts": getTime(),
            "y": y1,
            "x": x1,
            "state": 2,
            "id": squad_id,
            "ts": getTime()
        },
        "request":"changeSquadState"
        }
        
    request["params"] = encode(json.dumps(request["params"]))
    resp_txt = sendRequest(genReq(request))
    try:
        resp = json.loads(resp_txt)
        if resp.has_key("result") and resp["result"] == "ok":
            print "Squad moved, id: "+str(squad_id)
        else:
            print resp_txt
    except:
        print "Load JSON Error: "+resp_txt



def getSig(string, key=''):
    return hashlib.md5(string+key).hexdigest()
    
def sortParams(data):
    pl = []
    for p in data:
        pl.append(p+'='+str(data[p]))
    pl.sort()
    return "".join(pl)

def genReq(request):
    global tCount
    nrequest = {
        "random":getRandom(), "viewerId":pid, "authKey":auth, "appId":appId, "version":"1.1.1.0",
        "ts":getTime(), "tNN":tCount
    }
    for r in request:
        nrequest[r] = request[r]
    if tSession != "":
        nrequest["tSession"] = tSession
    nrequest["tKey"] = getSig(sortParams(nrequest))
    tCount+=1
    return nrequest


def init():
    global tSession
    request = {
        "request":"authorize", "source":0
    }
        
    resp_txt = sendRequest(genReq(request))
    try:
        resp = json.loads(resp_txt)
        if resp.has_key("session_id"):
            print "Auth completed tSession="+resp["session_id"]
            tSession = resp["session_id"]
            return resp
        else:
            print resp_txt
    except:
        print "Load JSON Error: "+resp_txt
        
    return None;



person = 2
if len(sys.argv) > 1:
    person = int(sys.argv[1])

enemyId = 0
if len(sys.argv) > 2:
    enemyId = sys.argv[2]
    
attack = True
if len(sys.argv) > 3:
    attack = False

persons = [
    {'pid':'124520', 'auth':'9037dffa6247a0c12e6846044660d736'},
    {'pid':'217858589', 'auth':'b121a65e293ffbe05c1cf1e623eecd97'},
    {'pid':'93902559', 'auth':'269ca0e4213c689bd8fe974e5073a024'}
    
]

pid = persons[person]['pid']
auth = persons[person]['auth']
appId = '4375733'
squad_id = 0
version = '1.1.1.0'
tCount = 1
tSession = ""

init()
m = getMap()
if m:
    enemy = getEnemy(m)
    if enemy and attack:
        base = loadBase(enemy)
        if base:
            b = killBase(base)
            r = attackBase(enemy['userId'])
            if r: print resultBaseFight(b)
