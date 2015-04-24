# -*- coding: utf-8 -*-

import sys
import json

def read():
    tfile = open(fatype, "r")
    d = tfile.read()
    tfile.close()
    return d

def write(s):
    tfile = open(fatype+"_", "w")
    tfile.write(s)
    tfile.close()
    
def getBaseData(data):
    if data.has_key("base") and data["base"].has_key("buildings"):
        builds = data["base"]["buildings"]
        for b in builds:
            if b.has_key("wp"):
                print b["buildingClass"]["name"]+":"+str(len(b["wp"]))
                for wp in b["wp"]:
                    print "\tlevel: %s, id: %s" % (str(wp["level"]), str(wp["id"]))
                    wp["level"] = 0
                    wp["id"] = 9
    return data

def getUnitData(data):
    if data.has_key("base") and data["base"].has_key("units"):
        builds = data["base"]["units"]
        for b in builds:
            if b.has_key("wp"):
                print "unit id: "+ str(b["id"])
                for wp in b["wp"]:
                    print "\tlevel: %s, id: %s" % (str(wp["level"]), str(wp["id"]))
                    wp["level"] = 0
                    wp["id"] = 0
    return data
fatype = "convert_wp"
battle_type = "base"

if True:
   data = read()
   data = json.loads(data)
   if "base" in battle_type:
       data = getBaseData(data)
   if "units" in battle_type:
       data = getUnitData(data)
   write(json.dumps(data))
   
