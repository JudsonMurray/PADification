# !usr/bin/env Python3

#   Name:   ZACHARY BLUE
#   Date:   JUNE 27TH 2017
#   Purpose:THE ACCOUNT OPTIONS SCREEN

import tkinter as tk
from tkinter import *
import tkinter.messagebox as mb
import pygubu

class AccountOptions:
    def __init__(self, master):
        self.master = master
        self.builder = pygubu.Builder()

        self.builder.add_from_file("src/ui/Account Options UI.ui")
        self.mainwindow = self.builder.get_object("Account Options",master)

    def onMainMenuClick(self):
        """Displays Main Menu"""
        self.master.showHomeScreen

#class PADification(tk.Tk):
#    def __init__(self, screenName = None, baseName = None, className = 'Tk', useTk = 1, sync = 0, use = None):
#        super().__init__(screenName, baseName, className, useTk, sync, use)

#        self.mainwindow = AccountOptions(self)

#        super().mainloop()

#PADification()