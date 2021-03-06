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
        """Returns a Dictionary of instance table """
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
        return math.ceil(minStat + (maxStat - minStat) * ((curLevel - 1) / (maxLevel - 1 if maxLevel - 1 > 0 else 1)) ** growthRate)

    def setCurrentExperience(self, value):
        """Set CurrentExperience and Update Stats to relect changes."""
        self.CurrentExperience = value
        if self.CurrentExperience < 0:
            self.CurrentExperience = 0
        if self.CurrentExperience > self.MaxExperience:
            self.CurrentExperience = self.MaxExperience
        self.updateStats()

    def setLevel(self, value):
        """set CurrentExperience to the appropriate value for a specified level"""
        self.setCurrentExperience(self.calcXP(value,self.ExpCurve))

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
    def __init__(self, PADSQL, TeamInstanceDict = None):
        self.PADSQL = PADSQL
        #Instance Variables
        self.TeamInstanceID = None
        self.Username = None
        self.TeamName = ""
        self.LeaderMonster = None
        self.SubMonsterOne = None
        self.SubMonsterTwo = None
        self.SubMonsterThree = None
        self.SubMonsterFour = None
        self.BadgeName = None

        #Objects
        self.Monsters = []

        #Calculated Values
        self.TeamHP = 0
        self.TeamRCV = 0
        self.FireATK = 0
        self.WaterATK = 0
        self.WoodATK = 0
        self.LightATK = 0
        self.DarkATK = 0
        self.TeamCost = 0

        if TeamInstanceDict != None:
            for i in TeamInstanceDict:
                setattr(self,i,TeamInstanceDict[i])
            self.update()

    def update(self):
        """Updates the Team."""
        self.Monsters = []
        if self.LeaderMonster != None:
            self.Monsters.append(Monster(self.PADSQL.selectMonsterInstance(self.LeaderMonster)[0]))
        if self.SubMonsterOne != None:
            self.Monsters.append(Monster(self.PADSQL.selectMonsterInstance(self.SubMonsterOne)[0]))
        if self.SubMonsterTwo != None:
            self.Monsters.append(Monster(self.PADSQL.selectMonsterInstance(self.SubMonsterTwo)[0]))
        if self.SubMonsterThree != None:
            self.Monsters.append(Monster(self.PADSQL.selectMonsterInstance(self.SubMonsterThree)[0]))
        if self.SubMonsterFour != None:
            self.Monsters.append(Monster(self.PADSQL.selectMonsterInstance(self.SubMonsterFour)[0]))

        self.TeamHP = 0
        self.TeamRCV = 0
        self.FireATK = 0
        self.WaterATK = 0
        self.WoodATK = 0
        self.LightATK = 0
        self.DarkATK = 0
        self.TeamCost = 0

        for i in self.Monsters:
            self.TeamHP += i.TotalHP
            self.TeamRCV += i.TotalRCV
            self.TeamCost += i.MonsterCost

            for a in ['Fire','Water','Wood','Light', 'Dark']:
                if i.PriAttribute == a and i.SecAttribute == a:
                    setattr(self,a + 'ATK', getattr(self, a + 'ATK') + (i.TotalATK + (i.TotalATK // 10)))
                elif i.PriAttribute == a:
                    setattr(self,a + 'ATK', getattr(self, a + 'ATK') + (i.TotalATK))
                elif i.SecAttribute == a:
                    setattr(self,a + 'ATK', getattr(self, a + 'ATK') + (i.TotalATK // 3))

    def getSaveDict(self):
        """Returns a Dictionary to represent an instance"""
        saveDict = {}
        saveVars = ['TeamInstanceID','Username', 'TeamName', 'LeaderMonster',
                    'SubMonsterOne', 'SubMonsterTwo', 'SubMonsterThree', 'SubMonsterFour', 'BadgeName' ]
        if self.LeaderMonster != None:
            for i in saveVars:
                saveDict[i] = getattr(self, i)

            return saveDict
        else:
            print('Team requires a Leader')

    def getTeamName(self):
        """Returns TeamName"""
        return self.TeamName

    def setTeamName(self, Value):
        """Sets TeamName"""
        if type(Value) == str and len(Value) <= 50:
            self.TeamName = Value
        else:
            print("Team Name invalid not set")

    def setBadge(self, badge):
        """Sets badge"""
        if type(badge) == str:
            self.BadgeName = badge
        else:
            print("Badge must be a string")

    def getBadge(self):
        """Gets Team Awoken Badge"""
        return self.BadgeName

    def setLeaderMonster(self, InstanceID = None):
        """Sets Leader Monster requires instanceID"""
        self.LeaderMonster = InstanceID
        self.update()

    def setSubMonsterOne(self, InstanceID = None):
        """Sets Leader Monster requires instanceID"""
        self.SubMonsterOne = InstanceID
        self.update()

    def setSubMonsterTwo(self, InstanceID = None):
        """Sets Leader Monster requires instanceID"""
        self.SubMonsterTwo = InstanceID
        self.update()
    
    def setSubMonsterThree(self, InstanceID = None):
        """Sets Leader Monster requires instanceID"""
        self.SubMonsterThree = InstanceID
        self.update()

    def setSubMonsterFour(self, InstanceID = None):
        """Sets Leader Monster requires instanceID"""
        self.SubMonsterFour = InstanceID
        self.update()
