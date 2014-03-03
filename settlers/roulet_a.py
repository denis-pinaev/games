import urllib
import json
import sys
import datetime

limit = 10000
ts = datetime.datetime.now()
if len(sys.argv) > 1:
    limit = int(sys.argv[1])

roulet_url = "http://109.234.155.174/settlers/server.php?request=useToken&authKey=1afebbff2c3e70596a0b01685bdd7e7e&viewerId=124520&tokenId=%s&appId=2181108&random=%s"
wish_url = "http://109.234.155.174/settlers/server.php?friendIds=115816280&authKey=1afebbff2c3e70596a0b01685bdd7e7e&viewerId=124520&item=token&request=askFriends&random=123&appId=2181108"
resp_url = "http://109.234.155.174/settlers/server.php?authKey=a3a45f05bf1d18cefce5773b4d707d95&viewerId=115816280&random=321&request=respondToFriendRequest&action=accept&appId=2181108&friendId=124520"
wish_count = 0
wish = False

if limit>0:
    for i in range(limit):
        try:
            urllib.urlopen(wish_url)
            urllib.urlopen(resp_url)
        except: print "was error"; print sys.exc_info()
        if i%50 == 0:
            print i

if True:
    req_wire = "http://109.234.155.174/settlers/server.php?appId=2181108&request=authorize&source=0&random=31075505&viewerId=124520&authKey=1afebbff2c3e70596a0b01685bdd7e7e"
    rrr = urllib.urlopen(req_wire)
    list = json.load(rrr)["profile"]["roulette"]["tokens"]
    o = {}
    for p in list:
        if p.has_key('name'):
             if o.has_key(p['name']):
                 o[p['name']] += 1
             else:
                 o[p['name']] = 1
    print o

c_count = 0
for r in list:
    c_count += 1
    try:
        req_ask = roulet_url % (str(r['id']), str(r['id'])+'119')
        resp = json.load(urllib.urlopen(req_ask))
        if not resp['result'] == 'ok': print resp
    except: print "was error"; print sys.exc_info()
    if c_count%50 == 0:
        te = datetime.datetime.now()
        dt = te - ts
        sec = dt.seconds
        s = str(sec)
        if sec>60:
            s = str(int(sec/60))+":"+str(sec%60)
        print 'time: ' + s, c_count