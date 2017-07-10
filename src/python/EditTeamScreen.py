#!/USR/BIN/ENV PYTHON 3.5
#   NAME:    KYLE GUNTON
#   DATE:    06/28/17
#   PURPOSE: FUNCTIONALITY FOR THE EDIT TEAM SCREEN 

#   -V. 0.0.1 -Created base functionality of selection monsters in player collection.
#   -V. 0.0.2 -Updated functionality of monster selection, added team slots, added remove monster
#   -V. 0.0.3 -Updated Screen display, updated File Paths
#   -V. 0.0.4 -Added functionality billy overwrote. Fixed multiple selection of one monster.
#   -V. 0.0.5 -Made many miscellaneous bug fixes

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

#variables to tell which monsters are selected within the collection


class MonsterFrame:
    def __init__(self, master, masterbuilder, i, ids, currentMonster, buttons, padsql, state, team, var):
        self.destroyerTeam = team
        self.master = master
        self.masterbuilder = masterbuilder
        self.i = i
        self.builder = pygubu.Builder()
        self.builder.add_from_file('src/ui/PlayerCollection.ui')
        self.monbut = self.builder.get_object('MonsFrame', self.master)
        self.builder.connect_callbacks(self)
        self.ids = ids
        self.currentMonster = currentMonster
        self.buttons = buttons
        self.padsql = padsql
        self.state = state
        self.var = var
        #Adds monster collection buttons to monster collection
        self.canLeadMon = self.masterbuilder.get_object('canLeadMon')
        self.canSubMon1 = self.masterbuilder.get_object('canSubMon1')
        self.canSubMon2 = self.masterbuilder.get_object('canSubMon2')
        self.canSubMon3 = self.masterbuilder.get_object('canSubMon3')
        self.canSubMon4 = self.masterbuilder.get_object('canSubMon4')

    def clickMe(self, event):
        '''Method for selection of a monster in the player collection'''
        self.count = 0
        self.leadMon = self.sub1 = self.sub2 = self.sub3 = self.sub4 = None
        for b in self.ids:
            if self.destroyerTeam.LeaderMonster == b:
                self.leadMon = self.count
            elif self.destroyerTeam.SubMonsterOne == b:
                self.sub1=self.count
            elif self.destroyerTeam.SubMonsterTwo== b:
                self.sub2=self.count
            elif self.destroyerTeam.SubMonsterThree == b:
                self.sub3=self.count
            elif self.destroyerTeam.SubMonsterFour == b:
                self.sub4=self.count
            self.count += 1

        if self.state == 'on':   #Only executes if a monster is not already in use
            #Retrieves information from database and removes excess string content
            self.builder.add_from_file('src/ui/EditTeam.ui')
            h = self.currentMonster.InstanceID
            self.image = tk.PhotoImage(file = "resource/PAD/Images/Thumbnails/" + str(self.currentMonster.MonsterClassID) + '.png').zoom(10).subsample(15)
            if self.var.get() == 0:
                self.canLeadMon.create_image(7, 7, image = self.image, anchor = tk.NW)
                if self.leadMon != None:# and self.leadMon != self.sub1 and self.leadMon != self.sub2 and self.leadMon != self.sub3 and self.leadMon != self.sub4:
                    self.buttons[self.leadMon].monbut.config(relief=FLAT)
                    self.buttons[self.leadMon].state = 'on'
                self.leadMon = self.i
                self.destroyerTeam.setLeaderMonster(int(h))
            elif self.var.get() == 1:
                self.canSubMon1.create_image(7, 7, image = self.image, anchor = tk.NW)
                if self.sub1 != None:# and self.sub1 != self.leadMon and self.sub1 != self.sub2 and self.sub1 != self.sub3 and self.sub1 != self.sub4:
                    self.buttons[self.sub1].monbut.config(relief=FLAT)
                    self.buttons[self.sub1].state = 'on'
                self.sub1 = self.i
                self.destroyerTeam.setSubMonsterOne(int(h))
            elif self.var.get() == 2:
                self.canSubMon2.create_image(7, 7, image = self.image, anchor = tk.NW)
                if self.sub2 != None:#  and self.sub2 != self.leadMon and self.sub2!= self.sub1 and self.sub2 != self.sub3 and self.sub2 != self.sub4:
                    self.buttons[self.sub2].monbut.config(relief=FLAT)
                    self.buttons[self.sub2].state = 'on'
                self.sub2 = self.i
                self.destroyerTeam.setSubMonsterTwo(int(h))
            elif self.var.get() == 3:
                self.canSubMon3.create_image(7, 7, image = self.image, anchor = tk.NW)
                if self.sub3 != None:#  and self.sub3 != self.leadMon and self.sub3 != self.sub1 and self.sub3 != self.sub2 and self.sub3 != self.sub4:
                    self.buttons[self.sub3].monbut.config(relief=FLAT)
                    self.buttons[self.sub3].state = 'on'
                self.sub3 = self.i
                self.destroyerTeam.setSubMonsterThree(int(h))
            elif self.var.get() == 4:
                self.canSubMon4.create_image(7, 7, image = self.image, anchor = tk.NW)
                if self.sub4 != None:#  and self.sub4 != self.leadMon and self.sub4 != self.sub1 and self.sub4 != self.sub2 and self.sub4 != self.sub3:
                    self.buttons[self.sub4].monbut.config(relief=FLAT)
                    self.buttons[self.sub4].state = 'on'
                self.sub4 = self.i
                self.destroyerTeam.setSubMonsterFour(int(h))

            
            self.state = 'off'
            self.buttons[self.i].monbut.config(relief=SUNKEN)
            self.updateTeamLabels()
            return

    def updateTeamLabels(self):
        self.masterbuilder.get_object('lblTeamHP').config(text=  'HP:    ' + str(self.destroyerTeam.TeamHP))
        self.masterbuilder.get_object('lblTeamCost').config(text='Cost: ' + str(self.destroyerTeam.TeamCost))
        self.masterbuilder.get_object('lblTeamRCV').config(text= 'RCV:  ' + str(self.destroyerTeam.TeamRCV))
        self.masterbuilder.get_object('lblFireATK').config(text= 'Fire ATK:     ' + str(self.destroyerTeam.FireATK))
        self.masterbuilder.get_object('lblWaterATK').config(text='Water ATK: ' + str(self.destroyerTeam.WaterATK))
        self.masterbuilder.get_object('lblWoodATK').config(text= 'Wood ATK: ' + str(self.destroyerTeam.WoodATK))
        self.masterbuilder.get_object('lblLightATK').config(text='Light ATK:   ' + str(self.destroyerTeam.LightATK))
        self.masterbuilder.get_object('lblDarkATK').config(text= 'Dark ATK:    ' + str(self.destroyerTeam.DarkATK))

        self.masterbuilder.get_object('lblSkillBindResist').config(text=  'Skill Bind Resist: ' + str(self.destroyerTeam.skillBindResist) + '%')
        self.masterbuilder.get_object('lblSkillBoost').config(text=   'Skill Boost: ' + str(self.destroyerTeam.skillBoost))
        self.masterbuilder.get_object('lblMoveTime').config(text=  'Move Time: ' + str(self.destroyerTeam.moveTime) + 's')
        self.masterbuilder.get_object('lblDarkResist').config(text=  'Dark Resist: ' + str(self.destroyerTeam.darkResist) + '%')
        self.masterbuilder.get_object('lblJammerResist').config(text=  'Jammer Resist: ' + str(self.destroyerTeam.jammerResist) + '%')
        self.masterbuilder.get_object('lblPoisonResist').config(text=  'Poison Resist: ' + str(self.destroyerTeam.poisonResist) + '%')
        self.masterbuilder.get_object('lblEnhancedFireChance').config(text=  'Enhanced Fire Chance: ' + str(self.destroyerTeam.enhancedFireChance) + '%')
        self.masterbuilder.get_object('lblEnhancedWaterChance').config(text=  'Enhanced Water Chance: ' + str(self.destroyerTeam.enhancedWaterChance) + '%')
        self.masterbuilder.get_object('lblEnhancedWoodChance').config(text=  'Enhanced Wood Chance: ' + str(self.destroyerTeam.enhancedWoodChance) + '%')
        self.masterbuilder.get_object('lblEnhancedLightChance').config(text=  'Enhanced Light Chance: ' + str(self.destroyerTeam.enhancedLightChance) + '%')
        self.masterbuilder.get_object('lblEnhancedDarkChance').config(text=  'Enhanced Dark Chance: ' + str(self.destroyerTeam.enhancedDarkChance) + '%')
        self.masterbuilder.get_object('lblEnhancedHealChance').config(text=  'Enhanced Heal Chance: ' + str(self.destroyerTeam.enhancedHealChance) + '%')
        self.masterbuilder.get_object('lblFireDR').config(text=  'Fire Dmg Reduction: ' + str(self.destroyerTeam.fireDmgReduction) + '%')
        self.masterbuilder.get_object('lblWaterDR').config(text=  'Water Dmg Reduction: ' + str(self.destroyerTeam.waterDmgReduction) + '%')
        self.masterbuilder.get_object('lblWoodDR').config(text=  'Wood Dmg Reduction: ' + str(self.destroyerTeam.woodDmgReduction) + '%')
        self.masterbuilder.get_object('lblLightDR').config(text=  'Light Dmg Reduction: ' + str(self.destroyerTeam.lightDmgReduction) + '%')
        self.masterbuilder.get_object('lblDarkDR').config(text=  'Dark Dmg Reduction: ' + str(self.destroyerTeam.darkDmgReduction) + '%')

        return

