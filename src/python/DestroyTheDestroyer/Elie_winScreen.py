#usr/bin/env Python3
#   NAME:       ELIE GODBOUT
#   DATE:       JANUARY 12TH 2017
#   PURPOSE:    WIN SCREEN / CREDITS SCREEN / MENUBAR

#   2017/01/12 - V0.1.0   original source code
#   2017/01/13 - V0.1.1   Changed long file names, Changed resource path for ui file
#   2017/01/13 - V0.1.2   placed menuBar in its own class
#   2017/01/13 - V0.1.3   placed the credits screen in its own class
#   2017/01/13 - V0.1.4   Added a new game button to winScreen
#   2017/01/16 - V0.1.5   Added newgame and loadgame to menubar and a load screen to the program
# EG   2017/01/18   -   V0.1.6  Changed builder.add_from_file of winscreen line 29
# EG   2017/01/19   -   V0.1.7  Added feats to the wincreen portion of the program
# EG   2017/01/19   -   V0.1.8  Testing: Application of gif to win screen
# EG   2017/01/19   -   V0.1.9  Testing: Unsuccessful. Returning to version V0.1.7
# EG   2017/01/19   -   V0.1.10 Adding credits scrolling as well as fixing load screen bugs
# EG   2017/01/20   -   V0.1.11 Credits screen button is default disabled / removed save from menuBar
# EG    2017/01/20  -   V0.1.12 grouped player data in one method and added the player data

import tkinter as tk
import pygubu
import pickle
from Entities import *

class WinnerScreen(object):
    def __init__(self, root):
        self._root = root
        print('success')

        #create builder
        self.builder = builder = pygubu.Builder()

        #select file
        builder.add_from_file('DTDui/Elie_winScreen.ui')

        #get screen
        self.winScreen = builder.get_object('winScreen', self._root)

        #callbacks 
        builder.connect_callbacks(self)
        
        #Add data to win screen.ui
    def winScreenUpdate(self):
        playername = self.builder.get_variable('playerName')
        playername.set(str(self._root.player.playerName))

        playerattack = self.builder.get_variable('atkHolder')
        playerattack.set(str(self._root.player.attacks))

        playerfloor = self.builder.get_variable('floHolder')
        playerfloor.set(str(self._root.player.floorsBeat))

        playerdd = self.builder.get_variable('ddHolder')
        playerdd.set(str(self._root.player.bossKills))
        
        self.image = tk.PhotoImage(file = "DTDresource/WindowDoge.gif")
        self.builder.get_object('windogeCanvas').create_image(13, 15, image = self.image,anchor=tk.NW)

        #return to main menu
    def mainMenu(self):
        self._root.player.hasWon = True
        print('main menu selected')
        self.winScreen.grid_forget()
            #return to MainMenu method/Zack's file
        self._root.showMainMenu()

        #start new game
    def newGame(self):
        self._root.player.hasWon = True
        print('from winScreen: New game')
        self.winScreen.grid_forget()
        self._root.showNewGame()

        


#---------------------------Credits Class--------------------------
class CreditsScreen(object):
    def __init__(self, root):
        self._root = root
        self.builder = builder = pygubu.Builder()

        builder.add_from_file('DTDui/Elie_winScreen.ui')

        self.creditsScreen = builder.get_object('creditsScreen', self._root)
        builder.connect_callbacks(self)

        #new credits scroll section
        ##############
        self.y = 400
        self.credits = builder.get_object('creditsScreenFrame')
        self.credits.grid_configure(pady=400)
        #self.loop()

    def loop(self):
        self.creditButton = self.builder.get_object('mainMenuButton_1')
        self.creditButton.config(state='disabled')
        #centered coordinates: x=190, y=110
        self.credits = self.builder.get_object('creditsScreenFrame', self._root)
        self.y -= 1
        self.credits.grid_configure(pady=self.y)
        #print(self.y)

        if self.y <= 110:
            self._root.after_cancel(self.loop)
            print('REACHED MAX MOVEMENT')
            self.creditButton.config(state='normal')
        else :
            self._root.after(10, self.loop)
            #print('more')

        ################

        #credits screen access method
    def mainMenu(self):
        print('credit screen method success')
        self.creditsScreen.grid_configure(pady=400)
        self.y = 400
        self.creditButton.config(state=tk.DISABLED)
        self.creditsScreen.grid_forget()
        self._root.showMainMenu()

