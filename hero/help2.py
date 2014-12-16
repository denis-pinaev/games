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


flist = [132632,329928,468013,496927,530108,592748,692795,723744,1627903,2403566,2708950,2869356,3170578,3734193,4347915,5118753,5241205,5387937,6514823,6560231,7903579,7915776,8179365,8566490,8736378,8749938,8987009,9206725,9341741,9392539,9424008,9499004,9644769,9894033,10718243,11053780,11305565,11965096,12755661,13098855,13152947,13395611,14035499,14224268,14533893,15413831,16043596,16761855,16871947,17023961,17162713,17382317,17422893,17691114,18876916,19014303,19113008,19760748,20142646,20407976,20630701,20633660,20937032,21016658,21519264,21786917,22064186,23594947,23741356,24231444,25497481,25797354,25854580,26918757,27183629,27624723,28884255,29082725,29431585,30243624,30565250,30816560,30895563,31004429,31130678,34021628,34789042,35006200,36257975,36407089,36729742,37256323,38763856,41284572,42456673,43522563,44292155,44801587,44969059,44994658,45979811,45991619,47654405,48558476,49431572,49809104,50058220,50343454,50512699,50958901,51120456,52270836,52437466,52475078,53271978,53335080,54632263,55000391,56518190,57056018,57338036,58092404,58394843,58875647,61038750,61191438,61340139,61435823,62290506,62341276,62760925,63636599,63859901,63901181,64313020,64594350,65857702,67455135,67710649,68487257,68488601,69326845,69606968,70095023,70519592,70781016,71735203,71783027,73940623,74288379,77096122,80529255,80789158,83011751,83069736,83224110,83480220,83547135,83588143,85419113,85496679,85551277,86453539,88413981,90673228,93902559,94808760,95556771,96160290,96199352,96744740,97486212,98345220,99142096,100556464,102137300,102281053,102560659,103183256,103493958,104020444,105864917,106027668,106358745,107402663,108534050,109076837,109176858,110148826,113271938,114233049,115082614,116665874,119252625,119303167,119477323,120530710,120810345,120865611,120963756,121510823,122209535,122266608,122627336,123565811,124383155,124604020,126909884,128536641,129394676,129452010,130871038,131314980,131332008,131784365,132287081,133063604,133072913,133283584,133469331,133678038,134142969,134147546,134314962,134697532,134996744,135031266,135362101,136068197,136964337,137192925,137503634,137558706,137710078,138334828,139092072,139372637,139532379,139579081,139616837,139784702,140195486,140226446,141522799,141565930,144338570,144536559,144867292,145043617,145415421,146069561,146383021,147155327,147304282,149304852,150394921,151977002,152441711,152643306,152754106,152825775,153222450,153674315,154151479,154238971,154560085,154708269,155355252,155592883,155748691,155908147,155929378,156721888,157135205,159662551,160347878,160511757,160561410,160728652,160863482,160973857,161471833,161609348,161702967,162556806,163653935,164354909,164859500,164868357,165373921,165573617,166076867,166389268,166419079,166662991,166924744,167693322,167847211,168084841,168247618,168410848,169259075,169306132,169671111,169768611,169837798,170010264,170375364,170578951,170681099,171202825,171324743,171471867,171976738,172752002,173695053,174542972,176393154,177682770,179331321,179499220,179891467,182419863,183296643,183483814,183819509,184392760,184753776,184936300,185150252,185825131,185957394,187361625,188299327,189811701,190542202,190930989,191381524,191876744,192132997,192722279,193190907,195668529,196086079,197047361,197305999,197485205,200139667,200544784,201418508,201983999,202691385,202787673,203083569,203772836,203803991,204029222,204246376,204382809,205424150,205903530,206077444,206945421,206972355,208368497,208374113,208545824,208782248,208802423,209439036,212240319,214407618,215526318,215608963,215810654,215829651,216900740,217552037,217594541,217858589,218291628,218607202,218661879,219260547,219341415,220849636,221055216,227897529,231451036,233828632,235757723,236031808,238896103,241116746,243964884,244124816,247488309,248644631,249384478,257227153,259050436,260038322,263469702,264084214]


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
