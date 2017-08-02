#!usr/bin/env Python3
#
#
#       NAME: WILLIAM GALE
#       DATE: 2017-07-04
#       PURPOSE: TestCases For PADification
#
#
import datetime
import unittest
import PADSQL
import random
from PADMonster import *

class TC3(unittest.TestCase):
    """Info Queury tests"""

    def __init__(self, methodName = 'runTest'):
        self.padsql = PADSQL.PADSQL()
        self.padsql.remote = False
        self.padsql.login('Padmin@pad.min', 'password')
        return super().__init__(methodName)


    def test_SelectMonsterClass_All(self):
        """returns a collection of ~2846 dictionaries"""
        self.assertGreater( len(self.padsql.selectMonsterClass()), 2800 )


    def test_SelectMonsterClass_Range(self):
        """returns a collection of within a range and ensure all monsterIds are in the Range"""
        minRange = 30
        maxRange = 200
        results = self.padsql.selectMonsterClass((minRange,maxRange))
        for i in results:
            self.assertTrue(i["MonsterClassID"] >= minRange and i["MonsterClassID"] <= maxRange)


    def test_SelectMonsterClass_String(self):
        """Returns the collection with MonsterName Containing the string and verifies results"""
        string = "myr"
        results = self.padsql.selectMonsterClass(string)
        for i in results:
            self.assertTrue(string in i["MonsterName"] or string.capitalize() in i["MonsterName"])

    
    def test_SelectMonsterClass_Int(self):
        """Returns a collection of a single dictionary by MonsterClassID"""
        value = 1
        result = self.padsql.selectMonsterClass(value)
        self.assertTrue(len(result) == 1 and result[0]["MonsterClassID"] == value)


    def test_Create_Monster_Object(self):
        """Instantiates a Monster from PADSQL query"""
        testmonster = Monster(self.padsql.selectMonsterClass(1)[0])
        self.assertIsInstance( testmonster, Monster)
        self.assertTrue(testmonster.MonsterName == "Tyrra")


    def test_selectMonsterInstance(self):
        """Test selectMonsterInstance does not raise integrity exceptions"""
        results = self.padsql.selectMonsterInstance()
        if len(results) != 0:
            self.padsql.selectMonsterInstance(random.choice(results)['InstanceID'])

    def test_saveMonsterInstance_NewMonster(self):
        """Creates a Monster Instance and inserts it into MonsterInstance Table
           Then Selects All Monster Instances and verifies newest for user is the monster created."""
        samples = self.padsql.selectMonsterClass()
        value = random.choice(samples)["MonsterClassID"]
        testMonster = Monster(self.padsql.selectMonsterClass(value)[0])
        self.padsql.saveMonster(testMonster.getSaveDict())
        self.assertTrue( self.padsql.selectMonsterInstance()[-1]['MonsterClassID'] == value)
        

    def test_saveMonsterInstance_Update(self):
        """Retrieves a Monster from MonsterInstance Table then modifies currentXP, 
        Updates record on MonsterInstance Table, Then retrieves information and verifies."""
        monsters = self.padsql.selectMonsterInstance()
        testmonster = Monster(random.choice(monsters))
        instanceID = testmonster.InstanceID
        curXP = testmonster.CurrentExperience
        newXP = random.randint(0, testmonster.MaxExperience)
        newXP = newXP if newXP != curXP else testmonster.MaxExperience - curXP
        testmonster.setCurrentExperience(newXP)
        self.padsql.saveMonster(testmonster.getSaveDict())
        verifyMonster = self.padsql.selectMonsterInstance(instanceID)
        self.assertTrue(verifyMonster[0]['CurrentExperience'] == newXP)

    def test_deleteMonster(self):
        """deletes a monster instance from the MonsterInstance Table"""
        instanceToDelete = random.choice(self.padsql.selectMonsterInstance())["InstanceID"]
        if len(self.padsql.selectMonsterInstance(instanceToDelete)) == 1:
            self.padsql.deleteMonster(instanceToDelete)
            self.assertTrue(len(self.padsql.selectMonsterInstance(instanceToDelete)) == 0)

    def test_selectTeamInstance(self):
        """Tests if selectTeamInstance raises integrity exceptions"""
        results = self.padsql.selectTeamInstance()
        if len(results) != 0:
            self.padsql.selectTeamInstance(results[-1]["TeamInstanceID"])

    def test_Create_Team_Object(self):
        """Tests Teams can be instantiated"""
        testteam = Team(self.padsql)
        self.assertIsInstance(testteam, Team)

    def test_Team_Create_Update_Delete(self):
        """Creates a Team of 5 new monsters, verifys its created, alters and updates then verifies, then deletes"""
        samples = self.padsql.selectMonsterClass()
        Monsters = []
        InstanceIDs = []
        for i in range(0,5):
            Monsters.append(Monster(random.choice(samples)))
            self.padsql.saveMonster(Monsters[i].getSaveDict())
            InstanceIDs.append(self.padsql.selectMonsterInstance()[-1]["InstanceID"])
        testTeam = Team(self.padsql)
        testTeam.setLeaderMonster(InstanceIDs[0])
        testTeam.setSubMonsterOne(InstanceIDs[1])
        testTeam.setSubMonsterTwo(InstanceIDs[2])
        testTeam.setSubMonsterThree(InstanceIDs[3])
        testTeam.setSubMonsterFour(InstanceIDs[4])

        self.padsql.saveTeam(testTeam.getSaveDict())

        loadedteam = Team(self.padsql,self.padsql.selectTeamInstance()[-1])
        teamInstanceID = loadedteam.TeamInstanceID
        self.assertTrue(loadedteam.LeaderMonster == InstanceIDs[0], "Team was not saved correctly.")
        loadedteam.setSubMonsterFour()
        self.padsql.saveTeam(loadedteam.getSaveDict())
        
        loadedteam = Team(self.padsql, self.padsql.selectTeamInstance(teamInstanceID)[0])
        self.assertTrue(loadedteam.SubMonsterFour == None,"Team was not updated.")

        self.padsql.deleteTeam(teamInstanceID)
        self.assertTrue(len(self.padsql.selectTeamInstance(teamInstanceID)) == 0, "Team still exists.")

        for i in InstanceIDs:
            self.padsql.deleteMonster(i)

    def test_getAwokenSkills(self):
        """Test method getAwokenSkills that it does not raise an integrity exception"""
        self.padsql.getAwokenSkills()

    def test_getLatentAwokenSkills(self):
        """Test method getLatentAwokenSkills that it does not raise an integrity exception"""
        self.padsql.getLatentAwokenSkills()

    def test_getAwokenSkillList(self):
        """Test method getAwokenSkillList that it does not raise an integrity exception"""
        samples = self.padsql.selectMonsterClass()
        for i in samples:
            self.padsql.getAwokenSkillList(i["MonsterClassID"])

    @unittest.skip("No saving of latent skill lists Implemented yet.")
    def test_getLatentAwokenSkillList(self):
        """Test method getLatentAwokenSkillList that it does not raise an integrity exception"""
        samples = self.padsql.selectMonsterInstance()
        for i in samples:
            self.padsql.getLatentAwokenSkillList(i["InstanceID"])

    def test_getAwokenBadges(self):
        """Test method getAwokenBadges that it does not raise an integrity exception"""
        self.padsql.getAwokenBadges()

    def test_getEvolutionTree(self):
        """Test method getEvolutionTree that it does not raise an integrity exception"""
        samples = self.padsql.selectMonsterClass()
        for i in samples:
            self.padsql.getEvolutionTree(i["MonsterClassID"])

    def test_getEvolutions(self):
        """Test method getEvolutions that it does not raise an integrity exception"""
        samples = self.padsql.selectMonsterClass()
        for i in samples:
            self.padsql.getEvolutions(i["MonsterClassID"])

    def test_getLeaderSkillDesc(self):
        samples = self.padsql.selectMonsterClass()
        for i in samples:
            self.padsql.getLeaderSkillDesc(i["LeaderSkillName"])

    def test_getActiveSkillDesc(self):
        samples = self.padsql.selectMonsterClass()
        for i in samples:
            self.padsql.getActiveSkillDesc(i["ActiveSkillName"])


if __name__ == '__main__':
    log_file = 'src/python/UnitTest/Log/Query_Test_log_' + '{:%Y-%m-%d %H-%M-%S}'.format(datetime.datetime.now()) + '.txt'
    f = open(log_file, "w")
    runner = unittest.TextTestRunner(f,verbosity = 2)
    unittest.main(testRunner=runner,verbosity=2,exit=False)
    f.close()


f = open(log_file, "r")
print(f.read())
f.close()