#!/USR/BIN/ENV PYTHON 3.5
#   NAME:    KYLE GUNTON
#   DATE:    07/14/17
#   PURPOSE: FUNCTIONALITY FOR THE BROWSE TEAM SCREEN 


import pygame
import tkinter as tk
from CustomWidgets import *
import pygubu
from tkinter import messagebox
from tkinter import *
import tkinter as tk
import pypyodbc
import sys
import PADSQL
import PADMonster
from PIL import Image, ImageFont, ImageDraw, ImageTk

#variables to tell which monsters are selected within the collection
class TeamBrowser():
    """Displays Edit Team Frame and Widgets"""
    def __init__(self, master):
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
        self.teamCanvas = [self.builder.get_object('canLeadMon'), 
                            self.builder.get_object('canSubMon1'),
                            self.builder.get_object('canSubMon2'), 
                            self.builder.get_object('canSubMon3'),
                            self.builder.get_object('canSubMon4')]
        self.teamMonsters = [self.SelectedTeam.LeaderMonster,
                             self.SelectedTeam.SubMonsterOne,
                             self.SelectedTeam.SubMonsterTwo,
                             self.SelectedTeam.SubMonsterThree,
                             self.SelectedTeam.SubMonsterFour]
        return

    def loadUserTeams(self):
        """Loads Teams into listbox"""
        self.connection = self.PADsql.connection
        self.teams = self.PADsql.selectTeamInstance()

        self.setImages(None)
        if len(self.teams) == 0:
            self.teamListBox.delete(0, END)
            self.updateTeamLabels(self.builder, PADMonster.Team(self.PADsql))
            self.thisBuild.get_object('lblTeamName').config(text='Not A Team')
            self.builder.get_object('btnEditTeam').config(state=DISABLED)
            self.builder.get_object('btnRemoveTeam').config(state=DISABLED)
            return
        else:
            destroyerTeamBase = self.PADsql.selectTeamInstance(self.teams[0]['TeamInstanceID'])
            self.SelectedTeam = PADMonster.Team(self.PADsql)
            self.teamListBox.delete(0, END)

            #Sort teams by name
            sorted = False
            while not sorted:
                yt = 0
                for i in range(0,len(self.teams)-1):
                    if str(self.teams[i]['TeamName'])[0:4] == "Team" and ((self.teams[i]['TeamName'])[5:20].strip(' ')).isdigit() and \
                        str(self.teams[i+1]['TeamName'])[0:4] == "Team" and ((self.teams[i]['TeamName'])[5:20].strip(' ')).isdigit():
                        if int((self.teams[i]['TeamName'])[5:20].strip(' ')) > int((self.teams[i+1]['TeamName'])[5:20].strip(' ')):
                            self.teams[i], self.teams[i + 1] = self.teams[i + 1], self.teams[i]
                            continue 
                    yt+=1
                if yt >= len(self.teams)-1:
                    sorted = True

            #insert teams into listbox
            for i in range(0,len(self.teams)):
                qq = str(self.teams[i]['TeamInstanceID'])
                self.teamListBox.insert(END, str(self.teams[i]['TeamName']) + '                                                            ' + qq)
            
            self.teamSelect(self)
            self.builder.get_object('btnEditTeam').config(state=NORMAL)
            self.builder.get_object('btnRemoveTeam').config(state=NORMAL)
            return

    def teamSelect(self, event):
        """Selects team from listbox"""
        if self.teamListBox.get(0) == '':
            self.updateTeam((0))
            return
        if self.teamListBox.get(ANCHOR) == '':
             self.teamListBox.selection_anchor(0)
        teamID = self.teamListBox.get(ANCHOR)
        if teamID == '':
            teamID = self.teamListBox.get(0)
        teamID = teamID[-10:].strip(' ')
        self.updateTeam(int(teamID))

    def updateTeam(self, i):
        """Updates Team Selected"""
        self.SelectedTeam = PADMonster.Team(self.PADsql) if i == 0 else PADMonster.Team(self.PADsql, self.PADsql.selectTeamInstance(int(i))[0])
        self.myMonsterList = []

        for i in self.SelectedTeam.Monsters:
            self.myMonsterList.append(ImageTk.PhotoImage(file = 'Resource/PAD/Images/thumbnails/'+ str(i.MonsterClassID) + '.png')) if i != None else self.myMonsterList.append(None)

        self.updateTeamLabels(self.builder, self.SelectedTeam)
        return

    def updateTeamLabels(self, build,team):
        """Updates team information labels"""
        self.SelectedTeam = team
        self.thisBuild = build
        self.SelectedTeam.update()
        self.teamMonsters = [self.SelectedTeam.LeaderMonster,
                             self.SelectedTeam.SubMonsterOne,
                             self.SelectedTeam.SubMonsterTwo,
                             self.SelectedTeam.SubMonsterThree,
                             self.SelectedTeam.SubMonsterFour]
        self.myMonsterL = []
        teamCanvas = [self.thisBuild.get_object('canLeadMon'), 
                            self.thisBuild.get_object('canSubMon1'),
                            self.thisBuild.get_object('canSubMon2'), 
                            self.thisBuild.get_object('canSubMon3'),
                            self.thisBuild.get_object('canSubMon4')]
        for i in teamCanvas:
            i.delete('ALL')
        i = 0
        j=0
        ww= int(teamCanvas[i].winfo_width())
        wh= int(teamCanvas[i].winfo_height())
        while i < 5:
            if self.teamMonsters[i] != None:
                self.fp = 'Resource/PAD/Images/thumbnails/'+ str(self.SelectedTeam.Monsters[j].MonsterClassID) + '.png'
                self.img = Image.open(self.fp).resize((ww-14,wh-14))
                self.myMonsterL.append(ImageTk.PhotoImage(self.img))
                j+=1
            else:
                self.myMonsterL.append(None)
            i += 1
        j = 0
        for i in range(0,5):
            if self.myMonsterL[i] != None:
                teamCanvas[i].create_image(7,7,image = self.myMonsterL[i], anchor = tk.NW, tag = "pic")
                MonsterStatTooltip(teamCanvas[i]).update(self.SelectedTeam.Monsters[j])
                j+=1
            else:
                MonsterStatTooltip(teamCanvas[i]).update()
                


        if build == self.builder:
            self.builder.get_object('lblTeamName').config(text='' + str(self.SelectedTeam.TeamName))

        if self.SelectedTeam.AwokenBadgeName == None:
            self.SelectedTeam.AwokenBadgeName = 'No Badge'

        self.AwokenBadgeImage = tk.PhotoImage(file = 'Resource/PAD/Images/Badges/'+ str(self.SelectedTeam.AwokenBadgeName).replace('/', '') + '.png')

        if len(self.SelectedTeam.Monsters) != 0 and self.SelectedTeam.Monsters[0].InstanceID == self.SelectedTeam.LeaderMonster and self.SelectedTeam.Monsters[0].LeaderSkillName != None:
            leaderskilldesc =  str(self.master.PADsql.getLeaderSkillDesc(self.SelectedTeam.Monsters[0].LeaderSkillName))
            count = 0
            spaces = []
            spacepos = 0
            self.range = 130
            while len(leaderskilldesc) > self.range:
                for i in str(leaderskilldesc[self.range - 130 : self.range]):
                    if i == ' ':
                        spaces.append(count)
                        spacepos = spaces[len(spaces) - 1]
                    count += 1

                leaderskilldesc = leaderskilldesc[0:spacepos] + '\n' + leaderskilldesc[spacepos + 1:]
                self.range += 130
            if len(leaderskilldesc) // 130 < 1:
                leaderskilldesc += '\n' * 3
            elif len(leaderskilldesc) // 260 < 1:
                leaderskilldesc += '\n' * 2
            elif len(leaderskilldesc) // 390 < 1:
                leaderskilldesc += '\n' * 1

            self.builder.get_object('lblLeaderSkill').config(text = "Leader Skill: " + self.SelectedTeam.Monsters[0].LeaderSkillName + '\n' + leaderskilldesc)
        else:
            self.builder.get_object('lblLeaderSkill').config(text = "Leader Skill: None"  + '\n' * 4)

        self.thisBuild.get_object('lblAwokenBadge').config(image = self.AwokenBadgeImage, anchor = CENTER)
        self.thisBuild.get_object('lblTeamHP').config(text=  'HP:    ' + str(self.SelectedTeam.TeamHP))
        self.thisBuild.get_object('lblTeamCost').config(text='Cost: ' + str(self.SelectedTeam.TeamCost))
        self.thisBuild.get_object('lblTeamRCV').config(text= 'RCV:  ' + str(self.SelectedTeam.TeamRCV))
        self.thisBuild.get_object('lblFireATK').config(text= 'Fire ATK:     ' + str(self.SelectedTeam.FireATK))
        self.thisBuild.get_object('lblWaterATK').config(text='Water ATK: ' + str(self.SelectedTeam.WaterATK))
        self.thisBuild.get_object('lblWoodATK').config(text= 'Wood ATK: ' + str(self.SelectedTeam.WoodATK))
        self.thisBuild.get_object('lblLightATK').config(text='Light ATK:   ' + str(self.SelectedTeam.LightATK))
        self.thisBuild.get_object('lblDarkATK').config(text= 'Dark ATK:    ' + str(self.SelectedTeam.DarkATK))
        self.thisBuild.get_object('lblSkillBindResist').config(text=  'Skill Bind Resist: ' + str(self.SelectedTeam.skillBindResist) + '%')
        self.thisBuild.get_object('lblSkillBoost').config(text=  'Skill Boost: ' + str(self.SelectedTeam.skillBoost))
        self.thisBuild.get_object('lblMoveTime').config(text=    'Move Time: ' + str(self.SelectedTeam.moveTime) + 's')
        self.thisBuild.get_object('lblDarkResist').config(text=  'Dark Resist: ' + str(self.SelectedTeam.darkResist) + '%')
        self.thisBuild.get_object('lblJammerResist').config(text='Jammer Resist: ' + str(self.SelectedTeam.jammerResist) + '%')
        self.thisBuild.get_object('lblPoisonResist').config(text='Poison Resist: ' + str(self.SelectedTeam.poisonResist) + '%')
        self.thisBuild.get_object('lblEnhancedFireChance').config(text=  'Enhanced Fire Chance: ' + str(self.SelectedTeam.enhancedFireChance) + '%')
        self.thisBuild.get_object('lblEnhancedWaterChance').config(text= 'Enhanced Water Chance: ' + str(self.SelectedTeam.enhancedWaterChance) + '%')
        self.thisBuild.get_object('lblEnhancedWoodChance').config(text=  'Enhanced Wood Chance: ' + str(self.SelectedTeam.enhancedWoodChance) + '%')
        self.thisBuild.get_object('lblEnhancedLightChance').config(text= 'Enhanced Light Chance: ' + str(self.SelectedTeam.enhancedLightChance) + '%')
        self.thisBuild.get_object('lblEnhancedDarkChance').config(text=  'Enhanced Dark Chance: ' + str(self.SelectedTeam.enhancedDarkChance) + '%')
        self.thisBuild.get_object('lblEnhancedHealChance').config(text=  'Enhanced Heal Chance: ' + str(self.SelectedTeam.enhancedHealChance) + '%')
        self.thisBuild.get_object('lblFireDR').config(text=  'Fire Dmg Reduction: ' + str(self.SelectedTeam.fireDmgReduction) + '%')
        self.thisBuild.get_object('lblWaterDR').config(text= 'Water Dmg Reduction: ' + str(self.SelectedTeam.waterDmgReduction) + '%')
        self.thisBuild.get_object('lblWoodDR').config(text=  'Wood Dmg Reduction: ' + str(self.SelectedTeam.woodDmgReduction) + '%')
        self.thisBuild.get_object('lblLightDR').config(text= 'Light Dmg Reduction: ' + str(self.SelectedTeam.lightDmgReduction) + '%')
        self.thisBuild.get_object('lblDarkDR').config(text=  'Dark Dmg Reduction: ' + str(self.SelectedTeam.darkDmgReduction) + '%')
        return

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
        return

    def newTeam(self, event):
        """Show Edit Team Screen with new team setup"""
        self.master.editTeam.loadTeam(PADMonster.Team(self.PADsql))
        self.master.showEditTeamScreen()
        return

    def btnEditTeam(self):
        """Show Edit Team Screen with selected team setup"""
        self.master.editTeam.loadTeam(self.SelectedTeam)
        self.master.showEditTeamScreen()
        return

    def removeTeam(self):
        """Removes selected team from the listbox as well as the database"""
        if self.teamListBox.get(ANCHOR) != '':
            self.PADsql.deleteTeam(self.SelectedTeam.TeamInstanceID)
            self.teamListBox.delete(ANCHOR)
            self.teamSelect(self)
            
        if len(self.teams) == 0:
            self.teamListBox.delete(0, END)
            self.updateTeamLabels(self.builder, PADMonster.Team(self.PADsql))
            self.thisBuild.get_object('lblTeamName').config(text='Not A Team')
            self.builder.get_object('btnEditTeam').config(state=DISABLED)
            self.builder.get_object('btnRemoveTeam').config(state=DISABLED)
            return
        return

    def onHomeClick(self, event):
        self.master.showHomeScreen()
        return

    def onCollectionClick(self, event):
        self.master.showPlayerCollection()
        return

    def onBookClick(self, EVENT):
        self.master.showMonsterBook()
        return

    def onTeamsClick(self, event):
        self.master.showTeamBrowser()
        return

    def onCommunityClick(self, event):
        #self.master.showCommunity()
        return

    def onTeamRankingClick(self, event):
        #self.master.showTeamRanking()
        return

    def onOptionsClick(self, EVENT):
        """Occurs When Account Options Button Is Clicked"""
        self.master.showAccountOptions()
        return