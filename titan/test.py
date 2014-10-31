import base64
import zlib
import json
s = "eNrVlOFqwyAQgN/F3zL0NMbkDfYMoxTbukVIstAk60rIu+90KYT19mMbHfSXuS9693ngTSwcWCk4 G9sw9Kx8mljt33yd2DsrJS5717l9GM4YKSEQ4BcAZ5V39VAhzS3C3Ws79tuqW+fQPKVX84Zf6pyo DWbm1wjPuGND7Ib4azh3/jHl5l+U7TfG6jfG8j+MJayV7d+M4ebGjev71Bmyzfqn0tgAs4R3qB4f SIz1PbovcXYLdwyeIYn71jeoOLHdGOpDaF8+58wyEC7WIhZbntwVA4IpgmmCZQQzBMsJZglWrNlm xmtKLGwKkwM8qCIDUWQWLxHHqdRS58YIoecPRTKU3w=="
#s = "eNqrVspMUbIy0FEqLkksSVWyMtRRKikGUiaGJiZGphaGZrUApYQJBQ=="
def decode(s):
    s = base64.decodestring(s)
    s = zlib.decompress(s)
    return s
    
def encode(s):
    s = zlib.compress(s)
    s = base64.encodestring(s)
    return s
    
    
s = 'eNpdi7ENgDAMBHf5OiDbsRPkbZCgoE6KIMTuOC3d3+n+wYAvdbWE64BTwg2Xia3v/Yyd0BuclVXFNi7BYyZiRoWqaK6SlUPHc/l7Ku8Hnq0W/A=='
print json.dumps(json.loads(decode(s)), indent=2)
s = 'eNoVjDkOwzAMwP6i2TEkWbKO3wRoh8zxkKLI36OMBEj+4YLcog/WQGcUUh3GDY4PJDb4QUrnOZgm2gwTFG9wrn19IUtbb24dVaabFp+QJCRmdYviGlD3cBmm9wNxhRlu'
print json.dumps(json.loads(decode(s)), indent=2)
s = '{"enemy":{"robots":[{"health":0,"id":0},{"health":0,"id":1},{"health":0,"id":2},{"health":0,"id":3},{"health":0,"id":4},{"health":0,"id":5}]},"f2":8063.638416212204,"f1":23116.86224089124,"ts":1414477746,"units":[{"typeId":3,"capacity":99000,"level":0,"arm":[{"id":2,"level":4}],"bonus_hp":[{"id":3,"level":4}],"health":1999,"wp":[{"id":6,"level":4},{"id":6,"level":4}],"y":22,"x":10,"id":0},{"typeId":3,"capacity":98000,"level":0,"arm":[{"id":2,"level":4}],"bonus_hp":[{"id":3,"level":4}],"health":1999,"wp":[{"id":6,"level":4},{"id":6,"level":4}],"y":23,"x":8,"id":1},{"typeId":3,"capacity":8000,"level":0,"arm":[{"id":2,"level":4}],"bonus_hp":[{"id":3,"level":4}],"health":1999,"wp":[{"id":6,"level":4},{"id":6,"level":4}],"y":23,"x":12,"id":2},{"typeId":3,"capacity":98000,"level":0,"y":24,"mass":1,"arm":[{"id":2,"level":4}],"bonus_hp":[{"id":3,"level":4}],"health":1999,"wp":[{"id":6,"level":4},{"id":6,"level":4}],"x":6,"id":3},{"typeId":3,"capacity":98000,"level":0,"y":24,"mass":1,"arm":[{"id":2,"level":4}],"bonus_hp":[{"id":3,"level":4}],"health":1999,"wp":[{"id":6,"level":4},{"id":6,"level":4}],"x":10,"id":4},{"typeId":3,"capacity":91000,"level":0,"id":5,"y":24,"arm":[{"id":2,"level":4}],"bonus_hp":[{"id":3,"level":4}],"health":1999,"wp":[{"id":6,"level":4},{"id":6,"level":4}],"x":14,"mass":1}],"id":0,"resources":{"gas":95462,"uranium":95462,"metal":96385}}'
#print encode(s)

#eJzVlNtuwyAMht/F16jCQAjkDfYMVTXRjC2RmoNy2FpFefc5aEuzlYvdtbtC+W3jz47xBL721QWyCbrm2Aw9ZPsJCu9OQwEZZ1C+0DGzGw0jmohoMqKpiJbMh5nBq4DMcC13WhqFWqAQXJGMdLlE1DujhVDcWBQkL7SoUKk0TZVmMNblVwHDpfVPS3YGuWtdXg5UorWcU7aTf/enkNd1VfAO7KtBzQcGx6Ye++eiXe3yp/2bHq21DD6ufnrjx24lCiUSQdnOFLztbxzZPAyyDMhm8/ejxI8GjGIzm3/r8RJM01W5fpmve5VwDsr6hP4ZOm6fepwdf7GHLbCWcD/ya/8WJbxPBp3vm7HLfb9syjdHh02UJrCxc3U5Vut35QdHt1laYMk8fwLsPpBQ
