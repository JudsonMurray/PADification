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


class MonsterFrame:
    def __init__(self, master, masterbuilder, i, ids, currentMonster, buttons, padsql):
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
        
    def clickMe(self, event):
        '''Occurs everytime a monster in the player collection is clicked'''
        
        global k
        global selectedMonster

        self.masterbuilder.get_object("btnFavoriteWishlist").config(state = NORMAL)
        self.masterbuilder.get_object("btnEdit").config(state = NORMAL)
        self.masterbuilder.get_object("btnRemove").config(state = NORMAL)
        
        #Creates photoimages for selected monster 
        self.s = PhotoImage(file = "Resource/PAD/Images/thumbnails/" + str(monsters[self.ids[self.i]]["MonsterClassID"]) +'.png')

        #Creates the photo image for the selected monster's awoken awoken skills
        self.aSList = self.padsql.getAwokenSkillList(monsters[self.ids[self.i]]["MonsterClassID"])
        self.aSListImg = []

        for i in range(1, len(self.aSList)):
            if i <= self.currentMonster.SkillsAwoke:
                if self.aSList[i] is not None:
                    self.aSListImg.append(PhotoImage(file = "Resource/PAD/Images/Awoken Skills/" + str(self.aSList[i]) +'.png'))
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
        if len(self.buttons) - 1 >= k:
            self.buttons[k].monbut.config(relief = FLAT)
        k = self.i
        
        self.buttons[self.i].monbut.config(relief = SUNKEN)


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
        
        buttons =[]

        k=-1

        #1: Creates a builder
        self.builder = builder = pygubu.Builder()

        #2: Loads an ui file
        builder.add_from_file('src/ui/PlayerCollection.ui')

        #3: Creates the widget using a master as parent
        self.mainwindow = builder.get_object('frmPlayerCollection')
        builder.connect_callbacks(self)

    def populateList(self):
        '''Populates the player collection list'''
        self.builder.get_object("btnFavoriteWishlist").config(state = DISABLED)
        self.builder.get_object("btnEdit").config(state = DISABLED)
        self.builder.get_object("btnRemove").config(state = DISABLED)

        global monsters
        
        # JBM - Modifying collection to Dictionary from List to make Monster Lookup easier
        instanceIDs = []
        monster = self.pds.selectMonsterInstance()

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
            self.buttons.append(MonsterFrame(self.container, self.builder, self.count, self.instantList, a, self.buttons, self.pds))
            self.buttons[self.count].monbut.grid(row=self.count // 10,column = self.count % 10)
            self.buttons[self.count].builder.get_object('FrameLabel').create_image(2,2, image = self.myMonsterList[self.count], anchor = tk.NW)
            self.buttons[self.count].builder.get_object('lblMonsterBrief').config(text = 'LVL:' + str(a.Level)+ '\nID: ' + str(a.MonsterClassID))
            self.count += 1

        self.container.config(height=(len(self.container.grid_slaves()) // 2) * 30)
    
    def RemoveMonster(self):
        '''Removes the selected monster from the DB and all its references, occurs when remove monster button is clicked'''

        #Removes monster instance from DB
        self.pds.deleteMonster(selectedMonster)

        #Removes references to the monster
        monsters.pop(selectedMonster)
        self.instantList.remove(selectedMonster)

        self.__RemoveInformation()
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
