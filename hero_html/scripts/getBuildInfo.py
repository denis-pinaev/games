import requests
import json
import zlib
import os

social = "vk"
vesionurl = "http://kn-%s-sc.playkot.com/current/get_launch_info.php?player_id=160511757&rsig=1033055981" % social
gameurl = "http://kn-scdn.playkot.com/%s/content/game_%s.swf"
version = "1111"

def get_version():
    resp = requests.post(vesionurl, allow_redirects=True)
    jstxt = json.loads(resp.text)
    version = jstxt["version"]
    client = jstxt["version"]
    if jstxt.has_key("client"): client = jstxt["client"]
    return int(client), version

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
    res = download_file(gameurl % (social,str(version)), "./tmp/game_%s_%s.swf" % (social,str(version)))
    if not res:
        version = version - 1
        res = download(i)
    return res
version, last_version = get_version()
print "server info version =",  version
if download():
    print "./tmp/game_%s_%s.swf" % (social,version)
    f = open("./tmp/game_%s_%s.swf" % (social,version), 'rb')
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
    os.remove("./tmp/game_%s_%s.swf" % (social,version))
