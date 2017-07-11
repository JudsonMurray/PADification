# !/usr/bin/env Python3

#   Name:   ZACHARY BLUE
#   Date:   JUNE 23RD 2017
#   Purpose:THE MONSTER EDIT SCREEN FOR THE PADification APPLICATION

import tkinter as tk
from tkinter import *
import tkinter.messagebox as mb
import pygubu

class MonsterEdit:
    def __init__(self, master):
        self.master  = master
        self.builder = pygubu.Builder()

        self.builder.add_from_file(r"src\ui\Monster Edit UI.ui")
        self.monsteredit = self.builder.get_object("Monster Edit")

        #self.__PopulateLatents()

    def __PopulateLatents(self):

        self.latentOne = self.builder.get_object("mnuLatentOne")
        a = Menu(self.latentOne, tearoff = 0)
        #self.latentOne["Menu"] = self.latentOne.menu

        self.latentOne.config(menu = a)

        mayoVar  = IntVar()
        ketchVar = IntVar()

        a.add_command ( label="mayo",
                          command = self.__Change )
        a.add_command ( label="ketchup",
                          command = self.master.showHomeScreen)

    def __Change(self):
        self.latentOne.config(text = "mayo")

#class PADification(tk.Tk):
#    def __init__(self, screenName = None, baseName = None, className = 'Tk', useTk = 1, sync = 0, use = None):
#        super().__init__(screenName, baseName, className, useTk, sync, use)

#        self.monsteredit = MonsterEdit(self)

#        super().mainloop()

#PADification()