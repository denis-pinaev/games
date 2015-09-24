import hashlib
buildInfo = {"version":5768,"time":"23.09.2015 14:46","hash":"73591d7cd6b2254bef2e3e6cd840b6e2"}
def getPauth(pid): return str(hashlib.md5(pid+buildInfo["hash"]).hexdigest())
def getGameVersion(): return str(buildInfo["version"])
