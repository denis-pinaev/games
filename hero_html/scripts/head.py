# -*- coding: utf-8 -*-
import json
import sys

def read(fname):
    f = open(fname, 'rb')
    data = f.read()
    f.close()
    return data

def write(fname, data):
    f = open(fname, 'wb')
    f.write(fname)
    f.close()

def load():
    return json.loads(read("players"))
    
def save(data):
    write("players", json.dumps(data, indent=4))

def loadTMP():
    return json.loads(read("tmp/tmp"))
    
def saveTMP(data):
    write("tmp/tmp", json.dumps(data, indent=4))
    
def getHead():
    res = ""
    PLAYERS = load()
    tmp = loadTMP()
    if create:
        res += '<form action="/run/head/save">'
        res += '<p><b>Создание нового игрока:</b></p>'
        res += '<p>Имя: <input type="text" name="name"><br/>'
        res += 'ID: <input type="text" name="pid"><br/>'
        res += 'auth: <input type="text" name="auth"><br/></p>'
        res += '<p><input type="submit" name="Создать"></p>'
        res += '</form>'
    elif save:
        res += '<p>Сохраняем...</p>'
    else:
        res += "<p>Players</p>"
        res += "<p>total = "+str(len(PLAYERS))+"</p>"
        res += '<p><a href="/run/head/create">Добавить</a></p>'
    return res

create = sys.argv[1] == "create"
save = sys.argv[1] == "save"
print getHead()
