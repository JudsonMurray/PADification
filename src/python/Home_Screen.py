#!/USR/BIN/ENV PYTHON 3.5
#   NAME:    KYLE GUNTON
#   DATE:    06/26/17
#   PURPOSE: FUNCTIONALITY FOR THE HOME SCREEN

#Version 0.0.1

import pygame
import tkinter as tk
import pygubu
from tkinter import messagebox
from tkinter import *
import tkinter as tk
import pypyodbc
import sys


class HomeScreen():
    """Displays Home Screen Frame and widgets"""
    def __init__(self, master):
        self.master = master
        #Load GUI
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('src/ui/HomeScreen.ui')
        self.titleImg = tk.PhotoImage(file = 'Resource/PAD/Images/PADification Title.png')
        self.mainwindow = builder.get_object('homePageFrame', master)
        
        #Add Title Image
        self.builder.get_object('titleImage').create_image(0,0, image =self.titleImg , anchor = tk.NW, tag = "pic")
    
        self.builder.connect_callbacks(self)
        #self.master.showSceen

    def onAccountOptionsClick(self, event):
        """Occurs When Account Options Button Is Clicked"""
        self.master.showAccountOptions()

    def onMonsterBookClick(self, event):
        self.master.showMonsterBook()

    def onMyMonstersClick(self):
        self.master.showPlayerCollection()

    def onMyTeamsClick(self, event):
        self.master.showTeamBrowser()