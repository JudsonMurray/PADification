#!usr/bin/env python3
#
#
#   NAME:       William Gale
#   DATE:       2017-06-23
#   PURPOSE:    All Mathematical Calculations will be described and Handled
#               within this Module for PAD Stats.

import math
import logging

class Monster():
    def __init__(self, monsterDictionary):
        #Logger
        self.logger = logging.getLogger("Padification.class.Monster")
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
        self.ActiveSkillDesc = None
        self.LeaderSkillDesc = None
        
        #Awoken Skill Variables
        self.AwokenSkillOne = None
        self.AwokenSkillTwo = None
        self.AwokenSkillThree = None
        self.AwokenSkillFour = None
        self.AwokenSkillFive = None
        self.AwokenSkillSix = None
        self.AwokenSkillSeven = None
        self.AwokenSkillEight = None
        self.AwokenSkillNine = None

        #Latent Skill Variables
        self.LatentSkillOne = None
        self.LatentSkillTwo = None
        self.LatentSkillThree = None
        self.LatentSkillFour = None
        self.LatentSkillFive = None
        self.LatentSkillSix = None

        #ActiveSkill Variables
        self.ActiveSkillMaxLevel = 0
        self.ActiveSkillMaxCoolDown = 0
        
        #Instance Variables
        self.InstanceID = None
        self.Email = None
        self.CurrentExperience = 0
        self.PlusATK = 0
        self.PlusRCV = 0
        self.PlusHP = 0
        self.SkillsAwoke = 0
        self.AssistMonsterID = None
        self.SkillLevel = 1
        self.LSListID = None
        self.WishList = 0 
        self.Favorites = 0

        #Calculated Variables
        self.MaxExperience = 0
        self.Level = 0
        self.AssistHP = 0
        self.AssistATK = 0
        self.AssistRCV = 0
        self.AwokenHP = 0
        self.AwokenATK = 0
        self.AwokenRCV = 0
        self.LatentHP = 0
        self.LatentATK = 0
        self.LatentRCV = 0
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
        savingItems = ['InstanceID', 'Email', 'CurrentExperience', 'PlusATK', 'PlusRCV', 'PlusHP', 'SkillsAwoke', 'AssistMonsterID', 'SkillLevel', 'LSListID', 'MonsterClassID', 'Favorites', 'WishList' ]
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


        values = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
        self.AwokenHP = 0
        self.AwokenATK = 0
        self.AwokenRCV = 0
        for i in range(0,9):
            if i < self.SkillsAwoke:
                awsk = getattr(self,"AwokenSkill" + values[i])
                if awsk == "Enhanced HP":
                    self.AwokenHP += 200
                elif awsk == "Enhanced Attack":
                    self.AwokenATK += 100
                elif awsk == "Enhanced Heal":
                    self.AwokenRCV += 100

        self.LatentHP = 0
        self.LatentATK = 0
        self.LatentRCV = 0
        for i in ["One", "Two", "Three", "Four", "Five", "Six"]:
            lask = getattr(self,"LatentSkill" + i)
            if lask == "Improved HP":
                self.LatentHP += round(self.HP * 0.015)
            elif lask == "Improved Attack":
                self.LatentATK += round(self.ATK * 0.01)
            elif lask == "Improved Healing":
                self.LatentRCV += round(self.RCV * 0.04)
            elif lask == "Improved All Stats":
                self.LatentHP += round(self.HP * 0.015)
                self.LatentATK += round(self.ATK * 0.01)
                self.LatentRCV += round(self.RCV * 0.04)

        self.TotalHP = self.HP + (self.PlusHP * 10) + self.AwokenHP + self.LatentHP + self.AssistHP
        self.TotalATK = self.ATK + (self.PlusATK * 5) + self.AwokenATK + self.LatentATK + self.AssistATK
        self.TotalRCV = self.RCV + (self.PlusRCV * 3) + self.AwokenRCV + self.LatentRCV + self.AssistRCV

        if self.ActiveSkillName != None:
            self.ActiveSkillCoolDown = self.ActiveSkillMaxCoolDown - (self.SkillLevel - 1)

    def calcLevel(self, currentXP, curveXP):
        """Calculated the Level of a monster Based on XP"""
        return int((currentXP / curveXP) ** (1/2.5) * 98 + 1)

    def calcXP(self, currentLevel, curveXP):
        """Calculated the Experience Needed at a certian level"""
        return math.ceil(curveXP * ((currentLevel - 1) / 98) ** 2.5)

    def calcStat(self, minStat, maxStat, curLevel, maxLevel, growthRate):
        """Calculated the Value of a stat at a given level"""
        return round(minStat + (maxStat - minStat) * ((curLevel - 1) / (maxLevel - 1 if maxLevel - 1 > 0 else 1)) ** growthRate)

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
        if value <= 0:
            value = 1
        if value > 99:
            value = 99
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
        if self.ActiveSkillMaxLevel != None:
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

    def calcAssistStats(self, MonsterInstance):
        if isinstance(MonsterInstance, Monster):
            if self.PriAttribute == MonsterInstance.PriAttribute:
                self.AssistHP = round(MonsterInstance.TotalHP * 0.1)
                self.AssistATK = round(MonsterInstance.TotalATK * 0.05)
                self.AssistRCV = round(MonsterInstance.TotalRCV * 0.15)
            else:
                self.AssistHP = 0
                self.AssistATK = 0
                self.AssistRCV = 0
        else:
            self.AssistHP = 0
            self.AssistATK = 0
            self.AssistRCV = 0
        self.updateStats()

