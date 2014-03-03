import urllib
import json
import sys
import datetime
import random
import time

#USAGE:
#getres_fill.py COUNT WHAT FROM TO MIN
#WHAT = add or fill (add ads count, fill - fill to count)

limit = 10
res = ''
lim_min = 0
send_from = 'alena_sid'
send_to = 'denis'#'vic_sid'
if len(sys.argv) > 1:
    limit = int(sys.argv[1])
if len(sys.argv) > 2:# and not sys.argv[2] == "all":
    res = sys.argv[2]
if len(sys.argv) > 5:
    lim_min = int(sys.argv[5])
if len(sys.argv) > 3:
    send_from = sys.argv[3]
if len(sys.argv) > 4:
    send_to = sys.argv[4]
p_list = {
         'denis':{'id':'124520', 'sid':'1afebbff2c3e70596a0b01685bdd7e7e'},
         'margo':{'id':'155908147', 'sid':'35bc671273dd6070a2318dbf1d3bb95a'},
         'alena_sid':{'id':'115816280', 'sid':'a3a45f05bf1d18cefce5773b4d707d95'},
         'vic_sid':{'id':'130857286', 'sid':'a539aabca5a8a3dfcb0890af9f19425b'}
         }
         
if not (p_list.has_key(send_to) and p_list.has_key(send_from)):
    print 'incorrect initial persons'
    time.sleep(99999)
send_to = p_list[send_to]
send_from = p_list[send_from]

def getRandom():
    return str(int(random.random()*1000000))

ts = datetime.datetime.now()
if not res or res == 'add' or res == 'fill':
    req_wire = "http://109.234.155.174/settlers/server.php?appId=2181108&request=authorize&source=0&random=%s&viewerId=%s&authKey=%s" % (getRandom(), send_to['id'], send_to['sid'])
    rrr = urllib.urlopen(req_wire)
    list = json.load(rrr)["profile"]["warehouse"]
else:
    list = {res: lim_min}

test = False
if test:
    s_y = []
    s_n = []
    for v in list:
        if int(list[v])>20:
            s_y.append(v)
        else:
            s_n.append(v)
    list = {}
    list['s_n'] = s_n
    list['s_y'] = s_y
    jdata = json.dumps(list)
    f = open('test', 'w')
    f.write(jdata)
    f.close()
    print 'saved'
    time.sleep(99999)
else:
    jdata = json.dumps(list, indent=4)
    print jdata

s_y = ["scissors", "coffee", "spatula", "shield", "sunflower_oil", "paper", "pitch", "glue", "milk", "juicyClover", "tinsel", "cup", "cherry", "broom", "sugar", "wood", "board", "furniture", "match", "pumpkin", "mixture", "scarabey", "sword", "food", "flour", "blanket", "mandarin", "spoon", "bandage", "goatCheese", "bread", "tickets", "bottleWine", "cornTortillas", "ballThread", "candy", "bag", "joustMedal", "bacon", "crayons", "nail", "ball", "sewingTools", "hammer", "pills", "ribbon", "rope", "vitamins", "lead", "armor", "reindeerMoss", "print", "clover", "pepper", "wheat", "water", "cookie", "grapes", "elixir", "ore", "pancake", "stone", "batiste", "cog", "pillow", "patty", "key", "apple", "bell", "hook", "brush", "tools", "realMoney", "sock", "pears", "paint", "beer", "jam", "mush", "mushroom", "chocolate", "flag", "mapleLeaf", "treasureMap", "spice", "steel", "bucket", "soup", "carrot", "cornmeal", "cake", "wrappingPaper", "honey", "kefir", "wildflowers", "harvest", "saw", "cotton", "lamp", "hop", "thermometer", "soap", "quartz", "firstClassGrain", "peas", "cement", "fertilizer", "tuna", "honeywine", "collar", "pulley", "croissant", "alarm", "sausages", "egg", "presentLabel"]
s_n = ["null", "d125", "d126", "d127", "d128", "d132", "d133", "d135", "d123", "d124", "observatory", "d69", "d68", "d122", "snowman", "d113", "icerun", "d121", "d0", "d88", "d111", "clockTower", "christmasTree", "d100", "oven", "d107", "braunFactory", "d120", "eiffelTower", "d65", "d64", "d67", "d66", "d80", "hren", "d76", "d77", "d75", "d78", "carousel", "d95", "d96", "gingerbreadHouse", "icecastle", "magicball", "icebear", "spruce", "d112", "d15", "danoneFactory", "iceHouse", "autumnTree"]

def save_new_value(val):
    f = open('new_value', 'a')
    f.write('%s\n ' % val)
    f.close()
    print 'new value:', val
    #time.sleep(1)

c_count = 0
while c_count<1:
    try:
        c_count = c_count + 1
        ll = len(list)
        cnt = 0
        for val in list:
            #if val in s_n: continue
            #if not val in s_y: save_new_value(val)
            cnt = cnt + 1
            value = 0 if res == 'add' else int(list[val])
            while value<limit and value>=lim_min:
                req_ask = "http://109.234.155.174/settlers/server.php?friendIds=%s&authKey=%s&viewerId=%s&item=%s&request=askFriends&random=%s&appId=2181108" % (send_from['id'], send_to['sid'], send_to['id'], val, getRandom())
                resp = "http://109.234.155.174/settlers/server.php?authKey=%s&viewerId=%s&random=%s&request=respondToFriendRequest&action=accept&appId=2181108&friendId=%s" % (send_from['sid'], send_from['id'], getRandom(), send_to['id'])
                print val+": "+str(list[val])+" "+str(cnt)+"("+str(ll)+")"
                try:
	                rrr1 = urllib.urlopen(req_ask)
	                rrr2 = urllib.urlopen(resp)
	                value = int(list[val]) + 1
	                list[val] = value
                except: print "inside err"
    except: print "was error"
    te = datetime.datetime.now()
    dt = te - ts
    sec = dt.seconds
    s = str(sec)
    if sec>60:
        s = str(int(sec/60))+":"+str(sec%60)
    print s