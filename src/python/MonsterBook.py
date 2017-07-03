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


class MonsterFrame():
    def __init__(self, master, monster, mbobject):
        #TK Variables
        self.Monbookobject = mbobject
        self.monster = monster
        self.master = master
        self.builder = pygubu.Builder()
        self.builder.add_from_file('src/ui/MonsterBook.ui')
        self.frame = self.builder.get_object('MonsFrame', master)
        self.thumbnail = PhotoImage(file = 'Resource/PAD/Images/thumbnails/' + str(self.monster.MonsterClassID) + ".png")
        self.FrameLabel = self.builder.get_object('FrameLabel')
        self.FrameLabel.create_image(2,2, image = self.thumbnail, anchor = tk.NW)
        self.builder.connect_callbacks(self)
        #Variables
        self.MonstertypeOne = None
        self.MonstertypeTwo = None
        self.MonstertypeThree = None

        #Label Configurations
        self.builder.get_object("lblMonsterID").config(text=str(self.monster.MonsterClassID))

        self.builder.get_object("lblMonsterName").config(text=str(self.monster.MonsterName))
        rarity = ""
        for i in range(0,self.monster.Rarity):
            rarity += '\u2605'
        self.builder.get_object("lblMonsterRarity").config(text= rarity, foreground= 'yellow')
        
        #type = 'Types: '
        #for i in [self.monster.MonsterTypeOne,self.monster.MonsterTypeTwo ,self.monster.MonsterTypeThree]:
        #    if i != None:
        #        type += str(i) + " "
        #self.builder.get_object("lblMonsterTypes").config(text= type)

        colors = {'Fire' : '#ff9966', 'Water' : '#99bbdd', 'Wood' : '#88ee77', 'Light' : '#ffff77', 'Dark' : '#ee99ee'}
        self.frame.config(bg = colors[self.monster.PriAttribute])
        for i in self.frame.grid_slaves():
            if i == self.builder.get_object("lblMonsterRarity"):
                continue
            i.config(background = colors[self.monster.PriAttribute])

        count = 1
        for i in ["MonsterTypeOne", "MonsterTypeTwo", "MonsterTypeThree"]:
            if getattr(self.monster, i) != None:
                setattr(self, i, PhotoImage(file = 'Resource/PAD/Images/Types/' + getattr(self.monster, i) + ".png") )
                self.builder.get_object("canFrameType" + str(count)).create_image(2,2, image = getattr(self, i), anchor = tk.NW)
            else:
                self.builder.get_object("canFrameType" + str(count)).grid_forget()
            count += 1

    def onFrameClick(self, event):
        self.Monbookobject.showInfo(self.monster, self.thumbnail)

class MonsterBook():
    """Displays Home Screen Frame and widgets"""
    def __init__(self, master):
        #Constants
        self.bgSearchText = "Enter Monster ID or Name"

        #TK Variables
        self.master = master
        self.MonsterResults = []
        self.MonsterFrames = []
        self.builder = pygubu.Builder()
        self.builder.add_from_file('src/ui/MonsterBook.ui')
        self.mainwindow = self.builder.get_object('frmMonsterBook', master)
        self.resultsFrame = self.builder.get_object('canMonsterList')
        self.builder.connect_callbacks(self)

        #Monster Info Variables
        self.MonstertypeOne = None
        self.MonstertypeTwo = None
        self.MonstertypeThree = None

    def update(self, search = None):
        self.MonsterResults = []
        self.MonsterFrames = []
        self.MonsterPages = []
        for i in self.resultsFrame.grid_slaves():
            i.grid_forget()
            i.destroy()

        for i in MonsterPages:
            i.destroy()

        monsters = self.master.PADsql.selectMonsterClass(search)
        for i in monsters:
            self.MonsterResults.append(Monster(i))


        for i in range(0,50 if len(self.MonsterResults) > 50 else len(self.MonsterResults)):
            self.MonsterFrames.append(MonsterFrame(self.resultsFrame, self.MonsterResults[i], self))
            self.MonsterFrames[-1].frame.grid(row = i)

        size = len(self.MonsterFrames) * 108
        if size < 750:
            size = 750
        self.resultsFrame.config(height = size)


    def clearInfo(self):
        self.builder.get_object("canMonsterSummary")
        self.builder.get_object("lblID").config(text = "")
        self.builder.get_object("lblName").config(text = "")
        self.builder.get_object("lblRarity").config(text= "")
        self.builder.get_object("lblMaxLevel").config(text= "----")
        self.builder.get_object("lblMaxHP").config(text= "----")
        self.builder.get_object("lblMaxATK").config(text= "----")
        self.builder.get_object("lblMaxRCV").config(text= "----")
        self.builder.get_object("lblMinHP").config(text= "----")
        self.builder.get_object("lblMinATK").config(text= "----")
        self.builder.get_object("lblMinRCV").config(text= "----")

        for i in ["MonsterTypeOne", "MonsterTypeTwo", "MonsterTypeThree"]:
            setattr(self, i, None)

    def showInfo(self,Monster, thumbnail):
        #self.builder.get_object(
        self.builder.get_object("canMonsterSummary").create_image(10,10, image = thumbnail, anchor = tk.NW)
        self.builder.get_object("lblID").config(text = str(Monster.MonsterClassID))
        self.builder.get_object("lblName").config(text = Monster.MonsterName)
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
            self.builder.get_object("lblActiveSkillDesc").config(text = self.master.PADsql.getActiveSkillDesc(Monster.ActiveSkillName))
        if Monster.LeaderSkillName != None:
            self.builder.get_object("lblLeaderSkillName").config(text = Monster.LeaderSkillName)
            self.builder.get_object("lblLeaderSkillDesc").config(text = self.master.PADsql.getLeaderSkillDesc(Monster.LeaderSkillName))

    def onSearchClick(self, event):
        search = self.builder.get_variable("SearchBar").get()
        if search == self.bgSearchText:
            search = ""
        try:
            search = int(search)
        except:
            pass
        self.clearInfo()
        self.update(search)
        
    
    def onSearchBarFocusIn(self, event):
        if self.builder.get_variable("SearchBar").get() == self.bgSearchText:
            self.builder.get_variable("SearchBar").set("")
        
    def onSearchBarFocusOut(self, event):
        if self.builder.get_variable("SearchBar").get() == "":
            self.builder.get_variable("SearchBar").set(self.bgSearchText)