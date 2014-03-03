import binascii
import pyamf
import sys
import json
import datetime
import time
import random
import requests

def sendRequest(params):
    url = 'http://flash.timus.ru/space/?vk=124520&auth=97fe8c57673858201adbc96bf9c706e1'

    xml = '<client name="space"><specOpsFight id="%d"/></client>' % params
    headers = {'Content-Type': 'text/xml'}
    print i, requests.post(url, data=xml, headers=headers).text[50:150]
    #resp = requests.post(url, data=params, allow_redirects=True)
    
    
for i in range(2502, 3000):
    sendRequest(i)
    

