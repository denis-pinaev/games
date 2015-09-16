import hashlib

buildInfo = {"version":5692,"time":"16.09.2015 12:16","hash":"41fcc9fe27a4f4a4608276e8f713589d"}

def getPauth(pid):
    return str(hashlib.md5(pid+buildInfo["hash"]).hexdigest())
def getGameVersion():
    return str(buildInfo["version"])