import base64
import zlib
import json
s = "eNrVk+tOwzAMhd/Fv6MpdrKs7RvwDGhCWclYpd7UCzBNfXecsYyOdppAIMGvqsdufD735ABbgiSSRi2MijQaQiKpBbjSFXtIDtBUm6prIbk/wM7ZvNtBIgVkj/wYxETDGY1mNDWj6WE9CPCzUKPWq9VKGwGNa6u+SV3rzRSusznX2etSwJNlcakNCegbW2Z98f46nPyxXGZT7698gDy3vNTHeu6eXX5p+bO0FsAbIZ5mm2LmI/QdH9KmKvv2YXdxPIXNcWfdZKkbQZkY1ZlJmjETIu8VUlvbNOv2/n9JHtDta3c3s3Pmi06OvoGn/jQeKnN79JHnF9F9gOinCeegcATFQ83p7lxBwykaBjR9DU1eooU9x2Zqt7Ctv5tGf915uG/6H1i/YcnTTDBwGi4chStYU0aemYIPGjN0WcGJ4rRQ8KwpvsZPIevLMTAiE/vKFn2kEc0iMkRaRjGSHt4AkRi6Qw=="
#s = "eNqrVspMUbIy0FEqLkksSVWyMtRRKikGUiaGJiZGphaGZrUApYQJBQ=="
def decode(s):
    s = base64.decodestring(s)
    s = zlib.decompress(s)
    return s
    
def encode(s):
    s = zlib.compress(s)
    s = base64.encodestring(s)
    return s
    

s = '{"enemy":{"robots":[{"health":0,"id":0},{"health":0,"id":1},{"health":0,"id":2},{"health":0,"id":3},{"health":0,"id":4}]},"f2":8063.638416212204,"f1":23116.86224089124,"ts":1414477746,"units":[{"typeId":4,"capacity":99000,"level":0,"arm":[{"id":1,"level":4}],"bonus_hp":[{"id":0,"level":4}],"health":999,"wp":[{"id":2,"level":4},{"id":2,"level":4}],"y":22,"x":10,"id":0},{"typeId":1,"capacity":8000,"level":0,"arm":[{"id":1,"level":0}],"bonus_hp":[{"id":0,"level":2}],"health":990,"wp":[{"id":2,"level":0},{"id":2,"level":0}],"y":23,"x":8,"id":1},{"typeId":1,"capacity":8000,"level":0,"arm":[{"id":1,"level":0}],"y":23,"health":136,"wp":[{"id":2,"level":0},{"id":2,"level":0}],"bonus_hp":[{"id":0,"level":2}],"x":12,"id":2},{"typeId":1,"capacity":8000,"level":0,"arm":[{"id":0,"level":0}],"y":24,"health":96,"mass":164,"wp":[{"id":1,"level":0},{"id":1,"level":0}],"bonus_hp":[{"id":0,"level":1}],"x":6,"id":3},{"typeId":1,"capacity":8000,"level":0,"arm":[{"id":0,"level":0}],"y":24,"health":96,"mass":164,"wp":[{"id":1,"level":0},{"id":1,"level":0}],"bonus_hp":[{"id":0,"level":1}],"x":10,"id":4},{"typeId":2,"capacity":11000,"level":0,"id":5,"time":1112,"arm":[{"id":2,"level":0}],"y":24,"health":360,"wp":[{"id":2,"level":1},{"id":2,"level":1}],"bonus_hp":[{"id":1,"level":0},{"id":1,"level":0}],"x":14,"mass":429}],"id":0,"resources":{"gas":5462,"uranium":5462,"metal":16385}}'
print encode(s)

#eJzVlN1uwjAMhd/F1xGKnRCavsGeAU1TYNmoRFvUn20I9d3nVC0LaxGgXe0q6rEbf8dxcgJf+PwI6QmqclM2NaTrE+y82zc7SKWA7JWXTkw0nNFoRlMzmu6eOwFvBGkijVoYlWg0hERSs4y8kUI0i8QQaZlYJJYDGWrUerVaaSOgLbIBtjke/FPYVcDWHdw2a9iOtVJytb3/8Pu+rqvyPrtnPweYRMCmLNr6ZXc4x+VlfKS31gr4/EmjKE1MJf6TQYilLy4Zt3Ikxpg4uQtY3gCmS2B5BVhOgeUIrHrgJDrmv/IOu45YqMyDWLcMhwZTNIMPA8spsI76yLy5q8MEGn2BjlP0+88KB3QT3ZT/RY7nCx2hU4yO+Is9pC/5Ome5D9FwbLGdmXmM7ChzbaBxOjk4a+K27+BLj23TZIM22K98XbbV1tfhvXx3vCy14Ypt5YqszcfP3DcuAPDDtuy6byj3kLs=
