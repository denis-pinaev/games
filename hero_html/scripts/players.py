# -*- coding: utf-8 -*-
import json
import sys
import urllib
from common_head import *

def getPlayerSysParams():
    name = ""
    auth = ""
    pid = ""
    for p in sys.argv:
        if "=" in p:
            p = p.split("=")
            if p[0] == "name": name = urllib.unquote(p[1]).replace("+"," "); continue
            if p[0] == "auth": auth = p[1]; continue
            if p[0] == "pid": pid = p[1]; continue
    return pid, auth, name
    
def removePlayer(pid):
    PLAYERS = loadPLAYERS()
    for i in range(len(PLAYERS)):
        p = PLAYERS[i]
        if p["pid"] == pid:
            del PLAYERS[i]
            savePLAYERS(PLAYERS)
            break;
            

def getHead():
    res = ""
    PLAYERS = loadPLAYERS()
    if open_list: setTMPParameter("isPlayersListOpen", True)
    if close_list: setTMPParameter("isPlayersListOpen", False)
    isPlayersListOpen = getTMPParameter("isPlayersListOpen", False)
    if create:
        res += '<form action="/run/players/save">'
        res += '<p><b>Создание нового игрока:</b></p>'
        res += '<p>Имя: <input type="text" name="name"><br/>'
        res += 'ID: <input type="number" name="pid"><br/>'
        res += 'auth: <input type="text" name="auth"><br/></p>'
        res += '<p><input type="submit" name="Создать"></p>'
        res += '</form>'
    elif save:
        pid, auth, name = getPlayerSysParams()
        found = False;
        for p in PLAYERS:
            if p["pid"] == pid:
                p['auth'] = auth
                p['name'] = name
                found = True
                break
        if not found:
            if pid == "" or auth == "" or name == "":
                res += '<p>Нельзя сохранить с пустыми данными</p>'
            else:
                PLAYERS.append({"pid":pid,"auth":auth,"name":name})
        savePLAYERS(PLAYERS)
        res += '<p>Сохранено '+name+'['+pid+'] <a href="/run/players">Вернуться</a></p>'
    else:
        res += "<p>Игроки. Количество = "+str(len(PLAYERS))+"</p>"
        if isPlayersListOpen:
            res += '<p><a href="/run/players/close">Свернуть список</a></p>'
        else:
            res += '<p><a href="/run/players/open">Развернуть список</a></p>'
        res += '<p><a href="/run/players/create">Добавить</a></p>'
    if isPlayersListOpen:
        res += '<table border="1" width="100%">'
        res += '<tr>'
        res += '<td>Имя</td>'
        res += '<td>ID</td>'
        res += '<td>Auth</td>'
        res += '<td>Выбор игрока</td>'
        res += '<td>Удаление игрока</td>'
        res += '</tr>'
        for p in PLAYERS:
            res += '<tr>'
            res += '<td>'+u_(p['name'])+'</td>'
            res += '<td>'+p['pid']+'</td>'
            res += '<td>'+p['auth']+'</td>'
            res += '<td><a href="/run/players/select/'+p['pid']+'">Выбрать</a></td>'
            res += '<td><a href="/run/players/remove/'+p['pid']+'">X</a></td>'
            res += '</tr>'
        res += '</table>'
    print res

create = sys.argv[1] == "create"
save = sys.argv[1] == "save"
open_list = sys.argv[1] == "open"
close_list = sys.argv[1] == "close"

if sys.argv[1] == "remove": removePlayer(sys.argv[2])

if sys.argv[1] == "select": setTMPParameter("pid", sys.argv[2])

commonHead()
getHead()
