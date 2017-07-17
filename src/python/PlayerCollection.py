#!/usr/bin/env python
#   Name:    Ryan Breau
#   Date:    06/23/17
#   Purpose: Functionality for the player collection screen
#   V.1.0   RB  Created base functionality for the player collection screen, known bugs are monster summary image is wrongly sized and type images not showing up
#   V.1.1   RB  Monster summary image now sized correctly and type images are now being displayed
#   V.1.2   RB  Changed the collection of information from the DB to use the PADSQL and PADMonster classes
#   V.1.3   RB  Remove monster functionality works, Monsters now stored in a dictionary
#   V.1.4   RB  Integrated with the PADification.py
#   V.1.5   RB  Added currently awoken awoken skills and disabled the monster summary buttons when a monster is not selected
#   V.1.6   RB  Added a okcancel messagebox when remove monster is clicked and now able to load Edit Monster screen when edit monster is clicked
#   V.1.7   RB  Added Wishlist functionality
#

from tkinter import *
import tkinter as tk
import pygubu
import random
import pypyodbc
import sys
import time
import PADMonster
import PADSQL
import MonsterEditScreen


class MonsterFrame:
    def __init__(self, master, masterbuilder, i, ids, currentMonster, buttons, padsql, selButton):
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
        self.selButton = selButton
        self.myMonster = tk.PhotoImage(file = "Resource/PAD/Images/thumbnails/" + str(monsters[self.ids[self.i]]["MonsterClassID"]) + '.png').subsample(2)
        self.builder.get_object("FrameLabel").create_image(2,2, image = self.myMonster, anchor = tk.NW)
        
    def clickMe(self, event):
        '''Occurs everytime a monster in the player collection is clicked'''
        
        global k
        global selectedMonster
        
        if monsters[self.ids[self.i]]["Favorites"]:
           self.masterbuilder.get_object("btnFavorite").config(state = Disabled)
        else:
            self.masterbuilder.get_object("btnFavorite").config(state = NORMAL)
        self.masterbuilder.get_object("btnEdit").config(state = NORMAL)
        self.masterbuilder.get_object("btnRemove").config(state = NORMAL)
        if monsters[self.ids[self.i]]["Favorites"]:
            self.masterbuilder.get_object("btnUnfavorite").config(state = NORMAL)
        if monsters[self.ids[self.i]]["WishList"]:
            self.masterbuilder.get_object("btnAddFromWishlist").config(state = NORMAL)
        
        #Creates photoimages for selected monster 
        self.s = PhotoImage(file = "Resource/PAD/Images/thumbnails/" + str(monsters[self.ids[self.i]]["MonsterClassID"]) +'.png').zoom(4)
        self.s = self.s.subsample(5)

        #Creates the photo image for the selected monster's awoken awoken skills
        self.aSList = self.padsql.getAwokenSkillList(monsters[self.ids[self.i]]["MonsterClassID"])
        self.aSListImg = []

        for i in range(1, len(self.aSList)):
            if i <= self.currentMonster.SkillsAwoke:
                if self.aSList[i] is not None:
                    self.aSListImg.append(PhotoImage(file = "Resource/PAD/Images/Awoken Skills/" + str(self.aSList[i]) +'.png'))
                else:
                    self.aSListImg.append(None)
            else:
                if self.aSList[i] is not None:
                    self.aSListImg.append(PhotoImage(file = "Resource/PAD/Images/Awoken Skills/not " + str(self.aSList[i]) +'.png'))
                else:
                    self.aSListImg.append(None)

        #Removes all the previously selected monster's, if there was one, awoken awoken skills
        self.masterbuilder.get_object("canASOne").delete("all")
        self.masterbuilder.get_object("canASTwo").delete("all")
        self.masterbuilder.get_object("canASThree").delete("all")
        self.masterbuilder.get_object("canASFour").delete("all")
        self.masterbuilder.get_object("canASFive").delete("all")
        self.masterbuilder.get_object("canASSix").delete("all")
        self.masterbuilder.get_object("canASSeven").delete("all")
        self.masterbuilder.get_object("canASEight").delete("all")
        self.masterbuilder.get_object("canASNine").delete("all")

        #Creates photimages for the types of the selected monster
        self.e = PhotoImage(file = "Resource/PAD/Images/Types/" + str(monsters[self.ids[self.i]]["MonsterTypeOne"]) + '.png')

        #Removes all the previously selected monster's, if there was one, secondary and tertiary types
        self.masterbuilder.get_object("canType2").delete("all")
        self.masterbuilder.get_object("canType3").delete("all")

        if not monsters[self.ids[self.i]]["MonsterTypeTwo"] is None:
            self.f = PhotoImage(file = "Resource/PAD/Images/Types/" + str(monsters[self.ids[self.i]]["MonsterTypeTwo"]) + '.png')
        else:
            self.f = None

        if not monsters[self.ids[self.i]]["MonsterTypeThree"] is None:
            self.g = PhotoImage(file = "Resource/PAD/Images/Types/" + str(monsters[self.ids[self.i]]["MonsterTypeThree"]) + '.png')
        else:
            self.g = None

        

        #Changes the relief of the 'buttons' to signify a selected 'button'
        #Prevents the program from trying to change the releif of a 'button' if it doesn't exist
        for i in range(0, (len(self.buttons))):
            self.buttons[i].monbut.config(relief = FLAT)
        k = self.selButton

        
        self.buttons[self.selButton].monbut.config(relief = SUNKEN)


        #Populates fields with neccessary information
        self.masterbuilder.get_object("canMonsterSummary").create_image(7,7, image = self.s, anchor = tk.NW)
        self.masterbuilder.get_object("lblName").config(text = "Monster Name: " + str(monsters[self.ids[self.i]]["MonsterName"]))
        self.masterbuilder.get_object("lblRarity").config(text = "Rarity: " + str(monsters[self.ids[self.i]]["Rarity"]))
        self.masterbuilder.get_object("lblHP").config(text = "HP: " + str(self.currentMonster.HP))
        self.masterbuilder.get_object("lblATK").config(text = "ATK: " + str(self.currentMonster.ATK))
        self.masterbuilder.get_object("lblRCV").config(text = "RCV: " + str(self.currentMonster.RCV))
        #self.masterbuilder.get_object("lblHP").config(text = "HP: " + str(monsters[self.ids[self.i]]["HP"]))
        #self.masterbuilder.get_object("lblATK").config(text = "ATK: " + str(monsters[self.ids[self.i]]["ATK"]))
        #self.masterbuilder.get_object("lblRCV").config(text = "RCV: " + str(monsters[self.ids[self.i]]["RCV"]))
        self.masterbuilder.get_object("lblID").config(text = "Monster ID: " + str(monsters[self.ids[self.i]]["MonsterClassID"]))
        self.masterbuilder.get_object("canType1").create_image(2,2, image = self.e, anchor = tk.NW)
        self.masterbuilder.get_object("canType2").create_image(2,2, image = self.f, anchor = tk.NW)
        self.masterbuilder.get_object("canType3").create_image(2,2, image = self.g, anchor = tk.NW)
        self.masterbuilder.get_object("canASOne").create_image(2,2, image = self.aSListImg[0], anchor = tk.NW)
        self.masterbuilder.get_object("canASTwo").create_image(2,2, image = self.aSListImg[1], anchor = tk.NW)
        self.masterbuilder.get_object("canASThree").create_image(2,2, image = self.aSListImg[2], anchor = tk.NW)
        self.masterbuilder.get_object("canASFour").create_image(2,2, image = self.aSListImg[3], anchor = tk.NW)
        self.masterbuilder.get_object("canASFive").create_image(2,2, image = self.aSListImg[4], anchor = tk.NW)
        self.masterbuilder.get_object("canASSix").create_image(2,2, image = self.aSListImg[5], anchor = tk.NW)
        self.masterbuilder.get_object("canASSeven").create_image(2,2, image = self.aSListImg[6], anchor = tk.NW)
        self.masterbuilder.get_object("canASEight").create_image(2,2, image = self.aSListImg[7], anchor = tk.NW)
        self.masterbuilder.get_object("canASNine").create_image(2,2, image = self.aSListImg[8], anchor = tk.NW)

        #Saves the instanceid of the selected monster for later use
        selectedMonster = monsters[self.ids[self.i]]["InstanceID"]

