#!/USR/BIN/ENV PYTHON 3.5
#   NAME:    Billy Gale 
#   DATE:    06/28/17
#   PURPOSE: MonsterBook Functionality
#
#
# 2017-07-03 - WG - v1.0 - Monster Book able to search and Displays a maximum of 50 results on one page.
# 2017-07-12 - WG - v1.1 - Monster book displays all information pertaining to monsters, Shows 7 results per page. Filters Are Added, Clear Filters also.
# 2017-07-13 - WG - v1.2 - Monster Book Has Tool Tips, Portrait Images Tool Tip and Fixed Memory Leak of Evolution Tree Frames not Being Deleted.

import tkinter as tk
import pygubu
import math
from PADMonster import Monster
from tkinter import messagebox as mb
from tkinter import *
from ast import literal_eval as le
from PIL import Image
from PIL import ImageTk
from idlelib import ToolTip
from CustomWidgets import *
import re
import logging

class MonsterBook():
    """Displays Home Screen Frame and widgets"""
    def __init__(self, master):
        #logger
        self.logger = logging.getLogger("Padification.ui.MonsterBook")
        #Constants
        self.bgSearchText = "Enter Monster ID or Name"
        self.RESULTSPERPAGE = 7

        #TK Variables
        self.master = master
        self.builder = pygubu.Builder()
        self.builder.add_from_file('src/ui/MonsterBook.ui')
        self.mainwindow = self.builder.get_object('frmMonsterBook', master)
        self.resultsFrame = self.builder.get_object('canMonsterList')
        self.canEvoFrame = self.builder.get_object('canEvoTree')
        self.builder.connect_callbacks(self)

        #Monster Info Variables
        self.MonstertypeOne = None
        self.MonstertypeTwo = None
        self.MonstertypeThree = None
        self.ASOne = None
        self.ASTwo = None
        self.ASThree = None
        self.ASFour = None
        self.ASFive = None
        self.ASSix = None
        self.ASSeven = None
        self.ASEight = None
        self.ASNine = None
        self.TTip = None

        #Results Variables
        self.evoFrames = []
        self.MonsterResults = []
        self.MonsterFrames = []
        self.curPage = 1
        self.Results = 0
        self.maxPage = 1
        self.monster = None
        self.thumbnail = None
        self.portraitImage = None
        self.portrait = None
        self.Tooltips = []
        self.PortraitTooltip = ImageTooltip(self.builder.get_object("canMonsterSummary"), self.portrait)

        #Filter Images
        ##### Atttribute Images #####
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

        ##### Frame Creation #####
        for i in range( 0 , self.RESULTSPERPAGE ):
            self.MonsterFrames.append(MonsterFrame(self.resultsFrame, self))

    def update(self):
        """Updates results Shown on Monster Book"""
        for i in self.resultsFrame.grid_slaves():
            i.grid_forget()

        #Populate Frame with results in range
        start = (self.curPage - 1) * self.RESULTSPERPAGE
        end = self.curPage * self.RESULTSPERPAGE
        if end > len(self.MonsterResults):
            end = len(self.MonsterResults)
        count = 0
        for i in range( start , end ):
            self.MonsterFrames[count].update(self.MonsterResults[i])
            if count == 0:
                self.MonsterFrames[count].frame.grid(row = count, padx = 9, pady = 4, sticky=tk.S)
            else:
                self.MonsterFrames[count].frame.grid(row = count, padx = 9)
            count += 1

        self.builder.get_object("lblPageNumber").config(text = "       / " + str(self.maxPage))
        self.builder.get_variable("varPageEnt").set(str(self.curPage))

    def nextPage(self, event):
        if self.curPage < self.maxPage:
            self.curPage += 1
            self.update()
            self.builder.get_variable("varPageEnt").set(str(self.curPage))
        elif self.curPage == self.maxPage and self.maxPage != 1:
            self.curPage = 1
            self.update()
            self.builder.get_variable("varPageEnt").set(str(self.curPage))

    def prevPage(self, event):
        if self.curPage > 1:
            self.curPage -= 1
            self.update()
            self.builder.get_variable("varPageEnt").set(str(self.curPage))
        elif self.curPage == 1 and self.maxPage != 1:
            self.curPage = self.maxPage
            self.update()
            self.builder.get_variable("varPageEnt").set(str(self.curPage))
    
    def clearInfo(self):
        """Clears Monster SUmmary Info"""
        self.monster = None
        self.thumbnail = None
        self.builder.get_object("canMonsterSummary")
        self.builder.get_object("lblIDName").config(text = "")
        self.builder.get_object("lblRarity").config(text= "")
        self.builder.get_object("lblMaxLevel").config(text= "----")
        self.builder.get_object("lblMaxHP").config(text= "----")
        self.builder.get_object("lblMaxATK").config(text= "----")
        self.builder.get_object("lblMaxRCV").config(text= "----")
        self.builder.get_object("lblMinHP").config(text= "----")
        self.builder.get_object("lblMinATK").config(text= "----")
        self.builder.get_object("lblMinRCV").config(text= "----")
        self.builder.get_object("lblLeaderSkillName").config(text = 'None')
        self.builder.get_object("lblLeaderSkillDesc").config(text = '')
        self.builder.get_object("lblActiveSkillName").config(text = 'None')
        self.builder.get_object("lblActiveSkillDesc").config(text = '')
        self.builder.get_object("lblActiveSkillMinCooldown").config(text = "Min CD: --")
        self.builder.get_object("lblActiveSkillMaxCooldown").config(text = "Max CD: --")

        for i in ["MonsterTypeOne", "MonsterTypeTwo", "MonsterTypeThree",
                  "ASOne", "ASTwo", "ASThree", "ASFour", "ASFive", "ASSix", "ASSeven", "ASEight", "ASNine"]:
            setattr(self, i, None)


    def showInfo(self,monster, thumbnail):
        """Shows The Information of the Selected monster"""
        #########################
        #### Delete ToolTips ####
        #########################

        self.Tooltips = []

        #########################
        #### UPDATE LABELS #####
        ########################
        self.monster = monster
        self.thumbnail = thumbnail
        self.builder.get_object("canMonsterSummary").create_image(10,10, image = self.thumbnail, anchor = tk.NW)

        self.portraitImage = Image.open("Resource/PAD/Images/portraits/"+ str(self.monster.MonsterClassID) + ".jpg")
        self.portrait = ImageTk.PhotoImage(self.portraitImage, self.portrait)
        self.PortraitTooltip.PhotoImage = self.portrait
        

        self.builder.get_object("lblIDName").config(text = str(monster.MonsterClassID) + " - " + monster.MonsterName)
        rarity = ""
        for i in range(0,monster.Rarity):
            rarity += '\u2605'
        self.builder.get_object("lblRarity").config(text= rarity, foreground= 'yellow')
        self.builder.get_object("lblMaxLevel").config(text = str(monster.MaxLevel))
        self.builder.get_object("lblMaxHP").config(text = str(monster.MaxHP))
        self.builder.get_object("lblMaxATK").config(text = str(monster.MaxATK))
        self.builder.get_object("lblMaxRCV").config(text = str(monster.MaxRCV))
        self.builder.get_object("lblMinHP").config(text = str(monster.MinHP))
        self.builder.get_object("lblMinATK").config(text = str(monster.MinATK))
        self.builder.get_object("lblMinRCV").config(text = str(monster.MinRCV))

        ######################################
        ##### UPDATE MONSTER TYPE IMAGES #####
        ######################################
        count = 1
        for i in ["MonsterTypeOne", "MonsterTypeTwo", "MonsterTypeThree"]:
            self.builder.get_object("canType" + str(count)).unbind("<Enter>")
            self.builder.get_object("canType" + str(count)).unbind("<Leave>")
            self.builder.get_object("canType" + str(count)).unbind("<ButtonPress>")
            if getattr(monster, i) != None:
                setattr(self, i, PhotoImage(file = 'Resource/PAD/Images/Types/' + getattr(monster, i) + ".png") )
                self.builder.get_object("canType" + str(count)).create_image(2,2, image = getattr(self, i), anchor = tk.NW)
                self.Tooltips.append(ToolTip.ToolTip(self.builder.get_object("canType" + str(count)) , getattr(monster, i)))
            else:
                setattr(self, i, None)
            count += 1

        ######################################
        ##### UPDATE AWOKEN SKILL IMAGES #####
        ######################################
        AwokenSkills = self.master.PADsql.getAwokenSkillList(monster.MonsterClassID)
        count = 1
        for i in ["ASOne", "ASTwo", "ASThree", "ASFour", "ASFive", "ASSix", "ASSeven", "ASEight", "ASNine"]:
            self.builder.get_object("can" + i).unbind("<Enter>")
            self.builder.get_object("can" + i).unbind("<Leave>")
            self.builder.get_object("can" + i).unbind("<ButtonPress>")
            if AwokenSkills[count] != None:
                setattr(self,i, PhotoImage(file = 'Resource/PAD/Images/Awoken Skills/' + AwokenSkills[count] + ".png"))
                self.builder.get_object("can" + i).create_image(2,2, image = getattr(self, i), anchor = tk.NW)
                self.Tooltips.append(ToolTip.ToolTip(self.builder.get_object("can" + i) , AwokenSkills[count]))
            else:
                setattr(self, i, None)
            count += 1
            
        ####################################
        ##### UPDATE SKILL INFORMATION #####
        ####################################
        if monster.ActiveSkillName != None:
            self.builder.get_object("lblActiveSkillName").config(text = monster.ActiveSkillName)
            self.builder.get_object("lblActiveSkillDesc").config(text = monster.ActiveSkillDesc)
            self.builder.get_object("lblActiveSkillMaxCooldown").config(text = "Max CD: " + str(monster.ActiveSkillMaxCoolDown))
            self.builder.get_object("lblActiveSkillMinCooldown").config(text = "Min CD: " + str(monster.ActiveSkillMaxCoolDown - monster.ActiveSkillMaxLevel + 1))
        else:
            self.builder.get_object("lblActiveSkillName").config(text = 'None')
            self.builder.get_object("lblActiveSkillDesc").config(text = '')
            self.builder.get_object("lblActiveSkillMinCooldown").config(text = "Min CD: --")
            self.builder.get_object("lblActiveSkillMaxCooldown").config(text = "Max CD: --")

        if monster.LeaderSkillName != None:
            self.builder.get_object("lblLeaderSkillName").config(text = monster.LeaderSkillName)
            self.builder.get_object("lblLeaderSkillDesc").config(text = monster.LeaderSkillDesc)
        else:
            self.builder.get_object("lblLeaderSkillName").config(text = 'None')
            self.builder.get_object("lblLeaderSkillDesc").config(text = '')
        
        ###############################
        ##### SHOW EVOLUTION TREE #####
        ###############################
        evoTree = self.master.PADsql.getEvolutionTree(monster.MonsterClassID)
        for i in self.evoFrames:
            i.EvoFrame.grid_forget()
            i.EvoFrame.destroy()

        self.evoFrames = []
        self.canEvoFrame
        evocol = 0
        for i in evoTree:
            evorow = 0
            for o in i:
                if o == None:
                    evorow += 1
                    continue
                frame = MonEvoFrame(self.canEvoFrame, self)
                self.evoFrames.append(frame)
                if isinstance(o, int):
                    frame.update(Monster(self.master.PADsql.selectMonsterClass(o)[0]))
                else:
                    if o != None:
                        frame.update(Monster(self.master.PADsql.selectMonsterClass(o[0])[0]))
                frame.EvoFrame.grid(column = evocol, row = evorow, padx = 4)
                evorow += 1
            evocol +=1

    def onSearchClick(self, event):
        ############################
        ##### PARSE SEARCH BAR #####
        ############################
        search = self.builder.get_variable("SearchBar").get()
        if search == self.bgSearchText:
            search = ""

        if search.isnumeric():
            search = int(search)
        elif re.match(r"(\d+,\s*\d+)", search):
            search = le("(" + search + ")")
        

        self.MonsterResults = []
        monsters = self.master.PADsql.selectMonsterClass(search)

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

        self.logger.info("Primary Attributes =", str(PriAttributes) + 
                         "\n" +self.builder.get_variable("varANDOR").get() + 
                         "\nSecondary Attributes =" + str(SecAttributes) + 
                         "\nTypes =" + str(TypeFilters))

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
        self.maxPage = math.ceil(len(self.MonsterResults) / self.RESULTSPERPAGE)
        self.curPage = 1
        self.update()
        self.builder.get_object("lblResults").config(text = str(len(self.MonsterResults)) + " Results Found.")
    
    def onSearchBarFocusIn(self, event):
        #Clears Search Bar on focus
        if self.builder.get_variable("SearchBar").get() == self.bgSearchText:
            self.builder.get_variable("SearchBar").set("")
        
    def onSearchBarFocusOut(self, event):
        #Populates empty Search bar on focus out
        if self.builder.get_variable("SearchBar").get() == "":
            self.builder.get_variable("SearchBar").set(self.bgSearchText)
    
    def onPageEnter(self, event):
        value = self.builder.get_variable("varPageEnt").get()

        while len(value) >= 1 and value[0] == '0':
            value = value.replace('0', '', 1)

        if len(value) == 0:
            value = '1'
        elif int(value) > self.maxPage:
            value = str(self.maxPage)

        self.builder.get_variable("varPageEnt").set(value)
        self.curPage = int(value)
        self.update()
        #print(self.builder.get_variable("varPageEnt").get())

    def validatePageEntry(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):

        if value_if_allowed == "":
            return True
        if not value_if_allowed.isnumeric():
            return False
        if not len(value_if_allowed) < 4:
            return False
        return True

    def validateTwoDigit(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):

        if value_if_allowed == "":
            return True
        if not value_if_allowed.isnumeric():
            return False
        if not len(value_if_allowed) < 3:
            return False
        return True

    def onHomeClick(self,event):
        self.master.showHomeScreen()

    def onCollectionClick(self,event):
        self.master.showPlayerCollection()

    def onBookClick(self,event):
        pass

    def onTeamsClick(self,event):
        self.master.showTeamBrowser()

    def onCommunityClick(self,event):
        pass

    def onTeamRankingClick(self,event):
        pass

    def onOptionsClick(self,event):
        self.master.showAccountOptions()

    def onAddToCollectionClick(self, event):
        if isinstance(self.monster, Monster):
            self.monster.WishList = self.builder.get_variable("varWishList").get()
            self.monster.setLevel(int(self.removeLeadingZeros(self.builder.get_variable("varSetLevel").get())))
            self.monster.setPlusHP(int(self.removeLeadingZeros(self.builder.get_variable("varPlusHP").get())))
            self.monster.setPlusATK(int(self.removeLeadingZeros(self.builder.get_variable("varPlusATK").get())))
            self.monster.setPlusRCV(int(self.removeLeadingZeros(self.builder.get_variable("varPlusRCV").get())))
            self.monster.setSkillsAwoke(int(self.removeLeadingZeros(self.builder.get_variable("varAwakens").get())))
            self.monster.setSkillLevel(int(self.removeLeadingZeros(self.builder.get_variable("varSkillLevel").get())))

            if mb.askokcancel("Add Monster","Are you sure you want to add " + str(self.monster.MonsterName) ):
                self.master.PADsql.saveMonster(self.monster.getSaveDict())

    def removeLeadingZeros(self, string):
        while len(string) > 1 and string[0] == '0':
            string = string.replace("0", '', 1)
        return string

    def clearFilters(self):
        """Deselect All Filters"""
        for i in [  "TypeAttacker", "TypeAwakenMaterial", "TypeBalanced",
                    "TypeDevil", "TypeDragon", "TypeEnhanceMaterial",
                    "TypeEvoMaterial", "TypeGod", "TypeHealer",
                    "TypeMachine", "TypePhysical", "TypeRedeemableMaterial",
                    "PriFire", "PriWater", "PriWood", "PriLight", "PriDark",
                    "SecFire", "SecWater", "SecWood", "SecLight", "SecDark" ]:
            self.builder.get_variable(i).set("")
        self.builder.get_variable("SearchBar").set(self.bgSearchText)
        self.master.focus()

