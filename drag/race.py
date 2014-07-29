import requests
import sys
import time

def read(fname):
    fatype = fname
    tfile = open(fatype, "r")
    d = tfile.read()
    tfile.close()
    return d
    

def sendRequest(params, method):
    try:
        url = 'http://nns-prod.elasticbeanstalk.com/api//'+method
        resp = requests.post(url, data=params, allow_redirects=True)
    except:
        print "Error in sendRequest!"
        time.sleep(5)
        return sendRequest(params)
    return bytearray(resp.text, "utf-8")


def readDataFile(fname):
    start_info = read(fname).split('\n')
    info = []
    for i in range(len(start_info)):
        start_info[i] = start_info[i][8+2:8+2+16*3]
        line = start_info[i]
        for j in range(16):
            letter = line[j*3:j*3+2]
            if(letter!="  " and letter!=""): info.append(letter)
    return bytearray.fromhex("".join(info))
    
def getRaceId(resp):
    rid = ""
    i = -1
    isStart = False
    while True:
        c = resp[i]
        if c>=ord('$') and c<=ord('z'):
            isStart = True
            rid = chr(c)+rid
        elif isStart:
            if rid[0:2] == "53":
                return rid
            else:
                isStart = False
                rid = ""
        i = i-1
        if i<-len(resp): return None;
    return rid
    
def getSession(resp):
    rid = ""
    i = -1
    isStart = False
    while True:
        c = resp[i]
        if c>=ord('$') and c<=ord('z'):
            isStart = True
            rid = chr(c)+rid
        elif isStart:
            if rid[0] == "$":
                return rid
            else:
                isStart = False
                rid = ""
        i = i-1
        if i<-len(resp): return None;
    return rid
    
def setRaceId(data, nrid):
    rid = getRaceId(data)
    data = data.replace(rid, nrid)
    return data
    
def setRaceTime(data, rtime):
    pos = 9*16+1
    fd = (rtime>>8) & 0xff
    ld = rtime & 0xff
    data[pos] = fd
    data[pos+1] = ld
    return data
    

def test():
    ba = readDataFile("test")
    #resp = sendRequest(ba, "configuration");
    #print getRaceId(resp)
    print ba+"|"
    ba = setRaceId(ba, "aaazaaa")
    ba = setRaceTime(ba, ord('z')+(ord('!')<<8))
    print ba+"|"


def auth():
    ba = readDataFile("auth")
    ba = sendRequest(ba, "auth")
    return getSession(ba)
    

def start_race(sid, rtype):
    ba = readDataFile(rtype)
    osid = getSession(ba)
    ba = ba.replace(osid, sid)
    ba = sendRequest(ba, "races")
    return getRaceId(ba)

def finish_race(sid, rid, rtime):
    ba = readDataFile("finishrace")
    osid = getSession(ba)
    ba = ba.replace(osid, sid)
    orid = getRaceId(ba)
    #time.sleep(10)
    ba = ba.replace(orid, rid)
    ba = setRaceTime(ba, rtime)
    ba = sendRequest(ba, "races")
    return ba
    
    
# friend # city3liga3 # quick # under14 # racers

sid = None
rid = None
count = 1
rtype = "friend"
if len(sys.argv) > 1:
    rtype = sys.argv[1]
if len(sys.argv) > 2:
    count = int(sys.argv[2])
if len(sys.argv) > 3:
    sid = sys.argv[3]
if len(sys.argv) > 4:
    rid = sys.argv[4]
    count = 1
    
if not sid: sid = auth()
print "session = " + sid
for i in range(count):
    if not rid:
        if sid: rid = start_race(sid, "startrace_"+rtype)
    if sid: print "race_id = " + rid
    if sid and rid: print finish_race(sid, rid, 6771)
    rid = None


