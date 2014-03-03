import urllib
import sys
import time
limit = 76;
# molotok 1 2 3 - http://178.132.201.36/messagesServer/messagesServlet?messageText=trick%5F2%231&method=sendMessage&sourceUserId=124520&r=576482%2E261531055&messageType=0&targetUserId=2113686
# blast_bonus#1 	star_bonus#1 messageText energy_booster1#1
if len(sys.argv) > 1:
    limit = int(sys.argv[1])
#id62247520@vk.com
bonus = ['trick_1','trick_2','trick_3','blast_bonus','star_bonus','energy_booster1']
for p in bonus:
	res_wire = "http://178.132.201.36/messagesServer/messagesServlet?messageType=0&method=sendMessage&targetUserId=124520&r=1&sourceUserId=62247520&messageText=%s%%231000" % p
	rrr = urllib.urlopen(res_wire)
	print res_wire[74:]
time.sleep(99999)

for i in range(1, limit):
    res_wire = "http://178.132.201.36/messagesServer/messagesServlet?messageType=1&method=sendMessage&targetUserId=85578490&r=1&sourceUserId=124520&messageText=material%%5F%s%%239999" % (str(i))
    rrr = urllib.urlopen(res_wire)
    print res_wire[74:]
    print i
