#!/usr/bin/env python
#   Name:    Ryan Breau
#   Date:    06/23/17
#   Purpose: Functionality for the player collection screen
#   V.1.0   RB  Created base functionality for the player collection screen, known bugs are monster summary image is wrongly sized and type images not showing up
#   V.1.1   RB  Monster summary image now sized correctly and type images are now being displayed
#   V.1.2   RB  Changed the collection of information from the DB to use the PADSQL and PADMonster classes
#   V.1.3   RB  Remove monster functionality works, self.monsters now stored in a dictionary
#   V.1.4   RB  Integrated with the PADification.py
#   V.1.5   RB  Added currently awoken awoken skills and disabled the monster summary buttons when a monster is not selected
#   V.1.6   RB  Added a okcancel messagebox when remove monster is clicked and now able to load Edit Monster screen when edit monster is clicked
#   V.1.7   RB  Added Wishlist functionality
#   V.1.8   RB  Added Available Evolutions
#   V.1.9   RB  Added Favorite functionality
#

import logging
from tkinter import *
import tkinter as tk
import pygubu
import random
import pypyodbc
import CustomWidgets
from PIL import Image
from PIL import ImageTk
from idlelib import ToolTip
import sys
import time
import PADMonster
from PADMonster import Monster
import PADSQL
import MonsterEditScreen
from ast import literal_eval as le


class EvoFrame:
    def __init__(self, master, nextMon):
        self.master = master
        self.nextMon = nextMon
        if self.nextMon != None:
            self.builder = pygubu.Builder()
            self.builder.add_from_file(r"src\ui\PlayerCollection.ui")
            self.evos = self.builder.get_object('frmEvos', self.master.masterbuilder.get_object("canEvoTree"))
            self.availEvo = tk.PhotoImage(file = "Resource/PAD/Images/thumbnails/" + str(self.nextMon[0]) + '.png').zoom(4).subsample(5)
            self.builder.get_object("canNextMon").create_image(7,7, image = self.availEvo, anchor = tk.NW)
            self.evos.config(highlightthickness = 5)
            self.check = self.nextMon[0]
            self.check = Monster((self.master.mastermaster.pds.selectMonsterClass(self.check))[0])

            self.evos.config(highlightbackground = 'Red')

            if self.nextMon[7]:
                self.evos.config(highlightbackground = 'Blue')

            if self.master.currentMonster.MonsterClassID > self.nextMon[0]:
                self.evos.config(highlightbackground = 'Yellow')

            self.builder.connect_callbacks(self)
        return