class EditTeam():
    """Displays Edit Team Frame and Widgets"""
    def __init__(self, master):
        #Declare Global Variables
        self.leadMon = self.sub1 = self.sub2 = self.sub3 = self.sub4 = None
        buttons = []
        state = []
        monsterClassIDs = []
        myMonsterList = []
        self.var = IntVar(0)
        teamMonsterSelected = Radiobutton(text='', variable=self.var, value=0)
        self.master = master
        
        #Connect to Database
        self.PADsql = self.master.PADsql

        #Create GUI and add title image
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('src/ui/EditTeam.ui')
        self.mainwindow = builder.get_object('EditTeamFrame', master)    
        self.titleImg = tk.PhotoImage(file = 'Resource/PAD/Images/PADification Title.png')
        self.builder.get_object('titleImage').create_image(0,0, image =self.titleImg , anchor = tk.NW, tag = "pic")
        self.canvas = builder.get_object('canMonsterList')
        self.teamCanvas = builder.get_object('teamMonstersFrame')
        #Create TeamObject
        destroyerTeam = PADMonster.Team(self.PADsql)
        self.destroyerTeam = destroyerTeam
        self.updateTeamLabelImages()
        self.updateTeamLabels()
        
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
       

        if (len(self.canvas.grid_slaves()) // 2) * 30 > 500:
            pass
        else:
            self.canvas.config(height=1000) 
        
        self.builder.connect_callbacks(self)
        
    def populateCollection(self):
        self.PADsql = self.master.PADsql
        # JBM - Modifying collection to Dictionary from List to make Monster Lookup easier
        instanceIDs = []
        monster = self.PADsql.selectMonsterInstance()

        monsters = dict()
        for i in monster:
            monsters[i["InstanceID"]] = i
            instanceIDs.append(i["InstanceID"])
        self.instantList = instanceIDs
        self.myMonsterList = []

        #Creates the photoimage for each monster instance of the user and stores them in a list
        for i in self.instantList:
            myMonster = tk.PhotoImage(file = "Resource/PAD/Images/thumbnails/" + str(monsters[i]["MonsterClassID"]) + '.png')
            myMonster = myMonster.subsample(2)
            self.myMonsterList.append(myMonster)

        self.container = self.builder.get_object('canMonsterList')

        for i in self.container.grid_slaves():
            i.grid_forget()
        
        #Creates a graphical list of monsters
        buttons = []
        self.buttons = buttons = []
        self.count = 0
        for i in monsters:
            b = self.instantList[self.count]
            a = PADMonster.Monster(monsters[b])
            self.state = 'on'
                
            self.buttons.append(MonsterFrame(self.container, self.builder, self.count, self.instantList, a, self.buttons, self.PADsql, self.state, self.destroyerTeam, self.var))
            self.buttons[self.count].monbut.grid(row=self.count // 10,column = self.count % 10)
            self.buttons[self.count].builder.get_object('FrameLabel').create_image(2,2, image = self.myMonsterList[self.count], anchor = tk.NW)
            self.buttons[self.count].builder.get_object('lblMonsterBrief').config(text = 'LVL:' + str(a.Level)+ '\nID: ' + str(a.MonsterClassID))
            
            if self.destroyerTeam.LeaderMonster == b or self.destroyerTeam.SubMonsterOne == b or self.destroyerTeam.SubMonsterTwo== b or self.destroyerTeam.SubMonsterThree == b  or self.destroyerTeam.SubMonsterFour == b :
                self.buttons[self.count].state = 'off'
                self.buttons[self.count].monbut.config(relief=SUNKEN)
            if self.destroyerTeam.LeaderMonster == b:
                self.leadMon = self.count
            elif self.destroyerTeam.SubMonsterOne == b:
                self.sub1=self.count
            elif self.destroyerTeam.SubMonsterTwo== b:
                self.sub2=self.count
            elif self.destroyerTeam.SubMonsterThree == b:
                self.sub3=self.count
            elif self.destroyerTeam.SubMonsterFour == b:
                self.sub4=self.count
            self.count += 1
        self.container.config(height=(len(self.container.grid_slaves()) // 2) * 30)

    def loadTeam(self, instance):
        self.teamInstance = instance
        self.updateTeam(self.teamInstance)
        self.populateCollection()

    def updateTeam(self, i):
        self.myMonsterL = []
        self.destroyerTeam = i
        destroyerTeam = self.destroyerTeam
        for i in self.destroyerTeam.Monsters:
            if i.MonsterClassID != None:
                self.myMonsterL.append(tk.PhotoImage(file = 'Resource/PAD/Images/thumbnails/'+ str(i.MonsterClassID) + '.png'))
            else:
                self.myMonsterL.append(None)

        while len(self.myMonsterL) < 5:
            self.myMonsterL.append(None)
 
        if self.myMonsterL[0] != None:
            self.canLeadMon.create_image(7,7,image = self.myMonsterL[0], anchor = tk.NW, tag = "pic")
        if self.myMonsterL[1] != None:
            self.canSubMon1.create_image(7,7,image = self.myMonsterL[1], anchor = tk.NW, tag = "pic")
        if self.myMonsterL[2] != None:
            self.canSubMon2.create_image(7,7,image = self.myMonsterL[2], anchor = tk.NW, tag = "pic")
        if self.myMonsterL[3] != None:
            self.canSubMon3.create_image(7,7,image = self.myMonsterL[3], anchor = tk.NW, tag = "pic")
        if self.myMonsterL[4] != None:
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
        self.var.set(0)
        self.raiseTeam()
        self.canLeadMon.config(relief=SUNKEN)
        return

    def sub1Click(self, event):
        """Command invoked when sub monster 1 is selected"""
        self.var.set(1)
        self.raiseTeam()
        self.canSubMon1.config(relief=SUNKEN)
        return

    def sub2Click(self, event):
        """Command invoked when sub monster 2 is selected"""
        self.var.set(2)
        self.raiseTeam()
        self.canSubMon2.config(relief=SUNKEN)
        return

    def sub3Click(self, event):
        """Command invoked when sub monster 3 is selected"""
        self.var.set(3)
        self.raiseTeam()
        self.canSubMon3.config(relief=SUNKEN)
        return

    def sub4Click(self, event):
        """Command invoked when sub monster 4 is selected"""
        self.var.set(4)
        self.raiseTeam()
        self.canSubMon4.config(relief=SUNKEN)
        return
    
    def removeMonster(self, event):
        """Remove monsterfrom selected team slot"""
        #self.canLeadMon = self.builder.get_object('canLeadMon')
        #self.canSubMon1 = self.builder.get_object('canSubMon1')
        #self.canSubMon2 = self.builder.get_object('canSubMon2')
        #self.canSubMon3 = self.builder.get_object('canSubMon3')
        #self.canSubMon4 = self.builder.get_object('canSubMon4')

        if self.var.get() == 0:
            self.canLeadMon.delete('all')
            if self.destroyerTeam.LeaderMonster != self.destroyerTeam.setLeaderMonster():
                self.destroyerTeam.setLeaderMonster()
                self.buttons[self.leadMon].monbut.config(relief=FLAT)
                self.buttons[self.leadMon].state = 'on'
        elif self.var.get() == 1:
            self.canSubMon1.delete('all')
            if self.destroyerTeam.SubMonsterOne != self.destroyerTeam.setSubMonsterOne():
                self.destroyerTeam.setSubMonsterOne()
                self.buttons[self.sub1].monbut.config(relief=FLAT)
                self.buttons[self.sub1].state = 'on'
        elif self.var.get() == 2:
            self.canSubMon2.delete('all')
            if self.destroyerTeam.SubMonsterTwo != self.destroyerTeam.setSubMonsterTwo():
                self.destroyerTeam.setSubMonsterTwo()
                self.buttons[self.sub2].monbut.config(relief=FLAT)
                self.buttons[self.sub2].state = 'on'
        elif self.var.get() == 3:
            self.canSubMon3.delete('all')
            if self.destroyerTeam.SubMonsterThree != self.destroyerTeam.setSubMonsterThree():
                self.destroyerTeam.setSubMonsterThree()
                self.buttons[self.sub3].monbut.config(relief=FLAT)
                self.buttons[self.sub3].state = 'on'   
        elif self.var.get() == 4:
            self.canSubMon4.delete('all')
            if self.destroyerTeam.SubMonsterFour != self.destroyerTeam.setSubMonsterFour():
                self.destroyerTeam.setSubMonsterFour()
                self.buttons[self.sub4].monbut.config(relief=FLAT)
                self.buttons[self.sub4].state = 'on'
        self.updateTeamLabels()
        return

    def updateTeamLabels(self):
        """Updates team information labels"""
        self.builder.get_object('lblTeamHP').config(text=  'HP:    ' + str(self.destroyerTeam.TeamHP))
        self.builder.get_object('lblTeamCost').config(text='Cost: ' + str(self.destroyerTeam.TeamCost))
        self.builder.get_object('lblTeamRCV').config(text= 'RCV:  ' + str(self.destroyerTeam.TeamRCV))
        self.builder.get_object('lblFireATK').config(text= 'Fire ATK:     ' + str(self.destroyerTeam.FireATK))
        self.builder.get_object('lblWaterATK').config(text='Water ATK: ' + str(self.destroyerTeam.WaterATK))
        self.builder.get_object('lblWoodATK').config(text= 'Wood ATK: ' + str(self.destroyerTeam.WoodATK))
        self.builder.get_object('lblLightATK').config(text='Light ATK:   ' + str(self.destroyerTeam.LightATK))
        self.builder.get_object('lblDarkATK').config(text= 'Dark ATK:    ' + str(self.destroyerTeam.DarkATK))

        self.builder.get_object('lblSkillBindResist').config(text=  'Skill Bind Resist: ' + str(self.destroyerTeam.skillBindResist) + '%')
        self.builder.get_object('lblSkillBoost').config(text=   'Skill Boost: ' + str(self.destroyerTeam.skillBoost))
        self.builder.get_object('lblMoveTime').config(text=  'Move Time: ' + str(self.destroyerTeam.moveTime) + 's')
        self.builder.get_object('lblDarkResist').config(text=  'Dark Resist: ' + str(self.destroyerTeam.darkResist) + '%')
        self.builder.get_object('lblJammerResist').config(text=  'Jammer Resist: ' + str(self.destroyerTeam.jammerResist) + '%')
        self.builder.get_object('lblPoisonResist').config(text=  'Poison Resist: ' + str(self.destroyerTeam.poisonResist) + '%')
        self.builder.get_object('lblEnhancedFireChance').config(text=  'Enhanced Fire Chance: ' + str(self.destroyerTeam.enhancedFireChance) + '%')
        self.builder.get_object('lblEnhancedWaterChance').config(text=  'Enhanced Water Chance: ' + str(self.destroyerTeam.enhancedWaterChance) + '%')
        self.builder.get_object('lblEnhancedWoodChance').config(text=  'Enhanced Wood Chance: ' + str(self.destroyerTeam.enhancedWoodChance) + '%')
        self.builder.get_object('lblEnhancedLightChance').config(text=  'Enhanced Light Chance: ' + str(self.destroyerTeam.enhancedLightChance) + '%')
        self.builder.get_object('lblEnhancedDarkChance').config(text=  'Enhanced Dark Chance: ' + str(self.destroyerTeam.enhancedDarkChance) + '%')
        self.builder.get_object('lblEnhancedHealChance').config(text=  'Enhanced Heal Chance: ' + str(self.destroyerTeam.enhancedHealChance) + '%')
        self.builder.get_object('lblFireDR').config(text=  'Fire Dmg Reduction: ' + str(self.destroyerTeam.fireDmgReduction) + '%')
        self.builder.get_object('lblWaterDR').config(text=  'Water Dmg Reduction: ' + str(self.destroyerTeam.waterDmgReduction) + '%')
        self.builder.get_object('lblWoodDR').config(text=  'Wood Dmg Reduction: ' + str(self.destroyerTeam.woodDmgReduction) + '%')
        self.builder.get_object('lblLightDR').config(text=  'Light Dmg Reduction: ' + str(self.destroyerTeam.lightDmgReduction) + '%')
        self.builder.get_object('lblDarkDR').config(text=  'Dark Dmg Reduction: ' + str(self.destroyerTeam.darkDmgReduction) + '%')
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
        teamName = self.builder.get_variable('teamName').get()
        self.destroyerTeam.setTeamName(teamName)
        saveThisTeam = self.destroyerTeam.getSaveDict()
        saveThisTeam['Email'] = self.PADsql.Email
        self.PADsql.saveTeam(saveThisTeam)
        self.master.showTeamBrowser()

if __name__ == '__main__':
    root = tk.Tk()
    app = EditTeam(root)
    root.mainloop()

    #KyleTD