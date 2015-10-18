import hashlib
buildInfo = {"version":5989,"time":"12.10.2015 16:10","hash":"b3e4cdae23063892cdf8114d83445149"}
def getPauth(pid): return str(hashlib.md5(pid+buildInfo["hash"]).hexdigest())
def getGameVersion(): return str(buildInfo["version"])