class PlayerCollection:
    def __init__(self, master):
        #Creates globals 
        global monsters
        global k
        global buttons

        self.pds = master.PADsql
        self.master = master
        self.startMonster = 0

        self.displayWishlist = 0

        buttons =[]
        self.currentPage = 1

        k = None
        #self.__UpdateMonsters()

        #1: Creates a builder
        self.builder = builder = pygubu.Builder()

        #2: Loads an ui file
        builder.add_from_file('src/ui/PlayerCollection.ui')

        #3: Creates the widget using a master as parent
        self.mainwindow = builder.get_object('frmPlayerCollection')
        builder.connect_callbacks(self)

    def pageOne(self):
        if k is None:
            self.startMonster = 0
            self.currentPage = 1
            self.__RemoveInformation()
        else:
            self.startMonster = 50 * (self.currentPage - 1)
        self.populateList()

    def onAddFromWishlistClick(self):

        a = PADMonster.Monster(monsters[selectedMonster])
        a.WishList = 0
        b = a.getSaveDict()

        global k
        k = None

        self.pds.saveMonster(b)

        monsters.pop(selectedMonster)
        self.instantList.remove(selectedMonster)

        self.__RemoveInformation()
        self.startMonster -= self.count
        self.populateList()

    def populateList(self):
        '''Populates the player collection list'''
        if k is None:
            self.builder.get_object("btnFavorite").config(state = DISABLED)
            self.builder.get_object("btnEdit").config(state = DISABLED)
            self.builder.get_object("btnRemove").config(state = DISABLED)
            self.builder.get_object("btnUnfavorite").config(state = DISABLED)
            self.builder.get_object("btnAddFromWishlist").config(state = DISABLED)

        global monsters
        
        self.builder.get_object("canMonsterList").delete("All")

        # JBM - Modifying collection to Dictionary from List to make Monster Lookup easier
        instanceIDs = []
        monster = self.pds.selectMonsterInstance(wishlist = self.displayWishlist)

        monsters = dict()
        for i in monster:
            monsters[i["InstanceID"]] = i
            instanceIDs.append(i["InstanceID"])
        self.instantList = instanceIDs
        #self.myMonsterList = []

        ##Creates the photoimage for each monster instance of the user and stores them in a list
        #for i in self.instantList:
        #    myMonster = tk.PhotoImage(file = "Resource/PAD/Images/thumbnails/" + str(monsters[i]["MonsterClassID"]) + '.png')
        #    myMonster = myMonster.subsample(2)
        #    self.myMonsterList.append(myMonster)

        self.container = self.builder.get_object('canMonsterList')
        

        for i in self.container.grid_slaves():
            i.grid_forget()
        
        #Creates a graphical list of monsters
        buttons = []
        self.buttons = buttons = []
        self.count = 0
        

        for i in monsters:
            if self.startMonster < 50 * self.currentPage and ((self.startMonster >= 50 * (self.currentPage - 1)) and not(self.startMonster == len(self.instantList))):
                b = self.instantList[self.startMonster]
                a = PADMonster.Monster(monsters[b])
                self.buttons.append(MonsterFrame(self.container, self.builder, self.startMonster, self.instantList, a, self.buttons, self.pds, self.count))
                self.buttons[self.count].monbut.grid(row=self.count // 10,column = self.count % 10)
                #self.buttons[self.count].builder.get_object('FrameLabel').create_image(2,2, image = self.myMonsterList[self.startMonster], anchor = tk.NW)
                self.buttons[self.count].builder.get_object('lblMonsterBrief').config(text = 'LVL:' + str(a.Level)+ '\nID: ' + str(a.MonsterClassID))
                self.count += 1
                self.startMonster += 1

        self.pages = (len(self.instantList) // 50) + 1
        if len(self.instantList) == 0:
            self.pages = 1
        elif len(self.instantList) % 50 == 0:
            self.pages -= 1

        if self.currentPage > self.pages:
            self.prev()

        if self.pages > self.currentPage:
            self.builder.get_object("btnNext").config(state = NORMAL)
        elif self.pages <= self.currentPage:
            self.builder.get_object("btnNext").config(state = DISABLED)
            
        self.builder.get_object('lblCurPage').config(text = "Page " + str(self.currentPage) + "/" + str(self.pages))

        self.container.config(height=(len(self.container.grid_slaves()) // 2) * 30)

        if k != None:
           self.buttons[k].monbut.config(relief = SUNKEN)

    def onWishlistClick(self):
        global k
        self.displayWishlist = 1
        self.currentPage = 1
        k = None
        #for i in range(0, (len(self.buttons) - 1)):
        #    self.buttons[i].monbut.config(relief = FLAT)
        self.builder.get_object("btnPrev").config(state = DISABLED)
        self.startMonster = 0
        self.builder.get_object("btnWishlist").config(state = DISABLED)
        self.builder.get_object("btnMonsterList").config(state = NORMAL)
        self.__RemoveInformation()
        self.populateList()

    def onMonsterListClick(self):
        self.displayWishlist = 0
        global k
        self.currentPage = 1
        k = None
        #for i in range(0, (len(self.buttons) - 1)):
        #    self.buttons[i].monbut.config(relief = FLAT)
        self.builder.get_object("btnPrev").config(state = DISABLED)
        self.startMonster = 0
        self.builder.get_object("btnMonsterList").config(state = DISABLED)
        self.builder.get_object("btnWishlist").config(state = NORMAL)
        self.__RemoveInformation()
        self.populateList()

    def onEditMonsterClick(self):
        self.master.monsterEdit.receiveInstanceID(selectedMonster, self.displayWishlist)
        self.master.showEditMonster()

    def onHomeClick(self):
        self.displayWishlist = 0
        global k
        k = None
        self.builder.get_object("btnWishlist").config(state = NORMAL)
        self.builder.get_object("btnMonsterList").config(state = DISABLED) 
        self.master.showHomeScreen()

    def onMyMonsterClick(self):
        self.master.showPlayerCollection()

    def onMonsterBookClick(self):
        self.displayWishlist = 0
        global k
        k = None
        self.builder.get_object("btnWishlist").config(state = NORMAL)
        self.builder.get_object("btnMonsterList").config(state = DISABLED) 
        self.master.showMonsterBook()

    def onMyTeamsClick(self):
        self.displayWishlist = 0
        global k
        k = None
        self.builder.get_object("btnWishlist").config(state = NORMAL)
        self.builder.get_object("btnMonsterList").config(state = DISABLED) 
        self.master.showTeamBrowser()

    def onPlayersClick(self):
        self.displayWishlist = 0
        global k
        k = None
        self.builder.get_object("btnWishlist").config(state = NORMAL)
        self.builder.get_object("btnMonsterList").config(state = DISABLED) 
        pass

    def onTeamRankingClick(self):
        self.displayWishlist = 0
        global k
        k = None
        self.builder.get_object("btnWishlist").config(state = NORMAL)
        self.builder.get_object("btnMonsterList").config(state = DISABLED) 
        pass

    def onAccountOptionsClick(self):
        self.displayWishlist = 0
        global k
        k = None
        self.builder.get_object("btnWishlist").config(state = NORMAL)
        self.builder.get_object("btnMonsterList").config(state = DISABLED) 
        self.master.showAccountOptions()

    def next(self):
        #for i in range(0, (len(self.buttons) - 1)):
        #    self.buttons[i].monbut.config(relief = FLAT)
        self.builder.get_object("btnPrev").config(state = NORMAL)
        global k
        k = None
        self.currentPage += 1
        if self.currentPage == self.pages:
            self.builder.get_object("btnNext").config(state = DISABLED)
        self.__RemoveInformation()
        self.populateList()

    def prev(self):
        #for i in range(0, (len(self.buttons) - 1)):
        #    self.buttons[i].monbut.config(relief = FLAT)
        self.builder.get_object("btnNext").config(state = NORMAL)
        self.currentPage -= 1
        global k
        k = None
        self.startMonster -= self.count + 50
        if self.currentPage == 1:
            self.builder.get_object("btnPrev").config(state = DISABLED)
        self.__RemoveInformation()
        self.populateList()

    def RemoveMonster(self):
        '''Removes the selected monster from the DB and all its references, occurs when remove monster button is clicked'''

        tkMessageBox = messagebox.askokcancel("Confirm", "Are your sure you want to remove this monster?")

        if tkMessageBox:
            #Removes monster instance from DB
            teams = self.pds.selectTeamInstance()
            for i in range(0,len(teams)):
                self.SelectedTeam = PADMonster.Team(self.pds, (teams[i]))

                if self.SelectedTeam.LeaderMonster == selectedMonster:
                    self.SelectedTeam.setLeaderMonster()
                if self.SelectedTeam.SubMonsterOne == selectedMonster:
                    self.SelectedTeam.setSubMonsterOne()
                if self.SelectedTeam.SubMonsterTwo == selectedMonster:
                    self.SelectedTeam.setSubMonsterTwo()
                if self.SelectedTeam.SubMonsterThree == selectedMonster:
                    self.SelectedTeam.setSubMonsterThree()
                if self.SelectedTeam.SubMonsterFour == selectedMonster:
                    self.SelectedTeam.setSubMonsterFour()
                self.SelectedTeam.update()
                self.pds.saveTeam(self.SelectedTeam.getSaveDict())
            self.pds.deleteMonster(selectedMonster)

            global k

            k = None

            #Removes references to the monster
            monsters.pop(selectedMonster)
            self.instantList.remove(selectedMonster)

            #self.__UpdateMonsters()
            self.__RemoveInformation()
            self.startMonster -= self.count
            self.populateList()

    def __RemoveInformation(self):
        '''Removes the information in the monster summary, runs during RemoveMonster'''
        self.builder.get_object("canMonsterSummary").delete('all')
        self.builder.get_object("lblName").config(text = "Monster Name: ")
        self.builder.get_object("lblRarity").config(text = "Rarity: ")
        self.builder.get_object("lblHP").config(text = "HP: ")
        self.builder.get_object("lblATK").config(text = "ATK: ")
        self.builder.get_object("lblRCV").config(text = "RCV: ")
        self.builder.get_object("lblID").config(text = "Monster ID: ")
        self.builder.get_object("canType1").delete("all")
        self.builder.get_object("canType2").delete("all")
        self.builder.get_object("canType3").delete("all")
        self.builder.get_object("canASOne").delete("all")
        self.builder.get_object("canASTwo").delete("all")
        self.builder.get_object("canASThree").delete("all")
        self.builder.get_object("canASFour").delete("all")
        self.builder.get_object("canASFive").delete("all")
        self.builder.get_object("canASSix").delete("all")
        self.builder.get_object("canASSeven").delete("all")
        self.builder.get_object("canASEight").delete("all")
        self.builder.get_object("canASNine").delete("all")
