import pyamf
import sys
import json
import datetime
import time
from pyamf.remoting.client import RemotingService
import requests
import random

sig = '4de6b3f2f43c13aa3d3729f3644628d4'




def getPlayersParams():
    return {
        'link':'http://vk.com/id124520',
        'photo_medium':'http://cs11514.vk.me/v11514520/1378/RktOGMb9ozk.jpg',
        'last_name':'Pinaev',
        'first_name':'Denis',
        'country':1,
        'uid':124520,
        'bdate':'8.3.1985',
        'sex':2
    }
    
def log(s):
    s = "[" + datetime.datetime.now().strftime('%d.%m %H:%M:%S')+"] " + s
    fatype = "zlog_collect"
    try:
        tfile = open(fatype, "a")
        tfile.write(s.encode('utf-8')+'\n')
        tfile.close()
    except:
        tfile = open(fatype, "w")
        tfile.write(s.encode('utf-8')+'\n')
        tfile.close()
        
def getRandom():
    return str(int(random.random()*100000))

def sendRequest(sig, command, params=None):
    client = RemotingService('http://armor5-two.ru/hunter/amfphp/server.php')
    service = client.getService('EntryPointGame/workRequest')
    return service._call('EntryPointGame/workRequest',sig,command,params)
    
    #client = RemotingService('http://37.200.66.212/current/gateway.php')
    #service = client.getService(command)
    #return service._call(command,pid,gid,params)
    
    
def getPlayer(params = {}):
    command = "Players.getPlayer"
    resp = False
    try:
        resp = sendRequest(sig,command,params)
    except:
        log("User: %s, Command: %s, ERROR!"%(sig,command))
    return resp
        
def getQuestPlayer(change = False):
    command = "Quest.getQuestPlayer"
    params = {'client':True} if change else {}
    resp = False
    try:
        resp = sendRequest(sig,command,params)
    except:
        log("User: %s, Command: %s, ERROR!"%(sig,command))
    return resp
        
def getResBuilds():
    command = "Builds.getPlayerBuildLocation"
    params = {}
    resp = False
    try:
        resp = sendRequest(sig,command,params)
    except:
        log("User: %s, Command: %s, ERROR!"%(sig,command))
    return resp
        
def collectResBuild(bid):
    command = "Builds.movingResourceByPlayer"
    params = {'id':int(bid)}
    resp = False
    try:
        resp = sendRequest(sig,command,params)
    except:
        log("User: %s, Command: %s, ERROR!"%(sig,command))
    return resp

def startAttack(quest):
    #return True
    command = "Quest.startAtack"
    params = {'name':quest}
    resp = False
    try:
        resp = sendRequest(sig,command,params)
    except:
        log("User: %s, Command: %s, ERROR!"%(sig,command))
    return resp

def killMob(mob):
    #return True
    command = "Quest.updateAtack"
    params = {'id':int(mob)}
    resp = False
    try:
        resp = sendRequest(sig,command,params)
    except:
        log("User: %s, Command: %s, ERROR!"%(sig,command))
    return resp

def checkNewLevel():
    command = "Players.checkNewLevel"
    params = {}
    resp = False
    try:
        resp = sendRequest(sig,command,params)
    except:
        log("User: %s, Command: %s, ERROR!"%(sig,command))
    return resp
    
def sale(count):
    command = "Products.saleProductsByPlayer"
    params = {'count':int(count), 'id':10}
    resp = False
    try:
        resp = sendRequest(sig,command,params)
    except:
        log("User: %s, Command: %s, ERROR!"%(sig,command))
    return resp
    
def doCommand(command, params):
    resp = False
    try:
        resp = sendRequest(sig,command,params)
    except:
        log("User: %s, Command: %s, ERROR!"%(sig,command))
    return resp

    

def checkZavod():
    timers = doCommand('Timers.getTimers', {})
    try:
        zid = '329799'
        zidf = False
        for t in timers:
            if t.has_key('data') and t['data'].has_key('player_build_id') and t['data']['player_build_id'] == zid:
                zidf = True
                break
        if not zid:
            doCommand('Builds.addStartProductionResource', {'timer':False,'id':int(zid)})
            print 'VoenZavod started'
        else: print 'VoenZavod working'
    except: print 'error Timers.getTimers'

