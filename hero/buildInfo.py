import hashlib

buildInfo = {"version":5441,"time":"21.08.2015 14:45","hash":"cfca0b34afa7424b0a0fa28343f3dca9"}

def getPauth(pid):
    return str(hashlib.md5(pid+buildInfo["hash"]).hexdigest())
def getGameVersion():
    return str(buildInfo["version"])