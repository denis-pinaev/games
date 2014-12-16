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
    

tfile = open("test", "a")

s = 'eNoNyrkNhTAQBcBeXrwf7WVjuw4aQILAAYdkByBE75945sGF8tOBPUsUC0lZkzvhRpEhZ+ZR2cyTBzEltD73FcUIvX3DJcUQx8yErbZWj326z8+FUBcUfv87URgH'
s = json.dumps(json.loads(decode(s)), indent=2)
print s
tfile.write(s.encode('utf-8')+'\n')
s = 'eNrtlc2OgjAQx99lzj20pcXKG3h2b8ZsqjRLE6i4wO4awrvvoOxapCYevJhwAv7zyY9h2kJdQcIEU7GMFWcEjDPFCZIWdo3NU+s+0L7ZEmic7V03LWRG53UGCSVgU7x0ZKKxgMYDWhTQRECT3bYjUNiqsgf3dioNlsBnXa6PjU5XfUU2dON3WqNnb1wQ+EEXtOGbcU5gd3BN9Z6VZ69zIwRy82XyofwDEiLZ61LvbY05WUQpZtefxX9GOg1nU4mPMw73GPt97U1Nw54iYb0/zDKi0vuaY27qgi16PjZBXxwbX0pv4G/Gjc/c7o4bX3pLYcwtvmATM7bAX8q9vRnebjO3EDflnS033MTM7e56ixfX8/cXkvxo1Q=='
s = json.dumps(json.loads(decode(s)), indent=2)
print s
tfile.write(s.encode('utf-8')+'\n')
#s = '{"enemy":{"robots":[{"health":0,"id":0},{"health":0,"id":1},{"health":0,"id":2},{"health":0,"id":3},{"health":0,"id":4},{"health":0,"id":5}]},"f2":8063.638416212204,"f1":23116.86224089124,"ts":1414477746,"units":[{"typeId":3,"capacity":99000,"level":0,"arm":[{"id":2,"level":4}],"bonus_hp":[{"id":3,"level":4}],"health":1999,"wp":[{"id":6,"level":4},{"id":6,"level":4}],"y":22,"x":10,"id":0},{"typeId":3,"capacity":98000,"level":0,"arm":[{"id":2,"level":4}],"bonus_hp":[{"id":3,"level":4}],"health":1999,"wp":[{"id":6,"level":4},{"id":6,"level":4}],"y":23,"x":8,"id":1},{"typeId":3,"capacity":8000,"level":0,"arm":[{"id":2,"level":4}],"bonus_hp":[{"id":3,"level":4}],"health":1999,"wp":[{"id":6,"level":4},{"id":6,"level":4}],"y":23,"x":12,"id":2},{"typeId":3,"capacity":98000,"level":0,"y":24,"mass":1,"arm":[{"id":2,"level":4}],"bonus_hp":[{"id":3,"level":4}],"health":1999,"wp":[{"id":6,"level":4},{"id":6,"level":4}],"x":6,"id":3},{"typeId":3,"capacity":98000,"level":0,"y":24,"mass":1,"arm":[{"id":2,"level":4}],"bonus_hp":[{"id":3,"level":4}],"health":1999,"wp":[{"id":6,"level":4},{"id":6,"level":4}],"x":10,"id":4},{"typeId":3,"capacity":91000,"level":0,"id":5,"y":24,"arm":[{"id":2,"level":4}],"bonus_hp":[{"id":3,"level":4}],"health":1999,"wp":[{"id":6,"level":4},{"id":6,"level":4}],"x":14,"mass":1}],"id":0,"resources":{"gas":95462,"uranium":95462,"metal":96385}}'
#print encode(s)

#eJzVlNtuwyAMht/F16jCQAjkDfYMVTXRjC2RmoNy2FpFefc5aEuzlYvdtbtC+W3jz47xBL721QWyCbrm2Aw9ZPsJCu9OQwEZZ1C+0DGzGw0jmohoMqKpiJbMh5nBq4DMcC13WhqFWqAQXJGMdLlE1DujhVDcWBQkL7SoUKk0TZVmMNblVwHDpfVPS3YGuWtdXg5UorWcU7aTf/enkNd1VfAO7KtBzQcGx6Ye++eiXe3yp/2bHq21DD6ufnrjx24lCiUSQdnOFLztbxzZPAyyDMhm8/ejxI8GjGIzm3/r8RJM01W5fpmve5VwDsr6hP4ZOm6fepwdf7GHLbCWcD/ya/8WJbxPBp3vm7HLfb9syjdHh02UJrCxc3U5Vut35QdHt1laYMk8fwLsPpBQ
tfile.close()    
