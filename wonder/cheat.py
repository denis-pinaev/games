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
prev_x = 1
prev_y = 1
dangerTypes = ["ballista", "catapulte", "tower"]
dangerCoords = [(0, 0), (0, 16), (0, 33), (16, 0), (33, 0), (33, 0), (33, 16), (33, 33)]
nextD = 0
for item in m:
    t, level = getType(item)
    print json.dumps(item)
    if prev_type != t:
        prev_type = t
    #    prev_x, prev_y = getCoords(item)
    #else:
    #    setCoords(item, prev_x, prev_y)
    #newType = changeType(prev_type)
    #setType(item, newType, 1)
    if t in dangerTypes:
        setType(item, t, 1)
        x, y = dangerCoords[nextD]
        nextD += 1
        if nextD>=len(dangerCoords): nextD = 0
        setCoords(item, x, y)
    if t in ["wall", "tree", "stone"]:
        setType(item, t, 1)
        setCoords(item, 36, 36)
    if item.has_key("units"): del item["units"]
    
jdata["result"]["data"]["map"]["field"] = sorted(m, key=lambda t: t["id"])
write("in", json.dumps(jdata))