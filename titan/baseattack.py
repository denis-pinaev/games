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

def getRandom():
    s = ''
    for i in range(9):
        c = str(int(random.random()*9)+1)
        s+=str(c)
    return s
    
def getTime():
    return str(int(time.time()))

def sendRequest0(params):
    url = 'http://titans-vk-sc1.playkot.com/current/server.php'
    resp = requests.get(url, data=params, allow_redirects=True)
    txt = resp.text
    return txt
    
def sendRequest(params):
    url = 'http://titans-vk-sc1.playkot.com/current/server.php?'
    ppp = urllib.urlencode(params)
    url+=ppp
    resp = requests.get(url)
    txt = resp.text
    return txt
    
result = {
  "enemy": {
    "buildings": [
      {
        "health": 0,
        "id": 0
      },
      {
        "health": 0,
        "id": 1
      },
      {
        "health": 0,
        "id": 2
      },
      {
        "health": 0,
        "id": 3
      },
      {
        "health": 0,
        "id": 4
      },
      {
        "health": 0,
        "id": 5
      },
      {
        "health": 0,
        "id": 6
      },
      {
        "health": 0,
        "id": 7
      },
      {
        "health": 0,
        "id": 8
      },
      {
        "health": 0,
        "id": 9
      }
    ]
  },
  "f2": 0,
  "f1": 4696722.395209581,
  "ts": 1414766004,
  "units": [
    {
      "typeId": 3,
      "capacity": 13000,
      "level": 0,
      "arm": [
        {
          "id": 2,
          "level": 4
        }
      ],
      "bonus_hp": [
        {
          "id": 3,
          "level": 4
        }
      ],
      "health": 1780,
      "wp": [
        {
          "id": 6,
          "level": 4
        },
        {
          "id": 6,
          "level": 4
        }
      ],
      "y": 22,
      "x": 10,
      "id": 0
    },
    {
      "typeId": 3,
      "capacity": 13000,
      "level": 0,
      "arm": [
        {
          "id": 2,
          "level": 4
        }
      ],
      "bonus_hp": [
        {
          "id": 3,
          "level": 4
        }
      ],
      "health": 1780,
      "wp": [
        {
          "id": 6,
          "level": 4
        },
        {
          "id": 6,
          "level": 4
        }
      ],
      "y": 23,
      "x": 8,
      "id": 1
    },
    {
      "typeId": 3,
      "capacity": 8000,
      "level": 0,
      "arm": [
        {
          "id": 2,
          "level": 4
        }
      ],
      "bonus_hp": [
        {
          "id": 3,
          "level": 4
        }
      ],
      "health": 1780,
      "wp": [
        {
          "id": 6,
          "level": 4
        },
        {
          "id": 6,
          "level": 4
        }
      ],
      "y": 23,
      "x": 12,
      "id": 2
    },
    {
      "typeId": 3,
      "capacity": 13000,
      "level": 0,
      "wp": [
        {
          "id": 6,
          "level": 4
        },
        {
          "id": 6,
          "level": 4
        }
      ],
      "arm": [
        {
          "id": 2,
          "level": 4
        }
      ],
      "bonus_hp": [
        {
          "id": 3,
          "level": 4
        }
      ],
      "health": 1780,
      "x": 6,
      "y": 24,
      "mass": 1,
      "id": 3
    },
    {
      "typeId": 3,
      "capacity": 13000,
      "level": 0,
      "wp": [
        {
          "id": 6,
          "level": 4
        },
        {
          "id": 6,
          "level": 4
        }
      ],
      "arm": [
        {
          "id": 2,
          "level": 4
        }
      ],
      "bonus_hp": [
        {
          "id": 3,
          "level": 4
        }
      ],
      "health": 1780,
      "x": 10,
      "y": 24,
      "mass": 1,
      "id": 4
    },
    {
      "typeId": 3,
      "capacity": 13000,
      "level": 0,
      "wp": [
        {
          "id": 6,
          "level": 4
        },
        {
          "id": 6,
          "level": 4
        }
      ],
      "arm": [
        {
          "id": 2,
          "level": 4
        }
      ],
      "bonus_hp": [
        {
          "id": 3,
          "level": 4
        }
      ],
      "health": 1780,
      "x": 14,
      "y": 24,
      "mass": 1,
      "id": 5
    }
  ],
  "id": 0
}

