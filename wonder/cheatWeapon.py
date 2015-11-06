import json

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
dangerTypes = ["ballista", "catapulta", "tower", "electricThrower", "flamethrower", "elementalTower"]
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
        if t == "townhall": setType(item, t, 10)
        setCoords(item, 3, 16)
    if item.has_key("units"): del item["units"]
    print wasS, getType(item)
nid = len(m)
for i in range(10):
    m.append({"y": 16, "x": 0, "state": 0, "type": "catapulta_1", "id": nid+i+1})
nid = len(m)
for i in range(10):
    m.append({"y": 16, "x": 0, "state": 0, "type": "miningWood_9", "id": nid+i+1})
nid = len(m)
for i in range(10):
    m.append({"y": 16, "x": 0, "state": 0, "type": "miningGold_9", "id": nid+i+1})
nid = len(m)
for i in range(10):
    m.append({"y": 16, "x": 0, "state": 0, "type": "miningRunes_9", "id": nid+i+1})
    
jdata["result"]["data"]["map"]["field"] = sorted(m, key=lambda t: t["id"])
write("in", json.dumps(jdata))