import requests
import json
import zlib

social = "fs"
vesionurl = "http://kn-%s-sc.playkot.com/current/get_launch_info.php" % social
gameurl = "http://kn-scdn.playkot.com/%s/content/game_%s.swf"
version = "1111"

def get_version():
    resp = requests.post(vesionurl, allow_redirects=True)
    jstxt = json.loads(resp.text)
    return jstxt["version"]

def download_file(url, local_filename):
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    print r.status_code
    if r.status_code in [404,403]: return False
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    return True

def download(i=0):
    global version
    if i>=100: print "Failed to found correct SWF file"; return False
    i = i + 1
    res = download_file(gameurl % (social,str(version)), "D:/downloads/games/game_%s_%s.swf" % (social,str(version)))
    if not res:
        version = version - 1
        res = download(i)
    return res
version = int(get_version())
print "server info version =",  version
if download():
    print "D:/downloads/games/game_%s_%s.swf" % (social,version)
    f = open("D:/downloads/games/game_%s_%s.swf" % (social,version), 'rb')
    f.read(3)
    tmp = 'FWS' + f.read(5) + zlib.decompress(f.read())
    f.close()
    start_index =  tmp.index('{"version":')
    end_index =  tmp.index('}', start_index)
    fileData = ""
    fileData += 'import hashlib\n'
    fileData += 'buildInfo = %s\n' % tmp[start_index:end_index+1]
    fileData += 'def getPauth(pid): return str(hashlib.md5(pid+buildInfo["hash"]).hexdigest())\n'
    fileData += 'def getGameVersion(): return str(buildInfo["version"])\n'
    f = open("buildInfo.py","w")
    f.write(fileData)
    f.close()
