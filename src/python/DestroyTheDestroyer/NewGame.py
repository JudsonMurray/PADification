#Version 1.0 - KYLE GUNTON - JANUARY 12TH, 2017
#version 1.01 -BG - Changed file resource path, Added functionaility to switch frames, Added dict to select class as globals() for some
#                       reason left out the player variables
#Version 1.02 - KG - Added stats window
#Version 1.03 - KG - Added new classes
#Version 1.04 - KG - Switched Character to player builder from player class
#Version 1.05 - KG - Added Easter Egg

import tkinter as tk
import pygubu
from tkinter import messagebox
from tkinter import *
from PlayerClasses import *
import json
import Entities
from Builders import *
class NewGame:
    """Displays NewGame Frame and widgets"""

    def __init__(self, master):
        self.master = master
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('DTDui/NewGame.ui')

        self.boxEggFound = False

        self.mainwindow = builder.get_object('NewGame', master)
        #ADD CLASSES TO LISTBOX
        self.classList = builder.get_object('playerClassList')
        self.classList.insert(END, "Adventurer")
        self.classList.insert(END, "Fighter")
        self.classList.insert(END, "Rogue")
        self.classList.insert(END, "Mage")
        


        self.classList.bind("<ButtonRelease-1>", self.updateDetails)
        """"""

        self.classDetails = builder.get_object('classDetails')
        builder.connect_callbacks(self)
        self.playerDetails = {}
        
        self.playerDetails = json.load((open(self.master.RESOURCEDIR + 'ClassData.txt')))
        
        x=1
    def startDifficultySelect(self):
        """Command to retrive data from widgets and open difficulty select window"""

        #Easter egg
        try:
            self.playerName = self.builder.get_variable('enterPlayerName').get()

            if self.playerName.lower() == "i am a box" and not self.boxEggFound:
                self.master.player = PlayerBuilder().build("Box", self.playerName)
                messagebox.showinfo("Easter Egg!", "YOU ARE NOW A BOX!")
                self.classList.insert(0, "Box")
                self.boxEggFound = True

            else:
                self.master.player =  PlayerBuilder().build(self.classList.get(ANCHOR), self.playerName)

            #self.getPlayerName()
            if len(self.playerName) == 0:
                raise ValueError
            #Code To Next Frame
            if self.master.player.getHp() < 0:
                raise KeyError
            self.mainwindow.grid_forget()
            self.master.showDifficultyFrame()

                
        except ValueError:
            messagebox.showinfo("Select A Class", "Please Enter A Name Before Leaving")

        except KeyError:
            messagebox.showinfo("Select A Class", "Click on one of the classes provided before leaving")

    def updateDetails(self, event):
        #adds Player object to root

        self.playerName = self.builder.get_variable('enterPlayerName').get()
        classdict = self.playerDetails

        self.player = classdict[self.classList.get(ANCHOR)]

        self.statString = statString = "Class:       " + self.classList.get(ANCHOR) + "\nHp:          " + str(self.player["HpMax"]) + "\nAtk :         " + str(self.player["Atk"]) + "\nDef:          " + str(self.player["Def"])\
            + "\nPotions:   "+ str(self.player["Pots"])
        
        self.classDetails.config(text = statString)

        
        self.playerImg = PhotoImage(file = self.player["img"])
        self.builder.get_object('PlayerImage').create_image(0, 0, image=self.playerImg, anchor=NW)
