import hashlib
buildInfo = {"version":6077,"time":"23.10.2015 14:25","hash":"4631cd12d06e21ce97bac3e49f24db37"}
def getPauth(pid): return str(hashlib.md5(pid+buildInfo["hash"]).hexdigest())
def getGameVersion(): return str(buildInfo["version"])