#---------------------------MenuBar Class--------------------------
class MenuBar(object):
    def __init__(self, root):
        self._root = root
        self.builder = builder = pygubu.Builder()

        builder.add_from_file('DTDui/Elie_winScreen.ui')
        #menu bar
        self.menuBar = menu = builder.get_object('menuBar', self._root)
        self._root.config(menu = self.menuBar)
        builder.connect_callbacks(self)

        #menuBar methods
    def menuBarQuit(self):
        self._root.destroy()

    def menuBarMainMenu(self):
        print('menu bar mainmenu')
        try:
            self._root.after_cancel(self._root.switch)
        except:
            pass
        self._root.showMainMenu()

    def menuBarNewGame(self):
        print('menu bar newgame')
        try:
            self._root.after_cancel(self._root.switch)
        except:
            pass
        self._root.showNewGame()

    def menuBarLoadGame(self):
        print('menu bar loadgame')
        try:
            self._root.after_cancel(self._root.switch)
        except:
            pass
        self._root.showLoadFrame()

#--------------------------Load Screen-----------------------------
class LoadScreen(object):
    def __init__(self, root):
        self._root = root

        self.builder = builder = pygubu.Builder()

        builder.add_from_file('DTDui/Elie_winScreen.ui')

        self.loadScreen = builder.get_object('loadScreen', self._root)
        builder.connect_callbacks(self)

        self.loadButton = builder.get_object('LoadButton')
        self.delButton = builder.get_object('deleteButton')

        #load Screen methods
    def upDatePlayerInfo(self, player):
        if isinstance(player, Player):
            playername = self.builder.get_variable('nameHolder')
            playername.set(str(player.playerName) + " The " + str(player.playerClass))

            playerhp = self.builder.get_variable('hpHolder')
            playerhp.set(str(player.playerMaxHp))

            playerattack = self.builder.get_variable('attackHolder')
            playerattack.set(str(player.playerAtk))

            playerdef = self.builder.get_variable('defHolder')
            playerdef.set(str(player.playerDef))

            playerpotion = self.builder.get_variable('potionHolder')
            playerpotion.set(str(player.potions))

            playerpotion = self.builder.get_variable('floorHolder')
            playerpotion.set(str(player.floorNum))

            self.playerImage = tk.PhotoImage(file = str(player.playerImage))

            self.builder.get_object('SpriteCanvas').create_image(13, 15, image = self.playerImage, anchor=tk.NW, tag = "pic")

            #Enable buttons
            self.loadButton.config(state='normal')
            self.delButton.config(state='normal')

        else:
            self.clearPlayerInfo()

    def clearPlayerInfo(self):
        
            #disable buttons
            self.loadButton.config(state=tk.DISABLED)
            self.delButton.config(state=tk.DISABLED)

            playername = self.builder.get_variable('nameHolder')
            playername.set("No Character")

            playerhp = self.builder.get_variable('hpHolder')
            playerhp.set("")

            playerattack = self.builder.get_variable('attackHolder')
            playerattack.set("")

            playerdef = self.builder.get_variable('defHolder')
            playerdef.set("")

            playerpotion = self.builder.get_variable('potionHolder')
            playerpotion.set("")

            playerpotion = self.builder.get_variable('floorHolder')
            playerpotion.set(str(""))

            self.builder.get_object('SpriteCanvas').delete("pic") 
            
            

    def mainMenu(self):
        print('from load screen: main menu')
        self.loadScreen.grid_forget()
        self._root.showMainMenu()

    def load(self):
        print('from load screen: load')
        self.loadScreen.grid_forget()
        self._root.load()
        self._root.showCombatFrame()

    def delete(self):
        print('from load screen: delete')
        open('savedata.dat', 'wb')
        self.clearPlayerInfo()
