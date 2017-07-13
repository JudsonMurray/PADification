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
        self.Email = None
        self.Password = None
        self.PlayerID = None
        self.Username = None
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

    def signup(self, Email, Password, Username, PlayerID):
        """Function will execute TSQL command to insert into Table Player"""

        self.connect()
        listValues = [Email, Password, Username, PlayerID]
        SQLCommand = ("INSERT INTO Player "
                      "(Email, Password, Username, PlayerID) "
                      "VALUES (?,?,?,?)")

        self.cursor.execute(SQLCommand, listValues)
        self.connection.commit()
        print("Sign up Successful")
        self.closeConnection()

    def login(self, Email, Password):
        """Log in with login Info"""
        self.connect()
        SQLCommand = ("SELECT [Email], [Password], [Username], [PlayerID] "
                        "FROM Player "
                        "WHERE [Email] = ? "
                        "AND [Password] = ?")
        values = [Email, Password]
        self.cursor.execute(SQLCommand, values)
        results = self.cursor.fetchone()
        if results:
            print("User login Successful")
            self.Email = Email
            self.Password = Password
            self.PlayerID = results[3]
            self.Username = results[2]
            self.signedIn = True
        else:
            print("Login Failed")
            self.closeConnection()

    def updateAccountInfo(self, Username, Password):
        SQLCommand = ("UPDATE Player "
                      "Set Username = ?, "
                      "Password = ? "
                      "WHERE Email = ?")
        
        value = (Username, Password, self.Email)
        self.cursor.execute(SQLCommand, values)
        self.connection.commit()

    def closeConnection(self):
        """Closes Connection to PADification Database"""
        self.connection.close()
        self.Email = None
        self.Password = None
        self.PlayerID = None
        self.Username = None
        self.signedIn = False

    def selectMonsterClass(self, monSearch = None, dictionary = True):
        """Retrieve Monster Class Info from MonsterClassTable, monSearch can be an INT Single ID,
           a tuple of 2 INT for Range, a string of monsterName for a like search or empty for entire collection.
           Returns a List of Tuples"""

        SQLCommand = ("SELECT MonsterClassID, MonsterName, Rarity, PriAttribute, SecAttribute, MonsterTypeOne, MonsterTypeTwo, MonsterTypeThree, ExpCurve, MaxLevel, MonsterCost, ASListID, LeaderSKill.LeaderSkillName, ActiveSkill.ActiveSkillName, MaxHP, MinHP, GrowthRateHP, MaxATK, MinATK, GrowthRateATK, MaxRCV, MinRCV, GrowthRateRCV, CurSell, CurFodder, MonsterPointValue, "
                      "ActiveSkillMaxLevel, ActiveSkillMaxCoolDown, ActiveSkill.ActiveSkillDesc, LeaderSKill.LeaderSkillDesc "
                      "FROM ((MonsterClass LEFT OUTER JOIN ActiveSkill ON MonsterClass.ActiveSkillName = ActiveSkill.ActiveSkillName) LEFT OUTER JOIN LeaderSkill ON MonsterClass.LeaderSkillName = LeaderSKill.LeaderSkillName) ")

        if type(monSearch) == tuple and len(monSearch) == 2:
            SQLCommand += "WHERE MonsterClassID BETWEEN " + str(monSearch[0]) + " AND " + str(monSearch[1])
        elif type(monSearch) == int:
            SQLCommand += "WHERE MonsterClassID = " + str(monSearch)
        elif type(monSearch) == str:
            SQLCommand += "WHERE MonsterName LIKE '%" + monSearch + "%'"

        SQLCommand += " ORDER BY MonsterClassID ASC"
        self.cursor.execute(SQLCommand)

        if dictionary:
            properties = ['MonsterClassID', 'MonsterName', 'Rarity', 'PriAttribute', 'SecAttribute', 'MonsterTypeOne', 'MonsterTypeTwo', 'MonsterTypeThree', 'ExpCurve', 'MaxLevel', 'MonsterCost', 'ASListID', 'LeaderSkillName', 'ActiveSkillName', 'MaxHP', 'MinHP', 'GrowthRateHP', 'MaxATK', 'MinATK', 'GrowthRateATK', 'MaxRCV', 'MinRCV', 'GrowthRateRCV', 'CurSell', 'CurFodder', 'MonsterPointValue', 'ActiveSkillMaxLevel', 'ActiveSkillMaxCoolDown', 'ActiveSkillDesc', 'LeaderSkillDesc']
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

    def selectMonsterInstance(self, monSearch = None, dictionary = True, wishlist = 0):

        
        SQLCommand = ("SELECT MonsterInstance.MonsterClassID, MonsterName, Rarity, PriAttribute, SecAttribute, MonsterTypeOne, MonsterTypeTwo, "
                        "MonsterTypeThree, ExpCurve, MaxLevel, MonsterCost, ASListID, LeaderSkillName, ActiveSkill.ActiveSkillName, MaxHP, MinHP, "
                        "GrowthRateHP, MaxATK, MinATK, GrowthRateATK, MaxRCV, MinRCV, GrowthRateRCV, CurSell, CurFodder, MonsterPointValue, "
                        "ActiveSkillMaxLevel, ActiveSkillMaxCoolDown, InstanceID, Email, CurrentExperience, PlusATK, PlusRCV, PlusHP, SkillsAwoke, "
                        "AssistMonsterID, SkillLevel, LSListID, Favorites, WishList "
                        "FROM (MonsterInstance LEFT OUTER JOIN (MonsterClass LEFT OUTER JOIN ActiveSkill ON MonsterClass.ActiveSkillName = ActiveSkill.ActiveSkillName) "
                        "ON MonsterInstance.MonsterClassID = MonsterClass.MonsterClassID)"
                        "WHERE MonsterInstance.Email = '" + str(self.Email) + "'and MonsterInstance.WishList = " + str(wishlist) )

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
                          'GrowthRateRCV', 'CurSell', 'CurFodder', 'MonsterPointValue', 'ActiveSkillMaxLevel', 'ActiveSkillMaxCoolDown', 
                          'InstanceID', 'Email', 'CurrentExperience', 'PlusATK', 'PlusRCV', 'PlusHP', 'SkillsAwoke', 'AssistMonsterID', 'SkillLevel', 'LSListID', 'Favorites', 'WishList' ]
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

    def saveMonster(self, InstanceDict):
        """Save Monster Instance Record"""
        keys = ['Email', 'CurrentExperience', 'PlusATK', 'PlusRCV', 'PlusHP', 'SkillsAwoke', 'AssistMonsterID', 'SkillLevel', 'LSListID', 'MonsterClassID', 'Favorites', 'WishList' ]
        if InstanceDict["InstanceID"] == None:
            #If it is a new Monster
            InstanceDict.pop("InstanceID")
            InstanceDict["Email"] = self.Email

            values = []
            for i in keys:
                values.append(InstanceDict[i])
                    

            SQLCommand = ("INSERT INTO MonsterInstance (Email, CurrentExperience, PlusATK, PlusRCV, PlusHP, SkillsAwoke, AssistMonsterID, SkillLevel, LSListID, MonsterClassID, Favorites, WishList) "
                          "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)")

            self.cursor.execute(SQLCommand,values)
            self.connection.commit()
            #print("Monster save Successful")

        else:
            """If it is a existing Monster instance"""

            setstr = 'SET '
            values = []
            for i in keys:
                values.append(InstanceDict[i])
                setstr += i + " = ?"  
                setstr += ", " if i != 'WishList' else " "
            values.append(InstanceDict["InstanceID"])

            SQLCommand = ("UPDATE MonsterInstance " + setstr +
                          "WHERE InstanceID = ?")

            self.cursor.execute(SQLCommand,values)
            self.connection.commit()

    def deleteMonster(self, InstanceID):
        """Delete a Monster Instance from MonsterInstance Table and the correspondin Latent Skill List"""
        self.cursor.execute("SELECT * FROM LatentSkillList WHERE InstanceID = " + str(InstanceID))
        LSL = self.cursor.fetchone()
        if LSL:
            self.cursor.execute("DELETE FROM LatentSkillList WHERE InstanceID = " + str(InstanceID))

        SQLCommand = "DELETE FROM MonsterInstance WHERE InstanceID = " + str(InstanceID)
        self.cursor.execute(SQLCommand)
        self.cursor.commit()

    def selectTeamInstance(self, teamsearch = None, dictionary = True):
        """Selects all teams, or by TeamInstanceID, or TeamName returns a list of dictionarys or tuples."""
        SQLCommand = ("SELECT TeamInstanceID, Email, TeamName, LeaderMonster, SubMonsterOne, SubMonsterTwo, SubMonsterThree, SubMonsterFour, AwokenBadgeName "
                "FROM Team "
                "WHERE Email = '" + str(self.Email) + "'" )
        if teamsearch == None:
            SQLCommand += " ORDER BY TeamName ASC"
        elif type(teamsearch) == int:
            SQLCommand += " AND TeamInstanceID = " + str(teamsearch)
        elif type(teamsearch) == str:
            SQLCommand += " AND TeamName LIKE '%" + teamsearch + "%'"

        self.cursor.execute(SQLCommand)

        if dictionary:
            properties = ['TeamInstanceID', 'Email', 'TeamName', 'LeaderMonster',
                          'SubMonsterOne', 'SubMonsterTwo', 'SubMonsterThree', 'SubMonsterFour', 
                          'AwokenBadgeName' ]
            teamcollection = []
            results = self.cursor.fetchone()
            while results:
                #Cycle through all results one by one.
                teamDict = {}      
                count = 0
                for i in results:
                    teamDict[properties[count]] = i
                    count += 1
                teamcollection.append(teamDict)
                results = self.cursor.fetchone()
            return teamcollection
        else:
            return self.cursor.fetchall()

    def saveTeam(self, TeamDict):
        """Save Team Instance Record"""
        keys = [ 'Email', 'TeamName', 'LeaderMonster',
                          'SubMonsterOne', 'SubMonsterTwo', 'SubMonsterThree', 'SubMonsterFour', 
                          'AwokenBadgeName' ]
        if TeamDict["TeamInstanceID"] == None:
            """If it is a new Team"""
            TeamDict.pop("TeamInstanceID")
            TeamDict["Email"] = self.Email

            values = []
            for i in keys:
                values.append(TeamDict[i])
                    

            SQLCommand = ("INSERT INTO Team (Email, TeamName, LeaderMonster, SubMonsterOne, SubMonsterTwo, SubMonsterThree, SubMonsterFour, AwokenBadgeName) "
                          "VALUES (?,?,?,?,?,?,?,?)")

            self.cursor.execute(SQLCommand,values)
            self.connection.commit()

        else:
            """If it is a existing Monster instance"""

            setstr = 'SET '
            values = []
            for i in keys:
                values.append(TeamDict[i])
                setstr += i + " = ?"  
                setstr += ", " if i != 'AwokenBadgeName' else " "
            values.append(TeamDict["TeamInstanceID"])

            SQLCommand = ("UPDATE Team " + setstr +
                          "WHERE TeamInstanceID = ?")

            self.cursor.execute(SQLCommand,values)
            self.connection.commit()

    def deleteTeam(self, TeamInstanceID):
        """Delete a Team Instance from Team Table"""
        SQLCommand = "DELETE FROM Team WHERE TeamInstanceID = " + str(TeamInstanceID)
        self.cursor.execute(SQLCommand)
        self.cursor.commit()

    def getAwokenSkills(self):
        """Returns a List of AwokenSkills"""
        SQLCommand = "SELECT * FROM AwokenSkill"
        self.cursor.execute(SQLCommand)

        results = self.cursor.fetchone()
        AwokenSkills = []
        while results:
            AwokenSkills.append(results[0])
            results = self.cursor.fetchone()
        return AwokenSkills

    def getLatentAwokenSkills(self):

        SQLCommand = "SELECT * FROM LatentSkill"
        self.cursor.execute(SQLCommand)

        results = self.cursor.fetchone()
        LatentSkills = []
        while results:
            LatentSkills.append(results[0])
            results = self.cursor.fetchone()
        return LatentSkills

    def getAwokenSkillList(self, MonsterClassID):
        """Returns a Tuple of a MonsterClass Awoken skills, listed in order starting with MonsterClassID"""
        
        SQLCommand = "SELECT * FROM AwokenSkillList WHERE ASListID = " + str(MonsterClassID)
        self.cursor.execute(SQLCommand)
        return self.cursor.fetchone()

    def getLatentAwokenSkillList(self, InstanceID):
        """Returns a List of Latent Awoken Skills a monster Instance has"""
        SQLCommand = "SELECT * FROM LatentSkillList WHERE InstanceID = " + str(InstanceID)
        self.cursor.execute(SQLCommand)
        return list[self.cursor.fetchone()]

    def getAwokenBadges(self):
        """Returns a List of Awoken Badges"""
        SQLCommand = "SELECT * FROM AwokenBadge"
        self.cursor.execute(SQLCommand)

        results = self.cursor.fetchone()
        AwokenBadges = []
        while results:
            AwokenBadges.append(results[0])
            results = self.cursor.fetchone()
        return AwokenBadges

    def getEvolutionTree(self, nextMonsterID):
        """Returns a Collection of Evolutions a list of lists of tuples to seperate Normal Ultimate and reincarnated"""
        Evolutions = []
        lowestID = nextMonsterID
        
        # Find Start of Tree.
        SQLCommand = ("SELECT NextMonsterID, BaseMonsterID FROM EvolutionTree "
                      "WHERE NextMonsterID = " + str(nextMonsterID) )
        self.cursor.execute(SQLCommand)
        results = self.cursor.fetchall()

        while results:
            lowestID = results[0][1]
            SQLCommand = ("SELECT NextMonsterID, BaseMonsterID FROM EvolutionTree "
                          "WHERE NextMonsterID = " + str(lowestID))
            self.cursor.execute(SQLCommand)
            results = self.cursor.fetchall()
        Evolutions.append([lowestID])


        # Iterate through tree and Add results
        SQLCommand = ("SELECT * FROM EvolutionTree "
                          "WHERE BaseMonsterID = " + str(lowestID))
        self.cursor.execute(SQLCommand)
        results = self.cursor.fetchall()
        Evolutions.append(results)

        subResults = []
        while results:
            SQLCommand = ("SELECT * FROM EvolutionTree "
                          "WHERE BaseMonsterID = " + str(results[0][0]))
            self.cursor.execute(SQLCommand)
            results = self.cursor.fetchall()

            if results:
                if results in Evolutions or results[0] in subResults:
                    continue
                else:
                    Evolutions.append(results)
            
            
                subResults = []

                for i in results:
                    SQLCommand = ("SELECT * FROM EvolutionTree "
                          "WHERE BaseMonsterID = " + str(i[0]))
                    self.cursor.execute(SQLCommand)
                    tempresult = self.cursor.fetchone()
                    if tempresult:
                        subResults.append(tempresult)
                    else:
                        subResults.append(None)

                    for i in Evolutions:
                        for o in subResults:
                            if o in i:
                                continue
                if subResults:
                    Evolutions.append(subResults)
        
        #for i in Evolutions:
        #    print(i)
        return Evolutions

    def getEvolutions(self, MonsterClassID):
        """Returns a Collection of Evolutions and devolutions a that a monster can access"""
        Evolutions = []
        SQLCommand = ("SELECT * FROM EvolutionTree "
                      "WHERE NextMonsterID = " + str(MonsterClassID) )
        self.cursor.execute(SQLCommand)
        results = self.cursor.fetchone()
        #Evolutions.append(results)
        if results == None:
            SQLCommand = ("SELECT * FROM EvolutionTree "
                      "WHERE BaseMonsterID = " + str(MonsterClassID) )
            self.cursor.execute(SQLCommand)
            results = self.cursor.fetchone()
            return results

        if results[7]: # if Ultimate
            SQLCommand = ("SELECT * FROM EvolutionTree "
                      "WHERE NextMonsterID = " + str(results[1]) )

            self.cursor.execute(SQLCommand)
            subresults = self.cursor.fetchone()
            dev = (results[1], results[0], 155, 156, 157, 158, 159, True)
            Evolutions.insert(0, dev)

        SQLCommand = ("SELECT * FROM EvolutionTree "
                      "WHERE BaseMonsterID = " + str(MonsterClassID) )
        self.cursor.execute(SQLCommand)
        results = self.cursor.fetchall()

        if results:
            for i in results:
                Evolutions.append(i)

        return Evolutions

    def getLeaderSkillDesc(self, LeaderSkillName):
        """Return LeaderSkill Desc"""
        if LeaderSkillName != None:
            if "'" in LeaderSkillName:
                LeaderSkillName = LeaderSkillName.replace("'", "''")
            
            SQLCommand = "SELECT LeaderSkillDesc FROM LeaderSkill Where LeaderSkillName = '" + LeaderSkillName + "'"
            self.cursor.execute(SQLCommand)
            result = self.cursor.fetchone()
            if result:
                return result[0] 
            else:
                print(LeaderSkillName.encode('ASCII', 'ignore'))


    def getActiveSkillDesc(self, ActiveSkillName):
        """Return ActiveSkill Desc"""
        if ActiveSkillName != None:
            if "'" in ActiveSkillName:
                ActiveSkillName = ActiveSkillName.replace("'", "''")

            SQLCommand = "SELECT ActiveSkillDesc FROM ActiveSkill Where ActiveSkillName = '" + ActiveSkillName + "'"
            self.cursor.execute(SQLCommand)
            result = self.cursor.fetchone()
            if result:
                return result[0] 
            else:
                print(LeaderSkillName.encode('ASCII', 'ignore'))
