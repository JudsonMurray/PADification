#!/USR/BIN/ENV PYTHON 3.5
#   NAME:    KYLE GUNTON
#   DATE:    06/28/17
#   PURPOSE: FUNCTIONALITY FOR THE EDIT TEAM SCREEN 

#   -V. 0.0.1 -Created base functionality of selection monsters in player collection.
#   -V. 0.0.2 -Updated functionality of monster selection, added team slots, added remove monster
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
global leadMon
global sub1
global sub2
global sub3
global sub4

leadMon = -1
sub1 = -1
sub2 = -1
sub3 = -1
sub4 = -1

class MonsterFrame:
    def __init__(self, master, mastermaster, i):
        self.master = master
        self.mastermaster = mastermaster
        self.i = i
        self.builder = pygubu.Builder()
        self.builder.add_from_file('ui/PlayerCollection.ui')
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
        global monsterClassIDs, myMonsterList, connection, cursor, teamMonsterSelected, var
        global leadMon, sub1, sub2, sub3, sub4
        global myMonsters, destroyerTeam
        if state[self.i] == 'on':
            #Call globals to be used in method

            #global rowFull
            #global teamCanvasWidth 
            #global teamCanvasHeight 
        
            #Retrieves information from database and removes excess string content
            h = int(monsterClassIDs[self.i])
            sql = "Select MonsterName From MonsterClass where MonsterClassID = {}".format(h)
            y = cursor.execute(sql)
            monsterName = y.fetchall()
            monsterName = str(monsterName).replace("(", "")
            monsterName = monsterName.replace(",)", "")
            monsterName = monsterName.replace("[", "")
            monsterName = monsterName.replace("]", "")
            monsterName = monsterName.replace("\'", "")

            self.builder.add_from_file('ui/EditTeam.ui')

            data = range(60)
            
            h = myMonsters[self.i]
            if var.get() == 0:
                self.image = myMonsterList[self.i].zoom(10).subsample(7)
                self.canLeadMon.create_image(7, 7, image = self.image, anchor = tk.NW)
                buttons[leadMon].monbut.config(relief=RAISED)
                state[leadMon] = 'on'
                state[self.i] = 'off'
                leadMon = self.i
                destroyerTeam.setLeaderMonster(int(h))

            elif var.get() == 1:
                self.image = myMonsterList[self.i].zoom(10).subsample(7)
                self.canSubMon1.create_image(7, 7, image = self.image, anchor = tk.NW)
                buttons[sub1].monbut.config(relief=RAISED)
                state[sub1] = 'on'
                state[self.i] = 'off'
                sub1 = self.i
                destroyerTeam.setSubMonsterOne(int(h))

            elif var.get() == 2:
                self.image = myMonsterList[self.i].zoom(10).subsample(7)
                self.canSubMon2.create_image(7, 7, image = self.image, anchor = tk.NW)
                buttons[sub2].monbut.config(relief=RAISED)
                state[sub2] = 'on'
                state[self.i] = 'off'
                sub2 = self.i
                destroyerTeam.setSubMonsterTwo(int(h))

            elif var.get() == 3:
                self.image = myMonsterList[self.i].zoom(10).subsample(7)
                self.canSubMon3.create_image(7, 7, image = self.image, anchor = tk.NW)
                buttons[sub3].monbut.config(relief=RAISED)
                state[sub3] = 'on'
                state[self.i] = 'off'
                sub3 = self.i
                destroyerTeam.setSubMonsterThree(int(h))

            elif var.get() == 4:
                self.image = myMonsterList[self.i].zoom(10).subsample(7)
                self.canSubMon4.create_image(7, 7, image = self.image, anchor = tk.NW)
                buttons[sub4].monbut.config(relief=RAISED)
                state[sub4] = 'on'
                state[self.i] = 'off'
                sub4 = self.i
                destroyerTeam.setSubMonsterFour(int(h))

            buttons[self.i].monbut.config(relief=SUNKEN)
                
            self.updateTeamLabels()

    def updateTeamLabels(self):
        self.mastermaster.get_object('lblTeamHP').config(text='HP: ' + str(destroyerTeam.TeamHP))
        self.mastermaster.get_object('lblTeamCost').config(text='Cost: ' + str(destroyerTeam.TeamCost))
        self.mastermaster.get_object('lblTeamRCV').config(text='RCV: ' + str(destroyerTeam.TeamRCV))
        self.mastermaster.get_object('lblFireATK').config(text='Fire ATK: ' + str(destroyerTeam.FireATK))
        self.mastermaster.get_object('lblWaterATK').config(text='Water ATK: ' + str(destroyerTeam.WaterATK))
        self.mastermaster.get_object('lblWoodATK').config(text='Wood ATK: ' + str(destroyerTeam.WoodATK))
        self.mastermaster.get_object('lblLightATK').config(text='Light ATK: ' + str(destroyerTeam.LightATK))
        self.mastermaster.get_object('lblDarkATK').config(text='Dark ATK: ' + str(destroyerTeam.DarkATK))

