import binascii
import json, sys, hashlib

def read():
    fatype = "cheat"
    tfile = open(fatype, "r")
    d = tfile.read()
    tfile.close()
    return d

def getSig(myStr):
    return binascii.crc32(myStr) & 0xffffffff
    
def getData():
    return getSig(pid+code2+data)

def log(s1, s2):
    fatype = "cheat"
    print s2
    if True:
        tfile = open(fatype, "w")
        tfile.write(s2+'!'+s1)
        tfile.close()
        

def calculateSignature(params):
    a = []
    middle = "="
    addon = "sasay_lalka))0"
    for p in params:
        a.append(p+middle+params[p]+addon)
    a = sorted(a)
    sa = "".join(a)
    sa = viewerId + sa
    return sa
    
def generateSignature(params):
    a = []
    middle = "#"
    addon = ""
    for p in params:
        a.append(p+middle+params[p]+addon)
    a = sorted(a)
    res = viewerId
    res += calculateSignature(a)
    res += calculateSignature(a)
    res += calculateSignature(a)
    print res
    return hashlib.md5(res).hexdigest()
    

viewerId = "124520"

data = read()

tparams = {
"authKey":"9986e2a37b006815324e70b65049759e",
"v":"60.1",
"viewerId":"124520",
"userId":"124520",
"sid":"358412656"
}

print "9f04c2c141f9ef5eebfe2d5766154f3a"

print generateSignature(tparams)

