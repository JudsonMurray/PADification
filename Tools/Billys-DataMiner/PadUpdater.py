#!usr/bin/env Python3
#
# NAME: William Gale
# DATE: Aprilish
# PURPOSE: Parse information from PuzzleDragonsx.com in to Tab Delimited Text
#
# ChangeLog
# -- WG -- Star Date 20.23.1522.1 -- The Crew of the PAD Excaliber Fear the worst as the Enemy updates
#       its tactics and numbers unexpectedly but frequently, All hope to stay up to date on the defense
#       seemed hopeless, But worry not brave crew! As the Gungho forces update we shall have their information
#       WE SHALL HAVE THEIR INFORMATION!!!!!
#


import codecs
import urllib
import urllib.request
import urllib.parse
import os
from html.parser import HTMLParser
from pathlib import Path
import Herder
import Evolution

globDict = []
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in



##                          ##
##      English Only List   ## <div class="iframenum">
##                          ## <a href="monster.asp?n=   to   "><img
def getUSList():

    page = urllib.request.urlopen('http://puzzledragonx.com/en/monsterbook.asp?ue=0&us=1&s1=1&s2=0&o1=1&o2=1&o3=1')
    data = page.read().decode('utf-8')
    USListFile = codecs.open('USList.py','w','utf-8')
    
    USListFile.write('USList = [ ')

    index = data.find('<div class="iframenum">')
    while data[index + len('<div class="iframenum">') : data.find('</div>',index)].isalnum():
        index = data.find('<div class="iframenum">',index)
        USListFile.write(data[index + len('<div class="iframenum">') : data.find('</div>',index)] + ',\n')
        index = data.find('</div>',index)
        index = data.find('<div class="iframenum">',index)
        

    USListFile.write(']')
    USListFile.close()
##                          ##
##       carddata.js        ##
##                          ##
def updateCardData(list):
    carddata = urllib.request.urlopen('http://puzzledragonx.com/en/script/autocomplete/carddata.js')
    Data = carddata.read().decode('utf-8')

    Data = Data[16:]
    carddata = eval(Data)
    CardDataFile = codecs.open('CardData.txt','w','utf-8')
    CardDataFile.write("MonsterID\tMonsterName\tMonsterNameJP\tRarity\tAttributeOne\tAttributeTwo\tMonsterTypeOne\tMonsterTypeTwo\tMaxLevel\tMaxHP\tMaxATK\tMaxRCV\tNumOfAwokenSkills\tUNKNOWN\tLeaderSkillDesc\tMonsterCost\tActiveSkillMaxCoolDown\tActiveSkillMaxLevel\tExperienceScale\tMonsterTypeThree\tUNKNOWNTWO" + "\n")
    
    for i in carddata:
        if i[0] in list:
            line = ""
            for o in i:
                line += (str(o) + "\t")
            CardDataFile.write(line + "\n")

    CardDataFile.close()
    print("CardData Updated.")
    
##                          ##
##      Dictionary.txt      ##
##                          ##
def updateDictionary(list):

    Dictionary = urllib.request.urlopen('http://puzzledragonx.com/en/script/autocomplete/dictionary.txt')
    Data = Dictionary.read().decode('utf-8')
    DictionaryFile = codecs.open('Dictionary.txt','w','utf-8')
    Data = eval(Data[Data.find('[[1,"Tyrra","') : Data.find(',"pages":')])
    DictionaryFile.write("MonsterID\tMonsterName\tMonsterNameJP\tRarity\tAttributeOne\tMaxLevel\tNumOfAwokenSkills" + "\n")

    for i in Data:
        if i[0] in list:
            line = ""
            for o in i:
                line += (str(o) + "\t")
            DictionaryFile.write(line + "\n")
    DictionaryFile.close()
    print("Dictionary Updated.")

