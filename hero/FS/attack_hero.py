import binascii
import json, sys

code2 = ''
person = 0
if len(sys.argv) > 1:
    person = int(sys.argv[1])
    
n_c = True
new_cheat = 0
if len(sys.argv) > 2:
    new_cheat = int(sys.argv[2])
    n_c = False

maxP = 4
if len(sys.argv) > 3:
    n_c = True
    maxP = int(sys.argv[3])
    
    
pids = ["3091478", "160511757", "144536559", '0']
pid = pids[person]
data = '\
'

#731331d4e19d1f5483acd67abf424b58
print pid

def rreplace(s, old, new, count):
    return (s[::-1].replace(old[::-1], new[::-1], count))[::-1]
    
def read():
    fatype = "cheat"
    tfile = open(fatype, "r")
    d = tfile.read()
    tfile.close()
    return d

def getSig(myStr):
    return binascii.crc32(myStr) & 0xffffffff
    
def getData():
    return getSig(pid+code2+data)

def log(s1, s2):
    fatype = "cheat"
    print s2
    if True:
        tfile = open(fatype, "w")
        tfile.write(s2+'!'+s1)
        tfile.close()
        
def convertEnemy(data):
    wasE = 0
    maxE = maxP
    o_c = 0
    o_nc = 0
    w_r = 0
    dataj2 = json.loads(data)
    if dataj2.has_key("mission") and dataj2["mission"].has_key("entities"):
        dataj = dataj2["mission"]["entities"]
        kset = dataj2["mission"]["missionTargets"]["units"]
        mlen = len(kset)
        if mlen<5: maxE = mlen
        for i2 in kset:
            i = str(i2)
            o = dataj[i]
            if True:
                wasE += 1
                if wasE < maxE:
                    o["owner"] = 1
                    o_c += 1
                else:
                    o_nc +=1
                if wasE >= maxE: wasE = 0
        kset = dataj.keys()
        for i2 in kset:
            i = str(i2)
            o = dataj[i]
            if o.has_key("subtype") and o["subtype"] == "wall" and o.has_key("owner") and o["owner"] == 2:
                w_r += 1
                del dataj[i]
    print "owner changed", o_c
    print "owner not changed", o_nc
    print "wall deleted", w_r
    return json.dumps(dataj2)


def killEnemy(data):
    global new_cheat
    dataj2 = json.loads(data)
    sunits = ''
    if dataj2.has_key("mission") and dataj2["mission"].has_key("entities"):
        dataj = dataj2["mission"]["entities"]
        
        new_cheat2 = int(dataj2["mission"]["actionId"])
        if new_cheat2 > new_cheat: new_cheat = new_cheat2

        kset = dataj2["mission"]["missionTargets"]["units"]
        for i2 in kset:
            i = str(i2)
            o = dataj[i]
            if o.has_key("dead"): continue
            if len(sunits)>0:
                sunits = '%s,"%s":{"turn":0.1,"dmg":10,"dead":1}' % (sunits, i)
            else: sunits = '%s"%s":{"turn":0.1,"dmg":10,"dead":1}' % (sunits, i)
            
        kset = dataj2["mission"]["missionTargets"]["list"]
        for i2 in kset:
            i = str(i2)
            o = dataj[i]
            if o.has_key("dead"): continue
            if len(sunits)>0:
                sunits = '%s,"%s":{"turn":0.1,"dmg":10,"dead":1}' % (sunits, i)
            else: sunits = '%s"%s":{"turn":0.1,"dmg":10,"dead":1}' % (sunits, i)

    sline = '{"entities":{%s},"rnd":123,"config":{},"globalSpells":null,"turn":0,"index":"default","aid":%d}' % (sunits, new_cheat)
    return sline




data = read()

data = data.replace('{"s":"\"9\""}','{"s":"\\"9\\""}',1)
#data = data.replace('{"s":"\"558\""}','{"s":"\\"558\\""}',1)
#data = data.replace('\"','\\"',1000)

#data = rreplace(data, '"battleType":"ranger","subtype":"unit","turn":0,"range":5,"speed":3,"initiative":100,"damage":100,"health":250,"maxHealth":250','"battleType":"ranger","subtype":"unit","turn":0,"range":5,"speed":3,"initiative":99985,"damage":100,"health":250,"maxHealth":250',3)
#data = rreplace(data, '"battleType":"ranger","subtype":"unit","turn":0,"range":5,"speed":3,"initiative":85,"damage":95,"health":240,"maxHealth":240','"battleType":"ranger","subtype":"unit","turn":0,"range":5,"speed":3,"initiative":99985,"damage":95,"health":240,"maxHealth":240',3)
#data = data.replace('"battleType":"ranger","subtype":"unit","turn":0,"range":5,"speed":3,"initiative":85,"damage":105,"health":280,"maxHealth":280','"battleType":"ranger","subtype":"unit","turn":0,"range":5,"speed":3,"initiative":99985,"damage":105,"health":280,"maxHealth":280',3)


dataar = data.split('!')

dddd = [dataar[0],'!'.join(str(x) for x in dataar[1:-1]), dataar[-1]]
dataar=dddd
code2 = 'Knights.doAction'
data = dataar[0]
if len(dataar)>1:
    data = dataar[1]
if len(dataar)>2:
    code2 = dataar[2]
    print dataar[0], getData()

if n_c:
    data = convertEnemy(data)
    
if new_cheat>0:
    data = killEnemy(data)

ddd = getData()

print ddd
log(str(data), str(ddd))
