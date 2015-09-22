import hashlib
buildInfo = {"version":5729,"time":"21.09.2015 15:13","hash":"9c3ec8ca3464f3af25be8644d77b2edf"}
def getPauth(pid): return str(hashlib.md5(pid+buildInfo["hash"]).hexdigest())
def getGameVersion(): return str(buildInfo["version"])
