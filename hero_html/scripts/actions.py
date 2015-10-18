# -*- coding: utf-8 -*-
import json
import sys
import urllib
import datetime
from common_head import *

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
    

def getHead():
    res = ""
    selected_pid = getTMPParameter("pid", None)
    if not selected_pid:
        res += '<p>Для действий в игре выберите игрока.</p>'
        res += '<p>Вернуться к <a href="/run/players/open">выбору активного игрока</a> для дальнейших операций.</p>'
        print res
        return
    PLAYERS = loadPLAYERS()
    res += '<p><table style="border-spacing:15px">'
    res += '<tr><td><p><a href="/run/actions/getBuildInfo">Получить последнюю версию игры</a><br/></p></td><td> (Любое обновление делает предыдущую версию нерабочей)</td></tr>'
    res += '<tr><td><p><a href="/run/actions/getPlayerInfo">Получить информацю игрока</a><br/></p></td><td> (Ресурсы, энергия, орден)</td></tr>'
    res += '<tr><td><p><a href="/run/actions/getPresentBox">Получить подарок ежедневку</a><br/>'
    res += '<a href="/run/actions/getPresentEnergy">Получить подарок энергию</a></p>'
    res += '</td><td> (За сутки можно получить суммарно всего 5 подарков.)</td></tr>'
    res += '<tr><td><p><a href="/run/actions/getMapRect">Получить область карты 100:50</a><br/></p></td><td> (будет доделано из координат по запросу)</td></tr>'
    res += '</table></p><br/>'

    if getMapRect:
        pid, auth = getPlayer()
        if not pid or not auth:
            res += "Не выбран игрок или возникла проблема с его получением."
        else:
            answ = runScript(['getMapRect', pid, auth])
            if True:
                maps = json.loads(answ)
                res += '<p><table border=1 width="100%">'
                res += '<tr><td>Тип</td><td>Уровень</td><td>Имя</td><td>Орден</td><td>Доход</td><td>Координаты</td><td>Пометки</td><td>Выбрать</td></tr>'
                for sity_name in maps["map"]:
                    sity = maps["map"][sity_name]
                    if sity.has_key("type") and sity["type"] == "town":
                        stype = "Город"
                        slevel = str(sity["level"])
                        sincome = str(sity["income"])
                        sclan = ""
                        if sity.has_key("clan_id"):
                            sclan = u_(maps["clans"][str(sity["clan_id"])]["name"])
                        sresources = str(int(sity["resources"]))
                        sname = u_(sity["name"])
                        sx = str(sity["x"])
                        sy = str(sity["y"])
                        sid = str(sity["id"])
                        abandoned = sity.has_key("abandoned")
                        dammaged = sity.has_key("maxDamage")
                        mark = ""
                        if(abandoned): mark+="Покинута. "
                        if(dammaged): mark+="Атакован. "
                        res += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s (%s в сутки)</td><td>%s:%s</td><td>%s</td><td><a href="/run/actions/selectSity/%s">Выбрать</a></td></tr>' % (stype,slevel,sname,sclan,sresources,sincome,sx,sy,mark,sid)
                for sity_name in maps["map"]:
                    sity = maps["map"][sity_name]
                    if sity.has_key("type") and sity["type"] == "village":
                        stype = "Деревня"
                        slevel = str(sity["level"])
                        sincome = str(sity["income"])
                        sclan = ""
                        if sity.has_key("clan_id"):
                            sclan = u_(maps["clans"][str(sity["clan_id"])]["name"])
                        sresources = str(int(sity["resources"]))
                        sname = u_(sity["name"])
                        sx = str(sity["x"])
                        sy = str(sity["y"])
                        sid = str(sity["id"])
                        abandoned = sity.has_key("abandoned")
                        dammaged = sity.has_key("maxDamage")
                        mark = ""
                        if(abandoned): mark+="Покинута. "
                        if(dammaged): mark+="Атакована. "
                        res += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s (%s в сутки)</td><td>%s:%s</td><td>%s</td><td><a href="/run/actions/selectSity/%s">Выбрать</a></td></tr>' % (stype,slevel,sname,sclan,sresources,sincome,sx,sy,mark,sid)
                res += '</table></p>'    
                if maps["error"] == 0:
                    res += '<p>успешно</a></p>'
            #except: None
            res += getRunLog(answ)
            
    if getPresentEnergy:
        pid, auth = getPlayer()
        if not pid or not auth:
            res += "Не выбран игрок или возникла проблема с его получением."
        else:
            answ = runScript(['getPresentEnergy', pid, auth])
            try:
                answ2 = json.loads(answ)
                if answ2["error"] == 0:
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
                if answ2["error"] == 0:
                    hashStr = answ2["presentURL"]
                    res += '<p>Подарок успешно получен: <a href='+hashStr+'>'+hashStr+'</a></p>'
            except: None
            res += getRunLog(answ)
    
    if getBuildInfo:
        answ = runScript(['getBuildInfo'])
        res += getRunLog(answ)
        
    if getPlayerInfo:
        pid, auth = getPlayer()
        if not pid or not auth:
            res += "Не выбран игрок или возникла проблема с его получением."
        else:
            answ = runScript(['getPlayerInfo', pid, auth])
            try:
                info = json.loads(answ)
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
                    td = (datetime.datetime.now() - datetime.datetime.fromtimestamp(int(info["playerStats"]["gwAttacks"])-60*60)).total_seconds()
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
                    res += "Энергия для глобальной атаки = "+str(energy_value)+" До следующей осталось "+td+" (иногда таймер сбивается)<br/>"
                    td = (datetime.datetime.now() - datetime.datetime.fromtimestamp(int(info["playerStats"]["gwHeals"])-60*60)).total_seconds()
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
                    res += "Энергия для глобальной защиты = "+str(energy_value)+" До следующей осталось "+td+" (иногда таймер сбивается)<br/>"
                except:
                    res += "Не удалось получить данные о глобальной войне.<br/>"

            except Exception as ex:
                print "getInfo error:\n", sys.exc_info()
            res += getRunLog(answ)


    res += '<p><a href="/run/actions">Вернуться</a></p>'
    print res

getMapRect = sys.argv[1] == "getMapRect"
getBuildInfo = sys.argv[1] == "getBuildInfo"
getPlayerInfo = sys.argv[1] == "getPlayerInfo"
getPresentBox = sys.argv[1] == "getPresentBox"
getPresentEnergy = sys.argv[1] == "getPresentEnergy"

commonHead()
getHead()
