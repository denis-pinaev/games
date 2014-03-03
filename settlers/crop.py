import urllib
import sys
import time
#2 - tikva
#3 - tomati
#4 - posoln
#5 - goroh
#6 - morkov
#8 - psheno
#9 - hlop
#10 - kapust
#11 - klubnika
#15 - perec
#17 - banani
crop = '17'
fields = ['17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36']
req_wire1 = "http://109.234.155.174/settlers/server.php?appId=2181108&random=244517541&request=buyCrops&viewerId=124520&typeId=%s&authKey=1afebbff2c3e70596a0b01685bdd7e7e&soilId=%s"
req_wire2 = "http://109.234.155.174/settlers/server.php?appId=2181108&random=259083609&request=fertilizeCrop&viewerId=124520&authKey=1afebbff2c3e70596a0b01685bdd7e7e&soilId=%s"
req_wire3 = "http://109.234.155.174/settlers/server.php?appId=2181108&random=206233993&request=harvestCrops&viewerId=124520&authKey=1afebbff2c3e70596a0b01685bdd7e7e&soilId=%s"
limit = 50;
if len(sys.argv) > 1:
    limit = int(sys.argv[1])

cnt = limit
limit = 1

for i in range(limit):
    for f in range(cnt):
        req_wire = req_wire1 % (crop, str(f))
        rrr = urllib.urlopen(req_wire)
        print req_wire[-70:]
    time.sleep(3)
    for f in range(cnt):
        req_wire = req_wire2 % (str(f))
        rrr = urllib.urlopen(req_wire)
        print req_wire[-70:]
    time.sleep(5)
    for f in range(cnt):
        req_wire = req_wire3 % (str(f))
        rrr = urllib.urlopen(req_wire)
        print req_wire[-70:]
    time.sleep(3)
    print i
