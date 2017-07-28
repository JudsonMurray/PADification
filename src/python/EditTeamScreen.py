#!/USR/BIN/ENV PYTHON 3.5
#   NAME:    KYLE GUNTON
#   DATE:    07/28/17
#   PURPOSE: FUNCTIONALITY FOR THE EDIT TEAM SCREEN 

#   -V. 0.0.1 -Created base functionality of selection monsters in player collection.
#   -V. 0.0.2 -Updated functionality of monster selection, added team slots, added remove monster
#   -V. 0.0.3 -Updated Screen display, updated File Paths
#   -V. 0.0.4 -Added functionality billy overwrote. Fixed multiple selection of one monster.
#   -V. 0.0.5 -Made many miscellaneous bug fixes
import logging
import pygame
import tkinter as tk
import pygubu
from CustomWidgets import *
from tkinter import messagebox
from tkinter import *
import tkinter as tk
import pypyodbc
import sys
import PADSQL
import PADMonster
from PADMonster import Monster
from ast import literal_eval as le

#variables to tell which monsters are selected within the collection

class AwokenBadge:
    def __init__(self, master, masterframe, builder, i):
        self.logger = logging.getLogger("Padification.ui.EditTeamScreen.AwokenBadge")
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
        self.logger = logging.getLogger("Padification.ui.EditTeamScreen.BadgeFrame")
        self.master = master
        self.masterbuilder = masterbuilder
        self.destroyerTeam = team
        self.builder = pygubu.Builder()
        self.builder.add_from_file('src/ui/EditTeam.ui')
        self.mainwidow = self.builder.get_object('frmBadges', self)

        self.badgeNum = None
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
            ToolTip.ToolTip(self.awokenBadgeLabels[i].image, str(self.awokenBadges[i]))

            w = 490 #width for the Tk root
            h = 190 # height for the Tk root
            ws = self.winfo_screenwidth() # width of the screen
            hs = self.winfo_screenheight() # height of the screen
            # calculate x and y coordinates for the Tk root window
            x = (ws/2) - (w/2)
            y = (hs/2) - (h/2)
            self.geometry('%dx%d+%d+%d' % (w,h, x, y))

        self.awokenBadgeImages.append(tk.PhotoImage(file = 'Resource/PAD/Images/Badges/No Badge.png'))
        if self.master.editTeam.badgeNum != None:
            self.masterbuilder.get_object('lblAwokenBadge').config(image = self.awokenBadgeImages[self.master.editTeam.badgeNum])
        #self.builder.get_object('okBadge').bind('<Button-1>', self.okBadge)
        self.builder.connect_callbacks(self)
        return

    def okBadge(self, event):
        if self.badgeNum != None:
            self.master.editTeam.badgeNum = self.badgeNum
            self.destroyerTeam.setBadge(self.setBadge)
            self.masterbuilder.get_object('lblAwokenBadge').config(image = self.awokenBadgeImages[self.badgeNum])
            self.destroy()
            ToolTip.ToolTip(self.masterbuilder.get_object("lblAwokenBadge"), str(self.setBadge))
            return
        tk.messagebox.showwarning("No Badge Selected", "Please select a badge before confirming.")
        return

    def cancelAwokenBadgeChanges(self, event):
        self.destroy()
        return

