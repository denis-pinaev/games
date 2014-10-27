# -*- coding: utf-8 -*-

import binascii
import pyamf
import sys
import json
import datetime
import time
import random
import requests
import urllib

def sendRequest0(params):
    url = 'http://titans-vk-sc1.playkot.com/current/server.php'
    resp = requests.get(url, data=params, allow_redirects=True)
    txt = resp.text
    return txt
    
def sendRequest(params):
    url = 'http://titans-vk-sc1.playkot.com/current/server.php?'
    ppp = urllib.urlencode(params)
    url+=ppp
    resp = requests.get(url)
    txt = resp.text
    return txt
    
req = []

req.append('''
params	eNqrViouSSxJVbIy1FEqKQZSJoYmxqYWxiYmOkqZKUpWBrUAqJcJBg==
appId	4375733
viewerId	124520
request	changeSquadState
authKey	9037dffa6247a0c12e6846044660d736
random	647253498
''')

req.append('''
params	eNoViz0OgCAMRu/SGQkfFFp6GxMdnGHQGO9uWd/PSzfZJrEGmoMMDC5VC3Oghywvfh1kKdCY+zwdebgWIKIIuDckMPeiLnxBrB0pu8sqorXx9wOoHxdJ
appId	4375733
viewerId	124520
request	changeSquadState
authKey	9037dffa6247a0c12e6846044660d736
random	408213676
''')

req.append('''
params	eNodyjsOg0AMRdG9uB4Q/mDsKVlAmqxglESILmEGiQix91jp3tU7JxyQO8SeTcTVSNiIB0/QKmQUFB6NJfob2Sspj6rm6JMYTgnWJ+Qh9Lbc3o+51FewBLWVFov/x/2zl1B0/QB3shvK
appId	4375733
viewerId	124520
request	changeSquadState
authKey	9037dffa6247a0c12e6846044660d736
random	485582452
''')

req.append('''
params	eNrN00tugzAQBuC7zNqKPH6HG/QMVVQ51GmQeIlH2whx99qEEBLopsmiOxgPv78x0EFTQ4QCBZeGG0EgeYeIEnC5y04QdVAV+yL0vHZwdDZtjsPy0NWTRQ1XamylxvtdT+CAEAnK5EYjolIazdagJFC5umir2NUB0FY2T9oMIrPlBD5sPV5lrrGpT1fa+Kg2T0blt1f4XWJb2jhp/AyGUn9/AWzVWQAUfIatw/jKz526T5cOvq9yyLkWpsHuSzsCPp8xAs2pdC+hRsBW2crzNDTvi7yt3443+Tithx083szt/MY+ZgFOdK1+l+PsNS02u5LpeQj+uBzZkj5GD2w2sSV9BvtyLIo+blfr9PGHAH498efS5ROO/S4vrIo/I8epZ9aHfWLpk//C5zsOLHy3yDZacy2ZVJwx1f8AWPZ6BQ==
appId	4375733
viewerId	124520
request	battleResults
authKey	9037dffa6247a0c12e6846044660d736
random	86921631
''')

req.append('''
random	140430067
viewerId	124520
request	getUserMap
authKey	9037dffa6247a0c12e6846044660d736
appId	4375733
''')

req.append('''
params	eNqrViouSSxJVbIy0FEqKVayMjQxNDE2tTC2NNFRykwBCtcCAKiwCQo=
appId	4375733
viewerId	124520
request	changeSquadState
authKey	9037dffa6247a0c12e6846044660d736
random	321280642
''')

req.append('''
random	779202955
viewerId	124520
request	checkAttacksOnBase
authKey	9037dffa6247a0c12e6846044660d736
appId	4375733
''')

req.append('''
random	496450792
id	0
action_id	
viewerId	124520
request	purchaseRepair
authKey	9037dffa6247a0c12e6846044660d736
appId	4375733
''')

count = 30
if len(sys.argv) > 1:
    count = int(sys.argv[1])

def readParams(req):
    p_ar = req.split('\n')
    a = {}
    for p in p_ar:
        if p:
            k = p.split()[0]
            v = p.split()[1]
            a[k] = v
    return a

def battle():
    for p in req[:-1]:
        params = readParams(p)
        sendRequest(params)
        #time.sleep(1)
        
for i in range(count): print i; battle()