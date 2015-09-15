import hashlib

buildInfo = {"version":5685,"time":"15.09.2015 10:33","hash":"2cd6dd150a2f9a62afc229fa8143e13f"}

def getPauth(pid):
    return str(hashlib.md5(pid+buildInfo["hash"]).hexdigest())
def getGameVersion():
    return str(buildInfo["version"])