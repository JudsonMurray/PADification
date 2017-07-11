#!/USR/BIN/ENV PYTHON 3.5
#   NAME:    KYLE GUNTON
#   DATE:    07/02/17
#   PURPOSE: FUNCTIONALITY FOR THE BROWSE TEAM SCREEN 


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
class TeamBrowser():
    """Displays Edit Team Frame and Widgets"""
    def __init__(self, master):
        #Declare Global Variables
        self.buttons = []
        self.state = []
        self.monsterClassIDs = []
        self.myMonsterList = []
        self.var = IntVar(0)
        self.teamMonsterSelected = Radiobutton(text='', variable=self.var, value=0)

        #Variables
        self.PADsql = master.PADsql
        self.master = master
        self.SelectedTeam = PADMonster.Team(self.PADsql)

        #Create GUI and add title image
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('src/ui/Team Browser.ui')
        self.mainwindow = builder.get_object('teamBrowserFrame', master)    
        self.titleImg = tk.PhotoImage(file = 'Resource/PAD/Images/PADification Title.png')
        self.builder.get_object('titleImage').create_image(0,0, image =self.titleImg , anchor = tk.NW, tag = "pic")
        self.teamCanvas = builder.get_object('teamMonstersFrame')
        self.builder.connect_callbacks(self)

        #Widgets to access
        self.teamListBox = self.builder.get_object('teamListBox')
        self.canLeadMon = self.builder.get_object('canLeadMon')
        self.canSubMon1 = self.builder.get_object('canSubMon1')
        self.canSubMon2 = self.builder.get_object('canSubMon2')
        self.canSubMon3 = self.builder.get_object('canSubMon3')
        self.canSubMon4 = self.builder.get_object('canSubMon4')

        #sets permanent images
        
        
        
    def loadUserTeams(self):
        self.connection = self.PADsql.connection
        teams = self.PADsql.selectTeamInstance()

        if len(teams) == 0:
            self.teamListBox.delete(0, END)
            self.setImages(None)
            self.updateTeamLabels(self.builder)
            return
        else:
            destroyerTeamBase = self.PADsql.selectTeamInstance(teams[0]['TeamInstanceID'])
            self.SelectedTeam = PADMonster.Team(self.PADsql)
            self.teamListBox.delete(0, END)
        
            for i in range(0,len(teams)):
                qq = str(teams[i]['TeamInstanceID'])
                self.teamListBox.insert(END, str(teams[i]['TeamName']) + '                                                            ' + qq)
        
            self.teamListBox.bind("<ButtonRelease-1>", self.teamSelect)
            teamID = self.teamListBox.get(ANCHOR)
            if teamID == '': 
                teamID = self.teamListBox.get(0)
            teamID = teamID[-6:]
            self.updateTeam(int(teamID))
            self.setImages(None)
            self.newteam = self.builder.get_object('btnNewTeam')
            return

    def newTeam(self, event):
        """Show Login Screen"""
        self.master.editTeam.loadTeam(PADMonster.Team(self.PADsql))
        self.master.showEditTeamScreen()

    def btnEditTeam(self, event):
        self.master.editTeam.loadTeam(self.SelectedTeam)
        self.master.showEditTeamScreen()

    def teamSelect(self, event):
        if self.teamListBox.isEmpty():
            return
        teamID = self.teamListBox.get(ANCHOR)
        if teamID == '': 
            teamID = self.teamListBox.get(0)
        teamID = teamID[-6:]
        self.updateTeam(int(teamID))

    def updateTeam(self, i):
        self.SelectedTeam = PADMonster.Team(self.PADsql, self.PADsql.selectTeamInstance(int(i))[0])

        self.monsterClassIDs = []
        self.myMonsterList = []

        for i in self.SelectedTeam.Monsters:
            if i != None:
                self.myMonsterList.append(tk.PhotoImage(file = 'Resource/PAD/Images/thumbnails/'+ str(i.MonsterClassID) + '.png'))
            else:
                self.myMonsterList.append(None)
        while len(self.myMonsterList) < 5:
            self.myMonsterList.append(None)
        self.updateTeamLabels(self.builder)

    def updateTeamLabels(self, build):
        """Updates team information labels"""
        self.SelectedTeam.update()
        self.thisBuild = build
        self.canLeadMon.delete('ALL')
        self.canSubMon1.delete('ALL')
        self.canSubMon2.delete('ALL')
        self.canSubMon3.delete('ALL')
        self.canSubMon4.delete('ALL')
        self.myMonsterL = []

        i = 0
        if self.SelectedTeam.LeaderMonster != None:
            self.myMonsterL.append(tk.PhotoImage(file = 'Resource/PAD/Images/thumbnails/'+ str(self.SelectedTeam.Monsters[i].MonsterClassID) + '.png'))
            i+= 1
        else:
            self.myMonsterL.append(None)

        if self.SelectedTeam.SubMonsterOne != None:
            self.myMonsterL.append(tk.PhotoImage(file = 'Resource/PAD/Images/thumbnails/'+ str(self.SelectedTeam.Monsters[i].MonsterClassID) + '.png'))
            i+= 1
        else:
            self.myMonsterL.append(None)
        if self.SelectedTeam.SubMonsterTwo != None:
            self.myMonsterL.append(tk.PhotoImage(file = 'Resource/PAD/Images/thumbnails/'+ str(self.SelectedTeam.Monsters[i].MonsterClassID) + '.png'))
            i+= 1
        else:
            self.myMonsterL.append(None)
        if self.SelectedTeam.SubMonsterThree != None:
            self.myMonsterL.append(tk.PhotoImage(file = 'Resource/PAD/Images/thumbnails/'+ str(self.SelectedTeam.Monsters[i].MonsterClassID) + '.png'))
            i+= 1
        else:
            self.myMonsterL.append(None)
        if self.SelectedTeam.SubMonsterFour != None:
            self.myMonsterL.append(tk.PhotoImage(file = 'Resource/PAD/Images/thumbnails/'+ str(self.SelectedTeam.Monsters[i].MonsterClassID) + '.png'))
            i+= 1
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


        self.thisBuild.get_object('lblTeamName').config(text='Team Name: ' + str(self.SelectedTeam.TeamName))
        self.thisBuild.get_object('lblTeamHP').config(text=  'HP:    ' + str(self.SelectedTeam.TeamHP))
        self.thisBuild.get_object('lblTeamCost').config(text='Cost: ' + str(self.SelectedTeam.TeamCost))
        self.thisBuild.get_object('lblTeamRCV').config(text= 'RCV:  ' + str(self.SelectedTeam.TeamRCV))
        self.thisBuild.get_object('lblFireATK').config(text= 'Fire ATK:     ' + str(self.SelectedTeam.FireATK))
        self.thisBuild.get_object('lblWaterATK').config(text='Water ATK: ' + str(self.SelectedTeam.WaterATK))
        self.thisBuild.get_object('lblWoodATK').config(text= 'Wood ATK: ' + str(self.SelectedTeam.WoodATK))
        self.thisBuild.get_object('lblLightATK').config(text='Light ATK:   ' + str(self.SelectedTeam.LightATK))
        self.thisBuild.get_object('lblDarkATK').config(text= 'Dark ATK:    ' + str(self.SelectedTeam.DarkATK))
        self.thisBuild.get_object('lblSkillBindResist').config(text=  'Skill Bind Resist: ' + str(self.SelectedTeam.skillBindResist) + '%')
        self.thisBuild.get_object('lblSkillBoost').config(text=   'Skill Boost: ' + str(self.SelectedTeam.skillBoost))
        self.thisBuild.get_object('lblMoveTime').config(text=  'Move Time: ' + str(self.SelectedTeam.moveTime) + 's')
        self.thisBuild.get_object('lblDarkResist').config(text=  'Dark Resist: ' + str(self.SelectedTeam.darkResist) + '%')
        self.thisBuild.get_object('lblJammerResist').config(text=  'Jammer Resist: ' + str(self.SelectedTeam.jammerResist) + '%')
        self.thisBuild.get_object('lblPoisonResist').config(text=  'Poison Resist: ' + str(self.SelectedTeam.poisonResist) + '%')
        self.thisBuild.get_object('lblEnhancedFireChance').config(text=  'Enhanced Fire Chance: ' + str(self.SelectedTeam.enhancedFireChance) + '%')
        self.thisBuild.get_object('lblEnhancedWaterChance').config(text=  'Enhanced Water Chance: ' + str(self.SelectedTeam.enhancedWaterChance) + '%')
        self.thisBuild.get_object('lblEnhancedWoodChance').config(text=  'Enhanced Wood Chance: ' + str(self.SelectedTeam.enhancedWoodChance) + '%')
        self.thisBuild.get_object('lblEnhancedLightChance').config(text=  'Enhanced Light Chance: ' + str(self.SelectedTeam.enhancedLightChance) + '%')
        self.thisBuild.get_object('lblEnhancedDarkChance').config(text=  'Enhanced Dark Chance: ' + str(self.SelectedTeam.enhancedDarkChance) + '%')
        self.thisBuild.get_object('lblEnhancedHealChance').config(text=  'Enhanced Heal Chance: ' + str(self.SelectedTeam.enhancedHealChance) + '%')
        self.thisBuild.get_object('lblFireDR').config(text=  'Fire Dmg Reduction: ' + str(self.SelectedTeam.fireDmgReduction) + '%')
        self.thisBuild.get_object('lblWaterDR').config(text=  'Water Dmg Reduction: ' + str(self.SelectedTeam.waterDmgReduction) + '%')
        self.thisBuild.get_object('lblWoodDR').config(text=  'Wood Dmg Reduction: ' + str(self.SelectedTeam.woodDmgReduction) + '%')
        self.thisBuild.get_object('lblLightDR').config(text=  'Light Dmg Reduction: ' + str(self.SelectedTeam.lightDmgReduction) + '%')
        self.thisBuild.get_object('lblDarkDR').config(text=  'Dark Dmg Reduction: ' + str(self.SelectedTeam.darkDmgReduction) + '%')
        return

    def onHomeClick(self, event):
        self.master.showHomeScreen()
        
    def onMonsterBookClick(self):
        self.master.showMonsterBook()

    def onAccountOptionsClick(self):
        """Occurs When Account Options Button Is Clicked"""
        self.master.showAccountOptions()

    def onMonsterBookClick(self, event):
        self.master.showMonsterBook()

    def onMyMonstersClick(self):
        self.master.showPlayerCollection()

    def onMyTeamsClick(self, event):
        self.master.showTeamBrowser()

    def removeTeam(self,event):
        self.PADsql.deleteTeam(self.SelectedTeam.TeamInstanceID)
        self.teamListBox.delete(ANCHOR)
        self.loadUserTeams()

    def setImages(self, build):
        """Set Images"""
        if build != None:
            self.thisBuild = build
        else:
           self.thisBuild = self.builder
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

        self.thisBuild.get_object('hpImg').config(image=self.recoveryImg) 
        self.thisBuild.get_object('recoveryImg').config(image=self.recoveryImg) 
        self.thisBuild.get_object('fireImg').config(image=self.fireImg) 
        self.thisBuild.get_object('waterImg').config(image=self.waterImg)
        self.thisBuild.get_object('woodImg').config(image=self.woodImg)
        self.thisBuild.get_object('lightImg').config(image=self.lightImg)
        self.thisBuild.get_object('darkImg').config(image=self.darkImg)
        self.thisBuild.get_object('skillBindResistImg').config(image=self.skillBindResistImg)
        self.thisBuild.get_object('fireDRImg').config(image=self.fireDmgReductionImg)
        self.thisBuild.get_object('waterDRImg').config(image=self.waterDmgReductionImg)
        self.thisBuild.get_object('woodDRImg').config(image=self.woodDmgReductionImg)
        self.thisBuild.get_object('lightDRImg').config(image=self.lightDmgReductionImg)
        self.thisBuild.get_object('darkDRImg').config(image=self.darkDmgReductionImg)
        self.thisBuild.get_object('darkResistImg').config(image=self.darkResistImg)
        self.thisBuild.get_object('jammerResistImg').config(image=self.jammerResistImg)
        self.thisBuild.get_object('poisonResistImg').config(image=self.poisonResistImg)
        self.thisBuild.get_object('enhancedFireChanceImg').config(image=self.enhancedFireChanceImg)
        self.thisBuild.get_object('enhancedWaterChanceImg').config(image=self.enhancedWaterChanceImg)
        self.thisBuild.get_object('enhancedWoodChanceImg').config(image=self.enhancedWoodChanceImg)
        self.thisBuild.get_object('enhancedLightChanceImg').config(image=self.enhancedLightChanceImg)
        self.thisBuild.get_object('enhancedDarkChanceImg').config(image=self.enhancedDarkChanceImg)
        self.thisBuild.get_object('enhancedHealChanceImg').config(image=self.enhancedHealChanceImg)
        self.thisBuild.get_object('moveTimeImg').config(image=self.moveTimeImg)
        self.thisBuild.get_object('skillBoostImg').config(image=self.skillBoostImg)
#if __name__ == '__main__':
#    root = tk.Tk()
#    app = TeamBrowser(root)
#    root.mainloop()