pid = '124520'
auth = '9037dffa6247a0c12e6846044660d736'
appId = '4375733'
squad_id = 0

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
        "random":getRandom(), "viewerId":pid, "authKey":auth, "appId":appId,
        "request":"getUserMap"
        }
        
    resp_txt = sendRequest(request)
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
        "random":getRandom(), "viewerId":pid, "authKey":auth, "appId":appId,
        "id":p['userId'],
        "squad_id":squad_id,
        "request":"loadBase"
        }
        
    resp_txt = sendRequest(request)
    try:
        resp = json.loads(resp_txt)
        if resp.has_key("result") and resp["result"] == "ok":
            print "Base loaded"
            return resp['base']
        else:
            print resp_txt
    except:
        print "Load JSON Error: "+resp_txt
        
    return None;
    
def killBase(base):
    res = []
    if base.has_key("buildings"):
        for b in base["buildings"]:
            if int(b['typeId']) != 12:
                res.append({'id':b['id'],'health':0})
    return res
    
def getEnemy(m):
    min_lvl = 999
    enemy = None
    for p in m:
        if p.has_key('userId'):
            s = str(p['userId'])
            while len(s)<15: s+=" "
            s+=p['firstName']+u" "+p['lastName']
            while len(s)<40: s+=" "
            s+=u"level:"+str(p['level'])
            if p.has_key('rating'):
                s+=u"\tRate:"+str(p['rating'])
            print s
            if int(p['level'])<min_lvl and p["userId"] != pid:
                min_lvl = int(p['level'])
                enemy = p
    return enemy

def exitBase():
    request = {
        "random":getRandom(), "viewerId":pid, "authKey":auth, "appId":appId,
        "params":{
            "state": 1,
            "id": squad_id,
            "ts": getTime()
        },
        "request":"changeSquadState"
        }
        
    request["params"] = encode(json.dumps(request["params"]))
    resp_txt = sendRequest(request)
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
        "random":getRandom(), "viewerId":pid, "authKey":auth, "appId":appId,
        "params":{
            "state": 0,
            "id": squad_id,
            "ts": getTime()
        },
        "request":"changeSquadState"
        }
        
    request["params"] = encode(json.dumps(request["params"]))
    resp_txt = sendRequest(request)
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
        "random":getRandom(), "viewerId":pid, "authKey":auth, "appId":appId,
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
    resp_txt = sendRequest(request)
    try:
        resp = json.loads(resp_txt)
        if resp.has_key("result") and resp["result"] == "ok":
            print "Squad moved, id: "+str(squad_id)
        else:
            print resp_txt
    except:
        print "Load JSON Error: "+resp_txt


req = []

req.append('''
random	337078583
viewerId	124520
params	eNpdi0EOQDAUBe/y1iXt96v1lw5g4wQNInZoJUTcXWNpOZmZGyeESuucJ83eONKaba2wjBCtcEGKv2anEFNIE6RSSBFi2DCT9Wwy73O/HSHvVH/UrUMbYo6b5wWUFRvk
appId	4375733
authKey	9037dffa6247a0c12e6846044660d736
request	changeSquadState
''')

req.append('''
random	388165203
viewerId	124520
params	eJzVlNtuwyAMht/F16jCQAjkDfYMVTXRjC2RmoNy2FpFefc5aEuzlYvdtbtC+W3jz47xBL721QWyCbrm2Aw9ZPsJCu9OQwEZZ1C+0DGzGw0jmohoMqKpiJbMh5nBq4DMcC13WhqFWqAQXJGMdLlE1DujhVDcWBQkL7SoUKk0TZVmMNblVwHDpfVPS3YGuWtdXg5UorWcU7aTf/enkNd1VfAO7KtBzQcGx6Ye++eiXe3yp/2bHq21DD6ufnrjx24lCiUSQdnOFLztbxzZPAyyDMhm8/ejxI8GjGIzm3/r8RJM01W5fpmve5VwDsr6hP4ZOm6fepwdf7GHLbCWcD/ya/8WJbxPBp3vm7HLfb9syjdHh02UJrCxc3U5Vut35QdHt1laYMk8fwLsPpBQ
appId	4375733
authKey	9037dffa6247a0c12e6846044660d736
request	battleResults
''')

req.append('''
random	105794554
viewerId	124520
params	eNqrVspMUbIy0FEqKVayMjQxNDExMrA0AvKLSxJLUoEytQCZHAj7
appId	4375733
authKey	9037dffa6247a0c12e6846044660d736
request	changeSquadState
''')

count = 1
if len(sys.argv) > 1:
    count = int(sys.argv[1])

#exitBase()
#move(None,None,0,0)
#move(0,0,None,None)
#enterBase()
m = getMap()
if m:
    enemy = getEnemy(m)
    if enemy:
        base = loadBase(enemy)
        if base:
            b = killBase(base)
            print b