class MonsterFrame:
    def __init__(self, master, masterbuilder, i, currentMonster, buttons, padsql, selButton, mastermaster):
        #logger
        self.logger = logging.getLogger("Padification.ui.PlayerCollection.MonsterFrame")

        self.master = master
        self.masterbuilder = masterbuilder
        self.i = i
        self.mastermaster = mastermaster
        self.builder = pygubu.Builder()
        self.builder.add_from_file('src/ui/PlayerCollection.ui')
        self.monbut = self.builder.get_object('MonsFrame', self.master)
        self.builder.connect_callbacks(self)
        self.currentMonster = currentMonster
        self.buttons = buttons
        self.padsql = padsql
        self.selButton = selButton
        self.myMonster = tk.PhotoImage(file = "Resource/PAD/Images/thumbnails/" + str(self.currentMonster.MonsterClassID) + '.png').subsample(2)
        self.builder.get_object("FrameLabel").create_image(2,2, image = self.myMonster, anchor = tk.NW)
        if self.currentMonster.Favorites:
           self.monbut.config(bg = 'Yellow')
           self.builder.get_object('lblMonsterBrief').config(bg = 'Yellow')
        else:
            self.monbut.config(bg = '#f0f0f0')
            self.builder.get_object('lblMonsterBrief').config(bg = '#f0f0f0')
        
    def clickMe(self, event):
        '''Occurs everytime a monster in the player collection is clicked'''
        
        global k
        global selectedMonster

        for i in self.masterbuilder.get_object("canEvoTree").grid_slaves():
                i.grid_forget()

        self.evos = self.mastermaster.pds.getEvolutions(self.currentMonster.MonsterClassID)
        if self.evos:
            self.evoFrames = []

            self.count = 0

            

            for i in self.evos:
                self.evoFrames.append(EvoFrame(self, i))
                self.evoFrames[self.count].evos.grid(row=self.count // 4,column = self.count % 4, padx = 8, pady = 8)
                self.count += 1

        if self.currentMonster.Favorites:
           self.monbut.config(bg = 'Yellow')
           self.builder.get_object('lblMonsterBrief').config(bg = 'Yellow')
           self.masterbuilder.get_object("btnFavorite").config(state = DISABLED)
           self.masterbuilder.get_object('btnRemove').config(state = DISABLED)
           self.masterbuilder.get_object("btnUnfavorite").config(state = NORMAL)
        else:
            self.monbut.config(bg = '#f0f0f0')
            self.builder.get_object('lblMonsterBrief').config(bg = '#f0f0f0')
            self.masterbuilder.get_object("btnFavorite").config(state = NORMAL)
            self.masterbuilder.get_object("btnUnfavorite").config(state = DISABLED)
            self.masterbuilder.get_object('btnRemove').config(state = NORMAL)
        self.masterbuilder.get_object("btnEdit").config(state = NORMAL)
        #self.masterbuilder.get_object("btnRemove").config(state = NORMAL)
        if self.currentMonster.Favorites:
            self.masterbuilder.get_object("btnUnfavorite").config(state = NORMAL)
        if self.currentMonster.WishList:
            self.masterbuilder.get_object("btnAddFromWishlist").config(state = NORMAL)
        
        #Creates photoimages for selected monster 
        self.s = PhotoImage(file = "Resource/PAD/Images/thumbnails/" + str(self.currentMonster.MonsterClassID) +'.png').zoom(4)
        self.s = self.s.subsample(5)

        #Creates the photo image for the selected monster's awoken awoken skills
        self.aSList = self.padsql.getAwokenSkillList(self.currentMonster.MonsterClassID)
        self.aSListImg = []

        self.awokenSkills = []

        for i in range(1, len(self.aSList)):
            if i <= self.currentMonster.SkillsAwoke:
                if self.aSList[i] is not None:
                    self.awokenSkills.append(self.aSList[i])
                    self.aSListImg.append(PhotoImage(file = "Resource/PAD/Images/Awoken Skills/" + str(self.aSList[i]) +'.png'))
                else:
                    self.awokenSkills.append(None)
                    self.aSListImg.append(None)
            else:
                if self.aSList[i] is not None:
                    self.awokenSkills.append(self.aSList[i])
                    self.aSListImg.append(PhotoImage(file = "Resource/PAD/Images/Awoken Skills/not " + str(self.aSList[i]) +'.png'))
                else:
                    self.awokenSkills.append(None)
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
        self.e = PhotoImage(file = "Resource/PAD/Images/Types/" + str(self.currentMonster.MonsterTypeOne) + '.png')

        #Removes all the previously selected monster's, if there was one, secondary and tertiary types
        self.masterbuilder.get_object("canType2").delete("all")
        self.masterbuilder.get_object("canType3").delete("all")

        if not self.currentMonster.MonsterTypeTwo is None:
            self.f = PhotoImage(file = "Resource/PAD/Images/Types/" + str(self.currentMonster.MonsterTypeTwo) + '.png')
        else:
            self.f = None

        if not self.currentMonster.MonsterTypeThree is None:
            self.g = PhotoImage(file = "Resource/PAD/Images/Types/" + str(self.currentMonster.MonsterTypeThree) + '.png')
        else:
            self.g = None

        

        #Changes the relief of the 'buttons' to signify a selected 'button'
        for i in range(0, (len(self.buttons))):
            self.buttons[i].monbut.config(relief = FLAT)
        k = self.selButton
        self.master.k = k
        
        self.buttons[self.selButton].monbut.config(relief = SUNKEN)

        self.latents = []

        if self.currentMonster.LSListID != None:
            if self.currentMonster.LatentSkillOne != None:
                self.baseImg = Image.open("Resource/PAD/Images/LatentAwokenSkills/" + str(self.currentMonster.LatentSkillOne) + '.png')
                self.baseImg = self.baseImg.resize((30,30), Image.ANTIALIAS)
                self.latents.append(ImageTk.PhotoImage(self.baseImg))
                self.masterbuilder.get_object("canLatentOne").create_image(2,2, image = self.latents[0], anchor = tk.NW)
            else:
                self.masterbuilder.get_object("canLatentOne").delete('all')
            if self.currentMonster.LatentSkillTwo != None:
                self.baseImg = Image.open("Resource/PAD/Images/LatentAwokenSkills/" + str(self.currentMonster.LatentSkillTwo) + '.png')
                self.baseImg = self.baseImg.resize((30,30), Image.ANTIALIAS)
                self.latents.append(ImageTk.PhotoImage(self.baseImg))
                self.masterbuilder.get_object("canLatentTwo").create_image(2,2, image = self.latents[1], anchor = tk.NW)
            else:
                self.masterbuilder.get_object("canLatentTwo").delete('all')
            if self.currentMonster.LatentSkillThree != None:
                self.baseImg = Image.open("Resource/PAD/Images/LatentAwokenSkills/" + str(self.currentMonster.LatentSkillThree) + '.png')
                self.baseImg = self.baseImg.resize((30,30), Image.ANTIALIAS)
                self.latents.append(ImageTk.PhotoImage(self.baseImg))
                self.masterbuilder.get_object("canLatentThree").create_image(2,2, image = self.latents[2], anchor = tk.NW)
            else:
                self.masterbuilder.get_object("canLatentThree").delete('all')
            if self.currentMonster.LatentSkillFour != None:
                self.baseImg = Image.open("Resource/PAD/Images/LatentAwokenSkills/" + str(self.currentMonster.LatentSkillFour) + '.png')
                self.baseImg = self.baseImg.resize((30,30), Image.ANTIALIAS)
                self.latents.append(ImageTk.PhotoImage(self.baseImg))
                self.masterbuilder.get_object("canLatentFour").create_image(2,2, image = self.latents[3], anchor = tk.NW)
            else:
                self.masterbuilder.get_object("canLatentFour").delete('all')
            if self.currentMonster.LatentSkillFive != None:
                self.baseImg = Image.open("Resource/PAD/Images/LatentAwokenSkills/" + str(self.currentMonster.LatentSkillFive) + '.png')
                self.baseImg = self.baseImg.resize((30,30), Image.ANTIALIAS)
                self.latents.append(ImageTk.PhotoImage(self.baseImg))
                self.masterbuilder.get_object("canLatentFive").create_image(2,2, image = self.latents[4], anchor = tk.NW)
            else:
                self.masterbuilder.get_object("canLatentFive").delete('all')
            if self.currentMonster.LatentSkillSix != None:
                self.baseImg = Image.open("Resource/PAD/Images/LatentAwokenSkills/" + str(self.currentMonster.LatentSkillSix) + '.png')
                self.baseImg = self.baseImg.resize((30,30), Image.ANTIALIAS)
                self.latents.append(ImageTk.PhotoImage(self.baseImg))
                self.masterbuilder.get_object("canLatentSix").create_image(2,2, image = self.latents[5], anchor = tk.NW)
            else:
                self.masterbuilder.get_object("canLatentSix").delete('all')
        else:
            self.masterbuilder.get_object("canLatentOne").delete('all')
            self.masterbuilder.get_object("canLatentTwo").delete('all')
            self.masterbuilder.get_object("canLatentThree").delete('all')
            self.masterbuilder.get_object("canLatentFour").delete('all')
            self.masterbuilder.get_object("canLatentFive").delete('all')
            self.masterbuilder.get_object("canLatentSix").delete('all')


        #Populates fields with neccessary information
        self.masterbuilder.get_object("canMonsterSummary").create_image(7,7, image = self.s, anchor = tk.NW)
        self.masterbuilder.get_object("lblName").config(text = "Monster Name: " + str(self.currentMonster.MonsterName))
        self.masterbuilder.get_object("lblRarity").config(text = "Rarity: " + str(self.currentMonster.Rarity))
        self.masterbuilder.get_object("lblHP").config(text = "HP: " + str(self.currentMonster.TotalHP))
        self.masterbuilder.get_object("lblATK").config(text = "ATK: " + str(self.currentMonster.TotalATK))
        self.masterbuilder.get_object("lblRCV").config(text = "RCV: " + str(self.currentMonster.TotalRCV))
        self.masterbuilder.get_object("lblID").config(text = "Monster ID: " + str(self.currentMonster.MonsterClassID))
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
        selectedMonster = self.currentMonster.InstanceID

        self.image = Image.open("Resource/PAD/Images/portraits/" + str(self.currentMonster.MonsterClassID) + ".jpg").resize((320,192))
        self.portrait = ImageTk.PhotoImage(self.image)

        self.mastermaster.typeOne.text = self.currentMonster.MonsterTypeOne

        if self.currentMonster.MonsterTypeTwo != None:
            self.mastermaster.typeTwo.text = self.currentMonster.MonsterTypeTwo
        else:
            self.mastermaster.typeTwo.text = None
            pass

        if self.currentMonster.MonsterTypeThree != None:
            self.mastermaster.typeThree.text = self.currentMonster.MonsterTypeThree
        else:
            self.mastermaster.typeThree.text = None

        if self.awokenSkills[0] is None:
            self.mastermaster.ASOne.text = None
            self.mastermaster.ASTwo.text = None
            self.mastermaster.ASThree.text = None
            self.mastermaster.ASFour.text = None
            self.mastermaster.ASFive.text = None
            self.mastermaster.ASSix.text = None
            self.mastermaster.ASSeven.text = None
            self.mastermaster.ASEight.text = None
            self.mastermaster.ASNine.text = None
        else:
            self.mastermaster.ASOne.text = self.awokenSkills[0]

        if self.awokenSkills[1] is None:
            self.mastermaster.ASTwo.text = None
            self.mastermaster.ASThree.text = None
            self.mastermaster.ASFour.text = None
            self.mastermaster.ASFive.text = None
            self.mastermaster.ASSix.text = None
            self.mastermaster.ASSeven.text = None
            self.mastermaster.ASEight.text = None
            self.mastermaster.ASNine.text = None
        else:
            self.mastermaster.ASTwo.text = self.awokenSkills[1]

        if self.awokenSkills[2] is None:
            self.mastermaster.ASThree.text = None
            self.mastermaster.ASFour.text = None
            self.mastermaster.ASFive.text = None
            self.mastermaster.ASSix.text = None
            self.mastermaster.ASSeven.text = None
            self.mastermaster.ASEight.text = None
            self.mastermaster.ASNine.text = None
        else:
            self.mastermaster.ASThree.text = self.awokenSkills[2]

        if self.awokenSkills[3] is None:
            self.mastermaster.ASFour.text = None
            self.mastermaster.ASFive.text = None
            self.mastermaster.ASSix.text = None
            self.mastermaster.ASSeven.text = None
            self.mastermaster.ASEight.text = None
            self.mastermaster.ASNine.text = None
        else:
            self.mastermaster.ASFour.text = self.awokenSkills[3]

        if self.awokenSkills[4] is None:
            self.mastermaster.ASFive.text = None
            self.mastermaster.ASSix.text = None
            self.mastermaster.ASSeven.text = None
            self.mastermaster.ASEight.text = None
            self.mastermaster.ASNine.text = None
        else:
            self.mastermaster.ASFive.text = self.awokenSkills[4]

        if self.awokenSkills[5] is None:
            self.mastermaster.ASSix.text = None
            self.mastermaster.ASSeven.text = None
            self.mastermaster.ASEight.text = None
            self.mastermaster.ASNine.text = None
        else:
            self.mastermaster.ASSix.text = self.awokenSkills[5]

        if self.awokenSkills[6] is None:
            self.mastermaster.ASSeven.text = None
            self.mastermaster.ASEight.text = None
            self.mastermaster.ASNine.text = None
        else:
            self.mastermaster.ASSeven.text = self.awokenSkills[6]

        if self.awokenSkills[7] is None:
            self.mastermaster.ASEight.text = None
            self.mastermaster.ASNine.text = None
        else:
            self.mastermaster.ASEight.text = self.awokenSkills[7]

        if self.awokenSkills[8] is None:
            self.mastermaster.ASNine.text = None
        else:
            self.mastermaster.ASNine.text = self.awokenSkills[8]

        if self.currentMonster.LatentSkillOne is None:
            self.mastermaster.LSOne.text = None
            self.mastermaster.LSTwo.text = None
            self.mastermaster.LSThree.text = None
            self.mastermaster.LSFour.text = None
            self.mastermaster.LSFive.text = None
            self.mastermaster.LSSix.text = None
        else:
            self.mastermaster.LSOne.text = self.currentMonster.LatentSkillOne

        if self.currentMonster.LatentSkillTwo is None:
            self.mastermaster.LSTwo.text = None
            self.mastermaster.LSThree.text = None
            self.mastermaster.LSFour.text = None
            self.mastermaster.LSFive.text = None
            self.mastermaster.LSSix.text = None
        else:
            self.mastermaster.LSTwo.text = self.currentMonster.LatentSkillTwo

        if self.currentMonster.LatentSkillThree is None:
            self.mastermaster.LSThree.text = None
            self.mastermaster.LSFour.text = None
            self.mastermaster.LSFive.text = None
            self.mastermaster.LSSix.text = None
        else:
            self.mastermaster.LSThree.text = self.currentMonster.LatentSkillThree

        if self.currentMonster.LatentSkillFour is None:
            self.mastermaster.LSFour.text = None
            self.mastermaster.LSFive.text = None
            self.mastermaster.LSSix.text = None
        else:
            self.mastermaster.LSFour.text = self.currentMonster.LatentSkillFour

        if self.currentMonster.LatentSkillFive is None:
            self.mastermaster.LSFive.text = None
            self.mastermaster.LSSix.text = None
        else:
            self.mastermaster.LSFive.text = self.currentMonster.LatentSkillFive

        if self.currentMonster.LatentSkillSix is None:
            self.mastermaster.LSSix.text = None
        else:
            self.mastermaster.LSSix.text = self.currentMonster.LatentSkillSix

        self.mastermaster.portrait.update(self.currentMonster)
        
class PlayerCollection:
    def __init__(self, master):
        #logger
        self.logger = logging.getLogger("Padification.ui.PlayerCollection.PlayerCollection")
        #Creates globals 
        
        global k
        global buttons
        global selectedMonster


        selectedMonster = None
        self.MonsterResults = None
        self.bgSearchText = 'Enter Monster ID or Name'
        self.pds = master.PADsql
        self.master = master
        self.startMonster = 0
        

        self.displayWishlist = 0

        buttons =[]
        self.currentPage = 1

        k = None
        self.k = k
        #self.__UpdateMonsters()

        #1: Creates a builder
        self.builder = builder = pygubu.Builder()

        #2: Loads an ui file
        builder.add_from_file('src/ui/PlayerCollection.ui')

        #3: Creates the widget using a master as parent
        self.mainwindow = builder.get_object('frmPlayerCollection')
        builder.connect_callbacks(self)
        
        self.imgTitleImage = PhotoImage(file = "Resource/PAD/Images/Padification Logo.png")
        self.builder.get_object('lblTitleImage').config(image = self.imgTitleImage)
        
        self.portrait = CustomWidgets.MonsterStatTooltip(self.builder.get_object("canMonsterSummary"))
        self.typeOne = ToolTip.ToolTip(self.builder.get_object("canType1"), None)
        self.typeTwo = ToolTip.ToolTip(self.builder.get_object("canType2"), None)
        self.typeThree = ToolTip.ToolTip(self.builder.get_object("canType3"), None)
        self.ASOne = ToolTip.ToolTip(self.builder.get_object("canASOne"), None)
        self.ASTwo = ToolTip.ToolTip(self.builder.get_object("canASTwo"), None)
        self.ASThree = ToolTip.ToolTip(self.builder.get_object("canASThree"), None)
        self.ASFour = ToolTip.ToolTip(self.builder.get_object("canASFour"), None)
        self.ASFive = ToolTip.ToolTip(self.builder.get_object("canASFive"), None)
        self.ASSix = ToolTip.ToolTip(self.builder.get_object("canASSix"), None)
        self.ASSeven = ToolTip.ToolTip(self.builder.get_object("canASSeven"), None)
        self.ASEight = ToolTip.ToolTip(self.builder.get_object("canASEight"), None)
        self.ASNine = ToolTip.ToolTip(self.builder.get_object("canASNine"), None)
        self.LSOne = ToolTip.ToolTip(self.builder.get_object("canLatentOne"), None)
        self.LSTwo = ToolTip.ToolTip(self.builder.get_object("canLatentTwo"), None)
        self.LSThree = ToolTip.ToolTip(self.builder.get_object("canLatentThree"), None)
        self.LSFour = ToolTip.ToolTip(self.builder.get_object("canLatentFour"), None)
        self.LSFive = ToolTip.ToolTip(self.builder.get_object("canLatentFive"), None)
        self.LSSix = ToolTip.ToolTip(self.builder.get_object("canLatentSix"), None)

        self.AttributeImages = dict()
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

    def pageOne(self):
        if k is None:
            self.startMonster = 0
            self.currentPage = 1
            self.__RemoveInformation()
            self.onSearchClick()
        else:
            self.startMonster = 50 * (self.currentPage - 1)
            self.k = k
            self.__UpdateInformation()
            self.populateList()
        

    def onAddFromWishlistClick(self):

        for a in self.MonsterResults:
            if a.InstanceID == selectedMonster:
                teams = self.pds.selectTeamInstance(dreamteam = self.displayWishlist)
                for i in teams:
                    self.SelectedTeam = PADMonster.Team(self.pds, i)

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

                a.WishList = 0
                b = a.getSaveDict()

                global k
                k = None

                self.pds.saveMonster(b)


                self.__RemoveInformation()
                self.startMonster -= self.count
                self.onSearchClick()
                break

    def populateList(self):
        '''Populates the player collection list'''
        if k is None:
            self.builder.get_object("btnFavorite").config(state = DISABLED)
            self.builder.get_object("btnEdit").config(state = DISABLED)
            self.builder.get_object("btnRemove").config(state = DISABLED)
            self.builder.get_object("btnUnfavorite").config(state = DISABLED)
            self.builder.get_object("btnAddFromWishlist").config(state = DISABLED)
        
        self.builder.get_object("canMonsterList").delete("All")

        self.container = self.builder.get_object('canMonsterList')

        for i in self.container.grid_slaves():
            i.grid_forget()
        
        allMonsters = self.master.PADsql.selectMonsterInstance()
        self.assistants = []
        for i in self.MonsterResults:
            for y in allMonsters:
                if i.InstanceID == y["AssistMonsterID"]:
                    self.assistants.append(y["InstanceID"])
                    break
        #Creates a graphical list of self.monsters
        buttons = []
        self.buttons = buttons = []
        self.count = 0
        for i in self.MonsterResults:
            if self.startMonster < 50 * self.currentPage and ((self.startMonster >= 50 * (self.currentPage - 1)) and not(self.startMonster == len(self.MonsterResults))):
                self.buttons.append(MonsterFrame(self.container, self.builder, self.startMonster, self.MonsterResults[self.startMonster], self.buttons, self.pds, self.count, self))
                self.buttons[self.count].monbut.grid(row=self.count // 10,column = self.count % 10)
                if self.MonsterResults[self.startMonster].InstanceID == selectedMonster:
                    self.buttons[self.count].monbut.config(relief = SUNKEN)
                
                for c in self.assistants:
                    if c == self.buttons[self.count].currentMonster.InstanceID:
                        self.buttons[self.count].monbut.config(highlightbackground= "#b2a89d",highlightcolor="#b2a89d",highlightthickness=3)
                self.buttons[self.count].builder.get_object('lblMonsterBrief').config(text = 'LVL:' + str(self.MonsterResults[self.startMonster].Level)+ '\nID: ' + str(self.MonsterResults[self.startMonster].MonsterClassID))
                self.count += 1
                self.startMonster += 1

        self.pages = (len(self.MonsterResults) // 50) + 1
        if len(self.MonsterResults) == 0:
            self.pages = 1
        elif len(self.MonsterResults) % 50 == 0:
            self.pages -= 1

        if self.currentPage > self.pages:
            self.prev()

        if self.pages > self.currentPage:
            self.builder.get_object("btnNext").config(state = NORMAL)
        elif self.pages <= self.currentPage:
            self.builder.get_object("btnNext").config(state = DISABLED)

        if self.currentPage == 1:
            self.builder.get_object("btnPrev").config(state = DISABLED)
            
        self.builder.get_variable('lblPageNumber').set( "    / " + str(self.pages))
        self.builder.get_variable('varPageEnt').set(str(self.currentPage))

        self.container.config(height=(len(self.container.grid_slaves()) // 2) * 30)

    def addToFavorites(self):
        self.edit = Monster(self.pds.selectMonsterInstance(selectedMonster, wishlist = self.displayWishlist)[0])

        self.edit.Favorites = 1
        self.buttons[k].monbut.config(bg = 'Yellow')
        self.buttons[k].builder.get_object('lblMonsterBrief').config(bg = 'Yellow')
        self.pds.saveMonster(self.edit.getSaveDict())
        self.buttons[k].currentMonster = Monster((self.pds.selectMonsterInstance(selectedMonster, wishlist = self.displayWishlist))[0])
        self.buttons[k].clickMe(self)
        self.MonsterResults[k + ((self.currentPage - 1) * 50)] = Monster((self.pds.selectMonsterInstance(selectedMonster, wishlist = self.displayWishlist))[0])
        pass

    def removeFromFavorites(self):
        self.edit = Monster((self.pds.selectMonsterInstance(selectedMonster, wishlist = self.displayWishlist))[0])

        self.edit.Favorites = 0
        self.buttons[k].monbut.config(bg = '#f0f0f0')
        self.buttons[k].builder.get_object('lblMonsterBrief').config(bg = '#f0f0f0')
        self.pds.saveMonster(self.edit.getSaveDict())
        self.buttons[k].currentMonster = Monster((self.pds.selectMonsterInstance(selectedMonster, wishlist = self.displayWishlist))[0])
        self.buttons[k].clickMe(self)
        self.MonsterResults[k + ((self.currentPage - 1) * 50)] = Monster((self.pds.selectMonsterInstance(selectedMonster, wishlist = self.displayWishlist))[0])
        pass

    def onWishlistClick(self):
        global k
        global selectedMonster
        self.displayWishlist = 1
        self.currentPage = 1
        k = None
        selectedMonster = None
        #for i in range(0, (len(self.buttons) - 1)):
        #    self.buttons[i].monbut.config(relief = FLAT)
        self.builder.get_object("btnPrev").config(state = DISABLED)
        self.startMonster = 0
        self.builder.get_object("btnWishlist").config(state = DISABLED)
        self.builder.get_object("btnMonsterList").config(state = NORMAL)
        self.__RemoveInformation()
        self.onSearchClick()

    def onMonsterListClick(self):
        self.displayWishlist = 0
        global k
        global selectedMonster
        self.currentPage = 1
        k = None
        selectedMonster = None
        #for i in range(0, (len(self.buttons) - 1)):
        #    self.buttons[i].monbut.config(relief = FLAT)
        self.builder.get_object("btnPrev").config(state = DISABLED)
        self.startMonster = 0
        self.builder.get_object("btnMonsterList").config(state = DISABLED)
        self.builder.get_object("btnWishlist").config(state = NORMAL)
        self.__RemoveInformation()
        self.onSearchClick()

    def onEditMonsterClick(self):
        self.k = k
        self.master.monsterEdit.receiveInstanceID(selectedMonster, self.displayWishlist)
        self.master.showEditMonster()

    def onHomeClick(self, event):
        self.displayWishlist = 0
        global k
        k = None
        self.builder.get_object("btnWishlist").config(state = NORMAL)
        self.builder.get_object("btnMonsterList").config(state = DISABLED) 
        self.master.showHomeScreen()

    def onCollectionClick(self, event):
        self.master.showPlayerCollection()

    def onBookClick(self, event):
        self.displayWishlist = 0
        global k
        k = None
        self.builder.get_object("btnWishlist").config(state = NORMAL)
        self.builder.get_object("btnMonsterList").config(state = DISABLED) 
        self.master.showMonsterBook()

    def onTeamsClick(self, event):
        self.displayWishlist = 0
        global k
        k = None
        self.builder.get_object("btnWishlist").config(state = NORMAL)
        self.builder.get_object("btnMonsterList").config(state = DISABLED) 
        self.master.showTeamBrowser()

    def onCommunityClick(self, event):
        self.displayWishlist = 0
        global k
        k = None
        self.builder.get_object("btnWishlist").config(state = NORMAL)
        self.builder.get_object("btnMonsterList").config(state = DISABLED) 
        pass

    def onTeamRankingClick(self, event):
        self.displayWishlist = 0
        global k
        k = None
        self.builder.get_object("btnWishlist").config(state = NORMAL)
        self.builder.get_object("btnMonsterList").config(state = DISABLED) 
        pass

    def onOptionsClick(self, event):
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
        #global k
        #k = None
        self.currentPage += 1
        if self.currentPage == self.pages:
            self.builder.get_object("btnNext").config(state = DISABLED)
        #self.__RemoveInformation()
        self.populateList()

    def prev(self):
        #for i in range(0, (len(self.buttons) - 1)):
        #    self.buttons[i].monbut.config(relief = FLAT)
        self.builder.get_object("btnNext").config(state = NORMAL)
        self.currentPage -= 1
        #global k
        #k = None
        self.startMonster -= self.count + 50
        if self.currentPage == 1:
            self.builder.get_object("btnPrev").config(state = DISABLED)
        #self.__RemoveInformation()
        self.populateList()

    def RemoveMonster(self):
        '''Removes the selected monster from the DB and all its references, occurs when remove monster button is clicked'''

        tkMessageBox = messagebox.askokcancel("Confirm", "Are your sure you want to remove this monster? The selected monster will be removed from all teams and assist positions.")

        if tkMessageBox:
            #Removes monster instance from DB
            teams = self.pds.selectTeamInstance(dreamteam = self.displayWishlist)
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
            

            global k

            k = None

            for i in self.MonsterResults:
                check = i
                if check.AssistMonsterID == selectedMonster:
                    check.AssistMonsterID = None
                    self.pds.saveMonster(check.getSaveDict())

            self.pds.deleteMonster(selectedMonster)

            #self.__UpdateMonsters()
            self.__RemoveInformation()
            self.startMonster -= self.count
            self.onSearchClick()

    def __UpdateInformation(self):
        global selectedMonster

        self.monster = self.pds.selectMonsterInstance(selectedMonster, wishlist = self.displayWishlist)
        self.monster = PADMonster.Monster(self.monster[0])
        self.builder.get_object("lblHP").config(text = "HP: " + str(self.monster.TotalHP))
        self.builder.get_object("lblATK").config(text = "ATK: " + str(self.monster.TotalATK))
        self.builder.get_object("lblRCV").config(text = "RCV: " + str(self.monster.TotalRCV))
        
        self.aSListImg = []
        self.builder.get_object("canASOne").delete("all")
        self.builder.get_object("canASTwo").delete("all")
        self.builder.get_object("canASThree").delete("all")
        self.builder.get_object("canASFour").delete("all")
        self.builder.get_object("canASFive").delete("all")
        self.builder.get_object("canASSix").delete("all")
        self.builder.get_object("canASSeven").delete("all")
        self.builder.get_object("canASEight").delete("all")
        self.builder.get_object("canASNine").delete("all")

        if self.monster.ASListID is None:
            pass
        else:
        #Creates the photo image for the selected monster's awoken awoken skills
            self.aSList = self.pds.getAwokenSkillList(self.monster.MonsterClassID)

            for i in range(1, len(self.aSList)):
                if i <= self.monster.SkillsAwoke:
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

            self.builder.get_object("canASOne").create_image(2,2, image = self.aSListImg[0], anchor = tk.NW)
            self.builder.get_object("canASTwo").create_image(2,2, image = self.aSListImg[1], anchor = tk.NW)
            self.builder.get_object("canASThree").create_image(2,2, image = self.aSListImg[2], anchor = tk.NW)
            self.builder.get_object("canASFour").create_image(2,2, image = self.aSListImg[3], anchor = tk.NW)
            self.builder.get_object("canASFive").create_image(2,2, image = self.aSListImg[4], anchor = tk.NW)
            self.builder.get_object("canASSix").create_image(2,2, image = self.aSListImg[5], anchor = tk.NW)
            self.builder.get_object("canASSeven").create_image(2,2, image = self.aSListImg[6], anchor = tk.NW)
            self.builder.get_object("canASEight").create_image(2,2, image = self.aSListImg[7], anchor = tk.NW)
            self.builder.get_object("canASNine").create_image(2,2, image = self.aSListImg[8], anchor = tk.NW)

        pass

    def __RemoveInformation(self):
        '''Removes the information in the monster summary, runs during RemoveMonster'''
        
        self.builder.get_object("btnFavorite").config(state = DISABLED)
        self.builder.get_object("btnEdit").config(state = DISABLED)
        self.builder.get_object("btnRemove").config(state = DISABLED)
        self.builder.get_object("btnUnfavorite").config(state = DISABLED)
        self.builder.get_object("btnAddFromWishlist").config(state = DISABLED)

        #self.portrait.photoImage = None
        self.typeOne.text = None
        self.typeTwo.text = None
        self.typeThree.text = None
        self.ASOne.text = None
        self.ASTwo.text = None
        self.ASThree.text = None
        self.ASFour.text = None
        self.ASFive.text = None
        self.ASSix.text = None
        self.ASSeven.text = None
        self.ASEight.text = None
        self.ASNine.text = None

        for i in self.builder.get_object("canEvoTree").grid_slaves():
            i.grid_forget()

        #self.builder.get_object("canMonsterSummary").unbind("<Enter>")
        #self.builder.get_object("canMonsterSummary").unbind("<Leave>")
        #self.builder.get_object("canMonsterSummary").unbind("<ButtonPress>")
        #self.builder.get_object("canMonsterSummary").delete('all')
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
        self.builder.get_object("canLatentOne").delete('all')
        self.builder.get_object("canLatentTwo").delete('all')
        self.builder.get_object("canLatentThree").delete('all')
        self.builder.get_object("canLatentFour").delete('all')
        self.builder.get_object("canLatentFive").delete('all')
        self.builder.get_object("canLatentSix").delete('all')

    def onSearchBarFocusIn(self, event):
        #Clears Search Bar on focus
        if self.builder.get_variable("SearchBar").get() == self.bgSearchText:
            self.builder.get_variable("SearchBar").set("")
        
    def onSearchBarFocusOut(self, event):
        #Populates empty Search bar on focus out
        if self.builder.get_variable("SearchBar").get() == "":
            self.builder.get_variable("SearchBar").set(self.bgSearchText)

    def onSearchClick(self, event = None):
        ############################
        ##### PARSE SEARCH BAR #####
        ############################
        global selectedMonster
        selectedMonster = None
        self.__RemoveInformation()

        search = self.builder.get_variable("SearchBar").get()
        if search == self.bgSearchText:
            search = ""

        if "," in search:
            search = le("(" + search + ")")
        elif search.isnumeric():
            search = int(search)

        self.MonsterResults = []
        self.monsters = self.master.PADsql.selectMonsterInstance(search, byInstanceID = False, wishlist = self.displayWishlist)



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
        ##### ADD FILTERED self.monsters TO RESULTS #####
        ############################################
        for i in self.monsters:
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
        self.startMonster = 0
        self.currentPage = 1
        self.populateList()
        self.builder.get_object("lblResults").config(text = str(len(self.MonsterResults)) + " of " + str(len(self.pds.selectMonsterInstance(wishlist = self.displayWishlist))))

    def onPageEnter(self, event):
        value = self.builder.get_variable("varPageEnt").get()
        
        while len(value) >= 1 and value[0] == '0':
            value = value.replace('0', '', 1)

        if len(value) == 0:
            value = '1'
        elif int(value) > self.pages:
            value = str(self.pages)
        
        self.builder.get_variable("varPageEnt").set(value)
        self.currentPage = int(value)
        self.startMonster = (self.currentPage - 1) * 50
        self.populateList()


    def validatePageEntry(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        if text in "0123456789\b" and len(value_if_allowed) < 4:
            return True
        else:
            return False

    def validateTwoDigit(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):

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