##                          ##
##      comparison.js       ##
##                          ##
def updateComparison(list):
    comparison = urllib.request.urlopen('http://puzzledragonx.com/en/script/comparison/comparison.js')
    Data = comparison.read().decode('utf-8')
    comparisonFile = codecs.open('comparison.txt','w','utf-8')
    Data = eval(Data[Data.find('{') : Data.find(';'):] )
    comparisonFile.write("MonsterID\tMaxLevel\tMaxHP\tMaxATK\tMaxRCV\tGrowthRateHP\tGrowthRateATK\tGrowthRateRcv\tCurSell\tCurFodder\tMinHP\tMinATK\tMinRCV" + "\n")
    for i in Data:
        if int(i) in list:
            line = str(i) + "\t"
            for o in Data[i]:
                line += (str(o) + "\t")
            comparisonFile.write(line + "\n")
    comparisonFile.close()
    print("Comparison Updated.")
##                          ##
##      MonsterAwoken.js    ##
##                          ##
def updateMonsterAwoken(list):
    AwokenSkills = urllib.request.urlopen('http://puzzledragonx.com/en/script/json/awokenskill.js')
    AwokenSkillData = AwokenSkills.read().decode('utf-8')
    AwokenSkillData = eval(AwokenSkillData[AwokenSkillData.find('{') : AwokenSkillData.find('}')+1:] )

    monsterawoken = urllib.request.urlopen('http://puzzledragonx.com/en/script/json/monsterawoken.js')
    Data = monsterawoken.read().decode('utf-8')
    monsterawokenFile = codecs.open('monsterawoken.txt','w','utf-8')
    Data = eval(Data[Data.find('{') : Data.find(';'):] )

    monsterawokenFile.write("ASListID\tAwokenSkillOne\tAwokenSkillTwo\tAwokenSkillThree\tAwokenSkillFour\tAwokenSkillFive\tAwokenSkillSix\tAwokenSkillSeven\tAwokenSkillEight\tAwokenSkillNine\n")
    for i in Data:
        if int(i) in list:
            line = str(i) + "\t"
            for o in range(0,9):
                try:
                    line += ("'" + str(AwokenSkillData[Data[i][o]][0]) + "'\t")
                except:
                    line += ('NULL\t')
            monsterawokenFile.write(line + "\n")
    monsterawokenFile.close()
    print("MonsterAwoken Updated.")

##                          ##
##      AwokenSkills.js     ##
##                          ##
def updateAwokenSkills():
    AwokenSkills = urllib.request.urlopen('http://puzzledragonx.com/en/script/json/awokenskill.js')
    AwokenSkillData = AwokenSkills.read().decode('utf-8')
    AwokenSkillsFile = codecs.open('AwokenSkills.txt','w','utf-8')
    AwokenSkillData = eval(AwokenSkillData[AwokenSkillData.find('{') : AwokenSkillData.find('}')+1:] )

    AwokenSkillsFile.write("ID\tName\tDescription\tValue\n")
    for i in AwokenSkillData:
        line = str(i) + "\t"
        for o in AwokenSkillData[i]:
            line += (str(o) + "\t")
        AwokenSkillsFile.write(line + "\n")
    AwokenSkillsFile.close()
    print('AwokenSKills Updated')
##                          ##
##      Thumbnails          ##
##                          ##
def updateThumbNails(list):
    for i in list:
        image = Path(os.path.join(script_dir, 'thumbnails/' + str(i[0]) + '.png'))
        if image.is_file():
            print(i[0], "exists already")
        else:
            try:
                urllib.request.urlretrieve('http://www.puzzledragonx.com/en/img/book/' + str(i[0]) +'.png', os.path.join(script_dir, 'thumbnails/' + str(i[0]) + '.png'))
                print(i[0], "Saved")
            except urllib.error.HTTPError:
                print("No image for", i[0])
    print('ThumbNails Saved')
##                          ##
##      Portraits           ##
##                          ##
def updatePortrait(list):
    for i in list:
        image = Path(os.path.join(script_dir, 'portraits/'+ str(i[0]) + '.jpg'))
        if image.is_file():
            print(i[0], "Portrait exists already")
        else:
            try:
                urllib.request.urlretrieve('http://www.puzzledragonx.com/en/img/monster/MONS_' + str(i[0]) +'.jpg', os.path.join(script_dir, 'portraits/' + str(i[0]) + '.jpg'))
                print(i[0], "Portrait Saved")
            except urllib.error.HTTPError:
                print("No image for", i[0])
    print('Portaits Saved')
