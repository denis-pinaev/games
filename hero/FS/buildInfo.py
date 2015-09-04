import hashlib

buildInfo = {"version":5516,"time":"04.09.2015 9:36","hash":"5ab2d5591d40b3a779549f1d1a21797a"}

def getPauth(pid):
    return str(hashlib.md5(pid+buildInfo["hash"]).hexdigest())
def getGameVersion():
    return str(buildInfo["version"])