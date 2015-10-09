import hashlib
buildInfo = {"version":5965,"time":"08.10.2015 14:35","hash":"0284238e0ccc178f50acbca3e14b2df0"}
def getPauth(pid): return str(hashlib.md5(pid+buildInfo["hash"]).hexdigest())
def getGameVersion(): return str(buildInfo["version"])
