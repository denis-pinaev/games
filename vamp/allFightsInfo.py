import pyamf
import sys
import json
import datetime
import time
from pyamf.remoting.client import RemotingService

data = {}
bid = 40048

if len(sys.argv) > 1:
    bid = int(sys.argv[1])

def log(s):
    s = "[" + datetime.datetime.now().strftime('%d.%m %H:%M:%S')+"]" + s
    fatype = "f_log_all"
    try:
        tfile = open(fatype, "a")
        tfile.write(s.encode('utf-8')+'\n')
        tfile.close()
    except:
        tfile = open(fatype, "w")
        tfile.write(s.encode('utf-8')+'\n')
        tfile.close()

def getClanList():
    data = {}
    client = RemotingService('http://dracula.irq.ru/Gateway.aspx')
    service = client.getService('MafiaAMF.AMFService')
    params1 = {
        "userId":"124520",
        "ServerVersion":11522,
        "SystemID":"1",
        "sig":"d6b9ab24005cf6447de56d505f09b9a9"
    }
    resp = service.dispatch(params1,"AMFService.ClanListGet",[{"IsFight":False}],False)
    if resp.has_key("data"):
        data = resp["data"]
    if data.has_key("Answer"):
        data = data["Answer"]
    if data.has_key("OtherData"):
        data = data["OtherData"]
    if data.has_key("ClanList"):
       data = data["ClanList"]
    return data

def getData(acrch=False):
    data = {}
    client = RemotingService('http://dracula.irq.ru/Gateway.aspx')
    service = client.getService('MafiaAMF.AMFService')
    params1 = {
        "userId":"124520",
        "ServerVersion":11522,
        "SystemID":"1",
        "sig":"d6b9ab24005cf6447de56d505f09b9a9"
    }
    resp = service.dispatch(params1,"AMFService.ClanFightInfoGet",[{"BattleDBID":bid,"IsArchive":acrch}],False)
    to_end = False
    if resp.has_key("data"):
        data = resp["data"]
    if data.has_key("Answer"):
        data = data["Answer"]
    if data.has_key("OtherData"):
        data = data["OtherData"]
    if data.has_key("ClanFightInfo"):
       data = data["ClanFightInfo"]
       to_end = True
    return data, to_end

clans = getClanList()
last_bid = bid
if clans:
    cn = []
    clans.sort(key=lambda x: x['Rang'], reverse=True)
    for i in range(30):
        c = clans[i]
        s = ''
        for k in c:
            s+='%s:%s, ' % (k, c[k])
        cn.append(c['Name'])
        print s[:100]
        log(s)
        
    while True:
        arch = False
        try:
            data, to_end = getData()
        except:
            try:
                data, to_end = getData(True)
                arch = True
            except:
                data = None
            to_end = False
        if data:
            if not arch:
                last_bid = bid
                A = data["ActorClanName"]
                T = data["TargetClanName"]
                if A in cn or T in cn:
                    s = "A: %s, T: %s, id:%s" % (A, T, str(bid))
                    print s
                    log(s)
        else:
            if bid - last_bid > 20:
                print 'End fights:', last_bid
                bid = last_bid
                time.sleep(5*60)
        if to_end:
            bid += 1
        else:
            print 'end_fights_error', last_bid
            time.sleep(30*60)
print 'global END'