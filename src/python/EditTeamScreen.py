#!/USR/BIN/ENV PYTHON 3.5
#   NAME:    KYLE GUNTON
#   DATE:    07/11/17
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

class AwokenBadge:
    def __init__(self, master, masterframe, builder, i):
        self.builder = builder
        self.master= master
        self.masterframe = masterframe
        self.i = i
        self.builder = pygubu.Builder() 
        self.builder.add_from_file('src/ui/EditTeam.ui')
        self.badgebut = self.builder.get_object('AwokenBadgeFrame', self.masterframe)
        self.image = self.builder.get_object('canAwokenBadge', self.builder.get_object('AwokenBadgeFrame'))

        self.badgebut.bind("<Button-1>", self.awokenBadgeClick)
        self.image.bind("<Button-1>", self.awokenBadgeClick)

    def awokenBadgeClick(self, event):
        self.master.setBadge = self.master.awokenBadges[self.i]
        self.master.badgeNum = self.i
        for i in self.master.awokenBadgeLabels:
            i.badgebut.config(relief=FLAT)
        self.badgebut.config(relief=SUNKEN)
        return

class BadgeFrame(tk.Toplevel):
    def __init__(self, master, masterbuilder, team):
        tk.Toplevel.__init__(self, master)
        self.masterbuilder = masterbuilder
        self.destroyerTeam = team
        self.builder = pygubu.Builder()
        self.builder.add_from_file('src/ui/EditTeam.ui')
        self.mainwidow = self.builder.get_object('frmBadges', self)

        self.badgeNum = None

        # set the dimensions of the screen 
        # and where it is placed
        self.transient(master) #set to be on top of the main window
        self.grab_set() #hijack all commands from the master (clicks on the main window are ignored)
        self.awokenBadges = self.master.PADsql.getAwokenBadges()
        self.setBadge = ''
        self.awokenBadgeImages = []
        self.awokenBadgeLabels = []
        for i in range(0, len(self.awokenBadges)):
            self.awokenBadgeImages.append(tk.PhotoImage(file = 'Resource/PAD/Images/Badges/'+ str(self.awokenBadges[i]).replace("/", '') + '.png'))
            self.awokenBadgeLabels.append(AwokenBadge(self, self.builder.get_object('frmBadges'), self.builder, i))
            self.awokenBadgeLabels[i].badgebut.grid(row=i // 7,column = i % 7)
            self.awokenBadgeLabels[i].image.create_image(7,7,image = self.awokenBadgeImages[i], anchor = tk.NW, tag = "pic")

            w = 490 #width for the Tk root
            h = 190 # height for the Tk root

            # get screen width and height
            ws = self.winfo_screenwidth() # width of the screen
            hs = self.winfo_screenheight() # height of the screen

            # calculate x and y coordinates for the Tk root window
            x = (ws/2) - (w/2)
            y = (hs/2) - (h/2)

            self.geometry('%dx%d+%d+%d' % (w,h, x, y))

        self.builder.get_object('okBadge').bind('<Button-1>', self.okBadge)
        self.builder.connect_callbacks(self)
        return

    def okBadge(self, event):
        self.destroyerTeam.setBadge(self.setBadge)
        if self.badgeNum != None:
            self.masterbuilder.get_object('lblAwokenBadge').config(image = self.awokenBadgeImages[self.badgeNum])
        self.destroy()
        return



class MonsterFrame:
    def __init__(self, master, masterbuilder, i, ids, currentMonster, buttons, padsql, state, team, var, padific):
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
        self.padific= padific
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
            self.image = tk.PhotoImage(file = "resource/PAD/Images/Thumbnails/" + str(self.currentMonster.MonsterClassID) + '.png').zoom(5).subsample(7)
            if self.var.get() == 0:
                self.canLeadMon.create_image(7, 7, image = self.image, anchor = tk.NW)
                self.leadMon = self.i
                self.destroyerTeam.setLeaderMonster(int(h))
            elif self.var.get() == 1:
                self.canSubMon1.create_image(7, 7, image = self.image, anchor = tk.NW)
                self.sub1 = self.i
                self.destroyerTeam.setSubMonsterOne(int(h))
            elif self.var.get() == 2:
                self.canSubMon2.create_image(7, 7, image = self.image, anchor = tk.NW)
                self.sub2 = self.i
                self.destroyerTeam.setSubMonsterTwo(int(h))
            elif self.var.get() == 3:
                self.canSubMon3.create_image(7, 7, image = self.image, anchor = tk.NW)
                self.sub3 = self.i
                self.destroyerTeam.setSubMonsterThree(int(h))
            elif self.var.get() == 4:
                self.canSubMon4.create_image(7, 7, image = self.image, anchor = tk.NW)
                self.sub4 = self.i
                self.destroyerTeam.setSubMonsterFour(int(h))

            for t in self.buttons:
                t.monbut.config(relief=FLAT)
                t.state = 'on'
                if t.currentMonster.InstanceID == self.destroyerTeam.LeaderMonster or\
                    t.currentMonster.InstanceID == self.destroyerTeam.SubMonsterOne or\
                    t.currentMonster.InstanceID == self.destroyerTeam.SubMonsterTwo or\
                    t.currentMonster.InstanceID == self.destroyerTeam.SubMonsterThree or\
                    t.currentMonster.InstanceID == self.destroyerTeam.SubMonsterFour:
                    t.state = 'off'
                    t.monbut.config(relief=SUNKEN)
            #self.padific.teamBrowser.setImages(self.masterbuilder)
            self.padific.teamBrowser.updateTeamLabels(self.masterbuilder, self.destroyerTeam)
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
        #self.master.teamBrowser.setImages(self.builder)
        #self.master.teamBrowser.updateTeamLabels(self.builder, self.destroyerTeam)
        
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
        self.page = 1
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
        self.pages = len(monsters) // 50 + 1
        if len(monsters) % 50 == 0:
            self.pages -=1
        
        self.builder.get_variable('lblCurPage').set(('Page' + str(self.page) + '/' + str(self.pages)))
        if self.page > self.pages:
            self.prev()
        if self.page == self.pages:
            self.builder.get_object('btnNext').config(state=DISABLED)
        else:
            self.builder.get_object('btnNext').config(state=NORMAL)
        if self.page == 1:
            self.builder.get_object('btnPrev').config(state=DISABLED)
        else:
            self.builder.get_object('btnPrev').config(state=NORMAL)


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
        self.count = 0 + (self.page - 1) * 50
        #if self.count % 50 == 0 and self.count != 0:
        #    self.count -=1
        tt = range(0 + (self.page - 1) * 50, (50 + (self.page - 1) * 50) if len(monsters) - 1 > (50 + (self.page - 1) * 50) else len(monsters))
        for i in range(0 + (self.page - 1) * 50, (50 + (self.page - 1) * 50) if len(monsters) - 1 > (50 + (self.page - 1) * 50) else len(monsters)):
            #print(self.count)
            b = self.instantList[self.count]
            a = PADMonster.Monster(monsters[b])
            self.state = 'on'
                
            self.buttons.append(MonsterFrame(self.container, self.builder, self.count, self.instantList, a, self.buttons, self.PADsql, self.state, self.destroyerTeam, self.var, self.master))
            self.buttons[self.count % 50].monbut.config(width=65)
            self.buttons[self.count % 50].monbut.grid(row=self.count // 10,column = self.count % 10)
            self.buttons[self.count % 50].builder.get_object('FrameLabel').create_image(2,2, image = self.myMonsterList[self.count], anchor = tk.NW)
            self.buttons[self.count % 50].builder.get_object('lblMonsterBrief').config(text = 'LVL:' + str(a.Level)+ '\nID: ' + str(a.MonsterClassID))
            
            if self.destroyerTeam.LeaderMonster == b or self.destroyerTeam.SubMonsterOne == b or\
                self.destroyerTeam.SubMonsterTwo== b or self.destroyerTeam.SubMonsterThree == b or\
                self.destroyerTeam.SubMonsterFour == b :
                self.buttons[self.count % 50].state = 'off'
                self.buttons[self.count % 50].monbut.config(relief=SUNKEN)
            self.count += 1
        self.container.config(height=(len(self.container.grid_slaves()) // 2) * 30)

    def loadTeam(self, instance):
        self.teamInstance = instance
        self.updateTeam(self.teamInstance)
        self.populateCollection()

    def updateTeam(self, i):
        self.myMonsterL = []
        self.destroyerTeam = i
        self.canLeadMon.delete('all')
        self.canSubMon1.delete('all')
        self.canSubMon2.delete('all')
        self.canSubMon3.delete('all')
        self.canSubMon4.delete('all')
        i = 0
        if self.destroyerTeam.LeaderMonster != None:
            self.myMonsterL.append(tk.PhotoImage(file = 'Resource/PAD/Images/thumbnails/'+ str(self.destroyerTeam.Monsters[i].MonsterClassID) + '.png').zoom(5).subsample(7))
            i+= 1
        else:
            self.myMonsterL.append(None)
        if self.destroyerTeam.SubMonsterOne != None:
            self.myMonsterL.append(tk.PhotoImage(file = 'Resource/PAD/Images/thumbnails/'+ str(self.destroyerTeam.Monsters[i].MonsterClassID) + '.png').zoom(5).subsample(7))
            i+= 1
        else:
            self.myMonsterL.append(None)
        if self.destroyerTeam.SubMonsterTwo != None:
            self.myMonsterL.append(tk.PhotoImage(file = 'Resource/PAD/Images/thumbnails/'+ str(self.destroyerTeam.Monsters[i].MonsterClassID) + '.png').zoom(5).subsample(7))
            i+= 1
        else:
            self.myMonsterL.append(None)
        if self.destroyerTeam.SubMonsterThree != None:
            self.myMonsterL.append(tk.PhotoImage(file = 'Resource/PAD/Images/thumbnails/'+ str(self.destroyerTeam.Monsters[i].MonsterClassID) + '.png').zoom(5).subsample(7))
            i+= 1
        else:
            self.myMonsterL.append(None)
        if self.destroyerTeam.SubMonsterFour != None:
            self.myMonsterL.append(tk.PhotoImage(file = 'Resource/PAD/Images/thumbnails/'+ str(self.destroyerTeam.Monsters[i].MonsterClassID) + '.png').zoom(5).subsample(7))
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


        self.builder.get_variable('teamName').set(self.destroyerTeam.TeamName)
        self.master.teamBrowser.setImages(self.builder)
        self.master.teamBrowser.updateTeamLabels(self.builder, self.destroyerTeam)

    def next(self):
        self.page +=1
        self.populateCollection()

    def prev(self):
        self.page -=1
        self.populateCollection()

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
        if self.var.get() == 0:
            self.canLeadMon.delete('all')
            if self.destroyerTeam.LeaderMonster != self.destroyerTeam.setLeaderMonster():
                self.destroyerTeam.setLeaderMonster()
        elif self.var.get() == 1:
            self.canSubMon1.delete('all')
            if self.destroyerTeam.SubMonsterOne != self.destroyerTeam.setSubMonsterOne():
                self.destroyerTeam.setSubMonsterOne()
        elif self.var.get() == 2:   
            self.canSubMon2.delete('all')
            if self.destroyerTeam.SubMonsterTwo != self.destroyerTeam.setSubMonsterTwo():
                self.destroyerTeam.setSubMonsterTwo()
        elif self.var.get() == 3:
            self.canSubMon3.delete('all')
            if self.destroyerTeam.SubMonsterThree != self.destroyerTeam.setSubMonsterThree():
                self.destroyerTeam.setSubMonsterThree()
        elif self.var.get() == 4:
            self.canSubMon4.delete('all')
            if self.destroyerTeam.SubMonsterFour != self.destroyerTeam.setSubMonsterFour():
                self.destroyerTeam.setSubMonsterFour()
        for t in self.buttons:
            t.monbut.config(relief=FLAT)
            t.state = 'on'
            if t.currentMonster.InstanceID == self.destroyerTeam.LeaderMonster or\
                t.currentMonster.InstanceID == self.destroyerTeam.SubMonsterOne or\
                t.currentMonster.InstanceID == self.destroyerTeam.SubMonsterTwo or\
                t.currentMonster.InstanceID == self.destroyerTeam.SubMonsterThree or\
                t.currentMonster.InstanceID == self.destroyerTeam.SubMonsterFour:
                t.state = 'off'
                t.monbut.config(relief=SUNKEN)
        
        self.master.teamBrowser.updateTeamLabels(self.builder, self.destroyerTeam)
        return

    def selectBadge(self, event):
        """opens Select Badge Frame"""
        inputDialog = BadgeFrame(self.master, self.builder, self.destroyerTeam)
        pass

    def cancelTeamEdit(self, event):
        self.master.showTeamBrowser()
        return

    def saveTeam(self, event):
        """Save team instance"""
        teamName = self.builder.get_variable('teamName').get()
        if len(teamName) > 20:

            return
        x=1
        teamName = teamName.lstrip()
        for i in self.master.teamBrowser.teamListBox.get(0,END):
            if i[0:4] == "Team" and i[5:20].strip(' ') == str(x):
                x+=1
        if teamName == '':
            teamName = "Team " + str(x)
        self.destroyerTeam.setTeamName(teamName)
        if self.destroyerTeam.AwokenBadgeName == 'No Badge':
            self.destroyerTeam.setBadge('')
        elif self.destroyerTeam.AwokenBadgeName != 'No Badge' and self.destroyerTeam.AwokenBadgeName != None:
            self.destroyerTeam.setBadge(str(self.destroyerTeam.AwokenBadgeName))
        saveThisTeam = self.destroyerTeam.getSaveDict()
        saveThisTeam['Email'] = self.PADsql.Email
        self.PADsql.saveTeam(saveThisTeam)
        self.master.showTeamBrowser()

if __name__ == '__main__':
    root = tk.Tk()
    app = EditTeam(root)
    root.mainloop()

    #KyleTD