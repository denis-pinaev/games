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
    if nextD<maxD: setType(item, "catapulta", 1)
    t, level = getType(item)
    if t not in ["wall", "tree", "stone"]: print json.dumps(item)
    if prev_type != t:
        prev_type = t
    #    prev_x, prev_y = getCoords(item)
    #else:
    #    setCoords(item, prev_x, prev_y)
    #newType = changeType(prev_type)
    #setType(item, newType, 1)
    if t in dangerTypes:
        #setType(item, t, 1)
        x, y = dangerCoords[nextD]
        nextD += 1
        if nextD>=len(dangerCoords): nextD = 0
        setCoords(item, x, y)
    else: setCoords(item, 3, 16)
    if t in ["wall", "tree", "stone"]:
        #setType(item, t, 1)
        setCoords(item, 36, 36)
    if item.has_key("units"): del item["units"]
    if not ("mining" in t):
        setType(item, t, 1)
        #if True:
            #item.has_key("stored"):
            #item["stored"] = 99999
    else:
        setType(item, t, 9)
#        if item.has_key("stored"):
#            for p in item["stored"]: item["stored"][p] = 99999
#        if str(item["id"])=="64":
#            setType(item, "miningGold", 9)
    if nextD>maxD:
        setType(item, pca, 9)
        if pca == "miningRunes": pca = "miningGold"; setCoords(item, 3, 16)
        elif pca == "miningGold": pca = "miningWood"; setCoords(item, 3, 16)
        elif pca == "miningWood": pca = "miningRunes"; setCoords(item, 3, 16)
        nextD = maxD
        
    #if not t in ["wall", "tree", "stone"]: setCoords(item, 15, 10)

    
jdata["result"]["data"]["map"]["field"] = sorted(m, key=lambda t: t["id"])
write("in", json.dumps(jdata))