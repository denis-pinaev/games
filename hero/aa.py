import binascii
def getSig(myStr):
    return binascii.crc32(myStr) & 0xffffffff
    
def getData(pid, data):
    return getSig(pid+data)


pid = ''
data = '1'

ddd = getData(pid, data)
print ddd



#{"paidStart":false,"sessionKey":"52f2040cbf0763.07665884","index":"66766","method":"recipeStart","ctr":15,"count":6,"extra":null,"rid":1402211739,"type":"entities"}