import json
import sys

from common import *
from common_head import *

pid = sys.argv[1]
auth = sys.argv[2]
data, gid, sid = init(pid, auth)
print json.dumps(data, indent=4)
