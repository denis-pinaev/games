import binascii
import pyamf
import sys
import json
import datetime
import time
import random
import requests
service = ''
method = ''

from common import *


flist = ["144536559", "9894033", "106358745", "49809104"]


person = 0#old!
error = 0
start_p = 1
end_p = 999
if len(sys.argv) > 1:
    start_p = int(sys.argv[1])
if len(sys.argv) > 2:
    end_p = int(sys.argv[2])



persons = [
              {"pid":"124520","auth":"1e365d477c3207804013abaddbb6a0c4","gid":0,"sid":""},#corc
              {"pid":"133569922","auth":"994c8cc961e087a786c64694c886fcaa","gid":0,"sid":""},#lenaSv_bot
              {"pid":"208142478","auth":"717417917b86a9c7803e57b08d2f2c93","gid":0,"sid":""},#natali_bot
              {"pid":"120625669","auth":"ff4c8063867f8b0df25fe96c7312d4d9","gid":0,"sid":""},#natali_bot
              {"pid":"111056787","auth":"ee75147a807484c815258d2beda7e4a3","gid":0,"sid":""},#natali_bot
              {"pid":"109934285","auth":"868a37525ac84e4195c85dd57aa24f07","gid":0,"sid":""},#natali_bot
              {"pid":"159451467","auth":"63611fcf4e9ec3466d7259158ce5b0f7","gid":0,"sid":""},#natali_bot
              {"pid":"134074215","auth":"eff7d223bd5695b4a8807902ed685fb4","gid":0,"sid":""},#natali_bot
              {"pid":"94808760","auth":"f5f30b3699376a2a34b9fc424a591307","gid":0,"sid":""},#natali_bot
              {"pid":"111495157","auth":"1fff1fe0698b494788270a883ba52c8b","gid":0,"sid":""},#natali_bot
              {"pid":"35179586","auth":"e2af60b040cb4c01490cef03fb0f2cb8","gid":0,"sid":""},#natali_bot
              {"pid":"28870526","auth":"7c56adad15a4d20c8566446be2723c91","gid":0,"sid":""},#natali_bot
              {"pid":"174398476","auth":"5d533104367202f9146c4ffa977142ac","gid":0,"sid":""},#natali_bot
              {"pid":"138528401","auth":"90d8a99bd708e79929c1cebbf62616cc","gid":0,"sid":""},#natali_bot
              {"pid":"134442962","auth":"772ceea1fac3cf2db57962d076757eb5","gid":0,"sid":""},#natali_bot
              {"pid":"163834109","auth":"36a870e45af6041189b3e6905945d6e7","gid":0,"sid":""},#bot_elina1
              {"pid":"153969376","auth":"9707e9bc5f45e2bd45d5d73dfbb768db","gid":0,"sid":""},#bot_elina1
              {"pid":"84324359","auth":"b61b0e2d2757946edcca304e6bdc853b","gid":0,"sid":""},#bot_elina1
              {"pid":"187983220","auth":"780ab57c2e9d076af714a03c5af687d0","gid":0,"sid":""},#some_bot
              {"pid":"187982281","auth":"1a352b0edca4bd66d8353bcacf43faf0","gid":0,"sid":""},#some_bot
              {"pid":"102137300","auth":"e78c0aad90f427b06653067a45de6c6b","gid":0,"sid":""},#corcc
              {"pid":"160511757","auth":"6dc2dba90c1cc9d935542aa6a60c6fb4","gid":0,"sid":""},#vasya tanakan
              {"pid":"107402663","auth":"81ac464a55f116dcd1c0441c4e11cb49","gid":0,"sid":""},#alex black
              {"pid":"108534050","auth":"be89b8b65bf6faea7d8a1a679f9b05db","gid":0,"sid":""},#vlad
              {"pid":"155908147","auth":"38e6c4c6f1a3ca43a78a6c499879ba7e","gid":0,"sid":""},#margo
              {"pid":"47654405","auth":"8868f86742f95fe034b6b04da48f5ac4","gid":0,"sid":""},#tregub
              {"pid":"156721888","auth":"fd0f8ffff11ba378e7bdae6a64e2bb1b","gid":0,"sid":""},#podolskaya irina
              {"pid":"120865611","auth":"ae8affc607866e40cd1f1b312bb69fda","gid":0,"sid":""},#elina-zp
              {"pid":"151977002","auth":"8fd177f25f5bd712eec60421deab2899","gid":0,"sid":""},#anna-maria
              {"pid":"329928","auth":"3537936f4b228959fa759ce2508574fd","gid":0,"sid":""},#sveta
              {"pid":"173550501","auth":"5ca7913de53548ac794d541672ce9e8b","gid":0,"sid":""},#bot_elina1
              {"pid":"34688001","auth":"fc8c2f798036ef2af8bbd6fbc312f7fb","gid":0,"sid":""},#botelina1
              {"pid":"6432236","auth":"f51966179add0bc14b234ca5d7de9211","gid":0,"sid":""},#KUUSAMO
              {"pid":"68487257","auth":"4f66fe9422f3b5f17ab1e90ce34a42d3","gid":0,"sid":""},#Nagaina
              {"pid":"144536559","auth":"731331d4e19d1f5483acd67abf424b58","gid":0,"sid":""},#polya
              {"pid":"218661879","auth":"4a7a2ac0efcadd1a42499e34ed217e8b","gid":0,"sid":""}#nikita
          ]
