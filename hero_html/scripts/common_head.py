# -*- coding: utf-8 -*-
import json
import subprocess
import sys

HOST_NAME = ''
PORT_NUMBER = 9000
PYTHON_PATH = '../python/python.exe'
SCRIPTS_PATH = './'
try:
    execfile('settings.ini')
except:
    print "Can't find settings. Use defaults."
    
def getRunLog(data):
    res = ""
    res += '<p>Script log:</p>'
    res += '<table width=100% border=1><tr><td>'
    data2 = data.replace(" ","&nbsp;")
    res += '<p style="font-size:80%">'+data2+'</p>'
    res += '</td></tr></table>'
    return res
    
def runScript(paths, scriptPath=SCRIPTS_PATH):
    sp = ["","","","","","",""]
    for i in range(7):
        if i<len(paths):
            sp[i] = paths[i]
    try:
        proc = subprocess.Popen([PYTHON_PATH, scriptPath+sp[0]+'.py', sp[1], sp[2], sp[3], sp[4], sp[5], sp[6]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return proc.communicate()[0]
    except Exception as ex:
        print ex
        print "runScript error:\n", sys.exc_info()
    return "ERROR"

def read(fname):
    f = open(fname, 'rb')
    data = f.read()
    f.close()
    return data

def write(fname, data):
    f = open(fname, 'wb')
    f.write(data)
    f.close()
    
def loadPlayer(pid):
    PLAYERS = loadPLAYERS()
    for p in PLAYERS:
        if str(p["pid"]) == str(pid):
            return p
    return None
    
def getPlayer():
    pid = getTMPParameter("pid", None)
    auth = None
    if pid:
        user = loadPlayer(pid)
        if user:
            auth = user["auth"]
    return pid, auth

def loadPLAYERS():
    try:
        return json.loads(read("tmp/players"))
    except:
        return []
    
def savePLAYERS(data):
    write("tmp/players", json.dumps(data, indent=4))

def loadTMP():
    try:
        return json.loads(read("tmp/tmp"))
    except:
        return {}
    
def saveTMP(data):
    write("tmp/tmp", json.dumps(data, indent=4))

def getTMPParameter(name, default):
    tmp = loadTMP()
    if tmp.has_key(name):
        return tmp[name]
    return default
    
def setTMPParameter(name, default):
    tmp = loadTMP()
    tmp[name] = default
    saveTMP(tmp)

def u_(name):
    if type(name) == type(u''): return name.encode("utf-8", "ignore")
    return name

def commonHead():
    res = ""
    selected_pid = getTMPParameter("pid", None)
    PLAYERS = loadPLAYERS()
    res += '<table border="1" width="100%">'
    res += '<tr>'
    res += '<td width="25%"><a href="/run/players/open">Настройка игроков</a></td>'
    res += '<td width="25%"><a href="/run/ignores/open">Настройка союзников</a></td>'
    res += '<td width="25%"><a href="/run/actions/open">Одиночные действия игрока</a></td>'
    res += '<td width="25%"><a href="/run/mass/open">Массовые действия (в разработке)</a></td>'
    res += '</tr>'
    res += '</table>'
    
    if selected_pid:
        for p in PLAYERS:
            if p["pid"] == selected_pid:
                res += "<p><b>Выбранный игрок: %s [%s]</b></p>" % (u_(p["name"]), u_(p["pid"]))
                break;
                
    print res
