#!/usr/bin/env python
#   Name:    Ryan Breau
#   Date:    1/12/2017
#   Purpose: Provides a results screen for the user where they can level up their character

#   1/12/2017 v1.0 Created functionality to work without other classes
#  BG -  1/12/2017 v1.01 Modified to implement 
#  RB -  1/13/2017 v1.02 Added a change to player level and disables buttons when not required
#  KG -  1/13/2017 v1.02 changed values for lvl up rewards/sets hp tomax after stat allocation
#  RB -  1/16/2017 v1.03 Altered display to utilize more space, added a canvas to display character model
#  BG -  1/17/2017 v1.04 Modified to add player image
#  BG -  1/19/2017 v1.05 Window can now update, no need to create new windows over and over.

from tkinter import *
import tkinter as tk
from tkinter import messagebox
import pygubu
import random

class LevelUp:
    def __init__(self, master):
        self.master = master
        #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load an ui file
        builder.add_from_file('DTDui/Results.ui')

        #3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('LevelUp', master)
        builder.connect_callbacks(self)

    def update(self):
        builder = self.builder
        #Saves the initial value of the stats/ Needs to be assigned with the Player's stats
        self.HP = self.master.player.playerMaxHp 
        self.DEF = self.master.player.playerDef
        self.ATK = self.master.player.playerAtk

        #testing variables used because of lack of true variable/ Use these to test if required
        self.hp = self.HP
        self.dEf = self.DEF
        self.atk = self.ATK
        self.floor = self.master.player.floorNum
        self.difficulty = self.master.combatFrame.diff
        
        #Player receives items
        pots = random.randint(1,3)
        self.master.player.potions += pots

        #player.addPotions(pots) /Can be used after linked or deleted not important at the moment

        #Equation deciding how many stat points are to be givento the player/ May need to change later
        self.statBoost = int(self.floor * 0.7 + self.difficulty)

        #Increases player level based on how many stat points are gained
        self.master.player.playerLevel += self.statBoost

        #Config's the labels that display Player specific data
        self.lvl = builder.get_object('lblLvl')
        self.lvl.config(text = 'lvl.' + str(self.master.player.playerLevel - self.statBoost) + ' --> lvl.'+ str(self.master.player.playerLevel))
        self.gained = builder.get_object('lblGained')
        self.gained.config(text = "Stat: " + str(self.statBoost))
        self.hpDisplay = builder.get_object('lblCurrentHP')
        self.hpDisplay.config(text = " HP: " + str(self.hp))
        self.atkDisplay = builder.get_object('lblCurrentATK')
        self.atkDisplay.config(text = " ATK: " + str(self.atk))
        self.defDisplay = builder.get_object('lblCurrentDEF')
        self.defDisplay.config(text = " DEF: " + str(self.dEf))
        self.floorDisplay = builder.get_object('lblFloorProg')
        self.floorDisplay.config(text = 'Floor ' + str(self.floor - 1) + " --> Floor " + str(self.floor))
        self.itemDisplay = builder.get_object('lblItem')
        self.itemDisplay.config(text = 'Item Get:                x '+ str(pots) +'             ' )
        self.potImage = builder.get_object('lblPots')
        self.a = PhotoImage(file = 'DTDresource/Health potion.gif')
        self.potImage.config(image = self.a)

        #Creates the objects for the buttons so they can be disabled and enabled later
        self.btnHpD = builder.get_object('btnHpDown')
        self.btnHpD.config(state = DISABLED)
        self.btnAtkD = builder.get_object('btnAtkDown')
        self.btnAtkD.config(state = DISABLED)
        self.btnDefD = builder.get_object('btnDefDown')
        self.btnDefD.config(state = DISABLED)
        self.btnHpU = builder.get_object('btnHpUp')
        self.btnHpU.config(state = 'normal')
        self.btnAtkU = builder.get_object('btnAtkUp')
        self.btnAtkU.config(state = 'normal')
        self.btnDefU = builder.get_object('btnDefUp')
        self.btnDefU.config(state = 'normal')
        self.btnConfirm = builder.get_object('btnConfirm') 
        self.btnConfirm.config(state = DISABLED)

        self.playerImage = PhotoImage(file = self.master.player.playerImage)
        builder.get_object("canPlayer").create_image(13,15, image = self.playerImage, anchor = tk.NW)

        

    def hpUp(self):
        '''Sends a string into the statUp method to differentiate between stats'''
        self.statUp("HP")

    def hpDown(self):
        '''Sends a string into the statDown method to differentiate between stats'''
        self.statDown("HP")

    def atkUp(self):
        '''Sends a string into the statUp method to differentiate between stats'''
        self.statUp("ATK")

    def atkDown(self):
        '''Sends a string into the statDown method to differentiate between stats'''
        self.statDown("ATK")

    def defUp(self):
        '''Sends a string into the statUp method to differentiate between stats'''
        self.statUp("DEF")

    def defDown(self):
        '''Sends a string into the statDown method to differentiate between stats'''
        self.statDown("DEF")

    def statUp(self, stat):
        '''Increases the chosen stat'''
        if self.statBoost > 0:  #Makes sure there is available stat points
            if stat == "HP":    #Checks which stat is to be increased
                self.hp += 5
                self.hpDisplay.config(text = " HP: " + str(self.hp))
                self.btnHpD.config(state = 'normal')#Enables the stat down button for the specific stat
            elif stat == "ATK":
                self.atk += 2
                self.atkDisplay.config(text = " ATK: " + str(self.atk))
                self.btnAtkD.config(state = 'normal')
            elif stat == "DEF":
                self.dEf += 1
                self.defDisplay.config(text = " DEF: " + str(self.dEf))
                self.btnDefD.config(state = 'normal')
            self.statBoost -= 1 #Lowers the remaining available stat points
            self.gained.config(text = "Stat: " + str(self.statBoost))
            if self.statBoost < 1:
                self.btnHpU.config(state = DISABLED)
                self.btnAtkU.config(state = DISABLED)
                self.btnDefU.config(state = DISABLED)
                self.btnConfirm.config(state ='normal')
        else:
            messagebox.showwarning("No Stats", "Out of usable stat points.")

    def statDown(self, stat):
        '''Decreases the chosen stat'''
        x =False
        if self.statBoost < int(self.floor * 0.7 + self.difficulty):    #Makes sure to not remove more stat points than you began with
            if stat == "HP" and self.hp -1 >= self.HP:  #Checks which stat is to be decreased and that it has been given any extra points
                self.hp -= 5
                self.hpDisplay.config(text = " HP: " + str(self.hp))
                x =True
                if self.hp == self.HP:
                    self.btnHpD.config(state = DISABLED) #Disables the stat down button when need be
            elif stat == "ATK"and self.atk -1 >= self.ATK:
                self.atk -= 2
                self.atkDisplay.config(text = " ATK: " + str(self.atk))
                x =True
                if self.atk == self.ATK:
                    self.btnAtkD.config(state = DISABLED)
            elif stat == "DEF"and self.dEf -1 >= self.DEF:
                self.dEf -= 1
                self.defDisplay.config(text = " DEF: " + str(self.dEf))
                x =True
                if self.dEf == self.DEF:
                    self.btnDefD.config(state = DISABLED)
            if x:
                self.statBoost += 1 #Raises the remaining stat points
                self.gained.config(text = "EXP: " + str(self.statBoost))
                self.btnHpU.config(state = 'normal')
                self.btnAtkU.config(state = 'normal')
                self.btnDefU.config(state = 'normal')
                self.btnConfirm.config(state =DISABLED)
            else:
                messagebox.showwarning("Lack of Stats", "You have not allocated any stat points in this stat.")
        else:
            messagebox.showwarning("Too Many Stats", "You cannot return stat points that have already been allocated.")

    def confirm(self):
        '''Asks the player if they are finished with their selection before continuing to the next floor'''
        if self.statBoost == 0:
            self.master.player.playerMaxHp = self.hp
            self.master.player.playerHp = self.master.player.playerMaxHp
            self.master.player.playerAtk = self.atk
            self.master.player.playerDef = self.dEf
            self.master.showCombatFrame()
        else:
            messagebox.showwarning("More Stats", "You still have stat points to allocate.")

#if __name__ == '__main__':
#    root = tk.Tk()
#    root.geometry("640x480")
#    app = LevelUp(root)
#    root.mainloop()