def collectBuildings(builds):
    needCheck = True
    for b in builds:
        if b.has_key('store_now') and int(b['store_now']) >= 1:
            if ('Plavilnya' in b['name_view']) or ('Shaht' in b['name_view']) or ('Voenzavod' in b['name_view']):
                print b['store_now'], 'in', b['player_build_id'], 'is', b['name_view'], collectResBuild(b['player_build_id'])['no_error']
                if 'Voenzavod' in b['name_view']: sale(b['store_now']); needCheck = False
    if needCheck: checkZavod()
            
def makeQuest(quest, player, quests):
    if player:
        if len(quests)>0:
            for q in quests:
                if q.has_key('name_type_quest') and q['name_type_quest'] == quest:
                    ce = int(player['energy'])
                    ne = int(q['energy_spend'])
                    print 'Energy: is %d, need %d'% (ce, ne)
                    if ce>=ne:
                        startQuest(q)
                        print 'energy', ce-ne
                    return
            print 'no quest'

def startQuest(quest):
    if quest.has_key('data'):
        quest_mobs = {}
        for m in quest['data']:
            mob = quest['data'][m]
            quest_mobs[mob['id']] = int(mob['count'])
        attack = startAttack(quest['name_type_quest'])
        if attack:
            for mob in quest_mobs:
                for i in range(quest_mobs[mob]):
                    print mob, i, killMob(mob)

def get_sig():
    url = "http://armor5-two.ru/hunter/index.php?api_url=http://api.vk.com/api.php&api_id=3520886&api_settings=2367494&viewer_id=124520&viewer_type=2&sid=%s&secret=%s&access_token=%s&user_id=124520&group_id=0&is_app_user=1&auth_key=23fb9d636ea543ec00b3907e398ed839&language=0&parent_language=0&ad_info=ElsdCQBeRVBmBRIKQgYIC35tWxEKDw5VR0FVIxEIYxFKVTluVg==&is_secure=0&ads_app_id=3520886_3b7ad026113b3f4f46&referrer=user_apps&lc_name=%s&hash=" % (getRandom(), getRandom(), getRandom(), getRandom())
    resp = requests.get(url, allow_redirects=True)
    text = resp.text
    s1 = text.find("var sid         = '")
    s2 = text.find("';",s1)
    #s1 = text.find('<p>Session: ')
    #s2 = text.find(' <b>version:')
    return text[s1+19:s2]

def getMobsInQuest(questt, quests):
    if len(quests)>0:
        for quest in quests:
            if quest.has_key('name_type_quest') and quest['name_type_quest'] == questt:
                mq = 0
                if quest.has_key('data'):
                    quest_mobs = {}
                    for m in quest['data']:
                        mob = quest['data'][m]
                        mq += int(mob['count'])
                        #print mob['id'], mob['count']
                return mq
        print 'no quest'
    return 0

def check_session(session, reconnect = False):
    global sig
    if not session or 'Close connect!' in session:
        print 'SESSION EXPIRE'
        if not reconnect: return False
        sig = get_sig()
        refreshTimers()
        return True
    return session

def refreshTimers():
    doCommand('Timers.getServerTime', {})
    doCommand('Timers.getTimers', {})
    doCommand('Players.getPlayer', {})
    
def getGoodQuest(quest):
    wanted = 20
    count = 0
    quests = getQuestPlayer()
    if quests: count = getMobsInQuest(quest, quests)
    print 'start count =', count
    while count<wanted:
        quests = getQuestPlayer(True)
        if quests:
            count = getMobsInQuest(quest, quests)
            print 'count =', count
        else: break
    print 'final count =', count
    return quests




def main_fight():
    print datetime.datetime.now().strftime('%H:%M:%S')
    refreshTimers()
    player = check_session(getPlayer())
    quest = 'arena_hard'#'arena_hard'#'quest_one'
    if player: quests = getGoodQuest(quest)#getQuestPlayer()
    if player and quests: makeQuest(quest, player, quests)
    
def main_cfight():
    while check_session(getPlayer(), True):
        print datetime.datetime.now().strftime('%H:%M:%S')
        player = check_session(getPlayer())
        refreshTimers()
        quest = 'arena_hard'#'arena_hard'#'quest_one'
        if player: quests = getGoodQuest(quest)#getQuestPlayer()
        if player and quests:
            e = int(player['energy'])
            while e>30:
                makeQuest(quest, player, quests)
                refreshTimers()
                e = int(getPlayer()['energy'])
        time.sleep(16*60)
    
