import hashlib
buildInfo = {"version":5990,"time":"12.10.2015 13:11","hash":"f813ddc4cc5ef8124b8b046fffb31c84"}
def getPauth(pid): return str(hashlib.md5(pid+buildInfo["hash"]).hexdigest())
def getGameVersion(): return str(buildInfo["version"])
