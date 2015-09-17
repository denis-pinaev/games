import hashlib
buildInfo = {"version":5720,"time":"17.09.2015 19:07","hash":"c292e9ab19d862ef253aa42594aa4ca6"}
def getPauth(pid): return str(hashlib.md5(pid+buildInfo["hash"]).hexdigest())
def getGameVersion(): return str(buildInfo["version"])