class MonsterFrame:
    def __init__(self, master, masterbuilder, i, currentMonster, buttons, padsql, state, team, var, padific):
        self.logger = logging.getLogger("Padification.ui.EditTeamScreen.MonsterFrame")
        self.destroyerTeam = team
        self.master = master
        self.masterbuilder = masterbuilder
        self.i = i
        self.builder = pygubu.Builder()
        self.builder.add_from_file('src/ui/PlayerCollection.ui')
        self.monbut = self.builder.get_object('MonsFrame', self.master)
        self.builder.connect_callbacks(self)
        #self.ids = ids
        self.currentMonster = currentMonster
        self.buttons = buttons
        self.padsql = padsql
        self.state = state
        self.var = var
        self.padific= padific
        #Adds monster collection buttons to monster collection
        self.teamCanvas = self.padific.editTeam.teamCanvas

    def clickMe(self, event):
        '''Method for selection of a monster in the player collection'''
        if self.state == 'on':   #Only executes if a monster is not already in use
            #Retrieves information from database and removes excess string content
            self.builder.add_from_file('src/ui/EditTeam.ui')
            h = self.currentMonster.InstanceID
            self.image = tk.PhotoImage(file = "resource/PAD/Images/Thumbnails/" + str(self.currentMonster.MonsterClassID) + '.png').zoom(5).subsample(7)
            if self.var.get() == 0:
                self.destroyerTeam.setLeaderMonster(int(h))
            elif self.var.get() == 1:
                self.destroyerTeam.setSubMonsterOne(int(h))
            elif self.var.get() == 2:
                self.destroyerTeam.setSubMonsterTwo(int(h))
            elif self.var.get() == 3:
                self.destroyerTeam.setSubMonsterThree(int(h))
            elif self.var.get() == 4:
                self.destroyerTeam.setSubMonsterFour(int(h))
            self.teamCanvas[self.var.get()].create_image(7, 7, image = self.image, anchor = tk.NW)

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
                    
            self.teamCanvas[self.var.get()].config(highlightbackground= "#f0f0f0",highlightcolor="#f0f0f0",highlightthickness=5)
            for c in self.padific.editTeam.assistants:
                if c == self.destroyerTeam.LeaderMonster:
                    self.teamCanvas[0].config(highlightbackground= "#b2a89d",highlightcolor="#b2a89d",highlightthickness=5)
                elif c == self.destroyerTeam.SubMonsterOne:
                    self.teamCanvas[1].config(highlightbackground= "#b2a89d",highlightcolor="#b2a89d",highlightthickness=5)
                elif c == self.destroyerTeam.SubMonsterTwo:
                    self.teamCanvas[2].config(highlightbackground= "#b2a89d",highlightcolor="#b2a89d",highlightthickness=5)
                elif c == self.destroyerTeam.SubMonsterThree:
                    self.teamCanvas[3].config(highlightbackground= "#b2a89d",highlightcolor="#b2a89d",highlightthickness=5)
                elif c == self.destroyerTeam.SubMonsterFour:
                    self.teamCanvas[4].config(highlightbackground= "#b2a89d",highlightcolor="#b2a89d",highlightthickness=5)
            self.padific.teamBrowser.updateTeamLabels(self.masterbuilder, self.destroyerTeam)
            return

