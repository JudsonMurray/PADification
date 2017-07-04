#!/USR/BIN/ENV PYTHON 3.5
#   NAME:    KYLE GUNTON
#   DATE:    07/04/17
#   PURPOSE: FUNCTIONALITY FOR THE EDIT TEAM SCREEN 

#   -V. 0.0.1 -Created base functionality of selection monsters in player collection.
#   -V. 0.0.2 -Updated functionality of monster selection, added team slots, added remove monster
#   -V. 0.0.3 -Updated Screen display, updated File Paths
#   -V. 0.0.4 -Added functionality billy overwrote. Fixed multiple selection of one monster.
#   -V. 0.0.5 -Made many miscellaneous bug fixes
#   -V. 0.0.6 -Added save team functionality, started integration with Team Browser Screen 

import pygame
import tkinter as tk
import pygubu
from tkinter import messagebox
from tkinter import *
import tkinter as tk
import pypyodbc
import sys
import PADSQL
import PADMonster
import TeamBrowserScreen
#variables to tell which monsters are selected within the collection
global leadMon, sub1, sub2, sub3, sub4
leadMon = sub1 = sub2 = sub3 = sub4 = None

class MonsterFrame:
    def __init__(self, master, mastermaster, i):
        self.master = master
        self.mastermaster = mastermaster
        self.i = i
        self.builder = pygubu.Builder()
        self.builder.add_from_file('src/ui/PlayerCollection.ui')
        self.monbut = self.builder.get_object('MonsFrame', self.master)
        self.builder.connect_callbacks(self)
        
        #Adds monster collection buttons to monster collection
        self.canLeadMon = self.mastermaster.get_object('canLeadMon')
        self.canSubMon1 = self.mastermaster.get_object('canSubMon1')
        self.canSubMon2 = self.mastermaster.get_object('canSubMon2')
        self.canSubMon3 = self.mastermaster.get_object('canSubMon3')
        self.canSubMon4 = self.mastermaster.get_object('canSubMon4')

    def clickMe(self, event):
        '''Method for selection of a monster in the player collection'''
        #Call globals to be used in method
        global monsterClassIDs, myMonsterList, connection, cursor, teamMonsterSelected, var
        global leadMon, sub1, sub2, sub3, sub4
        global myMonsters, destroyerTeam

        if state[self.i] == 'on':   #Only executes if a monster is notalready in use
            #Retrieves information from database and removes excess string content
            self.builder.add_from_file('src/ui/EditTeam.ui')
            h = myMonsters[self.i]
            if var.get() == 0:
                self.image =myMonsterList[self.i].zoom(10).subsample(7)
                self.canLeadMon.create_image(7, 7, image = self.image, anchor = tk.NW)
                if leadMon != None and leadMon != sub1 and leadMon != sub2 and leadMon != sub3 and leadMon != sub4:
                    buttons[leadMon].monbut.config(relief=FLAT)
                    state[leadMon] = 'on'
                leadMon = self.i
                destroyerTeam.setLeaderMonster(int(h))
            elif var.get() == 1:
                self.image = myMonsterList[self.i].zoom(10).subsample(7)
                self.canSubMon1.create_image(7, 7, image = self.image, anchor = tk.NW)
                if sub1 != None and sub1 != leadMon and sub1 != sub2 and sub1 != sub3 and sub1 != sub4:
                    buttons[sub1].monbut.config(relief=FLAT)
                    state[sub1] = 'on'
                sub1 = self.i
                destroyerTeam.setSubMonsterOne(int(h))
            elif var.get() == 2:
                self.image = myMonsterList[self.i].zoom(10).subsample(7)
                self.canSubMon2.create_image(7, 7, image = self.image, anchor = tk.NW)
                if sub2 != None and sub2 != leadMon and sub2!= sub1 and sub2 != sub3 and sub2 != sub4:
                    buttons[sub2].monbut.config(relief=FLAT)
                    state[sub2] = 'on'
                sub2 = self.i
                destroyerTeam.setSubMonsterTwo(int(h))
            elif var.get() == 3:
                self.image = myMonsterList[self.i].zoom(10).subsample(7)
                self.canSubMon3.create_image(7, 7, image = self.image, anchor = tk.NW)
                if sub3 != None and sub3 != leadMon and sub3 != sub1 and sub3 != sub2 and sub3 != sub4:
                    buttons[sub3].monbut.config(relief=FLAT)
                    state[sub3] = 'on'
                sub3 = self.i
                destroyerTeam.setSubMonsterThree(int(h))
            elif var.get() == 4:
                self.image = myMonsterList[self.i].zoom(10).subsample(7)
                self.canSubMon4.create_image(7, 7, image = self.image, anchor = tk.NW)
                if sub4 != None and sub4 != leadMon and sub4 != sub1 and sub4 != sub2 and sub4 != sub3:
                    buttons[sub4].monbut.config(relief=FLAT)
                    state[sub4] = 'on'
                sub4 = self.i
                destroyerTeam.setSubMonsterFour(int(h))

            state[self.i] = 'off'
            buttons[self.i].monbut.config(relief=SUNKEN)
            self.updateTeamLabels()
            return

    def updateTeamLabels(self):
        self.mastermaster.get_object('lblTeamHP').config(text=  'HP:    ' + str(destroyerTeam.TeamHP))
        self.mastermaster.get_object('lblTeamCost').config(text='Cost: ' + str(destroyerTeam.TeamCost))
        self.mastermaster.get_object('lblTeamRCV').config(text= 'RCV:  ' + str(destroyerTeam.TeamRCV))
        self.mastermaster.get_object('lblFireATK').config(text= 'Fire ATK:     ' + str(destroyerTeam.FireATK))
        self.mastermaster.get_object('lblWaterATK').config(text='Water ATK: ' + str(destroyerTeam.WaterATK))
        self.mastermaster.get_object('lblWoodATK').config(text= 'Wood ATK: ' + str(destroyerTeam.WoodATK))
        self.mastermaster.get_object('lblLightATK').config(text='Light ATK:   ' + str(destroyerTeam.LightATK))
        self.mastermaster.get_object('lblDarkATK').config(text= 'Dark ATK:    ' + str(destroyerTeam.DarkATK))

        self.mastermaster.get_object('lblSkillBindResist').config(text=  'Skill Bind Resist: ' + str(destroyerTeam.skillBindResist) + '%')
        self.mastermaster.get_object('lblSkillBoost').config(text=   'Skill Boost: ' + str(destroyerTeam.skillBoost))
        self.mastermaster.get_object('lblMoveTime').config(text=  'Move Time: ' + str(destroyerTeam.moveTime) + 's')
        self.mastermaster.get_object('lblDarkResist').config(text=  'Dark Resist: ' + str(destroyerTeam.darkResist) + '%')
        self.mastermaster.get_object('lblJammerResist').config(text=  'Jammer Resist: ' + str(destroyerTeam.jammerResist) + '%')
        self.mastermaster.get_object('lblPoisonResist').config(text=  'Poison Resist: ' + str(destroyerTeam.poisonResist) + '%')
        self.mastermaster.get_object('lblEnhancedFireChance').config(text=  'Enhanced Fire Chance: ' + str(destroyerTeam.enhancedFireChance) + '%')
        self.mastermaster.get_object('lblEnhancedWaterChance').config(text=  'Enhanced Water Chance: ' + str(destroyerTeam.enhancedWaterChance) + '%')
        self.mastermaster.get_object('lblEnhancedWoodChance').config(text=  'Enhanced Wood Chance: ' + str(destroyerTeam.enhancedWoodChance) + '%')
        self.mastermaster.get_object('lblEnhancedLightChance').config(text=  'Enhanced Light Chance: ' + str(destroyerTeam.enhancedLightChance) + '%')
        self.mastermaster.get_object('lblEnhancedDarkChance').config(text=  'Enhanced Dark Chance: ' + str(destroyerTeam.enhancedDarkChance) + '%')
        self.mastermaster.get_object('lblEnhancedHealChance').config(text=  'Enhanced Heal Chance: ' + str(destroyerTeam.enhancedHealChance) + '%')
        self.mastermaster.get_object('lblFireDR').config(text=  'Fire Dmg Reduction: ' + str(destroyerTeam.fireDmgReduction) + '%')
        self.mastermaster.get_object('lblWaterDR').config(text=  'Water Dmg Reduction: ' + str(destroyerTeam.waterDmgReduction) + '%')
        self.mastermaster.get_object('lblWoodDR').config(text=  'Wood Dmg Reduction: ' + str(destroyerTeam.woodDmgReduction) + '%')
        self.mastermaster.get_object('lblLightDR').config(text=  'Light Dmg Reduction: ' + str(destroyerTeam.lightDmgReduction) + '%')
        self.mastermaster.get_object('lblDarkDR').config(text=  'Dark Dmg Reduction: ' + str(destroyerTeam.darkDmgReduction) + '%')

        return

