import urllib
import json
import sys
import datetime

limit = 1111
res = ''
ts = datetime.datetime.now()
if len(sys.argv) > 1:
    limit = int(sys.argv[1])

if len(sys.argv) > 2:
    res = sys.argv[2]

corn_count = 0
corn = True if res == "corn" else False

#sunflower_oil
corn_url = "http://109.234.155.174/settlers/server.php?buildingId=71&appId=2181108&request=craftItem&type=cornTortillas&random=995452687&viewerId=124520&authKey=1afebbff2c3e70596a0b01685bdd7e7e"
wish_url = "http://109.234.155.174/settlers/server.php?random=425495258&request=useWish&items=egg&appId=2181108&viewerId=124520&authKey=1afebbff2c3e70596a0b01685bdd7e7e"
wish_count = 0
wish = True if res == "wish" else False

if not res:
    req_wire = "http://109.234.155.174/settlers/server.php?appId=2181108&request=authorize&source=0&random=31075505&viewerId=124520&authKey=1afebbff2c3e70596a0b01685bdd7e7e"
    rrr = urllib.urlopen(req_wire)
    list = json.load(rrr)["profile"]["warehouse"]
else:
    list = {res: 21}
if corn:
    list = {"sunflower_oil":21, "water":22, "cornmeal":21}
    corn_count = limit
    limit = 4 + 21
else:
    corn_count = 1
if wish:
    list = {"egg":21}
    limit += 21

c_count = 0
while c_count<corn_count:
    try:
        c_count = c_count + 1
        ll = len(list)
        cnt = 0
        for val in list:
            cnt = cnt + 1
            value = int(list[val])
            if corn: list = {"sunflower_oil":21, "water":22, "cornmeal":21}
            while value<limit and value>20:
                req_ask = "http://109.234.155.174/settlers/server.php?friendIds=155908147&authKey=1afebbff2c3e70596a0b01685bdd7e7e&viewerId=124520&item=%s&request=askFriends&random=666&appId=2181108" % (val)
                resp = "http://109.234.155.174/settlers/server.php?authKey=35bc671273dd6070a2318dbf1d3bb95a&viewerId=155908147&random=103644539&request=respondToFriendRequest&action=accept&appId=2181108&friendId=124520"
                print val+": "+str(list[val])+" "+str(cnt)+"("+str(ll)+")"
                try:
	                rrr1 = urllib.urlopen(req_ask)
	                rrr2 = urllib.urlopen(resp)
	                if wish: rrr3 = urllib.urlopen(wish_url); print "wish "+str((datetime.datetime.now()-ts).seconds)
	                value = int(list[val]) + 1
	                list[val] = value
                except: print "inside err"
        if corn:
            rrr1 = urllib.urlopen(corn_url)
            print "corn done: "+str(c_count)+"("+str(corn_count)+")"
    except: print "was error"
    te = datetime.datetime.now()
    dt = te - ts
    sec = dt.seconds
    s = str(sec)
    if sec>60:
        s = str(int(sec/60))+":"+str(sec%60)
    print s
if len(list)>5:
    for val in list:
        value = int(list[val])
        if value<20:
            print val+":"+str(value)
