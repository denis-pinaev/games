import binascii
import sys
import json
import datetime
import time
import random
import requests
from common import *
service = ''
method = ''


flist = [329928,468013,530108,723744,781347,1627903,2258045,2593701,2869356,3734193,5118753,5387937,6094809,6514823,6560231,7903579,7915776,8179365,8566490,8736378,8749938,8987009,9206725,9340436,9341741,9392539,9424008,9499004,9644769,9894033,11053780,13395611,13657474,13682347,14035499,14533893,15413831,15958677,16761855,16871947,17023961,17382317,17422893,17597867,17691114,17869508,18876916,19113008,20407976,20630701,20749920,21125851,21519264,21786917,22064186,23741356,24228206,25497481,25797354,25910703,26918757,27624723,29082725,29431585,29561030,30243624,30816560,30895563,31004429,31130678,31609701,34789042,35006200,35173024,36257975,36407089,36729742,37382223,38763856,41476261,42456673,43522563,44292155,44801587,45979811,45991619,47654405,48558476,49431572,49809104,50058220,50343454,50370359,50512699,51120456,51929816,52270836,52437466,54632263,55000391,55919900,57338036,58394843,58875647,58915036,58953401,59748772,60049738,61191438,61272675,61340139,62290506,62341276,62760925,63636599,63859901,63901181,64020001,64313020,64806698,66376526,67455135,67710649,68487257,69326845,69606968,70095023,70519592,70781016,71783027,73940623,74160220,74288379,74301509,76804953,80529255,80789158,83011751,83480220,83588143,85419113,85496679,85551277,86231630,86453539,88413798,93902559,94657370,94808760,96160290,96199352,98345220,98890676,99142096,100556464,102137300,102281053,102560659,104020444,105864917,106027668,106358745,107402663,107548914,108534050,110148826,110378065,113271938,113498289,114233049,115082614,115450084,116189705,118968807,119303167,120530710,120865611,120963756,121510823,121534477,122209535,122266608,122627336,123565811,124578041,124678851,126909884,128629575,130871038,131314980,131332008,131560152,131784365,132287081,133063604,133283584,133469331,133678038,134147546,134314962,134697532,134790186,134851573,134996744,135362101,135704016,136964337,137503634,137558706,137582371,137710078,138253629,138334828,138404751,138450680,139046492,139092072,139141886,139372637,139532379,139579081,139616837,139784702,140160953,140195486,141565930,142838011,143375730,143515909,144338570,144536559,144867292,145415421,146069561,146383021,147155327,147796570,149304852,150394921,150677716,150854089,151757834,151977002,152441711,152643306,152754106,152825775,153222450,153949465,154151479,154346731,154708269,155355252,155748691,155908147,155929378,156721888,156857008,159662551,160347878,160511757,160561410,160728652,160973857,161471833,161609348,161702967,162556806,164859500,165573617,165813444,166076867,166389268,166419079,166662991,166924744,167693322,167847211,168247618,169259075,169306132,169671111,169768611,169837798,170010264,170375364,170465393,170681099,171202825,171324743,171471867,171505982,171895829,171976738,173695053,174542972,176575416,177682770,177852802,179437656,179499220,182419863,183483814,184101062,184936300,185150252,185825131,185957394,186282895,189811701,190542202,190930989,191381524,191876744,192649336,193114664,193190907,195668529,196086079,196645066,197047361,197305999,197485205,198764553,200139667,200651449,201418508,202691385,202787673,203083569,203772836,203803991,204246376,204382809,206077444,206972355,208374113,208545824,208802423,209439036,214407618,215526318,215608963,215810654,216900740,217594541,218291628,218661879,219260547,219341415,220849636,221055216,232588432,233828632,235757723]


person = 0
error = 0

persons = [
              {"pid":"124520","auth":"1e365d477c3207804013abaddbb6a0c4","gid":0,"sid":""},#corc
          ]

pid = persons[person]["pid"]
auth = persons[person]["auth"]
gid = 0
sid = ''
data = ''
actionCommand = 'Knights.doAction'

init_log("help_priority")

    
ctr = 0
def getCTR():
    global ctr
    ctr += 1
    return str(ctr)
    
def getWorld(pers):
    global sid, gid, service, method
    service = actionCommand
    method = 'friendsGetWorld'
    init_params(nsid=sid, ngid=gid, nservice=service, nmethod=method)
    dataString = '{"rnd":%s,"friendId":"%s","ctr":%s,"sessionKey":"%s","method":"%s"}' % (getRandom(), pers, getCTR(), sid, method)
    params = createData(method, dataString)
    log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("getWorld %s done" % pers, True)
    else:
        log(resp["data"], True)
    return o

def sendHelp(pers, hbid):
    global sid, gid, service, method
    service = actionCommand
    method = 'friendHelpApply'
    init_params(nsid=sid, ngid=gid, nservice=service, nmethod=method)
    dataString = '{"friendId":"%s","list":[%s],"rnd":%s,"ctr":%s,"sessionKey":"%s","method":"%s"}' % (pers, hbid, getRandom(), getCTR(), sid, method)
    params = createData(method, dataString)
    log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("friendHelpApply done", True)
    else:
        log(resp["data"], True)        


no_help = []
nohf = ''
while len(flist)>0:        
    pers = persons[person]
    pid = pers['pid']
    auth = pers['auth']
    gid =  pers['gid']
    sid =  pers['sid']
    
    
    data, gid, sid = init(pid, auth)

    total = len(flist)
    i = 0
    left_arr = []
    while i<total:
        if len(nohf)>1: no_help = no_help + [nohf]; print "add to NO HELP arr"
        nohf = ''
        max_help = 5
        f = str(flist[i])
        nohf = f
        i += 1
        print "%d/%d (%d%%)" % (i, total, int(100*i/total))
        try: w = getWorld(f)
        except: continue
        if w["friend"].has_key("currentBuildingHelp"):
            ll = 5 - len(w["friend"]["currentBuildingHelp"])
            if ll<=0: nohf = '';continue
            max_help = ll
            try:
                qqq = ''
                for p in w["interaction"]: qqq = p;break
                ll = 5 - w["interaction"][qqq]["help"]
                if ll<=0: nohf = '';continue
                max_help = ll
            except: log("fail get count "+str(f))
        bbb = get_buildings_ids(w["friend"]["entities"])
        bk = []
        if w["friend"].has_key("recipes") and len(w["friend"]["recipes"])>0 and w["friend"]["recipes"].has_key("entities"):
            bk=get_help_string(w["friend"]["recipes"]["entities"],bbb,5)[:max_help]
        if len(bk) == 0: continue
        hs = ','.join(str(x) for x in bk)
        print hs
        if max_help>len(bk): left_arr = left_arr+[f]; print "add to left arr"
        sendHelp(f, hs)
        nohf = ''
            
    log('left_arr')
    log(','.join(str(x) for x in left_arr))
    flist = left_arr
    
if len(nohf)>1: no_help = no_help + [nohf]
for f in no_help:
    sendHelp(f, '1,2,3,4,5')
