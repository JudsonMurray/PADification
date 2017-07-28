#!usr/bin/env python3
#
#   Name :      WILLIAM GALE
#   Date :      January 18th
#   Purpose:    Base Entities class to be used by Builders

#   History:  
#               bg - jan 18th 2016 -    Initial coding mostly from PlayerClasses.py
#               bg - jan 19th 2016 -    Added Win condition check to Level class
#                                       Added PhotoImage of monsters directly into monster class, 
#                                       can't pickle PhotoImage so i can't add it to player.
from tkinter import PhotoImage

class Player():
    def __init__(self, playerClass = "", playerName = "", playerMaxHp = 0, playerAtk = 0, playerDef = 0, potions = 0, playerImage = ""):
        self.playerName = playerName
        self.playerClass = playerClass
        self.playerMaxHp = playerMaxHp
        self.playerHp = self.playerMaxHp
        self.playerAtk = playerAtk
        self.playerDef = playerDef
        self.playerLevel = 1
        self.potions = potions
        self.hasWon = False
        self.playerImage = playerImage
        self.floorNum = 1
        self.buffs = []
        self.bossKills = 0
        self.attacks = 0
        self.floorsBeat = 0
        self.damageTaken = 0
        self.monsterKills = 0
        self.score = 0
        self.gameMode = "normal"
        

    def addPotions(self, amount):
        self.potions += amount

    def minusPotions(self, amount):
        self.potions -= amount
    
    def usePotion(self):
        if self.hasPotions():
            amount = int(self.playerMaxHp * 0.25 + 5)
            self.minusPotions(1)
            self.addHp(amount)
            return "Used Potion! Healed for " + str(amount)
        else:
            return "No Potions!"

    def hasPotions(self):
        if self.potions > 0:
            return True
        else:
            return False

    def fullHeal(self):
        self.playerHp = self.playerMaxHp

    def isFullHp(self):
        return self.playerHp == self.playerMaxHp

    def addHp(self, amount):
        self.playerHp += amount
        if self.playerHp > self.playerMaxHp:
            self.playerHp = self.playerMaxHp

    def minusHp(self, amount):
        self.playerHp -= amount

    def getHp(self):
        return self.playerHp

    def getAtk(self):
        return self.playerAtk

    def getDef(self):
        return self.playerDef

    def getPots(self):
        return self.potions

    def __str__(self, **kwargs):
        return self.playerName + " the " + self.playerClass + " Level:" + str(self.playerLevel)



class Monster:
    def __init__(self, monName = "", monHP = 0, monAtk = 0, monDef = 0, monSpd = 0, monImg = ""):
        self.monsterName = monName
        self.monsterMaxHp = monHP
        self.monsterHp = self.monsterMaxHp
        self.monsterAtk = monAtk
        self.monsterDef = monDef
        self.monsterSpd = monSpd
        self.monsterImg = monImg
        self.monsterAbilites = []
        self.photoImage = PhotoImage(file = "DTDresource/" + monImg)

    def addMonsterHp(self, amount):
        self.monsterHp += amount
        if self.monsterHp > self.monsterMaxHp:
            self.monsterHp = self.monsterMaxHp
        return

    def minusMonsterHp(self, amount):
        self.monsterHp -= amount
        if self.monsterHp <= 0:
            self.monsterHp = 0
        return

    def monsterDificultyMultiplier(self, amount):
        self.monsterMaxHp *= amount
        self.monsterHp *= amount
        self.monsterAtk *= amount
        self.monsterDef *= amount

    def monsterLvlMultiplier(self, amount):
        self.monsterMaxHp += int(self.monsterMaxHp * (amount * 0.08))
        self.monsterHp = self.monsterMaxHp
        self.monsterAtk += int(self.monsterAtk * (amount * 0.08))
        self.monsterDef += int(self.monsterDef * (amount * 0.08))

    def __str__(self, **kwargs):
        return self.monsterName

class FloorLevel:
    def __init__(self, monsters = [None,None,None], BGM = "battleLoop.wav", winMonster = None):
        self.monsters = monsters
        self.floorMusic = BGM
        self.winMonster = winMonster

    def checkWin(self):
        if self.winMonster == None:
            return self.monsters[0].monsterHp <= 0 and self.monsters[1].monsterHp <= 0 and self.monsters[2].monsterHp <= 0
        elif self.winMonster >= 0 and self.winMonster <= 2:
            return self.monsters[self.winMonster].monsterHp <= 0

    def getFloorMusic(self):
        return self.floorMusic
            


        