persons_misha = [
              {"pid":"124520","auth":"1e365d477c3207804013abaddbb6a0c4","gid":0,"sid":""},#corc
              {"pid":"102137300","auth":"e78c0aad90f427b06653067a45de6c6b","gid":0,"sid":""},#corcc
              {"pid":"160511757","auth":"6dc2dba90c1cc9d935542aa6a60c6fb4","gid":0,"sid":""},#vasya tanakan
              {"pid":"155908147","auth":"38e6c4c6f1a3ca43a78a6c499879ba7e","gid":0,"sid":""},#margo
              {"pid":"49809104","auth":"faeaec9d6c41db027a1f8a2dc7244c38","gid":0,"sid":""},#misha_zhukov
              {"pid":"124678851","auth":"f659c32017ecad7b4d36b862f68351ef","gid":0,"sid":""},#misha_zhukov5
              {"pid":"182933786","auth":"662b4add4856bc946f65e70d9254c862","gid":0,"sid":""},#misha_zhukov4
              {"pid":"209559126","auth":"02e68b3110fbeac985c6846649e3cee2","gid":0,"sid":""},#misha_zhukov3
              {"pid":"200139667","auth":"0be685ed1b3787bc144ef88cf0d2de1d","gid":0,"sid":""},#misha_zhukov2
              {"pid":"199648989","auth":"14279d90af4c929b3f645e777e6b30fb","gid":0,"sid":""},#misha_zhukov1
              {"pid":"233828632","auth":"3cf7aac00f56163404482ed0550eb1dc","gid":0,"sid":""},#misha_zhukov7
              {"pid":"101053386","auth":"77a9e62eed9e7d25866efd2c8aeef30e","gid":0,"sid":""},#misha_zhukov6
              {"pid":"329928","auth":"3537936f4b228959fa759ce2508574fd","gid":0,"sid":""},#sveta
              {"pid":"173550501","auth":"5ca7913de53548ac794d541672ce9e8b","gid":0,"sid":""},#bot_elina1
              {"pid":"34688001","auth":"fc8c2f798036ef2af8bbd6fbc312f7fb","gid":0,"sid":""},#botelina1
              {"pid":"133569922","auth":"994c8cc961e087a786c64694c886fcaa","gid":0,"sid":""},#lenaSv_bot
              {"pid":"6432236","auth":"f51966179add0bc14b234ca5d7de9211","gid":0,"sid":""}#KUUSAMO

             ]
pid = persons[person]["pid"]
auth = persons[person]["auth"]
gid = 0
sid = ''
data = ''
actionCommand = 'Knights.doAction'
init_log("hero_help2_log")
#ctr = 0
ctr = int(random.random()*10000)
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
     

#'103'#altar
#'83'#hram
#'65825'#vadim ars
#'65562'#polya ars#73229,65562,65656,70732,67788

            #polya      vadim1     nataly2     oksana3       ulia4       nikita5      vlad6
flist = ["144536559", "9894033", "29431585"]#, "106358745", "56518190", "218661879", "217858589"]
person = 0
#flist = ['56518190']#ulia
#flist = ['218661879']#nikita
#flist = ['217858589']#vlad
sendSTR = ''

if start_p>1:
    flist = ["106358745", "56518190", "218661879", "217858589",     '215526318','159662551','73940623','114233049','65857702','68487257','31568442','13721794','116189705','35006200','179499220','79670506','203263126','196086079','151253340','202787673','169768611','9499004','29431585']
    flist = ['215526318']#comment!
    if end_p != 999: flist = [str(end_p)]
    persons = persons[:26]

if start_p>2:#misha;
    flist = ['49809104'];
    persons = persons_misha
    

f = flist[person]
j = 0



#if True:
for f in flist:
    j = j + 1
    i = 0
    total = len(persons)
    while i<total:
        pers = persons[i]
        pid = pers['pid']
        auth = pers['auth']
        gid =  pers['gid']
        sid =  pers['sid']
        data, gid, sid = init(pid, auth)

        i += 1
        print "%d/%d (%d%%) | %d/%d (%d%%)" % (i, total, int(100*i/total), j, len(flist), int(100*j/len(flist)))
        
        if len(sendSTR)>1:
            sendHelp(f, sendSTR)
            continue
        
        w = getWorld(f)
        max_help = 5
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
        sendHelp(f, hs)
    
