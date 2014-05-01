import pyamf
import sys
import json
import datetime
import time
from pyamf.remoting.client import RemotingService

data = {}
bid = 38427
sid = 11329

def log(s):
    s = "[" + datetime.datetime.now().strftime('%H:%M:%S')+"]" + s
    if "Ladder" in s and s.index("Ladder")<50: print s+'\n-----------------------'; return
    fatype = "log_"+str(bid)
    try:
        tfile = open(fatype, "a")
        tfile.write(s.encode('utf-8')+'\n')
        tfile.close()
    except:
        tfile = open(fatype, "w")
        tfile.write(s.encode('utf-8')+'\n')
        tfile.close()

def dif(o1, o2, t):
    cfield = ''
    spam_fields = ['AvatarWaterMark', 'Avatar']
    for f in o1:
        if o1[f]!=o2[f]:
            cfield = f
            break
    s = '['+t+'] {"changed":"'+cfield+'", "new":"'+str(o1[f])+'", "old":"'+str(o2[f])+'"}'
    if cfield in ["DmgDealed", "HealthCur"]:
        s = s[:-1]+', "dif":"'+str(o2[f]-o1[f])+'"}'
    for f in o1:
        try:
            if not f == cfield:
                if f == "PlayerName":
                     s+=', {"'+str(f)+'":"'+o1[f]+'"}'
                elif not f in spam_fields:
                     s+=', {"'+str(f)+'":"'+str(o1[f])+'"}'
        except:
            print sys.exc_info()
            s+=', {"unknown field":"'+f+'"}'
    log(s)

def changeInfo(atype):
    global data
    fatype = atype + "_" + str(bid)
    indata = data[atype]
    try:
        tfile = open(fatype, "r")
        fstr = tfile.read()
    except:
        fstr = ''
    cont = False
    if len(fstr)>0:
        fdata = json.loads(fstr)
        cont = True
    else:
        cont = False
        tfile = open(fatype, "w")
        tfile.write(json.dumps(indata))
        tfile.close()
        fdata = False
    if cont:
        cont = fdata == indata

    if not cont and fdata:
        for pers in indata:
            npdata = getPers(pers, fdata)
            if npdata:
                if npdata == getPers(pers, indata):
                    continue
                else:
                    dif(pers, npdata, atype[0])
            else:
                log("new! "+pers["PlayerName"])
        tfile = open(fatype, "w")
        tfile.write(json.dumps(indata))
        tfile.close()

def getPers(o, p):
    for pp in p:
        if pp["FighterDBID"] == o["FighterDBID"]: return pp
    return None
    

def getData():
    global data
    client = RemotingService('http://dracula.irq.ru/Gateway.aspx')
    service = client.getService('MafiaAMF.AMFService')
    params1 = {
        "userId":"124520",
        "ServerVersion":sid,
        "SystemID":"1",
        "sig":"d6b9ab24005cf6447de56d505f09b9a9"
    }
    resp = service.dispatch(params1,"AMFService.ClanFightInfoGet",[{"BattleDBID":bid,"IsArchive":False}],False)
    if resp.has_key("data"):
        data = resp["data"]
    if data.has_key("Answer"):
        data = data["Answer"]
    if data.has_key("OtherData"):
        data = data["OtherData"]
    if data.has_key("ClanFightInfo"):
        data = data["ClanFightInfo"]
    if data != {}:
        changeInfo("ActorPlayers")
        changeInfo("TargetPlayers")

def getBattlesData():
    data = []
    client = RemotingService('http://dracula.irq.ru/Gateway.aspx')
    service = client.getService('MafiaAMF.AMFService')
    params1 = {
        "userId":"124520",
        "ServerVersion":sid,
        "SystemID":"1",
        "sig":"d6b9ab24005cf6447de56d505f09b9a9"
    }
    resp = service.dispatch(params1,"AMFService.ClanFightListGet",[{}],False)
    if resp.has_key("data"):
        data = resp["data"]
    if data.has_key("Answer"):
        data = data["Answer"]
    if data.has_key("OtherData"):
        data = data["OtherData"]
    if data.has_key("ClanWarsList"):
        data = data["ClanWarsList"]
    return data

bid = getBattlesData()[0]["BattleDBID"]
print bid
while True:
    pause = 3
    try:
        getData()
    except:
        print sys.exc_info()
        pause = 10
        try:
            bids = getBattlesData()[0]
            if bids["Winner"] == 0:
                bid = bids["BattleDBID"]
        except: None
    time.sleep(pause)