##                  ##
##      PADHerder   ##
##                  ##
def monsterPADHerder(list):
    monstersData = Herder.Monsters
    HerderMonsters = codecs.open('HerderMonsters.txt','w','utf-8')

    line = ''    
    firstpass = True
    for i in monstersData:
        if firstpass:
            for o in i:
                line += str(o) + '\t'
            HerderMonsters.write(line + "\n")
            firstpass = False
        line = ''
        if i['id'] in list:
            for o in i:
                line += str(i[o]) + '\t'
            HerderMonsters.write(line + "\n")

    print('PADHerder monster info complete')
    HerderMonsters.close()

##                          ##
##  ActiveSkill PADHerder   ##
##                          ##
def ASPADHerder():
    ASData = Herder.ActiveSkills
    ASDataFile = codecs.open('ASData.txt','w','utf-8')

    line = ''    
    firstpass = True
    for i in ASData:
        if firstpass:
            for o in i:
                line += str(o) + '\t'
            ASDataFile.write(line + "\n")
            firstpass = False
        line = ''  
        for o in i:
            line += str(i[o]) + '\t'
        ASDataFile.write(line + "\n")
    ASDataFile.close()
    print("ASPADHerder Updated")
##                          ##
##  LeaderSkill PADHerder   ##
##                          ##
def LSPADHerder():
    LSData = Herder.LeaderSkills
    LSDataFile = codecs.open('LSData.txt','w','utf-8')

    line = ''    
    firstpass = True
    for i in LSData:
        if firstpass:
            for o in ['name', 'effect']:
                line += str(o) + '\t'
            LSDataFile.write(line + "\n")
            firstpass = False
        line = ''  
        for o in ['name', 'effect']:
            line += str(i[o]) + '\t'
        LSDataFile.write(line + "\n")
    LSDataFile.close()
    print("LSPADHerder Updated")

##                  ##
##  Evolution Tree  ## "1":[{"is_ultimate":false,"materials":[[152,1]],"evolves_to":2}]
##                  ##
def updateEvolution(List):
    EvoData = Evolution.Evolution
    EvoFile = codecs.open('Evolution.txt','w','utf-8')
    count = 0

    EvoFile.write("NextMonster\tBaseMonster\tEvoMaterialOne\tEvoMaterialTwo\tEvoMaterialThree\tEvoMaterialFour\tEvoMaterialFive\tUltimate\n")
    for i in EvoData:
        BaseMonster = i
        NextMonster = None
        EvoMaterial = []
        Ultimate = None
        if int(i) in List:
            BaseMonster = i
            for j in EvoData[i]:
                if int(j['evolves_to']) in List:
                    NextMonster = j['evolves_to']
                    Ultimate = j['is_ultimate']
            
                    for o in  j['materials']:
                        count = o[1]
                        while count > 0:
                            EvoMaterial.append(o[0])
                            count -= 1
                    while len(EvoMaterial) < 5:
                        EvoMaterial.append(None)
                    line = str(NextMonster) + '\t' + str(BaseMonster) + '\t'
                    for o in EvoMaterial:
                        line += str(o) + '\t'
                    line += str(Ultimate) + '\n'
                    EvoFile.write(line)
                    EvoMaterial = []
    print("Evolution Updated")

#getUSList()
import USList

#updateAwokenSkills()
#updateCardData(USList.USList)
#updateDictionary(USList.USList)
#updateComparison(USList.USList)
#KupdateMonsterAwoken(USList.USList)
#monsterPADHerder(USList.USList)
#updateThumbNails(USList.USList)
#updatePortrait(USList.USList)
#LSPADHerder()
#ASPADHerder()
updateEvolution(USList.USList)
