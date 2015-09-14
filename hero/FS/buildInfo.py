import hashlib

buildInfo = {"version":5671,"time":"14.09.2015 18:52","hash":"fc3f1622d3b1bc40091c4ea89d34c2c9"}

def getPauth(pid):
    return str(hashlib.md5(pid+buildInfo["hash"]).hexdigest())
def getGameVersion():
    return str(buildInfo["version"])