class EditTeam():
    """Displays Edit Team Frame and Widgets"""
    def __init__(self, master):
        #Declare Global Variables
        global monsterClassIDs, myMonsterList, teamMonsterSelected, myMonsters
        global connection, cursor
        global state, destroyerTeam, var, buttons
        buttons = []
        state = []
        monsterClassIDs = []
        myMonsterList = []
        var = IntVar(0)
        teamMonsterSelected = Radiobutton(text='', variable=var, value=0)
        
        self.PADsql = PADSQL.PADSQL()

        #Connect to Database
        self.PADsql.connect()
        cursor = self.PADsql.cursor
        connection = self.PADsql.connection

        #Retrieves monster Instance IDs from database
        sql = "SELECT InstanceID FROM monsterInstance WHERE Username = 'KyleTD'"
        playerTable = cursor.execute(sql)
        myMonsters = playerTable.fetchall()
        connection.commit()

        #PADification APP signup/login
        #self.PADsql.signup(['PADTest','PADTest','A@a.ap',100000000])
        self.PADsql.login('KyleTD','KyleTD')
        self.master = master
        #Create GUI and add title image
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('src/ui/EditTeam.ui')
        self.mainwindow = builder.get_object('EditTeamFrame', master)    
        self.titleImg = tk.PhotoImage(file = 'Resource/PAD/Images/PADification Title.png')
        self.builder.get_object('titleImage').create_image(0,0, image =self.titleImg , anchor = tk.NW, tag = "pic")
        self.canvas = builder.get_object('canMonsterCollection')
        self.teamCanvas = builder.get_object('teamMonstersFrame')
        #for i in range (0,500):
        #    leadMonster = PADMonster.Monster(self.PADsql.selectMonsterClass(393)[0])
        #    leadMonster.setCurrentExperience(4000000)

        #    leadMonster.setPlusATK(99)
        #    leadMonster.setPlusHP(99)
        #    leadMonster.setPlusRCV(99)
        #    leadMonster.setSkillsAwoke(6)


        #    self.PADsql.saveMonster(leadMonster.getSaveDict())

        #Create TeamObject
        destroyerTeam = PADMonster.Team(self.PADsql)
        self.updateTeamLabelImages()
        self.updateTeamLabels()

        x=0
        #Populates lists with monsterIDs
        for i in range(0,len(myMonsters)):
            myMonsters[i] = str(myMonsters[i]).replace("(", "")
            myMonsters[i] = str(myMonsters[i]).replace(",)", "")
                    
            self.PADsql.selectMonsterInstance(myMonsters[i])
            sql = "SELECT MonsterClassID FROM monsterInstance WHERE InstanceID = {}".format(myMonsters[i])
            
            myMonster = cursor.execute(sql)
            myMonster = myMonster.fetchone()
            myMonster = str(myMonster).replace("(", "")
            monsterClass = myMonster.replace(",)", "")
            monsterClassIDs += monsterClass,
            myMonster= tk.PhotoImage(file = 'Resource/PAD/Images/thumbnails/'+ str(monsterClass) + '.png').zoom(15)
            myMonster = myMonster.subsample(30)
            myMonsterList.append(myMonster)
            x+=1


        self.canLeadMon = self.builder.get_object('canLeadMon')
        self.canSubMon1 = self.builder.get_object('canSubMon1')
        self.canSubMon2 = self.builder.get_object('canSubMon2')
        self.canSubMon3 = self.builder.get_object('canSubMon3')
        self.canSubMon4 = self.builder.get_object('canSubMon4')
        
        self.canLeadMon.config(relief=SUNKEN)
        
        
        #teamMonsterSelected = self.builder.get_object('teamMonsterSelected')
        teamMonsterSelected.config(value=0)
        
        #Creates a list of buttons for the monsters in a players collection
        b = len(myMonsterList)

        leader = self.builder.get_object('canLeadMon')
       
        for i in range(0,b):
            buttons.append(MonsterFrame(self.canvas, self.builder, i))
            state.append('on')
            buttons[i].monbut.grid(row=i // 10,column = i % 10)
            buttons[i].builder.get_object('FrameLabel').create_image(2,2, image = myMonsterList[i], anchor = tk.NW)

        if (len(self.canvas.grid_slaves()) // 2) * 30 > 500:
            pass
        else:
            self.canvas.config(height=1000) 
        
        self.builder.connect_callbacks(self)
        
    def loadTeam(self, instance):
        self.teamInstance = instance
        self.updateTeam(self.teamInstance)
        for i in buttons:
            i.monbut
            x = 1
        return

    def updateTeam(self, i):
        sql = "SELECT LeaderMonster, SubMonsterOne ,SubMonsterTwo, SubMonsterThree, SubMonsterFour FROM team WHERE TeamInstanceID = {}".format(str(i))
        playerTable = cursor.execute(sql)
        monMonsters = playerTable.fetchall()

        destroyerTeamBase = self.PADsql.selectTeamInstance(i)
        if destroyerTeamBase[0]['LeaderMonster'] != None:
            destroyerTeam.setLeaderMonster(destroyerTeamBase[0]['LeaderMonster'])
        else:
            destroyerTeam.setLeaderMonster()
        if destroyerTeamBase[0]['SubMonsterOne'] != None:
            destroyerTeam.setSubMonsterOne(destroyerTeamBase[0]['SubMonsterOne'])
        else:
            destroyerTeam.setSubMonsterOne()
        if destroyerTeamBase[0]['SubMonsterTwo'] != None:
            destroyerTeam.setSubMonsterTwo(destroyerTeamBase[0]['SubMonsterTwo'])
        else:
            destroyerTeam.setSubMonsterTwo()
        if destroyerTeamBase[0]['SubMonsterThree'] != None:
            destroyerTeam.setSubMonsterThree(destroyerTeamBase[0]['SubMonsterThree'])
        else:
            destroyerTeam.setSubMonsterThree()
        if destroyerTeamBase[0]['SubMonsterFour'] != None:
            destroyerTeam.setSubMonsterFour(destroyerTeamBase[0]['SubMonsterFour'])
        else:
            destroyerTeam.setSubMonsterFour()
        mClassIDs = []
        global myMonsterList
        self.myMonsterL = []

        for i in monMonsters[0]:
            
            if i != None:
                sql = "SELECT MonsterClassID FROM monsterInstance WHERE InstanceID = {}".format(i)
            
                self.myMonster = cursor.execute(sql)
                self.myMonster = self.myMonster.fetchone()
                self.myMonster = str(self.myMonster).replace("(", "")
                monsterClass = self.myMonster.replace(",)", "")
                mClassIDs += monsterClass,
                self.myMonster= tk.PhotoImage(file = 'Resource/PAD/Images/thumbnails/'+ str(monsterClass) + '.png')
            else:
                self.myMonster = None
            self.myMonsterL.append(self.myMonster)
        self.canLeadMon = self.builder.get_object('canLeadMon')
        self.canSubMon1 = self.builder.get_object('canSubMon1')
        self.canSubMon2 = self.builder.get_object('canSubMon2')
        self.canSubMon3 = self.builder.get_object('canSubMon3')
        self.canSubMon4 = self.builder.get_object('canSubMon4')
        self.canLeadMon.create_image(7,7,image = self.myMonsterL[0], anchor = tk.NW, tag = "pic")
        self.canSubMon1.create_image(7,7,image = self.myMonsterL[1], anchor = tk.NW, tag = "pic")
        self.canSubMon2.create_image(7,7,image = self.myMonsterL[2], anchor = tk.NW, tag = "pic")
        self.canSubMon3.create_image(7,7,image = self.myMonsterL[3], anchor = tk.NW, tag = "pic")
        self.canSubMon4.create_image(7,7,image = self.myMonsterL[4], anchor = tk.NW, tag = "pic")
        self.updateTeamLabels()
        self.updateTeamLabelImages()

    def raiseTeam(self):
        """returns team selection to raised relief"""
        self.canLeadMon.config(relief=RAISED)
        self.canSubMon1.config(relief=RAISED)
        self.canSubMon2.config(relief=RAISED)
        self.canSubMon3.config(relief=RAISED)
        self.canSubMon4.config(relief=RAISED)
        return

    def leadClick(self, event):
        """Command invoked when leader monster is selected"""
        global var
        var.set(0)
        self.raiseTeam()
        self.canLeadMon.config(relief=SUNKEN)
        return

    def sub1Click(self, event):
        """Command invoked when sub monster 1 is selected"""
        global var
        var.set(1)
        self.raiseTeam()
        self.canSubMon1.config(relief=SUNKEN)
        return

    def sub2Click(self, event):
        """Command invoked when sub monster 2 is selected"""
        global var
        var.set(2)
        self.raiseTeam()
        self.canSubMon2.config(relief=SUNKEN)
        return

    def sub3Click(self, event):
        """Command invoked when sub monster 3 is selected"""
        global var
        var.set(3)
        self.raiseTeam()
        self.canSubMon3.config(relief=SUNKEN)
        return

    def sub4Click(self, event):
        """Command invoked when sub monster 4 is selected"""
        global var
        var.set(4)
        self.raiseTeam()
        self.canSubMon4.config(relief=SUNKEN)
        return

    def removeMonster(self, event):
        """Remove monsterfrom selected team slot"""
        self.canLeadMon = self.builder.get_object('canLeadMon')
        self.canSubMon1 = self.builder.get_object('canSubMon1')
        self.canSubMon2 = self.builder.get_object('canSubMon2')
        self.canSubMon3 = self.builder.get_object('canSubMon3')
        self.canSubMon4 = self.builder.get_object('canSubMon4')

        if var.get() == 0:
            self.canLeadMon.delete('all')
            if destroyerTeam.LeaderMonster != destroyerTeam.setLeaderMonster():
                destroyerTeam.setLeaderMonster()
                buttons[leadMon].monbut.config(relief=FLAT)
                state[leadMon] = 'on'
        elif var.get() == 1:
            self.canSubMon1.delete('all')
            if destroyerTeam.SubMonsterOne != destroyerTeam.setSubMonsterOne():
                destroyerTeam.setSubMonsterOne()
                buttons[sub1].monbut.config(relief=FLAT)
                state[sub1] = 'on'
        elif var.get() == 2:
            self.canSubMon2.delete('all')
            if destroyerTeam.SubMonsterTwo != destroyerTeam.setSubMonsterTwo():
                destroyerTeam.setSubMonsterTwo()
                buttons[sub2].monbut.config(relief=FLAT)
                state[sub2] = 'on'
        elif var.get() == 3:
            self.canSubMon3.delete('all')
            if destroyerTeam.SubMonsterThree != destroyerTeam.setSubMonsterThree():
                destroyerTeam.setSubMonsterThree()
                buttons[sub3].monbut.config(relief=FLAT)
                state[sub3] = 'on'   
        elif var.get() == 4:
            self.canSubMon4.delete('all')
            if destroyerTeam.SubMonsterFour != destroyerTeam.setSubMonsterFour():
                destroyerTeam.setSubMonsterFour()
                buttons[sub4].monbut.config(relief=FLAT)
                state[sub4] = 'on'
        self.updateTeamLabels()
        return

    def updateTeamLabels(self):
        """Updates team information labels"""
        x = destroyerTeam.TeamHP
        self.builder.get_object('lblTeamHP').config(text=  'HP:    ' + str(destroyerTeam.TeamHP))
        self.builder.get_object('lblTeamCost').config(text='Cost: ' + str(destroyerTeam.TeamCost))
        self.builder.get_object('lblTeamRCV').config(text= 'RCV:  ' + str(destroyerTeam.TeamRCV))
        self.builder.get_object('lblFireATK').config(text= 'Fire ATK:     ' + str(destroyerTeam.FireATK))
        self.builder.get_object('lblWaterATK').config(text='Water ATK: ' + str(destroyerTeam.WaterATK))
        self.builder.get_object('lblWoodATK').config(text= 'Wood ATK: ' + str(destroyerTeam.WoodATK))
        self.builder.get_object('lblLightATK').config(text='Light ATK:   ' + str(destroyerTeam.LightATK))
        self.builder.get_object('lblDarkATK').config(text= 'Dark ATK:    ' + str(destroyerTeam.DarkATK))

        self.builder.get_object('lblSkillBindResist').config(text=  'Skill Bind Resist: ' + str(destroyerTeam.skillBindResist) + '%')
        self.builder.get_object('lblSkillBoost').config(text=   'Skill Boost: ' + str(destroyerTeam.skillBoost))
        self.builder.get_object('lblMoveTime').config(text=  'Move Time: ' + str(destroyerTeam.moveTime) + 's')
        self.builder.get_object('lblDarkResist').config(text=  'Dark Resist: ' + str(destroyerTeam.darkResist) + '%')
        self.builder.get_object('lblJammerResist').config(text=  'Jammer Resist: ' + str(destroyerTeam.jammerResist) + '%')
        self.builder.get_object('lblPoisonResist').config(text=  'Poison Resist: ' + str(destroyerTeam.poisonResist) + '%')
        self.builder.get_object('lblEnhancedFireChance').config(text=  'Enhanced Fire Chance: ' + str(destroyerTeam.enhancedFireChance) + '%')
        self.builder.get_object('lblEnhancedWaterChance').config(text=  'Enhanced Water Chance: ' + str(destroyerTeam.enhancedWaterChance) + '%')
        self.builder.get_object('lblEnhancedWoodChance').config(text=  'Enhanced Wood Chance: ' + str(destroyerTeam.enhancedWoodChance) + '%')
        self.builder.get_object('lblEnhancedLightChance').config(text=  'Enhanced Light Chance: ' + str(destroyerTeam.enhancedLightChance) + '%')
        self.builder.get_object('lblEnhancedDarkChance').config(text=  'Enhanced Dark Chance: ' + str(destroyerTeam.enhancedDarkChance) + '%')
        self.builder.get_object('lblEnhancedHealChance').config(text=  'Enhanced Heal Chance: ' + str(destroyerTeam.enhancedHealChance) + '%')
        self.builder.get_object('lblFireDR').config(text=  'Fire Dmg Reduction: ' + str(destroyerTeam.fireDmgReduction) + '%')
        self.builder.get_object('lblWaterDR').config(text=  'Water Dmg Reduction: ' + str(destroyerTeam.waterDmgReduction) + '%')
        self.builder.get_object('lblWoodDR').config(text=  'Wood Dmg Reduction: ' + str(destroyerTeam.woodDmgReduction) + '%')
        self.builder.get_object('lblLightDR').config(text=  'Light Dmg Reduction: ' + str(destroyerTeam.lightDmgReduction) + '%')
        self.builder.get_object('lblDarkDR').config(text=  'Dark Dmg Reduction: ' + str(destroyerTeam.darkDmgReduction) + '%')
        return

    def updateTeamLabelImages(self):
        self.recoveryImg = tk.PhotoImage(file='Resource/PAD/Images/Attributes/RCVSymbol.png') 
        self.fireImg = tk.PhotoImage(file='Resource/PAD/Images/Attributes/FireSymbol.png')
        self.waterImg = tk.PhotoImage(file='Resource/PAD/Images/Attributes/WaterSymbol.png')
        self.woodImg = tk.PhotoImage(file='Resource/PAD/Images/Attributes/WoodSymbol.png')
        self.lightImg = tk.PhotoImage(file='Resource/PAD/Images/Attributes/LightSymbol.png') 
        self.darkImg = tk.PhotoImage(file='Resource/PAD/Images/Attributes/DarkSymbol.png') 

        self.skillBindResistImg = tk.PhotoImage(file='Resource/PAD/Images/Awoken Skills/Resistance-Skill Bind.png') 
        self.fireDmgReductionImg = tk.PhotoImage(file='Resource/PAD/Images/Awoken Skills/Reduce Fire Damage.png') 
        self.waterDmgReductionImg = tk.PhotoImage(file='Resource/PAD/Images/Awoken Skills/Reduce Water Damage.png') 
        self.woodDmgReductionImg = tk.PhotoImage(file='Resource/PAD/Images/Awoken Skills/Reduce Wood Damage.png') 
        self.lightDmgReductionImg = tk.PhotoImage(file='Resource/PAD/Images/Awoken Skills/Reduce Light Damage.png') 
        self.darkDmgReductionImg = tk.PhotoImage(file='Resource/PAD/Images/Awoken Skills/Reduce Dark Damage.png') 
        self.darkResistImg = tk.PhotoImage(file='Resource/PAD/Images/Awoken Skills/Resistance-Dark.png') 
        self.jammerResistImg = tk.PhotoImage(file='Resource/PAD/Images/Awoken Skills/Enhanced Fire Orbs.png') 
        self.poisonResistImg = tk.PhotoImage(file='Resource/PAD/Images/Awoken Skills/Resistance-Poison.png') 
        self.enhancedFireChanceImg = tk.PhotoImage(file='Resource/PAD/Images/Awoken Skills/Enhanced Fire Orbs.png') 
        self.enhancedWaterChanceImg = tk.PhotoImage(file='Resource/PAD/Images/Awoken Skills/Enhanced Water Orbs.png') 
        self.enhancedWoodChanceImg = tk.PhotoImage(file='Resource/PAD/Images/Awoken Skills/Enhanced Wood Orbs.png') 
        self.enhancedLightChanceImg = tk.PhotoImage(file='Resource/PAD/Images/Awoken Skills/Enhanced Light Orbs.png') 
        self.enhancedDarkChanceImg = tk.PhotoImage(file='Resource/PAD/Images/Awoken Skills/Enhanced Dark Orbs.png') 
        self.enhancedHealChanceImg = tk.PhotoImage(file='Resource/PAD/Images/Awoken Skills/Enhanced Heal Orbs.png') 
        self.moveTimeImg = tk.PhotoImage(file='Resource/PAD/Images/Awoken Skills/Extend Time.png') 
        self.skillBoostImg = tk.PhotoImage(file='Resource/PAD/Images/Awoken Skills/Skill Boost.png') 

        self.builder.get_object('hpImg').config(image=self.recoveryImg) 
        self.builder.get_object('recoveryImg').config(image=self.recoveryImg) 
        self.builder.get_object('fireImg').config(image=self.fireImg) 
        self.builder.get_object('waterImg').config(image=self.waterImg)
        self.builder.get_object('woodImg').config(image=self.woodImg)
        self.builder.get_object('lightImg').config(image=self.lightImg)
        self.builder.get_object('darkImg').config(image=self.darkImg)
        self.builder.get_object('skillBindResistImg').config(image=self.skillBindResistImg)
        self.builder.get_object('fireDRImg').config(image=self.fireDmgReductionImg)
        self.builder.get_object('waterDRImg').config(image=self.waterDmgReductionImg)
        self.builder.get_object('woodDRImg').config(image=self.woodDmgReductionImg)
        self.builder.get_object('lightDRImg').config(image=self.lightDmgReductionImg)
        self.builder.get_object('darkDRImg').config(image=self.darkDmgReductionImg)
        self.builder.get_object('darkResistImg').config(image=self.darkResistImg)
        self.builder.get_object('jammerResistImg').config(image=self.jammerResistImg)
        self.builder.get_object('poisonResistImg').config(image=self.poisonResistImg)
        self.builder.get_object('enhancedFireChanceImg').config(image=self.enhancedFireChanceImg)
        self.builder.get_object('enhancedWaterChanceImg').config(image=self.enhancedWaterChanceImg)
        self.builder.get_object('enhancedWoodChanceImg').config(image=self.enhancedWoodChanceImg)
        self.builder.get_object('enhancedLightChanceImg').config(image=self.enhancedLightChanceImg)
        self.builder.get_object('enhancedDarkChanceImg').config(image=self.enhancedDarkChanceImg)
        self.builder.get_object('enhancedHealChanceImg').config(image=self.enhancedHealChanceImg)
        self.builder.get_object('moveTimeImg').config(image=self.moveTimeImg)
        self.builder.get_object('skillBoostImg').config(image=self.skillBoostImg)
        return

    def selectBadge(self, event):
        pass

    def cancelTeamEdit(self, event):
        self.master.showTeamBrowser()

    def saveTeam(self, event):
        x = self.builder.get_variable('teamName').get()
        destroyerTeam.setTeamName(x)
        saveThisTeam = destroyerTeam.getSaveDict()
        self.PADsql.saveTeam(saveThisTeam)
        tb = self.master.teamBrowser
        #self.builder.get_object('')
        tb.teamListBox.insert(END, str(destroyerTeam.TeamInstanceID))
        zz =destroyerTeam.TeamInstanceID
        self.master.showTeamBrowser()

if __name__ == '__main__':
    root = tk.Tk()
    app = EditTeam(root)
    root.mainloop()