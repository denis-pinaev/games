import hashlib
buildInfo = {"version":6754,"time":"04.02.2016 13:58","hash":"246dfbbfd1e48acf2356451af2bb4dcb"}
def getPauth(pid): return str(hashlib.md5(pid+buildInfo["hash"]).hexdigest())
def getGameVersion(): return str(buildInfo["version"])
