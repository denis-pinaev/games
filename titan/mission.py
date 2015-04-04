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
    
unit_type = 15
unit_hp = 5700


resultBase = {
  "enemy": {
    "units": [
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
      }
    ], 
    "buildings": []
  }, 
  "mapSquadId": 32, 
  "missionType": 1, 
  "ts": 1418655005, 
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
        "random":getRandom(), "viewerId":pid, "authKey":auth, "appId":appId,"version":"1.1.1.0",
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
    
    
def launchDrone():

    request = {
        "random":getRandom(), "viewerId":pid, "authKey":auth, "appId":appId,"version":"1.1.1.0",
        "request":"launchDrone","ts": getTime()
        }
        
    resp_txt = sendRequest(request)
    try:
        resp = json.loads(resp_txt)
        if resp.has_key("result") and resp["result"] == "ok":
            print "launchDrone"
            return resp
        else:
            print resp_txt
    except:
        print "Load JSON Error: "+resp_txt
        
    return None;

def attackBase():
    request = {
        "random":getRandom(), "viewerId":pid, "authKey":auth, "appId":appId,"version":"1.1.1.0",
        "params":{
            "missionType": 1,
            "state": 3,
            "y": 0,
            "x": 0,
            "id": squad_id,
            "ts": getTime(),
        },
        "request":"startMission"
        }
        
    request["params"] = encode(json.dumps(request["params"]))
    resp_txt = sendRequest(request)
    try:
        resp = json.loads(resp_txt)
        if resp.has_key("result") and resp["result"] == "ok":
            print "startMission"
            return resp
        else:
            print resp_txt
    except:
        print "Load JSON Error: "+resp_txt
        
    return None

def resultBaseFight(mid=12):

    resultBase['ts'] = getTime()
    resultBase['mapSquadId'] = mid
    
    request = {
        "random":getRandom(), "viewerId":pid, "authKey":auth, "appId":appId,"version":"1.1.1.0",
        "params":resultBase,
        "request":"missionResults"
        }
        
    
    request["params"] = encode(json.dumps(request["params"]))
    resp_txt = sendRequest(request)
    try:
        resp = json.loads(resp_txt)
        if resp.has_key("result") and resp["result"] == "ok":
            print "missionResults"
            return resp
        else:
            print resp_txt
    except:
        print "Load JSON Error: "+resp_txt
        
    return None

person = 0
if len(sys.argv) > 1:
    person = int(sys.argv[1])

enemyId = 0
if len(sys.argv) > 2:
    enemyId =sys.argv[2]

persons = [
    {'pid':'124520', 'auth':'9037dffa6247a0c12e6846044660d736'},
    {'pid':'217858589', 'auth':'b121a65e293ffbe05c1cf1e623eecd97'},
    {'pid':'93902559', 'auth':'269ca0e4213c689bd8fe974e5073a024'}
    
]

pid = persons[person]['pid']
auth = persons[person]['auth']
appId = '4375733'
squad_id = 0

#while True:
#    time.sleep(60*60+10)
if True:
    getMap()
    if launchDrone():
        if attackBase():
            print resultBaseFight()["eventQuest"]
