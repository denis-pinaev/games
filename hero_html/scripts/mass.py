# -*- coding: utf-8 -*-
import json
import sys
import os
from common_head import *

def getHead():
    res = "<p>В данном разделе представлены операции для групп игроков выбранного ордена.</p>"
    res += "<p>Все игроки выбранного ордена, которые были внесены в <a href=\"/run/players/\">базу игроков</a>, будут выполнять одинаковое действие из списка ниже.</p>"
    res += "<p><b>В разработке. Пока все действия снизу идентичны <a href=\"/run/actions/\">одиночным действиям</a>.</b></p>"

    pid, auth = getPlayer()
    if not auth or not pid:
        res += '<p>Для действий в игре выберите игрока.</p>'
        res += '<p>Вернуться к <a href="/run/players/open">выбору активного игрока</a> для дальнейших операций.</p>'
        print res
        return

    player = loadPlayer(pid)
    needVersion = not os.path.exists('./buildInfo.py')
    canFight = os.path.exists('./fight.py')
    res += '<p><table style="border-spacing:15px">'
    res += '<tr><td><p><a href="/run/actions/getBuildInfo">Получить последнюю версию игры</a><br/></p></td><td> (Любое обновление в игре делает предыдущую версию нерабочей)</td></tr>'
    if needVersion:
        res += 'Не найдена версия игры.<br/>Для дальнейших действий нужно получить последнюю версию игры.'
    else:
        res += '<tr><td><p><a href="/run/actions/getPlayerInfo">Получить информацю ордена</a><br/></p></td><td> (Игроки, энергия, поселения)</td></tr>'
        if canFight: res += '<tr><td><p><a href="/run/actions/attack/1/pvp/0" onclick = "if (!confirm(\'Начать штурм всеми игроками ордена: '+u_(player["name"])+'?\')) return false;">Совершить штурм</a><br/></p></td><td> (Лог боя и результаты будут выведены)</td></tr>'
        res += '<tr><td><p>Получить поселения в области карты: '
        res += '<form action="/run/actions/getMapRect">'
        res += 'x <input type="number" name="x" min="-2000" max="2000" value="0">'
        res += ' y <input type="number" name="y" min="-2000" max="2000" value="0">'
        res += '<input type="submit" value="->">'
        res += '</form><br/></p></td><td> (Будут выведены поселения с возможностью атаки/защиты)</td></tr>'
    res += '</table></p><br/>'

    print res

commonHead()
getHead()
