import hashlib

buildInfo = {"version":5448,"time":"24.08.2015 17:01","hash":"704de7d0690d0c2558d62e8210b7ddce"}

def getPauth(pid):
    return str(hashlib.md5(pid+buildInfo["hash"]).hexdigest())
def getGameVersion():
    return str(buildInfo["version"])