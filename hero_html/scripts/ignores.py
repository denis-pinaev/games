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
    res = "<p>В данном разделе представлены союзные игроки или ордена,<br/>на которых не будут совершаться атаки в процессе автоматических действий в игре.</p>"
    ignores = loadignores()
    if open_list: setTMPParameter("isignoresListOpen", True)
    if close_list: setTMPParameter("isignoresListOpen", False)
    isignoresListOpen = getTMPParameter("isignoresListOpen", False)
    if create:
        res += '<form action="/run/ignores/save">'
        res += '<p><b>Добавление игрока союзника:</b></p>'
        res += '<p><table>'
        res += '<tr><td>Имя: </td><td><input type="text" name="name"></td><td> (Любая строка: ник, имя. Что бы понять, кто это)</td></tr>'
        res += '<tr><td>ID: </td><td><input type="number" name="pid"></td><td> (Числовой идентификатор пользователя ВК)</td></tr>'
        res += '</table></p>'
        res += '<input type="submit">'
        res += '</form>'
        res += '</br>'
        res += '<form action="/run/ignores/save">'
        res += '<p><b>Добавление союзного ордена:</b></p>'
        res += '<p>Имя: <input type="text" name="name"> (Точное название ордена из игры с учетом регистра)</p>'
        res += '<input type="hidden" name="pid" value="0">'
        res += '<p><input type="submit"></p>'
        res += '</form>'
    elif save:
        pid, name = getignoresysParams()
        found = False;
        if str(pid) == "0":
            for p in ignores['orden']:
                if u_(p["name"]) == u_(name):
                    found = True
                    res += '<p>Орден "'+ u_(name)+'" уже был добавлен</p>'
                    break
            if not found:
                if pid == "" or name == "":
                    res += '<p>Нельзя пустое имя ордена</p>'
                else:
                    ignores['orden'].append({"pid":str((datetime.datetime.now() - datetime.datetime.fromtimestamp(0)).total_seconds()),"name":name})
                    res += '<p>Сохранен орден '+u_(name)+'</p>'
        else:
            for p in ignores['players']:
                if p["pid"] == pid:
                    p['name'] = name
                    found = True
                    res += '<p>Союзник "'+ u_(name)+'" уже был добавлен</p>'
                    break
            if not found:
                if pid == "" or name == "":
                    res += '<p>Нельзя пустое имя игрока</p>'
                else:
                    ignores['players'].append({"pid":pid,"name":name})
                    saveignores(ignores)
                    res += '<p>Сохранен союзник '+u_(name)+'</p>'
        res += '<p><a href="/run/ignores">Вернуться</a></p>'
    else:
        res += "<p>Союзники: Игроков "+str(len(ignores['players']))+". Орденов "+str(len(ignores['orden']))+"</p>"
        if isignoresListOpen:
            res += '<p><a href="/run/ignores/close">Скрыть список союзников</a></p>'
        else:
            res += '<p><a href="/run/ignores/open">Показать список союзников</a></p>'
        res += '<p><a href="/run/ignores/create">Добавить нового союзника</a></p>'
    if isignoresListOpen:
        res += '<table border="1" width="50%">'
        res += '<tr>'
        res += '<td width="45%">Имя игрока</td>'
        res += '<td width="45%">Профиль в ВК</td>'
        res += '<td width="10%">Удаление союзника</td>'
        res += '</tr>'
        for p in ignores["players"]:
            res += '<tr>'
            res += '<td>'+u_(p['name'])+'</td>'
            res += '<td><a target="_blank" href="https://vk.com/id'+p['pid']+'">https://vk.com/id'+p['pid']+'</a></td>'
            res += '<td><a href="/run/ignores/remove/'+p['pid']+'" onclick = "if (!confirm(\'Действительно хотите удалить \\\''+u_(p['name'])+'\\\'?\')) return false;">X</a></td>'
            res += '</tr>'
        res += '</table><br/>'
        res += '<table border="1" width="25%">'
        res += '<tr>'
        res += '<td width="80%">Имя ордена</td>'
        res += '<td width="20%">Удаление ордена</td>'
        res += '</tr>'
        for p in ignores["orden"]:
            res += '<tr>'
            res += '<td>'+u_(p['name'])+'</td>'
            res += '<td><a href="/run/ignores/remove/'+str(p['pid'])+'" onclick = "if (!confirm(\'Действительно хотите удалить \\\''+u_(p['name'])+'\\\'?\')) return false;">X</a></td>'
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
