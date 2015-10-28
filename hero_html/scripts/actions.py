# -*- coding: utf-8 -*-
import json
import sys
import os
import urllib
import datetime
from common_head import *

def getErrorLog(mess):
    ret = "Ошибка во время выполнения: <b>"+mess+"</b><br/>"
    if "VERSION_UPDATE" in mess:
        ret += 'Необходимо <a href="/run/actions/getBuildInfo">обновить</a> версию игры.<br/>'
    if "AUTH" in mess:
        ret += 'Неверные данные игрока: ID, Ключ. Необходимо <a href="/run/players/open">обновить</a> данные.<br/>'
    return ret

def getPlayerSysParams():
    name = ""
    auth = ""
    pid = ""
    for p in sys.argv:
        if "=" in p:
            p = p.split("=")
            if p[0] == "name": name = urllib.unquote(p[1]); continue
            if p[0] == "auth": auth = p[1]; continue
            if p[0] == "pid": pid = p[1]; continue
    return pid, auth, name
    
def getMapRectParams():
    name = ""
    pid = ""
    x = getTMPParameter("mapRectX", 0)
    y = getTMPParameter("mapRectY", 0)
    for p in sys.argv:
        if "=" in p:
            p = p.split("=")
            if p[0] == "x": x = p[1]; setTMPParameter("mapRectX", x); continue
            if p[0] == "y": y = p[1]; setTMPParameter("mapRectY", y); continue
    return x, y
    
def getGlobalEnergy(timestamp):
    td = (datetime.datetime.now() - datetime.datetime.fromtimestamp(int(timestamp)-60*60)).total_seconds()
    s = int(td)
    m = s/60
    h = m/60
    energy_value = min(6,h/4)
    rh = h-energy_value*4
    rm = m-h*60
    rs = s-m*60
    tsl4 = 4*60*60
    tsl = tsl4 if energy_value>5 else rs + rm*60 + rh*60*60
    td = str(datetime.datetime.fromtimestamp(tsl4) - datetime.datetime.fromtimestamp(tsl))
    return int(energy_value), td

def getPrintSity(stype, sity, maps, player_name, canFight):
    slevel = str(sity["level"])
    sincome = str(sity["income"])
    sclan = ""
    sclanid = ""
    if sity.has_key("clan_id"):
        sclan = str(sity["clan_id"])
        sclanid = sclan
        if maps["clans"].has_key(sclan):
            sclan = u_(maps["clans"][sclan]["name"])
        else: sclan = "(Орден удален)"
    sresources = str(int(sity["resources"]))
    sx = str(sity["x"])
    sy = str(sity["y"])
    sname = "%s (%s:%s)" % (stype, sx, sy)
    if sity.has_key("name"):
        sname = u_(sity["name"])
    sid = str(sity["id"])
    abandoned = sity.has_key("abandoned")
    dammaged = sity.has_key("maxDamage")
    mark = ""
    if sity.has_key("action") and sity["action"] == "abandoning": mark+="Покидается. "
    if sity.has_key("action") and sity["action"] == "activating": mark+="Открытие. "
    if(abandoned): mark+="Покинуто. "
    if(dammaged): mark+="Атаковано. "
    my_clan = ""
    try:
        if maps.has_key("initInfo") and maps["initInfo"].has_key("clan") and maps["initInfo"]["clan"].has_key("info"):
            my_clan = maps["initInfo"]["playerStats"]["clan_id"]
    except: None
    stail = "Нет вариантов"
    if my_clan != "" and not (sity.has_key("action") and sity["action"] == "activating"):
        if sclanid == my_clan:
            energy_value = 0
            try:
                energy_value,td = getGlobalEnergy(maps["initInfo"]["playerStats"]["gwHeals"])
            except: None
            if dammaged and energy_value>0:
                stail = '<a href="/run/actions/healSity/%s" onclick = "if (!confirm(\'Защитить %s \\\'%s\\\' игроком \\\'%s\\\'?\')) return false;">Защита</a>' % (sid, stype, sname, player_name)
        else:
            energy_value = 0
            try:
                energy_value,td = getGlobalEnergy(maps["initInfo"]["playerStats"]["gwAttacks"])
            except: None
            if energy_value>0 and canFight:
                stail = '<a href="/run/actions/attack/1/gwAttack/%s" onclick = "if (!confirm(\'Атаковать %s \\\'%s\\\' игроком \\\'%s\\\'?\')) return false;">Атака</a>' % (sid, stype, sname, player_name)
    res = '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s (%s в сутки)</td><td>%s:%s</td><td>%s</td><td>%s</td></tr>' % (stype,slevel,sname,sclan,sresources,sincome,sx,sy,mark,stail)
    
    return res

