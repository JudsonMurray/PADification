#!usr/bin/env python3
#
#   Name :      WILLIAM GALE
#   Date :      January 18th
#   Purpose:    Object builders CombatFrame

#   History:  
#               bg - jan 18th 2016 - Initial coding
#               bg - jan 20th 2016 - Endless Mode Level Generation

import json
import random
from Entities import *


class MasterBuilder:
    def __init__(self):
        self.masterDictionary = {}
        self.masterCollection = []

    def load(self, filename = ""):
        self.masterDictionary = json.load( open(filename, "r") )
        for i in self.masterDictionary:
            self.masterCollection.append(i)

    def build(self):
        pass

class MonsterBuilder(MasterBuilder):
    """ Builds and returns monsters from Data File"""
    def __init__(self):
        super().__init__()
        self.load("DTDresource/EnemyData.txt")

    def build(self, specific = 0):
        if specific == 0:
            for i in range(0,1000):
                choice = random.choice(self.masterCollection)
                if self.masterDictionary[choice]["isBoss"] == False:
                    return Monster(choice, self.masterDictionary[choice]["HpMax"], self.masterDictionary[choice]["Atk"], self.masterDictionary[choice]["Def"], self.masterDictionary[choice]["Speed"],self.masterDictionary[choice]["img"])
        elif specific in self.masterDictionary:
            return Monster(specific, self.masterDictionary[specific]["HpMax"], self.masterDictionary[specific]["Atk"], self.masterDictionary[specific]["Def"], self.masterDictionary[specific]["Speed"],self.masterDictionary[specific]["img"])
        else:
            raise ValueError("Monster does not exist")

class PlayerBuilder(MasterBuilder):
    """Builds and returns player classes from data file"""
    def __init__(self):
        super().__init__()
        self.load("DTDresource/ClassData.txt")

    def build(self, className, playerName):
        if className in self.masterCollection:
            dic = self.masterDictionary
            i = className
            return Player(i, playerName, dic[i]["HpMax"], dic[i]["Atk"], dic[i]["Def"], dic[i]["Pots"], dic[i]["img"])
        else:
            raise ValueError("Class doesn't exist")
        
class LevelBuilder(MasterBuilder):
    """Level constructor"""
    def __init__(self):
        super().__init__()
        self.load("DTDresource/LevelData.txt")
        self.monsterBuilder = MonsterBuilder()

    def build(self,level):
        lDict = self.masterDictionary
        monster = self.monsterBuilder
        try:
            monsterCollection = [monster.build(lDict["Level" + str(level)]["monster1"]), \
                                 monster.build(lDict["Level" + str(level)]["monster2"]), \
                                 monster.build(lDict["Level" + str(level)]["monster3"])]
            try:
                winMons = lDict["Level" + str(level)]["winMonster"]
            except:
                winMons = None

            try:
                music = lDict["Level" + str(level)]["BGM"]
            except:
                music = "battleLoop.wav"
            return FloorLevel(monsterCollection, BGM = music, winMonster = winMons)
        except:
            if level % 10 == 0:
                return FloorLevel([monster.build("Left Arm"),monster.build("Kyle The Destroyer"),monster.build("Right Arm")], BGM = "bossFight.ogg", winMonster = 1)
            else:
                return FloorLevel([monster.build(),monster.build(),monster.build()])




#builder = MonsterBuilder()
#monsters = []
#for i in range(0,3):
#    monsters.append(builder.build())

#monsters.append(builder.build("Kyle The Destroyer"))

#for i in monsters:
#    print(str(i))

#builder = PlayerBuilder()

#player = builder.build("Mage", "Dave")
##print(player)
#levelbuilder = LevelBuilder()

#floor = levelbuilder.build(1)

#for i in floor.monsters:
#    print(i)
