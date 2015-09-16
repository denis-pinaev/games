import hashlib

buildInfo = {"version":5700,"time":"16.09.2015 14:59","hash":"fd936098998a94cd1a1c650cd1f99ea5"}

def getPauth(pid):
    return str(hashlib.md5(pid+buildInfo["hash"]).hexdigest())
def getGameVersion():
    return str(buildInfo["version"])