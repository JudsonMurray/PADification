#!usr/bin/env python3
#
#   Name :      WILLIAM GALE
#   Date :      January 12th
#   Purpose:    DestroyingTheDestroyer Combat game using tkinter and pygubu

# History:  
#       V 0.1 initial coding 
#       V 0.2 change player to Player class
#       V 0.3 added four more classes for player to choose from after they win - resets stats upon new game
#       + 0.3 All frames preloaded and unloadable
#       v 0.4 Made sure all windows are forgotten when show menu is hit, Added BGM.
#       v 0.5 Intergrated saving into the game
#       v 0.6 Added sounds and music to game
#       v 0.7 Modified to work with Builders
#       v 0.8 Added song check to play music to stop repeating same song.
#   EG  V 0.9 Added winScreen updates to update player data
from pygame.mixer import *
import pygame
import winsound
import tkinter as tk
import tkinter.messagebox as mb
import pygubu
import CombatFrame
import ZacksMenus
import PlayerClasses
import NewGame
import DifficultySelect
import Ryans_LvL_Up as lvlup
import Elie_winScreen as WinScreen
import pickle
from Builders import *
import Entities

class DestroyingTheDestroyer(tk.Toplevel):
    
    def __init__(self, master, screenName = None, baseName = None, className = 'Tk', useTk = 1, sync = 0, use = None):
        super().__init__(master)
        pygame.init() # Pygame initilization
        init() # Mixer initilization


        # Constants and variables
        self.RESOURCEDIR = "DTDresource/"
        self.UIDIR = "DTDui/"
        self.NORMAL = "normal"
        self.ENDLESS = "endless"
        self.currentSong = ""
        self.switch = None
        self.ticks = 0
        self.gameMode = self.NORMAL
        
        # Builders
        self.playerBuilder = PlayerBuilder()
        self.monsterBuilder = MonsterBuilder()
        self.levelBuilder = LevelBuilder()

        self.player = Entities.Player()
        self.addedClasses = 0
        
        # Game Frames
        self.title("Destroy The Destroyer")
        self.geometry("640x480")
        self.mainMenu = ZacksMenus.Title(self)
        self.menubar = WinScreen.MenuBar(self)
        self.combatFrame = CombatFrame.CombatFrame(self)
        self.newGameFrame = NewGame.NewGame(self)
        self.difficultyFrame = DifficultySelect.DifficultySelect(self)
        self.levelUpFrame = lvlup.LevelUp(self)
        self.gameover = ZacksMenus.GameOver(self)
        self.winScreen = WinScreen.WinnerScreen(self)
        self.creditFrame = WinScreen.CreditsScreen(self)
        self.loadFrame = WinScreen.LoadScreen(self)
        self.endlessScoreFrame = ZacksMenus.EndlessOVer(self)

        self.logPrint = self.combatFrame.combatLogPrint
        #show main menu
        
        self.transient(master) #set to be on top of the main window
        self.grab_set() #hijack all commands from the master (clicks on the main window are ignored)
        self.showMainMenu()
        self.timer()

        try:
            open("savedata.dat", 'rb')
        except:
            open("savedata.dat", 'xb')
        super().mainloop()

    def showCombatFrame(self):
        """Show Combat Frame"""
        self.forgetAll()
        self.save()
        self.combatFrame.generateFloor()
        self.combatFrame.updatePlayer()
        self.combatFrame.updateMonsters()
        self.combatFrame.combatFrame.grid()

    def showNewGame(self):
        """Show NewGame Frame"""
        self.forgetAll()
        #Add new classes if first time after player wins
        if self.player.hasWon and self.addedClasses < 4:
            self.newGameFrame.classList.insert(tk.END, "Explorer")
            self.newGameFrame.classList.insert(tk.END, "Gladiator")
            self.newGameFrame.classList.insert(tk.END, "Assassin")
            self.newGameFrame.classList.insert(tk.END, "Grand Mage")
            self.addedClasses = 4

        self.player = Entities.Player()
        #If player has won, add new classes
        self.builder2 = builder2 = pygubu.Builder()
        builder2.add_from_file('ui/NewGame.ui')

        self.newGameFrame.mainwindow.grid()

    def showDifficultyFrame(self):
        """Show Difficulty Frame"""
        self.forgetAll()
        self.difficultyFrame.mainwindow.grid()

    def showLevelUp(self):
        """Show Level up Frame"""
        self.playMusic("victory.wav")
        self.forgetAll()
        self.levelUpFrame.update()
        self.levelUpFrame.mainwindow.grid()

    def showGameOver(self):
        """Show Game Over"""
        self.playMusic("death.wav",0)
        self.forgetAll()
        self.gameover.mainwindow.grid()

    def showMainMenu(self):
        """ Show Main Menu """
        self.playMusic()
        self.forgetAll()
        self.mainMenu.mainwindow.grid()

    def showWinScreen(self):
        """ Show Win Screen """
        self.playMusic()
        self.forgetAll()
        self.winScreen.winScreenUpdate()
        self.winScreen.winScreen.grid()

    def showCreditsFrame(self):
        """ Shows Credits """
        self.playMusic()
        self.forgetAll()
        self.creditFrame.y = 400
        self.creditFrame.credits.grid_configure(pady=400)
        self.creditFrame.loop()
        self.creditFrame.creditsScreen.grid()

    def showLoadFrame(self):
        """ Show Load Screen """
        self.playMusic()
        self.forgetAll()
        try:
            self.loadFrame.upDatePlayerInfo(pickle.load(open( "savedata.dat", "rb" )))
        except:
            self.loadFrame.clearPlayerInfo()
        self.loadFrame.loadScreen.grid()

    def showEndlessScoreFrame(self):
        """ Show Endless Score Frame """
        self.playMusic()
        self.forgetAll()
        self.endlessScoreFrame.endlessOverUpdate()
        self.endlessScoreFrame.endlessOver.grid()

    def forgetAll(self):
        """Forgets all frames, Huzzah!"""
        self.mainMenu.mainwindow.grid_forget()
        self.combatFrame.combatFrame.grid_forget()
        self.newGameFrame.mainwindow.grid_forget()
        self.difficultyFrame.mainwindow.grid_forget()
        self.levelUpFrame.mainwindow.grid_forget()
        self.gameover.mainwindow.grid_forget()
        self.winScreen.winScreen.grid_forget()
        self.creditFrame.creditsScreen.grid_forget()
        self.loadFrame.loadScreen.grid_forget()
        self.endlessScoreFrame.endlessOver.grid_forget()

    def load(self):
        """ Load character from text """
        print("Loaded Character")
        try:
            self.player = pickle.load( open( "savedata.dat", "rb" ) )
            self.gameMode = self.player.gameMode
        except:
            print("No character saved")

        

    def save(self):
        """Save character to text"""
        self.logPrint("Game saved.", "save")
        self.player.gameMode = self.gameMode
        pickle.dump(self.player, open("savedata.dat", "wb"))
        

    def deleteSave(self):
        """Delete Save Data"""
        open("savedata.dat", "w")


    def playMusic(self, song = "bgm.wav", loops = -1):
        """Plays Music from the wav or ogg specified, loop -1 for indefinite and 0...n for specific loop amount"""
        if song != self.currentSong:
            music.load(self.RESOURCEDIR + song)
            music.play(loops=loops)
            self.currentSong = song
        else:
            return
    
    def timer(self):
        """ rudimentry timer """
        self.ticks += 1
        #print(self.ticks)
        self.after(1000, self.timer)

#DestroyingTheDestroyer()