def getHead():
    res = "<p>В данном разделе представлены действия в игре для выбранного игрока.</p>"
    pid, auth = getPlayer()
    if not auth or not pid:
        res += '<p>Для действий в игре выберите игрока.</p>'
        res += '<p>Вернуться к <a href="/run/players/open">выбору активного игрока</a> для дальнейших операций.</p>'
        print res
        return
    PLAYERS = loadPLAYERS()
    x,y = getMapRectParams()
    player = loadPlayer(pid)
    needVersion = not os.path.exists('./buildInfo.py')
    canFight = os.path.exists('./fight.py')
    
    if (not needVersion) and getBuildInfoLight:
        answ = runScript(['getBuildInfoLight'])
        ana = answ.split('\n')
        new_version = "None"
        for anal in ana:
            preLine = "server info version = "
            if preLine in anal: new_version = anal[anal.index(preLine)+len(preLine):]
        old_version = getTMPParameter("game_version", "No old version")
        
        if str(new_version) != str(old_version):
            res += '<p>Вышла новая версия игры! Необходимо обновить версию с "%s" до "%s"</p>' % (str(old_version), str(new_version))
            needVersion = True
        
    
    
    res += '<p><table style="border-spacing:15px">'
    res += '<tr><td><p><a href="/run/actions/getBuildInfo">Получить последнюю версию игры</a><br/></p></td><td> (Любое обновление в игре делает предыдущую версию нерабочей)</td></tr>'
    if needVersion:
        res += 'Не найдена или устарела версия игры.<br/>Для дальнейших действий нужно получить последнюю версию игры.'
    else:
        res += '<tr><td><p><a href="/run/actions/getPlayerInfo">Получить информацю игрока</a><br/></p></td><td> (Ресурсы, энергия, орден)</td></tr>'
        if canFight: res += '<tr><td><p><a href="/run/actions/attack/1/pvp/0" onclick = "if (!confirm(\'Начать штурм игроком: '+u_(player["name"])+'?\')) return false;">Совершить штурм</a><br/></p></td><td> (Лог боя и результаты будут выведены)</td></tr>'
        res += '<tr><td><p><a href="/run/actions/getPresentBox">Получить подарок ежедневку</a><br/>'
        res += '<a href="/run/actions/getPresentEnergy">Получить подарок энергию</a></p>'
        res += '</td><td> (За сутки можно получить суммарно всего 5 подарков.)</td></tr>'
        res += '<tr><td><p><a href="/run/actions/quest">Выполнить квесты</a><br/></p></td><td> (Выполняются активные квесты, для новых этапов нужно войти в игру)</td></tr>'
        res += '<tr><td><p>Получить поселения в области карты: '
        res += '<form action="/run/actions/getMapRect">'
        res += 'x <input type="number" name="x" min="-2000" max="2000" value="'+str(x)+'">'
        res += ' y <input type="number" name="y" min="-2000" max="2000" value="'+str(y)+'">'
        res += '<input type="submit" value="->">'
        res += '</form><br/></p></td><td> (Будут выведены поселения с возможностью атаки/защиты)</td></tr>'
    res += '</table></p><br/>'
    
    if attack:
        pid, auth = getPlayer()
        cycle = None
        if len(sys.argv)>2: cycle = sys.argv[2]
        battleType = None
        if len(sys.argv)>3: battleType = sys.argv[3]
        sity = None
        if len(sys.argv)>4: sity = sys.argv[4]
        if not pid or not auth or not sity or not battleType or not cycle:
            res += "Не выбран игрок или возникла проблема с его получением."
        else:
            answ = runScript(['fight', pid, '0', cycle, battleType, sity])
            try:
                ana = answ.split('\n')
                wasError = False
                wasFriend = False
                for anal in ana:
                    if "error" in anal:
                        wasError = True
                        res += '<p>Обнаружена ошибка: <pre>'+anal+'</pre> Скопируйте лог скрипта снизу для анализа.</p>'
                    if "WARNING" in anal:
                        wasFriend = True
                        res += '<p>Атакован игрок из списка исключений: <pre>'+anal+'</pre></p>'
                    if "TRY" in anal:
                        trys = 'TRY: id:'
                        lvls = ', level:'
                        ids = anal[anal.index(trys)+len(trys):anal.index(lvls)]
                        res += '<p>Атакован игрок: '+anal.replace(trys, '<a target="_blank" href="https://vk.com/id'+ids+'">https://vk.com/id').replace(lvls, '</a>, Уровень: ').replace(', clan:no clan', ', без ордена').replace(', clan:', ', Орден: ')+'</p>'
                    if "START ENERGY =" in anal:
                        res += '<p>Энергия для атаки в начале боя: '+anal.replace('START ENERGY =', '')+'</p>'
                    if "END ENERGY =" in anal:
                        res += '<p>Энергия для атаки в конце боя: '+anal.replace('END ENERGY =', '')+'</p>'
                if not wasError and not wasFriend:
                    res += '<p>Бой прошел успешно.</p><br/>'
            except: None
            res += getRunLog(answ)

    if healSity:
        pid, auth = getPlayer()
        sity = None
        if len(sys.argv)>2: sity = sys.argv[2]
        if not pid or not auth or not sity:
            res += "Не выбран игрок или возникла проблема с его получением."
        else:
            answ = runScript(['healSity', pid, auth, sity])
            try:
                maps = json.loads(answ)
                if not maps["error"] == 0: res += getErrorLog(maps["error"])
                else:
                    res += '<p>Защита города прошла успешно</p>'
            except: None
            res += getRunLog(answ)
            
    if getMapRect:
        x,y = getMapRectParams()
        pid, auth = getPlayer()
        if not pid or not auth:
            res += "Не выбран игрок или возникла проблема с его получением."
        else:
            player_name = u_(player["name"])
            answ = runScript(['getMapRect', pid, auth, x, y])
            try:
                maps = json.loads(answ)
                if not maps["error"] == 0: res += getErrorLog(maps["error"])
                else:
                    res += '<p><table border=1 width="100%">'
                    res += '<tr><td>Тип</td><td>Уровень</td><td>Имя</td><td>Орден</td><td>Доход</td><td>Координаты</td><td>Пометки</td><td>Действие</td></tr>'
                    for sity_name in maps["map"]:
                        sity = maps["map"][sity_name]
                        if sity.has_key("type") and sity["type"] == "castle":
                            res += getPrintSity("Крепость", sity, maps, player_name, canFight)
                    for sity_name in maps["map"]:
                        sity = maps["map"][sity_name]
                        if sity.has_key("type") and sity["type"] == "town":
                            res += getPrintSity("Город", sity, maps, player_name, canFight)
                    for sity_name in maps["map"]:
                        sity = maps["map"][sity_name]
                        if sity.has_key("type") and sity["type"] == "village":
                            res += getPrintSity("Деревня", sity, maps, player_name, canFight)
                    res += '</table></p>'    
            except: None
            res += getRunLog(answ)
            
    if getPresentEnergy:
        pid, auth = getPlayer()
        if not pid or not auth:
            res += "Не выбран игрок или возникла проблема с его получением."
        else:
            answ = runScript(['getPresentEnergy', pid, auth])
            try:
                answ2 = json.loads(answ)
                if not answ2["error"] == 0: res += getErrorLog(answ2["error"])
                else:
                    hashStr = answ2["presentURL"]
                    res += '<p>Подарок успешно получен: <a href='+hashStr+'>'+hashStr+'</a></p>'
            except: None
            res += getRunLog(answ)
    
    if getPresentBox:
        pid, auth = getPlayer()
        if not pid or not auth:
            res += "Не выбран игрок или возникла проблема с его получением."
        else:
            answ = runScript(['getPresentBox', pid, auth])
            try:
                answ2 = json.loads(answ)
                if not answ2["error"] == 0: res += getErrorLog(answ2["error"])
                else:
                    hashStr = answ2["presentURL"]
                    res += '<p>Подарок успешно получен: <a href='+hashStr+'>'+hashStr+'</a></p>'
            except: None
            res += getRunLog(answ)
    
    if quest:
        pid, auth = getPlayer()
        if not pid or not auth:
            res += "Не выбран игрок или возникла проблема с его получением."
        else:
            answ = runScript(['quest', pid, auth])
            try:
                answ2 = json.loads(answ)
                if not answ2["error"] == 0: res += getErrorLog(answ2["error"])
                else:
                    q_ar = answ2["questsDone"]
                    qs = ""
                    for q in q_ar: qs+=str(q) + " "
                    res += '<p>Выполненные квесты: (Всего '+str(len(q_ar))+')'+qs+'</p>'
            except: None
            res += getRunLog(answ)
    
    if getBuildInfo:
        answ = runScript(['getBuildInfo'])
        ana = answ.split('\n')
        new_version = "None"
        for anal in ana:
            preLine = "server info version = "
            if preLine in anal: new_version = anal[anal.index(preLine)+len(preLine):]

        if new_version != "None": setTMPParameter("game_version", str(new_version))
        if "200" in answ: res += "<p>Версия игры успешно обновлена до "+str(new_version)+"</p>"
        res += getRunLog(answ)
        
    if getPlayerInfo:
        pid, auth = getPlayer()
        if not pid or not auth:
            res += "Не выбран игрок или возникла проблема с его получением."
        else:
            answ = runScript(['getPlayerInfo', pid, auth])
            try:
                info = json.loads(answ)
                if not info["error"] == 0: res += getErrorLog(info["error"])
                else:
                    info_s = {
                        'stone' : "Ресурс камень",
                        'epower'  : 'Уровень экономики',
                        'power' : 'Сила армии',
                        'level' : 'Уровень',
                        'money' : 'Золото',
                        'energy' : 'Энергия для штурмов',
                        'cash' : 'Кристаллы',
                        'wood' : 'Ресурс дерево',
                        'iron' : 'Ресурс железо',
                        'population' : 'Население'
                    }
                    if info.has_key("player"):
                        for entry in info["player"]:
                            if entry in info_s:
                                res += info_s[entry] +": "+u_(str(info["player"][entry]))+"<br/>"
                    res += "Рейтинг: "+u_(str(info["playerStats"]['honor']))+"<br/>"
                                
                    try:
                        if info.has_key("clan") and info["clan"].has_key("info"):
                            res+="<br/>Информация ордена:<br/>"
                            res+="&nbsp;&nbsp;&nbsp;&nbsp;Название: "+u_(info["clan"]["info"]["name"])+'<br/>'
                            res+="&nbsp;&nbsp;&nbsp;&nbsp;Рейтинг: "+u_(info["clan"]["info"]["rating"])+'<br/>'
                            res+="&nbsp;&nbsp;&nbsp;&nbsp;ГВ рейтинг: "+u_(info["clan"]["info"]["gwrating"])+'<br/>'
                    except:
                        res += "<br/>Не удалось получить данные об ордене.<br/>"
                        
                    try:
                        energy_value,td = getGlobalEnergy(info["playerStats"]["gwAttacks"])
                        res += "Энергия для глобальной атаки: "+str(energy_value)+". До следующей осталось "+td+" (иногда таймер сбивается)<br/>"
                        energy_value,td = getGlobalEnergy(info["playerStats"]["gwHeals"])
                        res += "Энергия для глобальной защиты: "+str(energy_value)+". До следующей осталось "+td+" (иногда таймер сбивается)<br/>"
                    except:
                        res += "Не удалось получить данные о глобальной войне.<br/>"

            except Exception as ex:
                print "getInfo error:\n", sys.exc_info()
            res += getRunLog(answ)


    res += '<p><a href="/run/actions">Вернуться</a></p>'
    print res

attack = sys.argv[1] == "attack"
healSity = sys.argv[1] == "healSity"
getMapRect = sys.argv[1] == "getMapRect"
getBuildInfo = sys.argv[1] == "getBuildInfo"
getBuildInfoLight = sys.argv[1] == "open"
getPlayerInfo = sys.argv[1] == "getPlayerInfo"
getPresentBox = sys.argv[1] == "getPresentBox"
getPresentEnergy = sys.argv[1] == "getPresentEnergy"
quest = sys.argv[1] == "quest"

commonHead()
getHead()
