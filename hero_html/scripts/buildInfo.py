import hashlib
buildInfo = {"version":6211,"time":"05.11.2015 14:39","hash":"ee9cb499ca8e174f8da9b442022f5a88"}
def getPauth(pid): return str(hashlib.md5(pid+buildInfo["hash"]).hexdigest())
def getGameVersion(): return str(buildInfo["version"])
