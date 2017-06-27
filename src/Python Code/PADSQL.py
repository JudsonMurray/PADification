#!usr/bin/env Python3
#
# NAME      William GALE
# DATE      2017-06-16
# PURPOSE   Establishing and Managing SQL operations and connections
#           And Login authentication.

import pypyodbc

# SQL Server information.
localhost = ('Driver={SQL Server};'
            'Server=localhost;'
            'Database=PADification;'
            'uid=PADmin;pwd=PADmin;')

class PADSQL():
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.Username = None
        self.Password = None
        self.signedIn = False

    def connect(self):
        """Connect to the Sql Server and Establish a cursor"""
        notconnected = True
        attempts = 0
        while notconnected and attempts < 5:
            try:
                self.connection = pypyodbc.connect(localhost)
                notconnected = False
            except:
                print("Timeout, Retrying connection.", 4 - attempts, "attempts left.")
                attempts += 1

        if self.connection.connected:
            print("MSSQL 2014 server Connection Established.")
            self.cursor = self.connection.cursor()
        else:
            print("Connection Failed.")

    def signup(self, listValues):
        """Function will execute TSQL command to insert into Table Player"""
        self.connect()
        if len(listValues) != 4:
            raise ValueError(str(len(listValues)) + "given")

        SQLCommand = ("INSERT INTO Player "
                      "(Username, Password, Email, PlayerID) "
                      "VALUES (?,?,?,?)")

        self.cursor.execute(SQLCommand, listValues)
        self.connection.commit()
        print("Sign up Successful")
        self.closeConnection()

    def login(self, Username, Password):
        """Log in with login Info"""
        self.connect()
        SQLCommand = ("SELECT [Username], [Password] "
                        "FROM Player "
                        "WHERE [Username] = '" + Username + "' AND [Password] = '" + Password + "'")
        self.cursor.execute(SQLCommand)
        results = self.cursor.fetchone()
        if results:
            print("User login Successful")
            self.Username = Username
            self.Password = Password
            self.signedIn = True
        else:
            print("Login Failed")
            self.closeConnection()

    def selectMonsterClass(self, monSearch = None, dictionary = True):
        """Retrieve Monster Class Info from MonsterClassTable, monSearch can be an INT Single ID,
           a tuple of 2 INT for Range, a string of monsterName for a like search or empty for entire collection.
           Returns a List of Tuples"""

        SQLCommand = ("SELECT MonsterClassID, MonsterName, Rarity, PriAttribute, SecAttribute, MonsterTypeOne, MonsterTypeTwo, MonsterTypeThree, ExpCurve, MaxLevel, MonsterCost, ASListID, LeaderSkillName, ActiveSkill.ActiveSkillName, MaxHP, MinHP, GrowthRateHP, MaxATK, MinATK, GrowthRateATK, MaxRCV, MinRCV, GrowthRateRCV, CurSell, CurFodder, MonsterPointValue, LSSlots, "
                      "ActiveSkillMaxLevel, ActiveSkillMaxCoolDown "
                      "FROM (MonsterClass LEFT OUTER JOIN ActiveSkill ON MonsterClass.ActiveSkillName = ActiveSkill.ActiveSkillName)")

        if type(monSearch) == tuple and len(monSearch) == 2:
            SQLCommand += "WHERE MonsterClassID BETWEEN " + str(monSearch[0]) + " AND " + str(monSearch[1]) + " ORDER BY MonsterClassID ASC"
        elif type(monSearch) == int:
            SQLCommand += "WHERE MonsterClassID = " + str(monSearch)
        elif type(monSearch) == str:
            SQLCommand += "WHERE MonsterName LIKE '%" + monSearch + "%'" + " ORDER BY MonsterClassID ASC"

        self.cursor.execute(SQLCommand)

        if dictionary:
            properties = ['MonsterClassID', 'MonsterName', 'Rarity', 'PriAttribute', 'SecAttribute', 'MonsterTypeOne', 'MonsterTypeTwo', 'MonsterTypeThree', 'ExpCurve', 'MaxLevel', 'MonsterCost', 'ASListID', 'LeaderSkillName', 'ActiveSkillName', 'MaxHP', 'MinHP', 'GrowthRateHP', 'MaxATK', 'MinATK', 'GrowthRateATK', 'MaxRCV', 'MinRCV', 'GrowthRateRCV', 'CurSell', 'CurFodder', 'MonsterPointValue', 'LSSlots', 'ActiveSkillMaxLevel', 'ActiveSkillMaxCoolDown']
            monstercollection = []
            results = self.cursor.fetchone()
            while results:
                #Cycle through all results one by one.
                monDict = {}      
                count = 0
                for i in results:
                    monDict[properties[count]] = i
                    count += 1
                monstercollection.append(monDict)
                results = self.cursor.fetchone()
            return monstercollection
        else:
            return self.cursor.fetchall()

    def closeConnection(self):
        """Closes Connection to PADification Database"""
        self.connection.close()
        self.signedIn = False

    def saveMonster(self, InstanceDict):
        """Save Monster Instance Record"""
        keys = ['Username', 'CurrentExperience', 'PlusATK', 'PlusRCV', 'PlusHP', 'SkillsAwoke', 'AssistMonsterID', 'SkillLevel', 'LSListID', 'MonsterClassID']
        if InstanceDict["InstanceID"] == None:
            """If it is a new Monster"""
            InstanceDict.pop("InstanceID")
            InstanceDict["Username"] = self.Username

            values = []
            for i in keys:
                values.append(InstanceDict[i])
                    

            SQLCommand = ("INSERT INTO MonsterInstance (Username, CurrentExperience, PlusATK, PlusRCV, PlusHP, SkillsAwoke, AssistMonsterID, SkillLevel, LSListID, MonsterClassID) "
                          "VALUES (?,?,?,?,?,?,?,?,?,?)")

            self.cursor.execute(SQLCommand,values)
            self.connection.commit()
            print("Monster save Successful")

        else:
            """If it is a existing Monster instance"""

            setstr = 'SET '
            values = []
            for i in keys:
                values.append(InstanceDict[i])
                setstr += i + " = ?"  
                setstr += ", " if i != 'MonsterClassID' else " "
            values.append(InstanceDict["InstanceID"])

            SQLCommand = ("UPDATE MonsterInstance " + setstr +
                          "WHERE InstanceID = ?")

            self.cursor.execute(SQLCommand,values)
            self.connection.commit()

    def selectMonsterInstance(self, monSearch = None, dictionary = True):


        SQLCommand = ("SELECT MonsterInstance.MonsterClassID, MonsterName, Rarity, PriAttribute, SecAttribute, MonsterTypeOne, MonsterTypeTwo, MonsterTypeThree, ExpCurve, MaxLevel, MonsterCost, ASListID, LeaderSkillName, ActiveSkill.ActiveSkillName, MaxHP, MinHP, GrowthRateHP, MaxATK, MinATK, GrowthRateATK, MaxRCV, MinRCV, GrowthRateRCV, CurSell, CurFodder, MonsterPointValue, LSSlots, "
                "ActiveSkillMaxLevel, ActiveSkillMaxCoolDown, InstanceID, Username, CurrentExperience, PlusATK, PlusRCV, PlusHP, SkillsAwoke, AssistMonsterID, SkillLevel, LSListID "
                "FROM (MonsterInstance LEFT OUTER JOIN (MonsterClass LEFT OUTER JOIN ActiveSkill ON MonsterClass.ActiveSkillName = ActiveSkill.ActiveSkillName) ON MonsterInstance.MonsterClassID = MonsterClass.MonsterClassID)"
                "WHERE MonsterInstance.Username = '" + str(self.Username) + "'" )

        if monSearch == None:
            SQLCommand += " ORDER BY InstanceID ASC"
        elif type(monSearch) == int:
            SQLCommand += " AND InstanceID = " + str(monSearch)
        elif type(monSearch) == str:
            SQLCommand += " AND MonsterName LIKE '%" + monSearch + "%'"

        self.cursor.execute(SQLCommand)

        if dictionary:
            properties = ['MonsterClassID', 'MonsterName', 'Rarity', 'PriAttribute', 'SecAttribute',
                          'MonsterTypeOne', 'MonsterTypeTwo', 'MonsterTypeThree', 'ExpCurve', 'MaxLevel',
                          'MonsterCost', 'ASListID', 'LeaderSkillName', 'ActiveSkillName', 'MaxHP', 
                          'MinHP', 'GrowthRateHP', 'MaxATK', 'MinATK', 'GrowthRateATK', 'MaxRCV', 'MinRCV', 
                          'GrowthRateRCV', 'CurSell', 'CurFodder', 'MonsterPointValue', 'LSSlots', 'ActiveSkillMaxLevel', 'ActiveSkillMaxCoolDown', 
                          'InstanceID', 'Username', 'CurrentExperience', 'PlusATK', 'PlusRCV', 'PlusHP', 'SkillsAwoke', 'AssistMonsterID', 'SkillLevel', 'LSListID']
            monstercollection = []
            results = self.cursor.fetchone()
            while results:
                #Cycle through all results one by one.
                monDict = {}      
                count = 0
                for i in results:
                    monDict[properties[count]] = i
                    count += 1
                monstercollection.append(monDict)
                results = self.cursor.fetchone()
            return monstercollection
        else:
            return self.cursor.fetchall()

    def deleteMonster(self, InstanceID):
        """Delete a Monster Instance from MonsterInstance Table"""
        SQLCommand = "DELETE FROM MonsterInstance WHERE InstanceID = " + str(InstanceID)
        self.cursor.execute(SQLCommand)
        self.cursor.commit()

    def saveTeam(self, TeamDict):
        pass

    def selectTeamInstance(self, teamsearch = None, dictionary = True):
        """Selects Teams"""
        SQLCommand = ("SELECT "
                "FROM Team"
                "WHERE MonsterInstance.Username = '" + str(self.Username) + "'" )

    def deleteTeam(self, TeamInstanceID):
        """Delete a Team Instance from Team Table"""
        SQLCommand = "DELETE FROM Team WHERE TeamInstanceID = " + str(TeamInstanceID)
        self.cursor.execute(SQLCommand)
        self.cursor.commit()

                      