class MonsterFrame():
    def __init__(self, master, mbobject):
        #logger
        self.logger = logging.getLogger("Padification.ui.MonsterBook.MonsterFrame")
        #TK Variables
        self.Monbookobject = mbobject
        self.master = master
        self.builder = pygubu.Builder()
        self.builder.add_from_file('src/ui/MonsterBook.ui')
        self.frame = self.builder.get_object('MonsFrame', master)
        self.FrameLabel = self.builder.get_object('FrameLabel')
        self.builder.connect_callbacks(self)

        #Variables
        self.MonstertypeOne = None
        self.MonstertypeTwo = None
        self.MonstertypeThree = None
        self.monster = None
        self.thumbnail = None

    def update(self, monster):
        self.monster = monster
        self.thumbnail = PhotoImage(file = 'Resource/PAD/Images/thumbnails/' + str(self.monster.MonsterClassID) + ".png")
        self.FrameLabel.create_image(2,2, image = self.thumbnail, anchor = tk.NW)

        #Label Configurations
        self.builder.get_object("lblMonsterID").config(text=str(self.monster.MonsterClassID))

        self.builder.get_object("lblMonsterName").config(text=str(self.monster.MonsterName))
        rarity = ""
        for i in range(0,self.monster.Rarity):
            rarity += '\u2605'
        self.builder.get_object("lblMonsterRarity").config(text= rarity, foreground= 'yellow')

        #Background Colors
        colors = {'Fire' : '#ff9966', 'Water' : '#99bbdd', 'Wood' : '#88ee77', 'Light' : '#ffff77', 'Dark' : '#ee99ee'}
        self.frame.config(bg = colors[self.monster.PriAttribute])
        for i in self.frame.grid_slaves():
            if i == self.builder.get_object("lblMonsterRarity"):
                continue
            i.config(background = colors[self.monster.PriAttribute])
        
        #MonsterType image loader.
        count = 1
        for i in ["MonsterTypeOne", "MonsterTypeTwo", "MonsterTypeThree"]:
            if getattr(self.monster, i) != None:
                setattr(self, i, PhotoImage(file = 'Resource/PAD/Images/Types/' + getattr(self.monster, i) + ".png") )
                self.builder.get_object("canFrameType" + str(count)).create_image(2,2, image = getattr(self, i), anchor = tk.NW)
                self.builder.get_object("canFrameType" + str(count)).grid(row = 0, column = count)
                ToolTip.ToolTip(self.builder.get_object("canFrameType" + str(count)) , getattr(self.monster, i))
            else:
                self.builder.get_object("canFrameType" + str(count)).grid_forget()
            count += 1
        self.frame.config(width = 660)

    def onFrameClick(self, event):
        if self.monster != None:
            self.Monbookobject.showInfo(self.monster, self.thumbnail)

class MonEvoFrame():
    def __init__(self, master, mbobject):
        #logger
        self.logger = logging.getLogger("Padification.ui.MonsterBook.MonEvoFrame")
        #TK Variables
        self.Monbookobject = mbobject
        self.master = master
        self.builder = pygubu.Builder()
        self.builder.add_from_file('src/ui/MonsterBook.ui')
        self.EvoFrame = self.builder.get_object('MonsEvoFrame', master)
        self.EvoCanvas = self.builder.get_object('canEvoFrame')
        self.builder.connect_callbacks(self)


        #Variables
        self.monster = None
        self.thumbnail = None

    def update(self, monster):
        self.monster = monster
        self.smallThumbnail =PhotoImage(file = 'Resource/PAD/Images/thumbnails/' + str(self.monster.MonsterClassID) + ".png").subsample(2)
        self.thumbnail = PhotoImage(file = 'Resource/PAD/Images/thumbnails/' + str(self.monster.MonsterClassID) + ".png")
        self.EvoCanvas.create_image(2,2, image = self.smallThumbnail, anchor = tk.NW)

    def onFrameClick(self, event):
        if self.monster != None:
            self.Monbookobject.showInfo(self.monster, self.thumbnail)

