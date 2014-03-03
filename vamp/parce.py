import sys
import json

def main():

        fatype = "parce.res"

        tfile = open(fatype, "w")
        
        
        tfile2 = open("parce.txt", "r")
        s = tfile2.read()
        tfile2.close()
        
        s = json.dumps(json.loads(s), indent=4)
        print s
        
        tfile.write(s)
        
        tfile.close()
        
main()        