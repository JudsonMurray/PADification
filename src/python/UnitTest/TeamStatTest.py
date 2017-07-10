#!usr/bin/env Python3
#
#       NAME: WILLIAM GALE
#       DATE: 2017-07-04
#       PURPOSE: Create a csv of Team stat Caclulation to manually compare to Main sources.

import PADSQL
from PADMonster import *
import csv


class teamstat:
    def __init__(self, **kwargs):
        
        self.padsql = PADSQL.PADSQL()
        self.padsql.login('TestEmail1@test.test', 'Password')

        with open('src/python/UnitTest/TeamStatTestInput.csv') as csvfile:
            self.reader = csv.DictReader(csvfile)
            self.dicts = []
            for row in self.reader:
                self.dicts.append(row)

        self.LeaderMonsterID = int(self.dicts[0]["ID"])
        self.LeaderMonsterLevel = int(self.dicts[0]["Level"])

        self.SubMonsterOneID = int(self.dicts[1]["ID"])
        self.SubMonsterOneLevel = int(self.dicts[1]["Level"])

        self.SubMonsterTwoID = int(self.dicts[2]["ID"])
        self.SubMonsterTwoLevel = int(self.dicts[2]["Level"])

        self.SubMonsterThreeID = int(self.dicts[3]["ID"])
        self.SubMonsterThreeLevel = int(self.dicts[3]["Level"])

        self.SubMonsterFourID = int(self.dicts[4]["ID"])
        self.SubMonsterFourLevel = int(self.dicts[4]["Level"])



        self.MonstersinstanceIDs = []
        self.testTeam = Team(self.padsql)


        f = open("src/python/UnitTest/Log/TeamStats.csv", "w")
        count =0
        for i in [  'LeaderMonster',
                    'SubMonsterOne',
                    'SubMonsterTwo',
                    'SubMonsterThree',
                    'SubMonsterFour'  ]:
            if getattr(self, i + 'ID') != None:
                classmonster = Monster(self.padsql.selectMonsterClass(getattr(self, i + 'ID'))[0] )
                classmonster.setLevel(getattr(self, i + 'Level'))
                self.padsql.saveMonster(classmonster.getSaveDict())

                self.MonstersinstanceIDs.append(self.padsql.selectMonsterInstance()[-1]["InstanceID"])
                eval('self.testTeam.set' + i +"(" +str(self.MonstersinstanceIDs[-1]) +")")
       
                f.write(i + ","+str(self.testTeam.Monsters[count].MonsterName) + ",Level,"+ str(self.testTeam.Monsters[count].Level) +"\n")
                count += 1
            else:
                f.write(i + ",None\n")

        f.write("TeamHP,"+str(self.testTeam.TeamHP) + "\n")
        f.write("TeamRCV,"+str(self.testTeam.TeamRCV) + "\n")
        f.write("TeamFireATK,"+str(self.testTeam.FireATK) + "\n")
        f.write("TeamWaterATK,"+str(self.testTeam.WaterATK) + "\n")
        f.write("TeamWoodATK,"+str(self.testTeam.WoodATK) + "\n")
        f.write("TeamLightATK,"+str(self.testTeam.LightATK) + "\n")
        f.write("TeamDarkATK,"+str(self.testTeam.DarkATK) + "\n")
        f.write("TeamCost,"+str(self.testTeam.TeamCost) + "\n")
        f.write("skillBindResist,"+str(self.testTeam.skillBindResist) + "\n")
        f.write("fireDmgReduction,"+str(self.testTeam.fireDmgReduction)+ "\n")
        f.write("waterDmgReduction,"+str(self.testTeam.waterDmgReduction) + "\n")
        f.write("woodDmgReduction,"+str(self.testTeam.woodDmgReduction) + "\n")
        f.write("lightDmgReduction,"+str(self.testTeam.lightDmgReduction) + "\n")
        f.write("darkDmgReduction,"+str(self.testTeam.darkDmgReduction) + "\n")
        f.write("darkResist,"+str(self.testTeam.darkResist) + "\n")
        f.write("jammerResist,"+str(self.testTeam.jammerResist) + "\n")
        f.write("poisonResist,"+str(self.testTeam.poisonResist) + "\n")
        f.write("enhancedFireChance,"+str(self.testTeam.enhancedFireChance) + "\n")
        f.write("enhancedWaterChance,"+str(self.testTeam.enhancedWaterChance) + "\n")
        f.write("enhancedWoodChance,"+str(self.testTeam.enhancedWoodChance) + "\n")
        f.write("enhancedLightChance,"+str(self.testTeam.enhancedLightChance) + "\n")
        f.write("enhancedDarkChance,"+str(self.testTeam.enhancedDarkChance) + "\n")
        f.write("enhancedHealChance,"+str(self.testTeam.enhancedHealChance) + "\n")
        f.write("moveTime,"+str(self.testTeam.moveTime) + "\n")
        f.write("skillBoost,"+str(self.testTeam.skillBoost) + "\n")
        f.close()

        for i in self.MonstersinstanceIDs:
            #print(i)
            self.padsql.deleteMonster(i)







teamstat()