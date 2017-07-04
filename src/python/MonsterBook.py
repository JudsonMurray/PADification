#!/USR/BIN/ENV PYTHON 3.5
#   NAME:    Billy Gale 
#   DATE:    06/28/17
#   PURPOSE: MonsterBook Functionality
#
#
# 2017-07-03 - WG - v1.0 - Monster Book able to search and Displays a maximum of 50 results on one page.


from PADMonster import Monster
import tkinter as tk
import pygubu
from tkinter import messagebox as mb
from tkinter import *
from ast import literal_eval as le
import math



class MonsterFrame():
    def __init__(self, master, mbobject):
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
            else:
                self.builder.get_object("canFrameType" + str(count)).grid_forget()
            count += 1
        self.frame.config(width = 660)

    def onFrameClick(self, event):
        if self.monster != None:
            self.Monbookobject.showInfo(self.monster, self.thumbnail)

class MonsterBook():
    """Displays Home Screen Frame and widgets"""
    def __init__(self, master):
        #Constants
        self.bgSearchText = "Enter Monster ID or Name"
        self.RESULTSPERPAGE = 7

        #TK Variables
        self.master = master
        self.builder = pygubu.Builder()
        self.builder.add_from_file('src/ui/MonsterBook.ui')
        self.mainwindow = self.builder.get_object('frmMonsterBook', master)
        self.resultsFrame = self.builder.get_object('canMonsterList')
        self.builder.connect_callbacks(self)

        #Monster Info Variables
        self.MonstertypeOne = None
        self.MonstertypeTwo = None
        self.MonstertypeThree = None

        #Results Variables
        self.MonsterResults = []
        self.MonsterFrames = []
        self.curPage = 1
        self.Results = 0
        self.maxPage = 1

        for i in range( 0 , self.RESULTSPERPAGE ):
            self.MonsterFrames.append(MonsterFrame(self.resultsFrame, self))

    def update(self):
        """Updates results Shown on Monster Book"""
        #Clear Frame
        #self.MonsterFrames = []
        for i in self.resultsFrame.grid_slaves():
            i.grid_forget()
            #i.destroy()

        #Populate Frame with results in range
        start = (self.curPage - 1) * self.RESULTSPERPAGE
        end = self.curPage * self.RESULTSPERPAGE
        if end > len(self.MonsterResults):
            end = len(self.MonsterResults)
        count = 0
        for i in range( start , end ):
            self.MonsterFrames[count].update(self.MonsterResults[i])
            self.MonsterFrames[count].frame.grid(row = count)
            count += 1

        #Ensures canvas does not get to small.
        #size = (end - start) * 108
        #if size < 750:
        #    size = 750
        #self.resultsFrame.config(height = size)

        #Update Page Number
        self.builder.get_object("lblPageNumber").config(text = str(self.curPage) + " / " + str(self.maxPage))

    def nextPage(self, event):
        if self.curPage < self.maxPage:
            self.curPage += 1
            self.update()
            self.clearInfo()

    def prevPage(self, event):
        if self.curPage > 1:
            self.curPage -= 1
            self.update()
            self.clearInfo()

    def clearInfo(self):
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

        for i in ["MonsterTypeOne", "MonsterTypeTwo", "MonsterTypeThree"]:
            setattr(self, i, None)

    def showInfo(self,Monster, thumbnail):
        """Shows The Information of the Selected Monster"""
        self.builder.get_object("canMonsterSummary").create_image(10,10, image = thumbnail, anchor = tk.NW)
        self.builder.get_object("lblIDName").config(text = str(Monster.MonsterClassID) + " - " + Monster.MonsterName)
        #self.builder.get_object("lblName").config(text = Monster.MonsterName)
        rarity = ""
        for i in range(0,Monster.Rarity):
            rarity += '\u2605'
        self.builder.get_object("lblRarity").config(text= rarity, foreground= 'yellow')
        self.builder.get_object("lblMaxLevel").config(text = str(Monster.MaxLevel))
        self.builder.get_object("lblMaxHP").config(text = str(Monster.MaxHP))
        self.builder.get_object("lblMaxATK").config(text = str(Monster.MaxATK))
        self.builder.get_object("lblMaxRCV").config(text = str(Monster.MaxRCV))
        self.builder.get_object("lblMinHP").config(text = str(Monster.MinHP))
        self.builder.get_object("lblMinATK").config(text = str(Monster.MinATK))
        self.builder.get_object("lblMinRCV").config(text = str(Monster.MinRCV))
        
        count = 1
        for i in ["MonsterTypeOne", "MonsterTypeTwo", "MonsterTypeThree"]:
            if getattr(Monster, i) != None:
                setattr(self, i, PhotoImage(file = 'Resource/PAD/Images/Types/' + getattr(Monster, i) + ".png") )
                self.builder.get_object("canType" + str(count)).create_image(2,2, image = getattr(self, i), anchor = tk.NW)
            else:
                setattr(self, i, None)
            count += 1

        if Monster.ActiveSkillName != None:
            self.builder.get_object("lblActiveSkillName").config(text = Monster.ActiveSkillName)
            self.builder.get_object("lblActiveSkillDesc").config(text = Monster.ActiveSkillDesc)
        else:
            self.builder.get_object("lblActiveSkillName").config(text = 'None')
            self.builder.get_object("lblActiveSkillDesc").config(text = '')

        if Monster.LeaderSkillName != None:
            self.builder.get_object("lblLeaderSkillName").config(text = Monster.LeaderSkillName)
            self.builder.get_object("lblLeaderSkillDesc").config(text = Monster.LeaderSkillDesc)
        else:
            self.builder.get_object("lblLeaderSkillName").config(text = 'None')
            self.builder.get_object("lblLeaderSkillDesc").config(text = '')

    def onSearchClick(self, event):
        search = self.builder.get_variable("SearchBar").get()
        if search == self.bgSearchText:
            search = ""

        if "," in search:
            search = le("(" + search + ")")
        elif search.isnumeric():
            search = int(search)

        self.MonsterResults = []
        monsters = self.master.PADsql.selectMonsterClass(search)
        for i in monsters:
            self.MonsterResults.append(Monster(i))
        self.maxPage = math.ceil(len(self.MonsterResults) / self.RESULTSPERPAGE)
        self.curPage = 1
        self.update()
        self.builder.get_object("lblResults").config(text = str(len(self.MonsterResults)) + " Results Found.")
    
    def onSearchBarFocusIn(self, event):
        if self.builder.get_variable("SearchBar").get() == self.bgSearchText:
            self.builder.get_variable("SearchBar").set("")
        
    def onSearchBarFocusOut(self, event):
        if self.builder.get_variable("SearchBar").get() == "":
            self.builder.get_variable("SearchBar").set(self.bgSearchText)