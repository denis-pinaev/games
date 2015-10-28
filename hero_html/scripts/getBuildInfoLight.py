import requests
import json

social = "vk"
vesionurl = "http://kn-%s-sc.playkot.com/current/get_launch_info.php?player_id=160511757&rsig=1033055981" % social
version = "1111"

def get_version():
    resp = requests.post(vesionurl, allow_redirects=True)
    jstxt = json.loads(resp.text)
    version = jstxt["version"]
    client = jstxt["version"]
    if jstxt.has_key("client"): client = jstxt["client"]
    return int(client), version

version, last_version = get_version()
print "server info version =",  version
