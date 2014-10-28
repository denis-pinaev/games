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
random	915547788
viewerId	124520
params	eNqrVspMUbIy0FEqKVayMjQxNDExMjY0MNdRKi5JLEkFCtUCAJkVCPw=
appId	4375733
authKey	9037dffa6247a0c12e6846044660d736
request	changeSquadState
''')

req.append('''
random	602675342
viewerId	124520
params	eNoVyzEOgDAIheG7MNcGKBTsbUx0cC6Dxnh3cXvJ/70HLhiLVS1w7jCwQEwYJCTCjdAK3DD4zzO2OHKnyAtW6uysKiZqTW1NGmmlomFv3r1LE/T3A33hFvE=
appId	4375733
authKey	9037dffa6247a0c12e6846044660d736
request	changeSquadState
''')

req.append('''
random	481320737
viewerId	124520
params	eNodjEEOwjAMBP/ic1TF9raOc+QBvfQFUVshbkCCBEL8vaHH3dnZL70px4FtFHf4ZNE1sUmg29ZBoFYpMxgQZfT6QxmDJkEysJnCxAPVVtpOWfv+eZ3v66XU/e+deXm8Sj9j/R2aOhv4
appId	4375733
authKey	9037dffa6247a0c12e6846044660d736
request	changeSquadState
''')

req.append('''
random	388165203
viewerId	124520
params	eNrVk+tOwzAMhd/Fv6MpdrKs7RvwDGhCWclYpd7UCzBNfXecsYyOdppAIMGvqsdufD735ABbgiSSRi2MijQaQiKpBbjSFXtIDtBUm6prIbk/wM7ZvNtBIgVkj/wYxETDGY1mNDWj6WE9CPCzUKPWq9VKGwGNa6u+SV3rzRSusznX2etSwJNlcakNCegbW2Z98f46nPyxXGZT7698gDy3vNTHeu6eXX5p+bO0FsAbIZ5mm2LmI/QdH9KmKvv2YXdxPIXNcWfdZKkbQZkY1ZlJmjETIu8VUlvbNOv2/n9JHtDta3c3s3Pmi06OvoGn/jQeKnN79JHnF9F9gOinCeegcATFQ83p7lxBwykaBjR9DU1eooU9x2Zqt7Ctv5tGf915uG/6H1i/YcnTTDBwGi4chStYU0aemYIPGjN0WcGJ4rRQ8KwpvsZPIevLMTAiE/vKFn2kEc0iMkRaRjGSHt4AkRi6Qw==
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
    for p in req:
        params = readParams(p)
        sendRequest(params)
        #time.sleep(1)
        
for i in range(count): print i; battle()