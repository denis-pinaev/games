import hashlib
import requests
import time
import sys

data_init = {
'format':'json',
'sig':'9f8063c7ef3a0a9bb588bad7ff24b3dc',
'flashvars':'{"auth_key":"7407366522de227fab8b092baba5e476","hash":"","user_id":"124520","pf_version":"177","referrer":"unknown","pf_language":"ru","viewer_id":"124520"}',
'time':'0',
'method':'init'
}


data_test = {
'format':'json',
'from':'300',
'flashvars':'{"auth_key":"7407366522de227fab8b092baba5e476","hash":"","user_id":"124520","pf_version":"177","referrer":"unknown","pf_language":"ru","viewer_id":"124520"}',
'sid':'436',
'method':'contacts',
'sig':'2bbff918ba49f3be803e77970a4e931a',
'uid':'44211',
'action':'get',
'time':'1395743902'
}


data_start_level = {
'format':'json',
'uid':'44211',
'time':'1395757066',
'sid':'438',
'method':'level',
'action':'start',
'boost_ids':'',
'sig':'e2c0f96c298c7f49bfe75e40f5e51a2f',
'flashvars':'{"auth_key":"7407366522de227fab8b092baba5e476","pf_version":"177","user_id":"166794948","pf_language":"ru","hash":"","referrer":"unknown","viewer_id":"124520"}',
'level_id':'1'
}

data_end_level = {
'format':'json',
'uid':'44211',
'sig':'512931e99bacc0417e07a471e27cb56e',
'time':'1395757099',
'sid':'438',
'action':'complete',
'complete':'yes',
'point':'7080',
'level_id':'1',
'flashvars':'{"auth_key":"7407366522de227fab8b092baba5e476","pf_version":"177","user_id":"166794948","pf_language":"ru","hash":"","referrer":"unknown","viewer_id":"124520"}',
'method':'level'
}

data_virality = {
'action_id':'0',
'flashvars':'{"auth_key":"7407366522de227fab8b092baba5e476","hash":"","user_id":"124520","pf_version":"177","referrer":"unknown","pf_language":"ru","viewer_id":"124520"}',
'sig':'76abdfc39b880bfaa9fe815652af1458',
'sid':'442',
'method':'virality',
'format':'json',
'uid':'44211',
'action':'status',
'time':'1395772445'
}


#auth_key = '7407366522de227fab8b092baba5e476'
auth_key = 'fe60c3f5c077d9cf53824c0be6f3b3ab'


def sendRequest(command, params):
    url = 'http://indikot-vk.playflock.com/game.php'
    resp = requests.post(url, data=params, allow_redirects=True)
    txt = resp.text
    if 'error' in txt:
        print txt
        time.sleep(9999)


def getSig(string, key):
    return hashlib.md5(string+key).hexdigest()
    
def getTime():
    return str(int(time.mktime(time.localtime())))
   
   
def sortParams(data):
    pl = []
    for p in data:
        if p == 'sig': print 'sig was', data['sig'];continue
        pl.append(p+'='+str(data[p]))
    pl.sort()
    return "".join(pl)
    
    
def startLevel(level):
    data = data_start_level
    data['level_id'] = str(level)
    data['time'] = getTime()
    data['sid'] = sid
    sd = sortParams(data)
    sig = getSig(sd, auth_key)
    data['sig'] = sig
    sendRequest('', data)
   
def endLevel(level, point):
    data = data_end_level
    data['level_id'] = str(level)
    data['point'] = str(point)
    data['time'] = getTime()
    data['sid'] = sid
    sd = sortParams(data)
    sig = getSig(sd, auth_key)
    data['sig'] = sig
    sendRequest('', data)
   
def virality():
    data = data_virality
    data['time'] = getTime()
    data['sid'] = sid
    sd = sortParams(data)
    sig = getSig(sd, auth_key)
    data['sig'] = sig
    sendRequest('', data)
   
level = 1
point = 7891
sid = 444

if len(sys.argv) > 1:
    level = sys.argv[1]

if len(sys.argv) > 2:
    point = sys.argv[2]

if len(sys.argv) > 3:
    sid = sys.argv[3]
    
startLevel(level)
endLevel(level,point)
virality()