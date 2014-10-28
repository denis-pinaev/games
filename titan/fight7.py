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
random	784693642
viewerId	124520
params	eNqrVspMUbIy0FEqKVayMjQxNDExMjI3MtFRKi5JLEkFCtUCAJlQCQA=
appId	4375733
authKey	9037dffa6247a0c12e6846044660d736
request	changeSquadState
''')

req.append('''
random	159427964
viewerId	124520
params	eNoVizkOgDAMwP6SuVRNmpDjN0gwMLcDCPF3wmZb8gMXxKJVCpw7RCtwQ9CvY27zSC4wBwQyMhMpcfq/WBVWcSVBQ3TU7Ln2KujiZqt178hN3w+h9Rcx
appId	4375733
authKey	9037dffa6247a0c12e6846044660d736
request	changeSquadState
''')

req.append('''
random	620331914
viewerId	124520
params	eNqrVqpQstK10LM0NDMyNrKwNDYzsDQ2t9BRykxRsjLQUSopSg8uLE0Eckx0lCqVrIz1zMwNjS0NDAxNgcjMyFxHqbgksSQVKANW7FeQ7JRYDOUWK1kZmhiamBgZmZsZ1gIAnt0bTA==
appId	4375733
authKey	9037dffa6247a0c12e6846044660d736
request	changeSquadState
''')

req.append('''
random	492845279
viewerId	124520
params	eNrNU1lugzAQvYu/UeSxxw5wg54hiiqHOgWJTQbaRoi7d6AJIcWplI9K+YJ5s7xFcs+OgsXIgW8kqlCj1qAVBix7YzEPWNuwGBAQBY+AYGebqnOJJbhn74Y+KCXNFbY1+TiKMmCdM2XWFT/lEDBb2uI0LrjqUI0Xdz1LrcnbdOKYqIZghYEHEx5MejD0YGrYk5iuzM4SvoiCWp/1VOX2w+a3PL+h/RyLcYVnCcaJ2mWJndNRyPWcjo5gmY4CIIuzyoh613uJqU2StRRbyDnV9CNEwA5V2TWv6Y1kcYmQ2NtTbV8u2ZHB8EF//29suuf3Jx/3B2J9ymsY1obhvuGJy6cFFv3rSmGa8Z1onH1MgS4i0Gvp+gmVnx++/Fs58OeVjnell12e04EjjAZUBBu1RYFhJLYch280Q3cl
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