def main_collect():
    print datetime.datetime.now().strftime('%H:%M:%S')
    refreshTimers()
    if True:
        builds = check_session(getResBuilds())
        if builds: collectBuildings(builds)
        
def main_ccollect():
    while check_session(getPlayer(), True):
        print datetime.datetime.now().strftime('%H:%M:%S')
        refreshTimers()
        builds = check_session(getResBuilds())
        if builds: collectBuildings(builds)
        #main_boss()
        time.sleep(10*60)
        
def main_boss():
    if check_session(getPlayer(), True):
        print datetime.datetime.now().strftime('%H:%M:%S')
        refreshTimers()
        player = check_session(getPlayer())
        e = 0
        try:
            if player: e = int(player['energy'])
        except: e = 0
        print 'energy:', e
        while e>=30:
            res = doCommand('Quest.startBoss', {'name':'Denis Pinaev','id':1101})
            if not res: print 'error in boss start'; return
            res = doCommand('Quest.getInfoBossFight', {'id':41312})
            if not res: print 'error in getInfoBossFight'; return
            res = doCommand('Quest.getInfoBossPlayer', {'id':41312})
            if not res: print 'error in getInfoBossPlayer'; return
            boss_life = 1
            while boss_life>0:
                res = doCommand('Quest.updateBoss', {})
                if not res: print 'error in updateBoss'; return
                boss_life = int(res['boss_life'])
                print 'boss life:', boss_life
            res = doCommand('Quest.updateAtack', {'id':101})
            res = doCommand('Quest.getAwardOnBoss', {'type':False})
            e -= 30
            print 'energy:', e
        
        
def main_cccf():
    while check_session(getPlayer(), True):
        print datetime.datetime.now().strftime('%H:%M:%S')
        player = check_session(getPlayer())
        refreshTimers()
        quest = 'arena_hard'#'arena_hard'#'quest_one'
        if player: quests = getGoodQuest(quest)#getQuestPlayer()
        if player and quests:
            e = int(player['energy'])
            while e>50:
                makeQuest(quest, player, quests)
                refreshTimers()
                e = int(getPlayer()['energy'])
        builds = check_session(getResBuilds())
        if builds: collectBuildings(builds)
        time.sleep(10*61)

        
def main_info():
    print datetime.datetime.now().strftime('%H:%M:%S')
    refreshTimers()
    checkNewLevel()
    #getPlayer(getPlayersParams())
    player = check_session(getPlayer())
    if player:
        #print player
        print 'Energy: %s, Exp: %s/%s (%s), Level: %s, Money: %s (%s)\n' % (str(player['energy']),str(player['exp']),str(player['max_exp']),  str(int(player['max_exp'])-int(player['exp']))  ,str(player['level']),str(player['palladium']),str(player['diamonds']))
    else: print 'ERROR in player get'
    quests = check_session(getQuestPlayer())
    if quests:
        quests = sorted(quests, key=lambda x : int(x['exp']), reverse=True)
        for q in quests:
            name = q['name_type_quest'] if q.has_key('name_type_quest') else q['picture']
            print 'Quest: %s, Energy: %s, Exp: %s, Money: %s (%s)' % (str(name),str(q['energy_spend']),str(q['exp']),str(q['palladium']),str(q['diamonds']))
    builds = check_session(getResBuilds())
    if builds:
        print ''
        builds = sorted(builds, key=lambda x : x['store_now'], reverse=True)
        for b in builds:
            print 'Building: %s, Count: %s, Level: %s, Work: %s' % (b['name_view'], str(b['store_now']), str(b['level']), str(not(str(b['production_work'])=='0')))
    
        
def main():
    print datetime.datetime.now().strftime('%H:%M:%S')
    print 'zzzz'
      
      
      
#sig = get_sig()
for a in sys.argv[1:]:
    if len(a)>5: sig = a
    if a == 'sig': sig = get_sig()
    if a == 'c': main_collect()
    if a == 'cc': main_ccollect()
    if a == 'cf': main_cfight()
    if a == 'cccf': main_cccf()
    if a == 'f': main_fight()
    if a == 'i': main_info()
    if a == 'b': main_boss()
    if a == 'z': main()
#if True:
#    try:
#        main()
#    except:
#        log(str(sys.exc_info()))
#        print sys.exc_info()