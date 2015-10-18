# -*- coding: utf-8 -*-
import time
import sys
import BaseHTTPServer
import subprocess

HOST_NAME = ''
PORT_NUMBER = 9000
PYTHON_PATH = '../python/python.exe'
SCRIPTS_PATH = './'
try:
    execfile('settings.ini')
except:
    print "Can't find settings. Use defaults."

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        try:
            s.wfile.write(answerPath(s.path))
        except Exception as ex:
            print ex
            print "answerPath error:\n", sys.exc_info()
        
def run():
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
    
    
def runScript(paths, scriptPath=SCRIPTS_PATH):
    sp = ["","","","","",""]
    for i in range(6):
        if i<len(paths):
            sp[i] = paths[i]
    try:
        proc = subprocess.Popen([PYTHON_PATH, scriptPath+sp[0]+'.py', sp[1], sp[2], sp[3], sp[4], sp[5]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return proc.communicate()[0]
    except Exception as ex:
        print ex
        print "answerPath error:\n", sys.exc_info()
    return "ERROR"
    
def answerPath(path):
    resp = ""
    resp += "<html><head><title>Hero game.</title><meta charset=\"UTF-8\"></head>"
    resp += "<body>"
    path = path.replace("?","/").replace("&","/")
    paths = path.split("/")[1:]
    if path == "/":
        resp += runScript(['players'])
    if paths[0] == "run":
        answ = runScript(paths[1:])
        answ = answ.replace('\n','<br/>\n')
        resp += "<p>"+answ+"</p>"
    resp += "</body></html>"
    return resp

run()