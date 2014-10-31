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
random	387076316
viewerId	124520
params	eNqrVspMUbIy0FEqLkksSVWyMtRRKikGUiaGJiZGphaGZrUApYQJBQ==
appId	4375733
authKey	9037dffa6247a0c12e6846044660d736
request	changeSquadState
''')

req.append('''
random	244564434
viewerId	124520
params	eNpdi7ENgDAMBHf5OiDbsRPkbZCgoE6KIMTuOC3d3+n+wYAvdbWE64BTwg2Xia3v/Yyd0BuclVXFNi7BYyZiRoWqaK6SlUPHc/l7Ku8Hnq0W/A==
appId	4375733
authKey	9037dffa6247a0c12e6846044660d736
request	changeSquadState
''')

req.append('''
random	337078583
viewerId	124520
params	eNpdi0EOQDAUBe/y1iXt96v1lw5g4wQNInZoJUTcXWNpOZmZGyeESuucJ83eONKaba2wjBCtcEGKv2anEFNIE6RSSBFi2DCT9Wwy73O/HSHvVH/UrUMbYo6b5wWUFRvk
appId	4375733
authKey	9037dffa6247a0c12e6846044660d736
request	changeSquadState
''')

req.append('''
random	388165203
viewerId	124520
params	eJzVlNtuwyAMht/F16jCQAjkDfYMVTXRjC2RmoNy2FpFefc5aEuzlYvdtbtC+W3jz47xBL721QWyCbrm2Aw9ZPsJCu9OQwEZZ1C+0DGzGw0jmohoMqKpiJbMh5nBq4DMcC13WhqFWqAQXJGMdLlE1DujhVDcWBQkL7SoUKk0TZVmMNblVwHDpfVPS3YGuWtdXg5UorWcU7aTf/enkNd1VfAO7KtBzQcGx6Ye++eiXe3yp/2bHq21DD6ufnrjx24lCiUSQdnOFLztbxzZPAyyDMhm8/ejxI8GjGIzm3/r8RJM01W5fpmve5VwDsr6hP4ZOm6fepwdf7GHLbCWcD/ya/8WJbxPBp3vm7HLfb9syjdHh02UJrCxc3U5Vut35QdHt1laYMk8fwLsPpBQ
appId	4375733
authKey	9037dffa6247a0c12e6846044660d736
request	battleResults
''')

req.append('''
random	105794554
viewerId	124520
params	eNqrVspMUbIy0FEqKVayMjQxNDExMrA0AvKLSxJLUoEytQCZHAj7
appId	4375733
authKey	9037dffa6247a0c12e6846044660d736
request	changeSquadState
''')

count = 1
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
    for p in req:
        params = readParams(p)
        sendRequest(params)
        #time.sleep(1)
        
for i in range(count): print i; battle()