import hashlib
buildInfo = {"version":5942,"time":"06.10.2015 16:28","hash":"4a5c29763e3019ec2d591618d24bf3d1"}
def getPauth(pid): return str(hashlib.md5(pid+buildInfo["hash"]).hexdigest())
def getGameVersion(): return str(buildInfo["version"])
