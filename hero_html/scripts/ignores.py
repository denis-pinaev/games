# -*- coding: utf-8 -*-
import json
import sys
import urllib
import datetime
from common_head import *

def loadignores():
    try:
        return json.loads(read("tmp/ignores"))
    except Exception as ex:
        return {"players":[],"orden":[]}
    
def saveignores(data):
    write("tmp/ignores", json.dumps(data, indent=4))

    
def getignoresysParams():
    name = ""
    pid = ""
    for p in sys.argv:
        if "=" in p:
            p = p.split("=")
            if p[0] == "name": name = urllib.unquote(p[1]).replace("+"," "); continue
            if p[0] == "pid": pid = p[1]; continue
    return pid, name
    
def removeignores(pid):
    ignores = loadignores()
    for i in range(len(ignores['orden'])):
        p = ignores['orden'][i]
        if str(p["pid"]) == str(pid):
            del ignores['orden'][i]
            saveignores(ignores)
            break;
    for i in range(len(ignores['players'])):
        p = ignores['players'][i]
        if str(p["pid"]) == str(pid):
            del ignores['players'][i]
            saveignores(ignores)
            break;
            

def getHead():
    res = ""
    ignores = loadignores()
    if open_list: setTMPParameter("isignoresListOpen", True)
    if close_list: setTMPParameter("isignoresListOpen", False)
    isignoresListOpen = getTMPParameter("isignoresListOpen", False)
    if create:
        res += '<form action="/run/ignores/save">'
        res += '<p><b>Исключение атаки игрока:</b></p>'
        res += '<p>Имя: <input type="text" name="name"><br/>'
        res += 'ID: <input type="number" name="pid"><br/>'
        res += '<input type="submit"></p>'
        res += '</form>'
        res += '</br>'
        res += '<form action="/run/ignores/save">'
        res += '<p><b>Исключение атаки Ордена:</b></p>'
        res += '<p>Имя: <input type="text" name="name">'
        res += '<input type="hidden" name="pid" value="0">'
        res += '<input type="submit"></p>'
        res += '</form>'
    elif save:
        pid, name = getignoresysParams()
        found = False;
        if str(pid) == "0":
            for p in ignores['orden']:
                if p["name"] == name:
                    found = True
                    break
            if not found:
                if pid == "" or name == "":
                    res += '<p>Нельзя пустое имя ордена</p>'
                else:
                    ignores['orden'].append({"pid":str((datetime.datetime.now() - datetime.datetime.fromtimestamp(0)).total_seconds()),"name":name})
        else:
            for p in ignores['players']:
                if p["pid"] == pid:
                    p['name'] = name
                    found = True
                    break
            if not found:
                if pid == "" or name == "":
                    res += '<p>Нельзя пустое имя</p>'
                else:
                    ignores['players'].append({"pid":pid,"name":name})
        saveignores(ignores)
        res += '<p>Сохранено '+name+' <a href="/run/ignores">Вернуться</a></p>'
    else:
        res += "<p>Исключения. Игроков "+str(len(ignores['players']))+". Орденов "+str(len(ignores['orden']))+"</p>"
        if isignoresListOpen:
            res += '<p><a href="/run/ignores/close">Свернуть список</a></p>'
        else:
            res += '<p><a href="/run/ignores/open">Развернуть список</a></p>'
        res += '<p><a href="/run/ignores/create">Добавить исключение</a></p>'
    if isignoresListOpen:
        res += '<table border="1" width="100%">'
        res += '<tr>'
        res += '<td>Имя игрока</td>'
        res += '<td>ID</td>'
        res += '<td>Удаление исключения</td>'
        res += '</tr>'
        for p in ignores["players"]:
            res += '<tr>'
            res += '<td>'+u_(p['name'])+'</td>'
            res += '<td>'+p['pid']+'</td>'
            res += '<td><a href="/run/ignores/remove/'+p['pid']+'">X</a></td>'
            res += '</tr>'
        res += '</table>'
        res += '<table border="1" width="50%">'
        res += '<tr>'
        res += '<td>Имя ордена</td>'
        res += '<td>Удаление исключения</td>'
        res += '</tr>'
        for p in ignores["orden"]:
            res += '<tr>'
            res += '<td>'+u_(p['name'])+'</td>'
            res += '<td><a href="/run/ignores/remove/'+str(p['pid'])+'">X</a></td>'
            res += '</tr>'
        res += '</table>'
    print res

create = sys.argv[1] == "create"
save = sys.argv[1] == "save"
open_list = sys.argv[1] == "open"
close_list = sys.argv[1] == "close"

if sys.argv[1] == "remove": removeignores(sys.argv[2])

commonHead()
getHead()
