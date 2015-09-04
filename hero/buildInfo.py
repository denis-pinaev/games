import hashlib

buildInfo = {"version":5491,"time":"03.09.2015 13:04","hash":"c6eeb9ff9b9f009d78375de6a6a8d491"}

def getPauth(pid):
    return str(hashlib.md5(pid+buildInfo["hash"]).hexdigest())
def getGameVersion():
    return str(buildInfo["version"])