class Team():
    def __init__(self, PADSQL, TeamInstanceDict = None):
        self.logger = logging.getLogger("Padification.class.Team")
        self.PADSQL = PADSQL
        #Instance Variables
        self.TeamInstanceID = None
        self.Email = None
        self.TeamName = ""
        self.LeaderMonster = None
        self.SubMonsterOne = None
        self.SubMonsterTwo = None
        self.SubMonsterThree = None
        self.SubMonsterFour = None
        self.AwokenBadgeName = None

        #Objects
        self.Monsters = []
        self.DreamTeam = 0

        #Calculated Values
        self.TeamHP = 0
        self.TeamRCV = 0
        self.FireATK = 0
        self.WaterATK = 0
        self.WoodATK = 0
        self.LightATK = 0
        self.DarkATK = 0
        self.TeamCost = 0

        self.skillBindResist= 0
        self.fireDmgReduction = 0
        self.waterDmgReduction = 0
        self.woodDmgReduction = 0
        self.lightDmgReduction = 0
        self.darkDmgReduction = 0
        self.darkResist = 0
        self.jammerResist = 0
        self.poisonResist = 0
        self.enhancedFireChance = 0
        self.enhancedWaterChance = 0
        self.enhancedWoodChance = 0
        self.enhancedLightChance = 0
        self.enhancedDarkChance = 0
        self.enhancedHealChance = 0
        self.moveTime = 0.0
        self.skillBoost = 0

        if TeamInstanceDict != None:
            for i in TeamInstanceDict:
                setattr(self,i,TeamInstanceDict[i])
            self.update()

    def update(self):
        """Updates the Team."""
        self.Monsters = []
        if self.DreamTeam:
            x=1
        else:
            x=0
        monmon = self.PADSQL.selectMonsterInstance(self.LeaderMonster, wishlist = x, allUsers = True)
        if self.LeaderMonster != None:
            self.Monsters.append(Monster(self.PADSQL.selectMonsterInstance(self.LeaderMonster, wishlist = x, allUsers = True)[0]))
        else:
            self.Monsters.append(None)
        if self.SubMonsterOne != None:
            self.Monsters.append(Monster(self.PADSQL.selectMonsterInstance(self.SubMonsterOne, wishlist = x, allUsers = True)[0]))
        else:
            self.Monsters.append(None)
        if self.SubMonsterTwo != None:
            self.Monsters.append(Monster(self.PADSQL.selectMonsterInstance(self.SubMonsterTwo, wishlist = x, allUsers = True)[0]))
        else:
            self.Monsters.append(None)
        if self.SubMonsterThree != None:
            self.Monsters.append(Monster(self.PADSQL.selectMonsterInstance(self.SubMonsterThree, wishlist = x, allUsers = True)[0]))
        else:
            self.Monsters.append(None)
        if self.SubMonsterFour != None:
            self.Monsters.append(Monster(self.PADSQL.selectMonsterInstance(self.SubMonsterFour, wishlist = x, allUsers = True)[0]))
        else:
            self.Monsters.append(None)

        self.TeamHP = 0
        self.TeamRCV = 0
        self.FireATK = 0
        self.WaterATK = 0
        self.WoodATK = 0
        self.LightATK = 0
        self.DarkATK = 0
        self.TeamCost = 0
        self.skillBindResist= 0
        self.fireDmgReduction = 0
        self.waterDmgReduction = 0
        self.woodDmgReduction = 0
        self.lightDmgReduction = 0
        self.darkDmgReduction = 0
        self.darkResist = 0
        self.jammerResist = 0
        self.poisonResist = 0
        self.enhancedFireChance = 0
        self.enhancedWaterChance = 0
        self.enhancedWoodChance = 0
        self.enhancedLightChance = 0
        self.enhancedDarkChance = 0
        self.enhancedHealChance = 0
        self.moveTime = 0.0
        self.skillBoost = 0

        for i in self.Monsters:
            if i != None:
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

                i.ASList= self.PADSQL.getAwokenSkillList(i.MonsterClassID) 
                i.awokenSkills = []
                for x in range(1, i.SkillsAwoke + 1):
                    i.awokenSkills.append(i.ASList[x])

                for b in i.awokenSkills:
                    if b == 'Resistance-Skill Bind':
                        self.skillBindResist += 20
                    if b == 'Enhanced Fire Orbs':
                        self.enhancedFireChance += 20
                    if b == 'Enhanced Water Orbs':
                        self.enhancedWaterChance += 20
                    if b == 'Enhanced Wood Orbs':
                        self.enhancedWoodChance += 20
                    if b == 'Enhanced Light Orbs':
                        self.enhancedLightChance += 20
                    if b == 'Enhanced Dark Orbs':
                        self.enhancedDarkChance += 20
                    if b == 'Enhanced Heal Orbs':
                        self.enhancedHealChance += 20
                    if b == 'Reduce Fire Damage':
                        self.fireDmgReduction += 1
                    if b == 'Reduce Water Damage':
                        self.waterDmgReduction += 1
                    if b == 'Reduce Wood Damage':
                        self.woodDmgReduction += 1
                    if b == 'Reduce Light Damage':
                        self.lightDmgReduction += 1
                    if b == 'Reduce Dark Damage':
                        self.darkDmgReduction += 1
                    if b == 'Extend Time':
                        self.moveTime += 0.50
                    if b == 'Resistance-Dark':
                        self.darkResist += 20
                    if b == 'Resistance-Jammers':
                        self.jammerResist += 20
                    if b == 'Resistance-Poison':
                        self.poisonResist += 20
                    if b == 'Skill Boost':
                        self.skillBoost += 1

    def getSaveDict(self):
        """Returns a Dictionary to represent an instance"""
        saveDict = {}
        saveVars = ['TeamInstanceID','Email', 'TeamName', 'LeaderMonster',
                    'SubMonsterOne', 'SubMonsterTwo', 'SubMonsterThree', 'SubMonsterFour', 'AwokenBadgeName', 'DreamTeam' ]
        
        for i in saveVars:
            saveDict[i] = getattr(self, i)

        return saveDict

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
        if badge == 'None' or badge == '':
            self.AwokenBadgeName = None
        elif type(badge) == str:
            self.AwokenBadgeName = badge
        else:
            print("Badge must be a string")

    def getBadge(self):
        """Gets Team Awoken Badge"""
        return self.BadgeName

    def setDreamState(self, dreamstate):
        self.DreamTeam = dreamstate
        return

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

