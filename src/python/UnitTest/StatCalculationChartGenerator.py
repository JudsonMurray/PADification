#!usr/bin/env Python3
#
#       NAME: WILLIAM GALE
#       DATE: 2017-07-04
#       PURPOSE: Create a csv of stat to level calculations to manually compare to Main sources.

import PADSQL
from PADMonster import *


padsql = PADSQL.PADSQL()
padsql.connect()

#MonsterId to check
MonsterID = 572

testmonster = Monster(padsql.selectMonsterClass(MonsterID)[0])
f = open("src/python/UnitTest/Log/StatchartMonID" + str(MonsterID) + ".csv", "w")
f.write("CurXP,")
for i in range (1,testmonster.MaxLevel + 1):
    testmonster.setLevel(i)
    f.write(str(testmonster.CurrentExperience) + ",")
f.write("\n")
f.write("Level,")
for i in range (1,testmonster.MaxLevel + 1):
    f.write(str(i) + ",")
f.write("\n")
f.write("HP,")
for i in range (1,testmonster.MaxLevel + 1):
    testmonster.setLevel(i)
    f.write(str(testmonster.HP) + ",")
f.write("\n")
f.write("ATK,")
for i in range (1,testmonster.MaxLevel + 1):
    testmonster.setLevel(i)
    f.write(str(testmonster.ATK) + ",")
f.write("\n")
f.write("RCV,")
for i in range (1,testmonster.MaxLevel + 1):
    testmonster.setLevel(i)
    f.write(str(testmonster.RCV) + ",")
f.write("\n")

f.close()
