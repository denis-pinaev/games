import hashlib
buildInfo = {"version":5770,"time":"23.09.2015 17:48","hash":"9d663360f8a0471c1904dcd1f2d00f00"}
def getPauth(pid): return str(hashlib.md5(pid+buildInfo["hash"]).hexdigest())
def getGameVersion(): return str(buildInfo["version"])
