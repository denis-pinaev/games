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
    res = "<p>В данном разделе создаются, удаляются и выбираются игроки, которыми в дальнейшем будут совершаться действия в игре.</p>"
    PLAYERS = loadPLAYERS()
    if open_list: setTMPParameter("isPlayersListOpen", True)
    if close_list: setTMPParameter("isPlayersListOpen", False)
    isPlayersListOpen = getTMPParameter("isPlayersListOpen", False)
    if create:
        res += '<form action="/run/players/save">'
        res += '<p><b>Создание нового игрока:</b></p>'
        res += '<p><table>'
        res += '<tr><td>Имя: </td><td><input type="text" name="name"></td><td> (Любая строка: ник, имя. Что бы понять, кто это)</td></tr>'
        res += '<tr><td>ID: </td><td><input type="number" name="pid"></td><td> (Числовой идентификатор пользователя ВК)</td></tr>'
        res += '<tr><td>auth: </td><td><input type="text" name="auth"></td><td> (Ключ авторизации игрока в игре)</td></tr>'
        res += '</table></p>'
        res += '<p><input type="submit" value="Создать"></p>'
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
                res += '<p>Сохранено '+u_(name)+'['+pid+']</p>'
            res += '<p><a href="/run/players">Вернуться</a></p>'
    else:
        res += "<p>Игроки. Количество = "+str(len(PLAYERS))+"</p>"
        if isPlayersListOpen:
            res += '<p><a href="/run/players/close">Скрыть список игроков</a></p>'
        else:
            res += '<p><a href="/run/players/open">Показать список игроков</a></p>'
        res += '<p><a href="/run/players/create">Добавить нового игрока</a></p>'
    if isPlayersListOpen:
        res += '<table border="1" width="50%">'
        res += '<tr>'
        res += '<td width="40%">Имя</td>'
        res += '<td width="40%">Профиль в ВК</td>'
        #res += '<td>Auth</td>'
        res += '<td width="10%">Выбор игрока</td>'
        res += '<td width="10%">Удаление</td>'
        res += '</tr>'
        for p in PLAYERS:
            res += '<tr>'
            res += '<td width="40%">'+u_(p['name'])+'</td>'
            res += '<td width="40%"><a target="_blank" href="https://vk.com/id'+p['pid']+'">https://vk.com/id'+p['pid']+'</a></td>'
            #res += '<td>'+p['auth']+'</td>'
            res += '<td width="10%"><a href="/run/players/select/'+p['pid']+'">Выбрать</a></td>'
            res += '<td width="10%"><a href="/run/players/remove/'+p['pid']+'" onclick = "if (!confirm(\'Действительно хотите удалить \\\''+u_(p['name'])+'\\\'?\')) return false;">X</a></td>'
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
