import hashlib

buildInfo = {"version":5689,"time":"15.09.2015 18:13","hash":"13959c4496f719d2a93f42291d7184e7"}

def getPauth(pid):
    return str(hashlib.md5(pid+buildInfo["hash"]).hexdigest())
def getGameVersion():
    return str(buildInfo["version"])