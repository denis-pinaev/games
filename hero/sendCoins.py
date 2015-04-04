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


persons = [
              {"pid":"124520","auth":"1e365d477c3207804013abaddbb6a0c4","gid":0,"sid":""},#corc
              {"pid":"194459289","auth":"e1fc9071463c5a1bad148235fbb4fbfc","gid":0,"sid":""},#LOH1
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
              {"pid":"191288670","auth":"db466f4da075a381d7bb0e21101255b4","gid":0,"sid":""},#ivan malinin bot
              {"pid":"190850909","auth":"67531b4203e16d19611db56645c42aec","gid":0,"sid":""},#ivan malinin bot
              {"pid":"74163736","auth":"8943b2c7e241b1a97342d3c87346de23","gid":0,"sid":""},#NAZAR
              {"pid":"6432236","auth":"f51966179add0bc14b234ca5d7de9211","gid":0,"sid":""},#KUUSAMO
              {"pid":"68487257","auth":"4f66fe9422f3b5f17ab1e90ce34a42d3","gid":0,"sid":""},#Nagaina
              {"pid":"144536559","auth":"731331d4e19d1f5483acd67abf424b58","gid":0,"sid":""},#polya
              {"pid":"29431585","auth":"55f56ea187574da9b2ed69474db78ac0","gid":0,"sid":""},#natali_vlasova
              {"pid":"218661879","auth":"4a7a2ac0efcadd1a42499e34ed217e8b","gid":0,"sid":""},#nikita
              {"pid":"179499220","auth":"49e1540eb72f701a7c0924054ef10fc1","gid":0,"sid":""},#yura
              {"pid":"169768611","auth":"9bc9bdd4929458a2108f1ae419906f66","gid":0,"sid":""},#lenaSv
              {"pid":"73940623","auth":"9ba0d48c2a9b701ffa031504b5232451","gid":0,"sid":""},#VitaShani
              {"pid":"161702967","auth":"a5738509fb8e7486b45e8ba01436c6bb","gid":0,"sid":""},#mari kremer
              {"pid":"114233049","auth":"b2c5894ec83e287b4c2563402b064248","gid":0,"sid":""},#ivan malinin
              {"pid":"11305565","auth":"40328e38ddaac299a62bafe98d4cfaac","gid":0,"sid":""}#Oleg bosyak
          ]

actionCommand = 'Knights.doAction'

init_log("hero_send_coins_log")

ctr = int(random.random()*10000)

def getCTR():
    global ctr
    ctr += 1
    return str(ctr)
 

#send present: {modules:{holidays:{sentCoins:{id:1}}}}
#data	{"module":"holidays","ctr":2,"data":{"list":["9894033","144536559","11305565"],"name":"dreamscape"},"sessionKey":"542020e730cfc8.30775803","moduleMethod":"sendCoin","method":"moduleDoAction"}
def sendGift(pid):
    global sid, gid, service, method
    service = actionCommand
    method = 'moduleDoAction'
    init_params(nsid=sid, ngid=gid, nservice=service, nmethod=method)
    #dataString = '{"active":{"%s":null},"ctr":%s,"sessionKey":"%s","method":"%s","order":[%s],"stat":{"exercises":[[%s,0]]},"completed":{"%s":1},"resources":{}}' % (q,getCTR(),sid,method,restq,q,q)
    dataString = '{"module":"holidays","ctr":%s,"data":{"list":["%s"],"name":"dreamscape"},"sessionKey":"%s","moduleMethod":"sendCoin","method":"%s"}' % (getCTR(),pid,sid,method)
    params = createData(method, dataString)
    log("%s:%s %s" % (service, method, json.dumps(params)))
    resp = sendRequest(service, params)
    o = json.loads(resp["data"])
    error = o["error"]
    if error == 0:
        log("sendCoin to %s done" % pid, True)
    else:
        log(resp["data"], True)
    return o


if True:
    for pers in persons:
        pid = pers['pid']
        auth = pers['auth']
        gid =  pers['gid']
        sid =  pers['sid']
        data, gid, sid = init(pid, auth)
        pers['gid'] = gid
        pers['sid'] = sid
        pid = pers['pid']
        auth = pers['auth']
        gid =  pers['gid']
        sid =  pers['sid']
        
        send = 0
        try:
            print 'level = '+str(data['player']['level'])
            if int(data['player']['level'])>9:
                coins=data['modules']['holidays']['sentCoins']
                send = len(coins)
                print coins
            if send<3: sendGift("124520")
#            if send<2: sendGift("144536559")
        except: print 'error '+pid

'''
data:{"data":{"gift":1,"ids":["70095023"]},"sessionKey":"54f822a5c0c8e8.39426663","v":"4582","module":"FriendsGifts","moduleMethod":"sendGift","ctr":3,"method":"moduleDoAction"}
cmd:Knights.doAction
sig:2827210758
pid:124520
gid:999038
'''