import hashlib
buildInfo = {"version":6147,"time":"28.10.2015 14:32","hash":"d724c3f729679cf67da340da56a23c4d"}
def getPauth(pid): return str(hashlib.md5(pid+buildInfo["hash"]).hexdigest())
def getGameVersion(): return str(buildInfo["version"])