class EditTeam():
    """Displays Edit Team Frame and Widgets"""
    def __init__(self, master):
        #logger
        self.logger = logging.getLogger("Padification.ui.EditTeamScreen.EditTeam")
        #Declare Global Variables
        self.leadMon = self.sub1 = self.sub2 = self.sub3 = self.sub4 = None
        buttons = []
        state = []
        monsterClassIDs = []
        self.myMonsterList = []
        self.var = IntVar(0)
        self.master = master
        self.bgSearchText = "Enter Monster ID or Name"
        #Connect to Database
        self.PADsql = self.master.PADsql
        self.MonsterResults = None
        #Create GUI
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('src/ui/EditTeam.ui')
        self.mainwindow = builder.get_object('EditTeamFrame', master)    
        self.canvas = builder.get_object('canMonsterList')
        self.teamCanvas = builder.get_object('teamMonstersFrame')
        #Create TeamObject
        destroyerTeam = PADMonster.Team(self.PADsql)
        self.destroyerTeam = destroyerTeam
        self.imgTitleImage = PhotoImage(file = "Resource/PAD/Images/Padification Logo.png")
        self.builder.get_object('lblTitleImage').config(image = self.imgTitleImage)
        self.teamCanvas = [self.builder.get_object('canLeadMon'),
                           self.builder.get_object('canSubMon1'),
                           self.builder.get_object('canSubMon2'),
                           self.builder.get_object('canSubMon3'),
                           self.builder.get_object('canSubMon4')]

        self.teamCanvas[0].config(relief=SUNKEN)

        b = len(self.myMonsterList)
        self.page = 1        
        self.builder.connect_callbacks(self)
        
    def populateCollection(self, filter = None):
        """Populate Users Monsters from their Monster Collection into buttons"""
        self.PADsql = self.master.PADsql
        instanceIDs = []
        self.filter = filter
        if filter == None:
            monster = self.PADsql.selectMonsterInstance(wishlist = self.dreamteam)
        else:
            monster = filter
        allMonsters = self.PADsql.selectMonsterInstance(wishlist = self.dreamteam)
        self.count = 0
        pops = []
        self.assistants = []
        for i in range(0,len(monster)):
            for y in allMonsters:
                if filter == None:
                    if monster[i]["InstanceID"] == y["AssistMonsterID"]:
                        self.assistants.append(y["InstanceID"])
                        pops.append(i)
                        break
                elif monster[i].InstanceID == y["AssistMonsterID"]:
                        self.assistants.append(y["InstanceID"])
                        pops.append(i)
                        break
                self.count += 1
        for i in pops[::-1]:
            monster.pop(i)

        monsters = dict()
        self.myMonsterList = []
        
        ToolTip.ToolTip(self.builder.get_object("lblAwokenBadge"), self.destroyerTeam.AwokenBadgeName)
        #configures pages to match collection size
        self.pages = len(monster) // 50 + 1
        if len(monster) % 50 == 0:
            self.pages -=1
        if self.pages == 0:
            self.pages = 1
        
        self.builder.get_variable('lblPageNumber').set(('   /' + str(self.pages)))
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
        self.builder.get_variable('varPageEnt').set((self.page))


        #Creates the photoimage for each monster instance of the user and stores them in a list
        for i in range(0, len(monster)):
            if filter == None:
                y = int(monster[i]["MonsterClassID"])
            else:
                y = int(monster[i].MonsterClassID)
            self.myMonster = tk.PhotoImage(file = "Resource/PAD/Images/thumbnails/" + str(y) + '.png')
            self.myMonster = self.myMonster.subsample(2)
            self.myMonsterList.append(self.myMonster)

        self.container = self.builder.get_object('canMonsterList')

        for i in self.container.grid_slaves():
            i.grid_forget()

        #Creates a graphical list of monsters
        buttons = []
        self.buttons = buttons = []
        self.count = 0
        tt = range(0 + (self.page - 1) * 50, (50 + (self.page - 1) * 50) if len(monster) - 1 > (50 + (self.page - 1) * 50) else len(monster))
        for i in range(0 + (self.page - 1) * 50, (50 + (self.page - 1) * 50) if len(monster) - 1 > (50 + (self.page - 1) * 50) else len(monster)):
            if filter == None:
                b = monster[i]["InstanceID"]
                thisdict = monster[i]
            else:
                b = monster[i].InstanceID
                thisdict = self.PADsql.selectMonsterInstance(b, wishlist = self.dreamteam)[0]
                
            a = PADMonster.Monster(thisdict)
            self.state = 'on'

            self.buttons.append(MonsterFrame(self.container, self.builder, self.count, a, self.buttons, self.PADsql, self.state, self.destroyerTeam, self.var, self.master))
            self.buttons[self.count].monbut.config(width=69)
            self.buttons[self.count].monbut.grid(row=self.count // 10,column = self.count % 10)
            self.buttons[self.count].builder.get_object('FrameLabel').create_image(2,2, image = self.myMonsterList[self.count+ (self.page - 1) * 50], anchor = tk.NW)
            self.buttons[self.count].builder.get_object('lblMonsterBrief').config(text = 'LVL:' + str(a.Level)+ '\nID: ' + str(a.MonsterClassID))
            for c in self.assistants:
                if c == self.buttons[self.count].currentMonster.InstanceID:
                    self.buttons[self.count].monbut.config(highlightbackground= "#b2a89d",highlightcolor="#b2a89d",highlightthickness=3)
                    break
                else:
                    self.buttons[self.count].monbut.config(highlightbackground= None,highlightcolor=None,highlightthickness=3)

            if self.destroyerTeam.LeaderMonster == b or self.destroyerTeam.SubMonsterOne == b or\
                self.destroyerTeam.SubMonsterTwo== b or self.destroyerTeam.SubMonsterThree == b or\
                self.destroyerTeam.SubMonsterFour == b :
                self.buttons[self.count].state = 'off'
                self.buttons[self.count].monbut.config(relief=SUNKEN)
            self.count += 1 
        self.container.config(height=(len(self.container.grid_slaves()) // 2) * 30)

    def loadTeam(self, instance, dreamteam = 0):
        """Loads user's team and calls methods to pupulate feilds"""
        self.dreamteam = dreamteam
        self.badgeNum = None
        self.master.updateProfile(self.builder)
        self.leadClick(self)
        self.teamInstance = instance
        self.updateTeam(self.teamInstance)
        self.populateCollection()
        self.AttributeImages = dict()

                    #### ATTRIBUTE IMAGES #####
        for i in ["Fire","Water","Wood","Light","Dark"]:
            self.AttributeImages[i] = PhotoImage(file = 'Resource/PAD/Images/Attributes/' + i + "Symbol.png")
            self.builder.get_object("chkPri" + i).config(image = self.AttributeImages[i])
            ToolTip.ToolTip(self.builder.get_object("chkPri" + i) , i)
            self.builder.get_object("chkSec" + i).config(image = self.AttributeImages[i])
            ToolTip.ToolTip(self.builder.get_object("chkSec" + i) , i)
                    ##### TYPE IMAGES #####
        self.TypeImages = dict()
        for i in ["Attacker", "Awaken Material", "Balanced", "Devil", "Dragon", "Enhance Material",
                  "Evo Material", "God", "Healer", "Machine", "Physical", "Redeemable Material" ]:
            self.TypeImages[i] = PhotoImage(file = 'Resource/PAD/Images/Types/' + i + ".png")
            self.builder.get_object("chkType" + i.replace(" ", "")).config(image = self.TypeImages[i])
            ToolTip.ToolTip(self.builder.get_object("chkType" + i.replace(" ", "")) , i)

    def updateTeam(self, team):
        """"Updates team information"""
        self.myMonsterL = []
        self.destroyerTeam = team
        self.destroyerTeam.setDreamState(self.dreamteam)
        for i in range(0,5):
            self.teamCanvas[i].delete('all')
        self.builder.get_variable('teamName').set(self.destroyerTeam.TeamName)
        self.master.teamBrowser.setImages(self.builder)
        self.master.teamBrowser.updateTeamLabels(self.builder, self.destroyerTeam)

    def next(self):
        """Load next page of monsters"""
        self.page +=1
        if self.filter is not None:
            self.populateCollection(self.filter)
        else:
           self.populateCollection()

    def prev(self):
        """Load prev page of monsters"""
        self.page -=1
        if self.filter is not None:
            self.populateCollection(self.filter)
        else:
            self.populateCollection()

    def raiseTeam(self):
        """returns team selection to raised relief"""
        for i in range(0,5):
            self.teamCanvas[i].config(relief=RAISED)
        return

    def leadClick(self, event):
        """Command invoked when leader monster is selected"""
        self.var.set(0)
        self.raiseTeam()
        self.teamCanvas[0].config(relief=SUNKEN)
        return

    def sub1Click(self, event):
        """Command invoked when sub monster 1 is selected"""
        self.var.set(1)
        self.raiseTeam()
        self.teamCanvas[1].config(relief=SUNKEN)
        return

    def sub2Click(self, event):
        """Command invoked when sub monster 2 is selected"""
        self.var.set(2)
        self.raiseTeam()
        self.teamCanvas[2].config(relief=SUNKEN)
        return

    def sub3Click(self, event):
        """Command invoked when sub monster 3 is selected"""
        self.var.set(3)
        self.raiseTeam()
        self.teamCanvas[3].config(relief=SUNKEN)
        return

    def sub4Click(self, event):
        """Command invoked when sub monster 4 is selected"""
        self.var.set(4)
        self.raiseTeam()
        self.teamCanvas[4].config(relief=SUNKEN)
        return
    
    def removeMonster(self, event):
        """Remove monsterfrom selected team slot"""
        
        self.teamCanvas[self.var.get()].config(highlightbackground= "#f0f0f0",highlightcolor="#f0f0f0",highlightthickness=5)
        if self.var.get() == 0:
            if self.destroyerTeam.LeaderMonster != self.destroyerTeam.setLeaderMonster():
                self.destroyerTeam.setLeaderMonster()
        elif self.var.get() == 1:
            if self.destroyerTeam.SubMonsterOne != self.destroyerTeam.setSubMonsterOne():
                self.destroyerTeam.setSubMonsterOne()
        elif self.var.get() == 2:   
            if self.destroyerTeam.SubMonsterTwo != self.destroyerTeam.setSubMonsterTwo():
                self.destroyerTeam.setSubMonsterTwo()
        elif self.var.get() == 3:
            if self.destroyerTeam.SubMonsterThree != self.destroyerTeam.setSubMonsterThree():
                self.destroyerTeam.setSubMonsterThree()
        elif self.var.get() == 4:
            if self.destroyerTeam.SubMonsterFour != self.destroyerTeam.setSubMonsterFour():
                self.destroyerTeam.setSubMonsterFour()
        self.teamCanvas[self.var.get()].delete('all')
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
        return

    def cancelTeamEdit(self, event):
        """Discard changes made to team and return to Team Browser Screen"""
        self.master.showTeamBrowser()
        return

    def saveTeam(self, event):
        """Save team instance"""
        teamName = self.builder.get_variable('teamName').get()
        if len(teamName) > 20:
            tk.messagebox.showinfo("Too Long", "The Name you have entered is too long! \nPlease enter a name betwwn 0-20 characters long")
            return
        x=1
        teamName = teamName.lstrip()
        for i in self.master.teamBrowser.teams:
            if i["TeamName"][0:4] == "Team" and i["TeamName"][5:20].strip(' ') == str(x):
                x+=1
        if teamName == '':
            teamName = "Team " + str(x)
        self.destroyerTeam.setDreamState(self.dreamteam)
        self.destroyerTeam.setTeamName(teamName)
        if self.destroyerTeam.AwokenBadgeName == 'No Badge':
            self.destroyerTeam.setBadge('')
        elif self.destroyerTeam.AwokenBadgeName != 'No Badge' and self.destroyerTeam.AwokenBadgeName != None:
            self.destroyerTeam.setBadge(str(self.destroyerTeam.AwokenBadgeName))
        saveThisTeam = self.destroyerTeam.getSaveDict()
        saveThisTeam['Email'] = self.PADsql.Email
        self.PADsql.saveTeam(saveThisTeam)
        
        tt = self.PADsql.selectTeamInstance(dreamteam = self.dreamteam)
        tID = 0
        for i in range(0, len(tt)):
            if tt[i]['TeamInstanceID'] > tID:
                tID = tt[i]['TeamInstanceID']
        tt = self.PADsql.selectTeamInstance(int(tID), dreamteam = self.dreamteam)
        if self.destroyerTeam.TeamInstanceID != None and self.destroyerTeam.TeamInstanceID != 0:
            self.master.teamBrowser.SelectedTeam = self.destroyerTeam
        else:
            self.master.teamBrowser.SelectedTeam = PADMonster.Team(self.PADsql,tt[0])
        self.master.showTeamBrowser()
        return


    def onSearchBarFocusIn(self, event):
        """Clears Search Bar on focus"""
        if self.builder.get_variable("SearchBar").get() == self.bgSearchText:
            self.builder.get_variable("SearchBar").set("")
        
    def onSearchBarFocusOut(self, event):
        """Populates empty Search bar on focus out"""
        if self.builder.get_variable("SearchBar").get() == "":
            self.builder.get_variable("SearchBar").set(self.bgSearchText)

    def onSearchClick(self, event):
        """Search for monsters within collection to be displayed"""
        ############################
        ##### PARSE SEARCH BAR #####
        ############################
        search = self.builder.get_variable("SearchBar").get()
        if search == self.bgSearchText:
            search = ""

        if "," in search and search != ",":
            search = le("(" + search + ")")
        elif search.isnumeric():
            search = int(search)

        self.MonsterResults = []
        monsters = self.master.PADsql.selectMonsterInstance(search, byInstanceID = False)

        #################################
        ##### GET ATTRIBUTE FILTERS #####
        #################################
        PriAttributes = []
        for i in ["PriFire", "PriWater", "PriWood", "PriLight", "PriDark"]:
            if self.builder.get_variable(i).get() != "" and self.builder.get_variable(i).get() != "0":
                PriAttributes.append(self.builder.get_variable(i).get())
        SecAttributes = []
        for i in ["SecFire", "SecWater", "SecWood", "SecLight", "SecDark"]:
            if self.builder.get_variable(i).get() != "" and self.builder.get_variable(i).get() != "0":
                SecAttributes.append(self.builder.get_variable(i).get())

        ##### IF NOTHING SELECTED ADD ALL FILTERS #####
        if len(PriAttributes) == 0 and len(SecAttributes) == 0:
            PriAttributes = ["Fire","Water","Wood","Light","Dark"]
            SecAttributes = ["Fire","Water","Wood","Light","Dark"]
            self.builder.get_variable("varANDOR").set("OR")

        ##### SINGLE ATTRIBUTE SWITCH TO 'OR' #####
        elif len(PriAttributes) == 0 or len(SecAttributes) == 0:
            self.builder.get_variable("varANDOR").set("OR")

        ############################
        ##### GET TYPE FILTERS #####
        ############################
        TypeFilters = []
        for i in ["TypeAttacker", "TypeAwakenMaterial", "TypeBalanced", "TypeDevil", "TypeDragon", "TypeEnhanceMaterial",
            "TypeEvoMaterial", "TypeGod", "TypeHealer", "TypeMachine", "TypePhysical", "TypeRedeemableMaterial" ]:
            if self.builder.get_variable(i).get() != "" and self.builder.get_variable(i).get() != "0":
                TypeFilters.append(self.builder.get_variable(i).get())

        ##### IF NOTHING SELECTED ADD ALL FILTERS #####
        if len(TypeFilters) == 0:
            TypeFilters = ["Attacker", "Awaken Material", "Balanced", "Devil", "Dragon", "Enhance Material",
                "Evo Material", "God", "Healer", "Machine", "Physical", "Redeemable Material" ]

        ############################################
        ##### ADD FILTERED MONSTERS TO RESULTS #####
        ############################################
        for i in monsters:
            if self.builder.get_variable("varANDOR").get() == "OR":
                if i["PriAttribute"] in PriAttributes or i["SecAttribute"] in SecAttributes:
                    if i["MonsterTypeOne"] in TypeFilters or i["MonsterTypeTwo"] in TypeFilters or i["MonsterTypeThree"] in TypeFilters:
                        self.MonsterResults.append(Monster(i))

            elif self.builder.get_variable("varANDOR").get() == "AND":
                if i["PriAttribute"] in PriAttributes and i["SecAttribute"] in SecAttributes:
                    if i["MonsterTypeOne"] in TypeFilters or i["MonsterTypeTwo"] in TypeFilters or i["MonsterTypeThree"] in TypeFilters:
                        self.MonsterResults.append(Monster(i))

        ################################################
        ##### CALCULATE MAXPAGES AND SET PAGE TO 1 #####
        ################################################
        self.page = 1
        self.populateCollection(self.MonsterResults)
        self.builder.get_object("lblResults").config(text = str(len(self.MonsterResults)) + " Results Found.")

    def onPageEnter(self, event):
        """Load specified page of monsters"""
        value = self.builder.get_variable("varPageEnt").get()
        
        while len(value) >= 1 and value[0] == '0':
            value = value.replace('0', '', 1)

        if len(value) == 0:
            value = '1'
        elif int(value) > self.pages:
            value = str(self.pages)

        self.builder.get_variable("varPageEnt").set(value)
        self.page = int(value)
        self.populateCollection(self.MonsterResults)


    def validatePageEntry(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        """Confirm Values entered are numeric"""
        if text in "0123456789\b" and len(value_if_allowed) < 4:
            return True
        else:
            return False

    def validateTwoDigit(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        """Confirm Values entered are numeric"""
        if text in "0123456789\b" and len(value_if_allowed) < 3:
            return True
        else:
            return False

    def clearFilters(self):
        """Deselect All Filters"""
        for i in [  "TypeAttacker", "TypeAwakenMaterial", "TypeBalanced",
                    "TypeDevil", "TypeDragon", "TypeEnhanceMaterial",
                    "TypeEvoMaterial", "TypeGod", "TypeHealer",
                    "TypeMachine", "TypePhysical", "TypeRedeemableMaterial",
                    "PriFire", "PriWater", "PriWood", "PriLight", "PriDark",
                    "SecFire", "SecWater", "SecWood", "SecLight", "SecDark" ]:
            self.builder.get_variable(i).set("")

    def onProfileImageClick(self, event):
        """Allows user to choose a profile Image"""
        value = sd.askstring("Change Profile Image", "Enter Monster ID or Name:", parent=self.builder.get_object("canProfileImage"))
        if value is not None:
            if value.isnumeric():
                value = int(value)

            if self.master.PADsql.updateProfileImage(value):
                self.master.updateProfile(self.builder)
            else:
                mb.showinfo("Profile Image", "Monster ID Does Not Exist")



if __name__ == '__main__':
    root = tk.Tk()
    app = EditTeam(root)
    root.mainloop()

    #KyleTD