class EditTeam():
    """Displays Edit Team Frame and Widgets"""
    def __init__(self, master):
        #Declare Global Variables
        global monsterClassIDs
        global myMonsterList
        global connection 
        global cursor
        global teamMonsterSelected
        global state
        global myMonsters
        global destroyerTeam
        global var
        state = []
        monsterClassIDs = []
        myMonsterList = []
        var = IntVar(0)
        teamMonsterSelected = Radiobutton(text='', variable=var, value=0)
        
        PADsql = PADSQL.PADSQL()

        #Connect to Database
        PADsql.connect()
        cursor = PADsql.cursor
        connection = PADsql.connection

        #Retrieves monster Instance IDs from database
        sql = "SELECT InstanceID FROM monsterInstance WHERE Username = 'PADTest'"
        playerTable = cursor.execute(sql)
        myMonsters = playerTable.fetchall()
        connection.commit()

        #PADification APP signup/login
        #PADsql.signup(['PADTest','PADTest','A@a.ap',100000000])
        PADsql.login('PADTest','PADTest')
        self.master = master
        #Create GUI and add title image
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('ui/EditTeam.ui')
        self.mainwindow = builder.get_object('EditTeamFrame', master)    
        self.titleImg = tk.PhotoImage(file = 'C:/Users/kyleg/Documents/Visual Studio 2015/SWTS1102/Home Screen/PADification Title.png')
        self.builder.get_object('titleImage').create_image(0,0, image =self.titleImg , anchor = tk.NW, tag = "pic")
        self.canvas = builder.get_object('canMonsterCollection')
        self.teamCanvas = builder.get_object('Frame_1')
        self.recoveryImg = tk.PhotoImage(file='RCVSymbol.png') 
        self.fireImg = tk.PhotoImage(file='FireSymbol.png')
        self.waterImg = tk.PhotoImage(file='WaterSymbol.png')
        self.woodImg = tk.PhotoImage(file='WoodSymbol.png')
        self.lightImg = tk.PhotoImage(file='LightSymbol.png') 
        self.darkImg = tk.PhotoImage(file='DarkSymbol.png') 
        self.builder.get_object('recoveryImg').config(image=self.recoveryImg) 
        self.builder.get_object('fireImg').config(image=self.fireImg) 
        self.builder.get_object('waterImg').config(image=self.waterImg)
        self.builder.get_object('woodImg').config(image=self.woodImg)
        self.builder.get_object('lightImg').config(image=self.lightImg)
        self.builder.get_object('darkImg').config(image=self.darkImg)
        #for i in range (0,500):
        #    leadMonster = PADMonster.Monster(PADsql.selectMonsterClass(393)[0])
        #    leadMonster.setCurrentExperience(4000000)

        #    leadMonster.setPlusATK(99)
        #    leadMonster.setPlusHP(99)
        #    leadMonster.setPlusRCV(99)
        #    leadMonster.setSkillsAwoke(6)


        #    PADsql.saveMonster(leadMonster.getSaveDict())

        #Create TeamObject
        destroyerTeam = PADMonster.Team(PADsql)

        x=0
        #Populates lists with monsterIDs
        for i in range(0,len(myMonsters)):
            myMonsters[i] = str(myMonsters[i]).replace("(", "")
            myMonsters[i] = str(myMonsters[i]).replace(",)", "")
                    
            PADsql.selectMonsterInstance(myMonsters[i])
            sql = "SELECT MonsterClassID FROM monsterInstance WHERE InstanceID = {}".format(myMonsters[i])
            
            myMonster = cursor.execute(sql)
            myMonster = myMonster.fetchone()
            myMonster = str(myMonster).replace("(", "")
            monsterClass = myMonster.replace(",)", "")
            monsterClassIDs += monsterClass,
            myMonster= tk.PhotoImage(file = 'thumbnails/'+ str(monsterClass) + '.png').zoom(15)
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
        global buttons
        buttons = []
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

    def leadClick(self, event):
        """Command invoked when leader monster is selected"""
        global var
        var.set(0)
        self.canLeadMon.config(relief=SUNKEN)
        self.canSubMon1.config(relief=RAISED)
        self.canSubMon2.config(relief=RAISED)
        self.canSubMon3.config(relief=RAISED)
        self.canSubMon4.config(relief=RAISED)
        return

    def sub1Click(self, event):
        """Command invoked when sub monster 1 is selected"""
        global var
        var.set(1)
        self.canLeadMon.config(relief=RAISED)
        self.canSubMon1.config(relief=SUNKEN)
        self.canSubMon2.config(relief=RAISED)
        self.canSubMon3.config(relief=RAISED)
        self.canSubMon4.config(relief=RAISED)
        return

    def sub2Click(self, event):
        """Command invoked when sub monster 2 is selected"""
        global var
        var.set(2)
        self.canLeadMon.config(relief=RAISED)
        self.canSubMon1.config(relief=RAISED)
        self.canSubMon2.config(relief=SUNKEN)
        self.canSubMon3.config(relief=RAISED)
        self.canSubMon4.config(relief=RAISED)
        return

    def sub3Click(self, event):
        """Command invoked when sub monster 3 is selected"""
        global var
        var.set(3)
        self.canLeadMon.config(relief=RAISED)
        self.canSubMon1.config(relief=RAISED)
        self.canSubMon2.config(relief=RAISED)
        self.canSubMon3.config(relief=SUNKEN)
        self.canSubMon4.config(relief=RAISED)
        return

    def sub4Click(self, event):
        """Command invoked when sub monster 4 is selected"""
        global var
        var.set(4)
        self.canLeadMon.config(relief=RAISED)
        self.canSubMon1.config(relief=RAISED)
        self.canSubMon2.config(relief=RAISED)
        self.canSubMon3.config(relief=RAISED)
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
                buttons[leadMon].monbut.config(relief=RAISED)
                state[leadMon] = 'on'

        elif var.get() == 1:
            self.canSubMon1.delete('all')
            if destroyerTeam.SubMonsterOne != destroyerTeam.setSubMonsterOne():
                destroyerTeam.setSubMonsterOne()
                buttons[sub1].monbut.config(relief=RAISED)
                state[sub1] = 'on'

        elif var.get() == 2:
            self.canSubMon2.delete('all')
            if destroyerTeam.SubMonsterTwo != destroyerTeam.setSubMonsterTwo():
                destroyerTeam.setSubMonsterTwo()
                buttons[sub2].monbut.config(relief=RAISED)
                state[sub2] = 'on'

        elif var.get() == 3:
            self.canSubMon3.delete('all')
            if destroyerTeam.SubMonsterThree != destroyerTeam.setSubMonsterThree():
                destroyerTeam.setSubMonsterThree()
                buttons[sub3].monbut.config(relief=RAISED)
                state[sub3] = 'on'   

        elif var.get() == 4:
            self.canSubMon4.delete('all')
            if destroyerTeam.SubMonsterFour != destroyerTeam.setSubMonsterFour():
                destroyerTeam.setSubMonsterFour()
                buttons[sub4].monbut.config(relief=RAISED)
                state[sub4] = 'on'

        self.updateTeamLabels()
        return

    def updateTeamLabels(self):
        """Updates team information labels"""
        x = destroyerTeam.TeamHP
        self.builder.get_object('lblTeamHP').config(text='HP: ' + str(destroyerTeam.TeamHP))
        self.builder.get_object('lblTeamCost').config(text='Cost: ' + str(destroyerTeam.TeamCost))
        self.builder.get_object('lblTeamRCV').config(text='RCV: ' + str(destroyerTeam.TeamRCV))
        self.builder.get_object('lblFireATK').config(text='Fire ATK: ' + str(destroyerTeam.FireATK))
        self.builder.get_object('lblWaterATK').config(text='Water ATK: ' + str(destroyerTeam.WaterATK))
        self.builder.get_object('lblWoodATK').config(text='Wood ATK: ' + str(destroyerTeam.WoodATK))
        self.builder.get_object('lblLightATK').config(text='Light ATK: ' + str(destroyerTeam.LightATK))
        self.builder.get_object('lblDarkATK').config(text='Dark ATK: ' + str(destroyerTeam.DarkATK))
        return

if __name__ == '__main__':
    root = tk.Tk()
    app = EditTeam(root)
    root.mainloop()