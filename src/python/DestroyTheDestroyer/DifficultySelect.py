#Version 1.0 - KYLE GUNTON - JANUARY 12TH, 2017
#Version 1.01 - Billy Gale - Jan 12TH, 2017 - Added code to next frame and changed resource path

import pygubu
from tkinter import messagebox
from tkinter import *
from PlayerClasses import *
class DifficultySelect:
    """Display DifficultySelect Widgets"""

    def __init__(self, master):
        self.master = master
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('DTDui/DifficultySelect.ui')
        self.mainwindow = builder.get_object('DifficultySelect', master)
        self.diffBar = builder.get_object('difficultyBar')
        self.diffLabel = builder.get_object('difficultyMessage')
        self.diffLabel.config(text = "CAUTION! It Is Not Advisesable To Continue!")
        self.diffBar.bind("<ButtonRelease-1>", self.messageConfig)
        self.monsterImage = builder.get_object('monsterImage')
        self.monsterImage = PhotoImage(file = self.master.RESOURCEDIR + Pikachu().monsterImg)
        self.builder.get_object('monsterImage').create_image(150, 50, image=self.monsterImage, anchor=NW)
        builder.connect_callbacks(self)

    def setDifficulty(self):
        #self.difficulty =  self.diffBar.get()
        self.master.combatFrame.diff = self.diffBar.get()
        #Code To Next Frame
        self.mainwindow.grid_forget()
        self.master.showCombatFrame()
        
    def messageConfig(self, event):
        if self.diffBar.get() == 1:
            self.diffLabel.config(text = "CAUTION! It Is Not Advisable To Continue!")
            self.monsterImage = PhotoImage(file = self.master.RESOURCEDIR + "Pikachu.gif")
        if self.diffBar.get() == 2:
            self.diffLabel.config(text = "WARNING! Your Body May Be Found, However The Chanses Are Slim!")
            self.monsterImage = PhotoImage(file = self.master.RESOURCEDIR + "Cthulu.gif")
        if self.diffBar.get() == 3:
            self.diffLabel.config(text = "You Will Die")
            self.monsterImage = PhotoImage(file = self.master.RESOURCEDIR + "Wendigo.gif")

        
        self.builder.get_object('monsterImage').create_image(150, 50, image=self.monsterImage, anchor=NW)