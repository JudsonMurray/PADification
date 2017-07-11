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
        self.canEvoFrame = self.builder.get_object('canEvoTree')
        self.builder.connect_callbacks(self)

        #Monster Info Variables
        self.MonstertypeOne = None
        self.MonstertypeTwo = None
        self.MonstertypeThree = None

        #Results Variables
        self.evoFrames = []
        self.MonsterResults = []
        self.MonsterFrames = []
        self.curPage = 1
        self.Results = 0
        self.maxPage = 1

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

    def showInfo(self,monster, thumbnail):
        """Shows The Information of the Selected monster"""
        self.builder.get_object("canMonsterSummary").create_image(10,10, image = thumbnail, anchor = tk.NW)
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
        
        count = 1
        for i in ["MonsterTypeOne", "MonsterTypeTwo", "MonsterTypeThree"]:
            if getattr(monster, i) != None:
                setattr(self, i, PhotoImage(file = 'Resource/PAD/Images/Types/' + getattr(monster, i) + ".png") )
                self.builder.get_object("canType" + str(count)).create_image(2,2, image = getattr(self, i), anchor = tk.NW)
            else:
                setattr(self, i, None)
            count += 1

        if monster.ActiveSkillName != None:
            self.builder.get_object("lblActiveSkillName").config(text = monster.ActiveSkillName)
            self.builder.get_object("lblActiveSkillDesc").config(text = monster.ActiveSkillDesc)
        else:
            self.builder.get_object("lblActiveSkillName").config(text = 'None')
            self.builder.get_object("lblActiveSkillDesc").config(text = '')

        if monster.LeaderSkillName != None:
            self.builder.get_object("lblLeaderSkillName").config(text = monster.LeaderSkillName)
            self.builder.get_object("lblLeaderSkillDesc").config(text = monster.LeaderSkillDesc)
        else:
            self.builder.get_object("lblLeaderSkillName").config(text = 'None')
            self.builder.get_object("lblLeaderSkillDesc").config(text = '')


        evoTree = self.master.PADsql.getEvolutionTree(monster.MonsterClassID)

        for i in self.evoFrames:
            i.EvoFrame.grid_forget()

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
                frame.EvoFrame.grid(column = evocol, row = evorow, padx = 2, pady = 7)
                evorow += 1
            evocol +=1


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

class MonEvoFrame():
    def __init__(self, master, mbobject):
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
        self.thumbnail = PhotoImage(file = 'Resource/PAD/Images/thumbnails/' + str(self.monster.MonsterClassID) + ".png")
        self.EvoCanvas.create_image(2,2, image = self.thumbnail, anchor = tk.NW)

    def onFrameClick(self, event):
        if self.monster != None:
            self.Monbookobject.showInfo(self.monster, self.thumbnail)