import hashlib

buildInfo = {"version":5697,"time":"16.09.2015 17:56","hash":"ff5a33268cfe44b0e3c0feae87a5f5bd"}

def getPauth(pid):
    return str(hashlib.md5(pid+buildInfo["hash"]).hexdigest())
def getGameVersion():
    return str(buildInfo["version"])