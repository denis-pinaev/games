# -*- coding: utf-8 -*-

import binascii
import sys
import json
import datetime
import time
import random
import requests
from buildInfo import *

building_constants = {
                         'ars':'1616757075',
                         'kuzn':'867834348',
                         'hram':'752737343',
                         'wood':'972790757',
                         'stone':'39569244',
                         'iron':'229141479',
                         'gold':'965182906',
                         'main':'490400668',
                         'altar':'1212037112',
                         'sklad':'733825800',
                         'runa':'1074334687',
                         'gnom':'239693933',
                         'plav':'1766343544',
                         'rist':'2101222815',
                         'mag':'447398184',
                         'palatka':'482206421',
                         'kazarma':'335153735',
                         'strelbishe':'723972021',
                         'orden':'1166013905',
                         'tower':'357378297'
                     }
                     
buildinds_priority = ['orden','ars','main','altar','plav','kuzn','runa','hram','gnom','mag','rist','iron','wood','stone','sklad','gold','kazarma','strelbishe','palatka']

actionCommand = 'Knights.doAction'
log_file = 'test'
service = ''
method = ''
gid = 0
pid=''
sid = ''
auth=''



def init_log(name):
    global log_file
    log_file = name
    
def init_params(npid=None, nauth=None, ngid=None, nsid=None, nmethod=None, nservice=None):
    global pid, auth, gid, sid, method, service
    if npid is not None: pid = npid
    if nauth is not None: auth = nauth
    if ngid is not None: gid=ngid
    if nsid is not None: sid=nsid
    if nmethod is not None: method=nmethod
    if nservice is not None: service=nservice
    
def getRandom():
    return str(int(random.random()*1000))
    
def log(s, pr=False, filename=False, needTime=True):
    if needTime:
        s = "[" + datetime.datetime.now().strftime('%d.%m %H:%M:%S')+"] " + s
    if pr: print s
    fatype = filename if filename else "./tmp/hero_"+log_file+"_log"
    try:
        tfile = open(fatype, "a")
        tfile.write(s.encode('utf-8')+'\n')
        tfile.close()
    except:
        tfile = open(fatype, "w")
        tfile.write(s.encode('utf-8')+'\n')
        tfile.close()

def sendRequest(command, params):
    try:
        url = 'http://kn-vk-sc.playkot.com/current/json-gate.php'
        resp = requests.post(url, data=params, allow_redirects=True)
        txt = resp.text.split('!', 1)[1]
        first = txt.find("adInfo")
        if txt.find('"adInfo":"[]"')>0: first = -1;
        if first > 0:
            second = txt.find('}', first)
            txt = txt[:first]+"a\":\"0"+txt[second+1:]
        txt = txt.replace('"a":"0,"', '"a":"0"},"')
        
        return {"data":txt}
    except:
        print "Error in sendRequest!"
        time.sleep(5)
        return sendRequest(command, params)
    
def getSig2(myStr):
    return binascii.crc32(myStr) & 0xffffffff
    
def getSig(data):
    return getSig2(pid+service+data)
    
def createData(method, data):
    o = {}
    o["data"] = data
    o["sig"] = getSig(data)
    o["cmd"] = service
    o["gid"] = gid
    o["pid"] = pid
    return o
    
def init(npid, nauth, post=False):
    global sid, gid, service, method, pid, auth
    init_params(npid=npid, nauth=nauth)
    service = 'Knights.initialize'
    method = 'initialize'
    initString = '{"age":30,"gender":1,"rnd":%s,"referralType":6,"newDay":false,"owner_id":"","hash":{%s}%s,"auth_key":"%s","sid":"","pauth":"%s","v":"%s"}'
    sid = ''
    gid = 0
    postString = ''
    hashString = ''
    if post:
        postString = '"post":"%s"' % (post)
        hashString = ',"postHash":"%s"' % (post)
    params = createData(method, initString % (getRandom(), postString, hashString, auth, getPauth(pid), getGameVersion()))
    #log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    #print resp["data"][:100]
    #if auth == "" : resp["data"] = resp["data"][:-1]
    o = json.loads(resp["data"])
    #log(json.dumps(o, indent=4))
    error = o["error"]
    if error == 0:
        sid = o["sessionKey"]
        gid = o["player"]["player_id"]
        #log("pid: %s, sid: %s, gid: %s" % (str(npid), str(sid), str(gid)), True)
    #else:
    #    log(resp["data"], True)
        #if "BANNED" in error: time.sleep(9999999)
        
    return (o, gid, sid)
    
def print_user_info(ar):
    for build in buildinds_priority:
        print build+":"
        for i in range(len(ar[build])):
            for k in ar[build][i]:
                x = ar[build][i][k]['x']
                y = ar[build][i][k]['y']
                print '   %s x=%s,y=%s' % (str(k),str(x),str(y))
                     
def get_buildings_extend(ent):
    ret = {}
    for build in building_constants:
        ret[build] = []
        const = str(building_constants[build])
        for en in ent:
            e = ent[en]
            if str(e['id']) == const:
                ret[build] = ret[build] + [{str(e['sceneId']):{"x":e['x'],"y":e['y']}}]
    return ret
                
def get_buildings_ids(ent):
    ret = {}
    for build in building_constants:
        ret[build] = []
        const = str(building_constants[build])
        for en in ent:
            e = ent[en]
            if str(e['id']) == const:
                ret[build] = ret[build] + [str(e['sceneId'])]
    return ret
                
def get_help_string(bk, ba, max_help):
    if len(bk)>0:
        kset = bk.keys()
        for k in kset:
            if bk[k].has_key("ready"): del bk[k]#; print "del ready "+k
    if len(bk)<1: return ''
    rbk = []
    kset = bk.keys()
    for wb in buildinds_priority:
        wba = ba[wb]
        for i in range(len(wba)):
            wbid = wba[i]
            for bkb in kset:
                if bkb == wbid: rbk = rbk + [bkb]#; print wb, wbid
    return rbk
