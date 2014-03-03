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


flist = ["918782","1987501","2416558","5387937","5647484","8378576","9499004","9643705","9644769","9894033","10317563","11744515","11941820","12550355","13392964","13721794","15413831","17597867","20633660","23594947","23696561","23741356","25497481","25596947","29431585","30816560","35006200","36257975","39891066","40878733","43522563","44292155","45991619","49809104","51120456","52437466","55000391","55862518","56518190","59748772","63137923","63901181","65857702","66459154","68487257","73940623","74160220","74806494","76371100","79670506","80789158","88113128","92037271","95069185","96160290","98890676","102137300","102281053","107548914","107929089","110378065","111407093","113880094","114233049","117122651","123565811","126484574","131812626","132281103","132287081","132521220","134147546","135602130","136385925","136936719","139046492","140195486","141565930","142114973","144867292","150936134","151253340","151757834","152094690","152400052","152441711","155355252","155748691","155908147","156536071","156922782","159250578","159662551","161702967","166076867","166662991","166924744","166966602","167289649","168066456","169259075","169306132","169768611","170462428","171202825","171478433","173118026","173385219","176560783","177852802","178865014","178866614","179499220","182419863","182827425","185825131","185957394","186282895","187957443","187982281","187983220","190930989","191261914","191876744","192259232","193132103","197155961","197305999","197485205","198389624","199648989","200139667","202787673","202856374","203083569","203263126","203512422","208374113","208545824","208802423","209439036","214407618","215479511","215526318","215608963","216264996","216872895","217594541","218036812","218291628","218661879","219053664","220415082","220673526","221255204","221471812","225672624","227631552","229820266","232269822","232501305","232502497"]


person = 0
error = 0

persons = [
              {"pid":"144536559","auth":"731331d4e19d1f5483acd67abf424b58","gid":0,"sid":""},#poly
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
