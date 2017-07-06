#!usr/bin/env Python3
#
#       NAME: WILLIAM GALE
#       DATE: 2017-07-04
#       PURPOSE: Create a csv of Team stat Caclulation to manually compare to Main sources.

import PADSQL
from PADMonster import *



class teamstat:
    def __init__(self, **kwargs):
        
        self.padsql = PADSQL.PADSQL()
        self.padsql.login('Username', 'Password')

        self.LeaderMonsterID = 1
        self.SubMonsterOneID = 1
        self.SubMonsterTwoID = None
        self.SubMonsterThreeID = 1
        self.SubMonsterFourID = 1

        self.LeaderMonsterLevel = 1
        self.SubMonsterOneLevel = 1
        self.SubMonsterTwoLevel = 1
        self.SubMonsterThreeLevel = 1
        self.SubMonsterFourLevel = 1

        self.MonstersinstanceIDs = []
        self.testTeam = Team(self.padsql)
        f = open("src/python/UnitTest/Log/TeamStats.csv", "w")
        count = 0
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
       
                f.write(i + ","+str(self.testTeam.Monsters[0].MonsterName) + ",Level,"+ str(self.testTeam.Monsters[count].Level) +"\n")
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
        
        f.close()

        for i in self.MonstersinstanceIDs:
            print(i)
            self.padsql.deleteMonster(i)


teamstat()