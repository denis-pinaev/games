import hashlib
buildInfo = {"version":5714,"time":"17.09.2015 11:10","hash":"326cd7241aaf9a0176d96c8e39a47cf3"}
def getPauth(pid): return str(hashlib.md5(pid+buildInfo["hash"]).hexdigest())
def getGameVersion(): return str(buildInfo["version"])
