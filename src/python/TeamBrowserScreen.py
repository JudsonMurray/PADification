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
global leadMon, sub1, sub2, sub3, sub4
leadMon = sub1 = sub2 = sub3 = sub4 = None

class TeamBrowser():
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
        self.PADsql.login('KyleTD','KyleTD')

        sql = ("SELECT TeamInstanceID FROM team WHERE Username = {}").format("'"+self.PADsql.Username+"'")
        team = cursor.execute(sql)
        teamID = team.fetchall()
        #Retrieves monster Instance IDs from database
        sql = "SELECT LeaderMonster, SubMonsterOne ,SubMonsterTwo, SubMonsterThree, SubMonsterFour FROM team WHERE TeamInstanceID = {}".format(teamID[0][0])
        playerTable = cursor.execute(sql)
        myMonsters = playerTable.fetchall()
        connection.commit()
        
        destroyerTeamBase = self.PADsql.selectTeamInstance(teamID[0][0])
        destroyerTeam = PADMonster.Team(self.PADsql)
        
        #PADification APP signup/login
        #self.PADsql.signup(['PADTest','PADTest','A@a.ap',100000000])
        self.master = master
        #Create GUI and add title image
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('src/ui/Team Browser.ui')
        self.mainwindow = builder.get_object('teamBrowserFrame', master)    
        self.titleImg = tk.PhotoImage(file = 'Resource/PAD/Images/PADification Title.png')
        self.builder.get_object('titleImage').create_image(0,0, image =self.titleImg , anchor = tk.NW, tag = "pic")
        self.teamCanvas = builder.get_object('teamMonstersFrame')
        x=0

        #Populates lists with monsterIDs
        self.teamListBox = builder.get_object('teamListBox')

        for i in range(0,len(teamID)):
            qq = str(teamID[i][0])
            self.teamListBox.insert(END, qq)
        
        self.updateTeam(int(self.teamListBox.get(0)))
        self.teamListBox.bind("<ButtonRelease-1>", self.teamSelect)
        self.builder.connect_callbacks(self)

    def newTeam(self, event):
        """Show Login Screen"""
        self.master.showEditTeamScreen(None)

    def btnEditTeam(self, event):
        edit = self.master.editTeam
        edit.loadTeam(destroyerTeam.TeamInstanceID)
        self.master.showEditTeamScreen(destroyerTeam.TeamInstanceID)

    def teamSelect(self, event):
        teamID = self.teamListBox.get(ANCHOR)
        if teamID == '': 
            teamID = self.teamListBox.get(0)
        self.updateTeam(int(teamID))
        print('s')

    def updateTeam(self, i):
        global myMonsters
        global monsterClassIDs
        destroyerTeam.TeamInstanceID = i
        sql = "SELECT LeaderMonster, SubMonsterOne ,SubMonsterTwo, SubMonsterThree, SubMonsterFour FROM team WHERE TeamInstanceID = {}".format(str(i))
        playerTable = cursor.execute(sql)
        myMonsters = playerTable.fetchall()

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
        monsterClassIDs = []
        global myMonsterList
        myMonsterList = []

        for i in myMonsters[0]:
            
            if i != None:
                sql = "SELECT MonsterClassID FROM monsterInstance WHERE InstanceID = {}".format(i)
            
                myMonster = cursor.execute(sql)
                myMonster = myMonster.fetchone()
                myMonster = str(myMonster).replace("(", "")
                monsterClass = myMonster.replace(",)", "")
                monsterClassIDs += monsterClass,
                myMonster= tk.PhotoImage(file = 'Resource/PAD/Images/thumbnails/'+ str(monsterClass) + '.png')
            else:
                myMonster = None
            myMonsterList.append(myMonster)
        self.updateTeamLabels()

    def updateTeamLabels(self):
        """Updates team information labels"""
        destroyerTeam.update()
        self.canLeadMon = self.builder.get_object('canLeadMon')
        self.canSubMon1 = self.builder.get_object('canSubMon1')
        self.canSubMon2 = self.builder.get_object('canSubMon2')
        self.canSubMon3 = self.builder.get_object('canSubMon3')
        self.canSubMon4 = self.builder.get_object('canSubMon4')
        self.canLeadMon.delete('pic')
        self.canSubMon1.delete('pic')
        self.canSubMon2.delete('pic')
        self.canSubMon3.delete('pic')
        self.canSubMon4.delete('pic')

        self.canLeadMon.create_image(7,7,image = myMonsterList[0], anchor = tk.NW, tag = "pic")
        self.canSubMon1.create_image(7,7,image = myMonsterList[1], anchor = tk.NW, tag = "pic")
        self.canSubMon2.create_image(7,7,image = myMonsterList[2], anchor = tk.NW, tag = "pic")
        self.canSubMon3.create_image(7,7,image = myMonsterList[3], anchor = tk.NW, tag = "pic")
        self.canSubMon4.create_image(7,7,image = myMonsterList[4], anchor = tk.NW, tag = "pic")

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

if __name__ == '__main__':
    root = tk.Tk()
    app = TeamBrowser(root)
    root.mainloop()