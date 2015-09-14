import hashlib

buildInfo = {"version":5679,"time":"14.09.2015 19:20","hash":"dc2f0c195f0c25ab1e744bb5f4f72103"}

def getPauth(pid):
    return str(hashlib.md5(pid+buildInfo["hash"]).hexdigest())
def getGameVersion():
    return str(buildInfo["version"])