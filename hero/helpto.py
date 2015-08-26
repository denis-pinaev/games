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
lim = 31
if len(sys.argv) > 3:
    lim = int(sys.argv[3])



persons = [
              {"pid":"124520","auth":"1e365d477c3207804013abaddbb6a0c4","gid":0,"sid":""},#corc
              {"pid":"194459289","auth":"e1fc9071463c5a1bad148235fbb4fbfc","gid":0,"sid":""},#LOH1
              {"pid":"191288670","auth":"db466f4da075a381d7bb0e21101255b4","gid":0,"sid":""},#ivan malinin bot
              {"pid":"190850909","auth":"67531b4203e16d19611db56645c42aec","gid":0,"sid":""},#ivan malinin bot
              {"pid":"191291100","auth":"76c06116794fa041156ac0014f8a6d18","gid":0,"sid":""},#Ivan bot1
              {"pid":"10700095","auth":"ae8c0a04a4fe4e9a909e17aa45cd6fd3","gid":0,"sid":""},#mariKr_bot
              {"pid":"133569922","auth":"994c8cc961e087a786c64694c886fcaa","gid":0,"sid":""},#lenaSv_bot
              {"pid":"107402663","auth":"81ac464a55f116dcd1c0441c4e11cb49","gid":0,"sid":""},#alex black
              {"pid":"155908147","auth":"38e6c4c6f1a3ca43a78a6c499879ba7e","gid":0,"sid":""},#margo
              {"pid":"156721888","auth":"fd0f8ffff11ba378e7bdae6a64e2bb1b","gid":0,"sid":""},#podolskaya irina
              {"pid":"108534050","auth":"be89b8b65bf6faea7d8a1a679f9b05db","gid":0,"sid":""},#vlad
              {"pid":"120865611","auth":"ae8affc607866e40cd1f1b312bb69fda","gid":0,"sid":""},#elina-zp
              {"pid":"151977002","auth":"8fd177f25f5bd712eec60421deab2899","gid":0,"sid":""},#anna-maria
              {"pid":"329928","auth":"3537936f4b228959fa759ce2508574fd","gid":0,"sid":""},#sveta
              {"pid":"102137300","auth":"e78c0aad90f427b06653067a45de6c6b","gid":0,"sid":""},#corcc
              {"pid":"47654405","auth":"8868f86742f95fe034b6b04da48f5ac4","gid":0,"sid":""},#tregub
              {"pid":"160511757","auth":"6dc2dba90c1cc9d935542aa6a60c6fb4","gid":0,"sid":""},#vasya tanakan
              {"pid":"163834109","auth":"36a870e45af6041189b3e6905945d6e7","gid":0,"sid":""},#bot_elina1
              {"pid":"153969376","auth":"9707e9bc5f45e2bd45d5d73dfbb768db","gid":0,"sid":""},#bot_elina1
              {"pid":"84324359","auth":"b61b0e2d2757946edcca304e6bdc853b","gid":0,"sid":""},#bot_elina1
              {"pid":"173550501","auth":"5ca7913de53548ac794d541672ce9e8b","gid":0,"sid":""},#bot_elina1
              {"pid":"34688001","auth":"fc8c2f798036ef2af8bbd6fbc312f7fb","gid":0,"sid":""},#botelina1
              {"pid":"233828632","auth":"3cf7aac00f56163404482ed0550eb1dc","gid":0,"sid":""},#misha_zhukov7
              {"pid":"101053386","auth":"77a9e62eed9e7d25866efd2c8aeef30e","gid":0,"sid":""},#misha_zhukov6
              {"pid":"124678851","auth":"f659c32017ecad7b4d36b862f68351ef","gid":0,"sid":""},#misha_zhukov5
              {"pid":"182933786","auth":"662b4add4856bc946f65e70d9254c862","gid":0,"sid":""},#misha_zhukov4
              {"pid":"209559126","auth":"02e68b3110fbeac985c6846649e3cee2","gid":0,"sid":""},#misha_zhukov3
              {"pid":"200139667","auth":"0be685ed1b3787bc144ef88cf0d2de1d","gid":0,"sid":""},#misha_zhukov2
              {"pid":"199648989","auth":"14279d90af4c929b3f645e777e6b30fb","gid":0,"sid":""},#misha_zhukov1
              {"pid":"56518190","auth":"22f411e60eebd913b689b19705900ab2","gid":0,"sid":""},#ulia
              {"pid":"93902559","auth":"d40ce5e63d99e92fd57859c7be81729c","gid":0,"sid":""},#vadimbot0
              {"pid":"217858589","auth":"8b9107a32674785b79463d5585ec4918","gid":0,"sid":""},#vadimbot1
              {"pid":"65706308","auth":"a889a08c37aa0430b62ae6a5928e6950","gid":0,"sid":""},#vadimbot2
              {"pid":"217752865","auth":"bc8251178d92e9f671d7f23f19fbb4a7","gid":0,"sid":""},#vadimbot3
              {"pid":"107564843","auth":"81af0508db36b84e869e2b77a9b4a142","gid":0,"sid":""},#vadimbot4
              {"pid":"107738176","auth":"3194740fd9573509f0d3c523be6e4541","gid":0,"sid":""},#vadimbot5
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
              {"pid":"208142478","auth":"717417917b86a9c7803e57b08d2f2c93","gid":0,"sid":""},#natali_bot
              {"pid":"187983220","auth":"780ab57c2e9d076af714a03c5af687d0","gid":0,"sid":""},#some_bot
              {"pid":"187982281","auth":"1a352b0edca4bd66d8353bcacf43faf0","gid":0,"sid":""},#some_bot
              {"pid":"6432236","auth":"f51966179add0bc14b234ca5d7de9211","gid":0,"sid":""},#KUUSAMO
              {"pid":"70711104","auth":"8cb2770434df20b95841e497ceace746","gid":0,"sid":""}#Mitya
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
    #log("%s:%s %s" % (service, method, json.dumps(params)))
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
    #log("%s:%s %s" % (service, method, json.dumps(params)))
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
flist = []#"144536559", "9894033" ,"29431585", "106358745", "56518190", "218661879", "217858589"]
person = 0
#flist = ['56518190']#ulia
#flist = ['218661879']#nikita
#flist = ['217858589']#vlad
sendSTR = ''


#persons = persons[:36]

flist_dop = ["201099159","181091930","157598696","203144892",    "93902559","144536559","9894033","70711104","20633660","56518190", "218661879", "106358745","217858589","29431585", '65857702','23594947','11305565','50958901','159662551','73940623','114233049','161702967','179331321','692795','31568442','13721794','52437466','35006200','179499220','79670506','203263126','196086079','151253340','202787673','169768611','9499004','29431585']

if start_p>1:
    flist = flist_dop
    #flist = ['161702967']#comment!
    if end_p != 999:
        flist = [str(end_p)]
        flist_dop = []
    persons = persons[:lim]

if start_p>2:#misha;
    flist = ['49809104'];
    flist_dop = []
    persons = persons_misha
    

#f = flist[person]

#comment below!
#sendSTR = '828'
#flist = ['144536559']
#persons = persons[:18]

#if True:
i = 0
total = len(persons)
flist = flist + flist_dop
while i<total:
    pers = persons[i]
    pid = pers['pid']
    auth = pers['auth']
    gid =  pers['gid']
    sid =  pers['sid']
    data, gid, sid = init(pid, auth)

    i += 1
    j = 0
    for f in flist:
        if f in flist_dop and i>lim: continue
        j = j + 1
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
    
