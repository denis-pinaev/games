import requests
import json

social = "vk"
vesionurl = "http://kn-%s-sc.playkot.com/current/get_launch_info.php" % social
gameurl = "http://kn-cdn.playkot.com/%s/content/game_%s.swf"
version = "1111"

def get_version():
    resp = requests.post(vesionurl, allow_redirects=True)
    jstxt = json.loads(resp.text)
    return jstxt["version"]

def download_file(url, local_filename):
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    if r.status_code == 404: return False
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    return True

def download(i=0):
    global version
    if i>=10: print "Failed to found correct SWF file"; return False
    i = i + 1
    res = download_file(gameurl % (social,str(version)), "D:/downloads/game_%s_%s.swf" % (social,str(version)))
    if not res:
        version = version - 1
        res = download(i)
    return res
version = int(get_version())
print "server info version =",  version
if download(): print "D:/downloads/game_%s_%s.swf" % (social,version)
