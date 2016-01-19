import json
import sys

def read(fname):
    f = open(fname, 'rb')
    data = f.read()
    f.close()
    return data

def write(fname, data):
    f = open(fname, 'wb')
    f.write(data)
    f.close()

def getType(item):
    t = item["type"]
    if "_" in t:
        return t.split("_")[0], t.split("_")[1]
    else:
        print "WARN: no '_' in type: " + t
        return t, 0

def getCoords(item):
    return item["x"], item["y"]

def setType(item, t, level=1):
    item["type"] = t+"_"+str(level)

def setCoords(item, x, y):
    item["x"] = x
    item["y"] = y
    
def changeType(t):
    defType = "wall"
    dangerTypes = ["ballista", "catapulte", "tower"]
    if t in dangerTypes: return defType
    return t

data = read("in")
jdata = json.loads(data)
m = jdata["result"]["data"]["map"]["field"]
m = sorted(m, key=lambda t: t["type"])
prev_type = ""
pca = "miningRunes"
prev_x = 1
prev_y = 1
dangerTypes = ["ballista", "catapulta", "tower", "electricThrower", "flamethrower", "elementalTower", "ballistaGoblin", "catapultaGoblin", "towerGoblin", "electricThrowerGoblin", "flamethrowerGoblin", "elementalTowerGoblin"]
dangerCoords = [(0, 16), (0, 16), (0, 16), (16, 0), (33, 0), (33, 0), (33, 16), (33, 33)]
nextD = 0
maxD = 3
for item in m:
    t, level = getType(item)
    wasS = json.dumps(item)
    if t in ["wall", "tree", "stone"]: setCoords(item, 36, 36); continue
    if t in dangerTypes:
        setType(item, "catapulta", 1)
        setCoords(item, 0, 16)
    else:
        if "townhall" in t: setType(item, t, 10)
        setCoords(item, 3, 16)
    if item.has_key("units"): del item["units"]
    print wasS, getType(item)

cata_count = 1
wood_count = 1
gold_count = 1
runa_count = 1
if len(sys.argv)>1: cata_count = int(sys.argv[1])
if len(sys.argv)>2: wood_count = int(sys.argv[2])
if len(sys.argv)>3: gold_count = int(sys.argv[3])
if len(sys.argv)>4: runa_count = int(sys.argv[4])


nid = len(m)
for i in range(cata_count):
    m.append({"y": 16, "x": 0, "state": 0, "type": "catapulta_1", "id": nid+i+1})
nid = len(m)
for i in range(wood_count):
    m.append({"y": 16, "x": 0, "state": 0, "type": "miningWood_10", "id": nid+i+1})
nid = len(m)
for i in range(gold_count):
    m.append({"y": 16, "x": 0, "state": 0, "type": "miningGold_10", "id": nid+i+1})
nid = len(m)
for i in range(runa_count):
    m.append({"y": 16, "x": 0, "state": 0, "type": "miningRunes_10", "id": nid+i+1})
    
jdata["result"]["data"]["map"]["field"] = sorted(m, key=lambda t: t["id"])
write("in", json.dumps(jdata))