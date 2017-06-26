#!usr/bin/env python3
#
#
#   NAME:       William Gale
#   DATE:       2017-06-23
#   PURPOSE:    All Mathematical Calculations will be described and Handled
#               within this Module for PAD Stats.

import math

class Monster():
    def __init__(self, monsterDictionary):
        #Class Variables
        self.MonsterClassID = None
        self.MonsterName = None
        self.Rarity = None
        self.PriAttribute = None
        self.SecAttribute = None
        self.MonsterTypeOne = None
        self.MonsterTypeTwo = None
        self.MonsterTypeThree = None
        self.ExpCurve = None
        self.MaxLevel = None
        self.MonsterCost = None
        self.ASListID = None
        self.LeaderSkillName = None
        self.ActiveSkillName = None
        self.MaxHP = None
        self.MinHP = None
        self.GrowthRateHP = None
        self.MaxATK = None
        self.MinATK = None
        self.GrowthRateATK = None
        self.MaxRCV = None
        self.MinRCV = None
        self.GrowthRateRCV = None
        self.CurSell = None
        self.CurFodder = None
        self.MonsterPointValue = None
        self.LSSlots = None

        #ActiveSkill Variables
        self.ActiveSkillMaxLevel = 0
        self.ActiveSkillMaxCoolDown = 0
        
        #Instance Variables
        self.InstanceID = None
        self.Username = None
        self.CurrentExperience = 0
        self.PlusATK = 0
        self.PlusRCV = 0
        self.PlusHP = 0
        self.SkillsAwoke = 0
        self.AssistMonsterID = None
        self.SkillLevel = 1
        self.LSListID = None

        #Calculated Variables
        self.MaxExperience = 0
        self.Level = 0
        self.HP = 0
        self.ATK = 0
        self.RCV = 0
        self.TotalHP = 0
        self.TotalATK = 0
        self.TotalRCV = 0
        self.ActiveSkillCoolDown = 0

        for i in monsterDictionary:
            setattr(self,i,monsterDictionary[i])

        self.MaxExperience = self.calcXP(self.MaxLevel, self.ExpCurve)

        if self.InstanceID == None:
            self.CurrentExperience = self.MaxExperience

        self.updateStats()

    def getSaveDict(self):
        savingItems = ['InstanceID', 'Username', 'CurrentExperience', 'PlusATK', 'PlusRCV', 'PlusHP', 'SkillsAwoke', 'AssistMonsterID', 'SkillLevel', 'LSListID', 'MonsterClassID']
        savedict = {}
        for i in savingItems:
            savedict[i] = getattr(self,i)
        return savedict

    def updateStats(self):
        """Updates the Stats of a monster"""
        self.Level = self.calcLevel(self.CurrentExperience, self.ExpCurve)
        self.HP = self.calcStat(self.MinHP, self.MaxHP, self.Level, self.MaxLevel, self.GrowthRateHP)
        self.ATK = self.calcStat(self.MinATK, self.MaxATK, self.Level, self.MaxLevel, self.GrowthRateATK)
        self.RCV = self.calcStat(self.MinRCV, self.MaxRCV, self.Level, self.MaxLevel, self.GrowthRateRCV)        

        self.TotalHP = self.HP + (self.PlusHP * 10)
        self.TotalATK = self.ATK + (self.PlusATK * 5)
        self.TotalRCV = self.RCV + (self.PlusRCV * 3)

    def calcLevel(self, currentXP, curveXP):
        """Calculated the Level of a monster Based on XP"""
        return int((currentXP / curveXP) ** (1/2.5) * 98 + 1)

    def calcXP(self, currentLevel, curveXP):
        """Calculated the Experience Needed at a certian level"""
        return math.ceil(curveXP * ((currentLevel - 1) / 98) ** 2.5)

    def calcStat(self, minStat, maxStat, curLevel, maxLevel, growthRate):
        """Calculated the Value of a stat at a given level"""
        return int(minStat + (maxStat - minStat) * ((curLevel - 1) / (maxLevel - 1)) ** growthRate)

    def setCurrentExperience(self, value):
        """Set CurrentExperience and Update Stats to relect changes."""
        self.CurrentExperience = value
        if self.CurrentExperience < 0:
            self.CurrentExperience = 0
        if self.CurrentExperience > self.MaxExperience:
            self.CurrentExperience = self.MaxExperience
        self.updateStats()

    def getCurrentExperience(self):
        """Return Current Experience"""
        return self.CurrentExperience

    def setPlusATK(self,value):
        """Set PlusATK"""
        self.PlusATK = value
        if self.PlusATK > 99:
            self.PlusATK = 99
        if self.PlusATK < 0:
            self.PlusATK = 0
        self.updateStats()

    def setPlusRCV(self,value):
        """Set PlusRCV"""
        self.PlusRCV = value
        if self.PlusRCV > 99:
            self.PlusRCV = 99
        if self.PlusRCV < 0:
            self.PlusRCV = 0
        self.updateStats()

    def setPlusHP(self,value):
        """Set PlusHP"""
        self.PlusHP = value
        if self.PlusHP > 99:
            self.PlusHP = 99
        if self.PlusHP < 0:
            self.PlusHP = 0
        self.updateStats()

    def setSkillLevel(self,value):
        """Sets the skill Level"""
        self.SkillLevel = value
        if self.SkillLevel > self.ActiveSkillMaxLevel:
            self.SkillLevel = self.ActiveSkillMaxLevel
        if self.SkillLevel < 1:
            self.SkillLevel = 1

    def setSkillsAwoke(self, value):
        """Sets the Number of skills Awoke"""
        self.SkillsAwoke = value
        if self.SkillsAwoke < 0:
            self.SkillsAwoke = 0
        if self.SkillsAwoke > 9:
            self.SkillsAwoke = 9

class Team():
    def __init__(self, TeamInstance = None):

        pass

#print(calcStat(20,5000,40,99,1.5))
#print(calcLevel(505,1500000)) 
#print(calcXP(5,1500000))