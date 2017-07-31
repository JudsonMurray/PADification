# !/usr/bin/env Python3

#   Name:   WILLIMAM GALE
#   Date:   JUNE 28TH 2017
#   Purpose: Main for Padification Application.

# v1.0 WG - Integrated Code from Zachs Test_Integration.py,

#3rd Party Modules
import logging
import datetime
import pypyodbc
import tkinter as tk
from tkinter import *
import tkinter.messagebox as mb
import pygubu
import os
import sys
import ctypes
import inspect

#1st Party Modules
import ResourcePath as RP
import PADSQL
import PADMonster
import PlayerCollection
import MonsterEditScreen
import Monster_Info_Screen
import EditTeamScreen
import Home_Screen
import Account_Options_Screen
import MonsterBook
import TeamBrowserScreen
from CustomWidgets import *

#System Information.
windll_user32 = ctypes.windll.user32
screenWidth = windll_user32.GetSystemMetrics(0)
screenHeight = windll_user32.GetSystemMetrics(1)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
logPath = (os.path.dirname(os.path.dirname(currentdir)) + r"\log" )

#Loggin Configuration.
logging.basicConfig(filename=RP.LOGPATH + r'\{:%Y-%m-%d %H-%M-%S}'.format(datetime.datetime.now()) + '.log', level=logging.WARN , format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())
logging.info("Application Start")

class PADification(tk.Tk):
    def __init__(self, screenName = None, baseName = None, className = 'Tk', useTk = 1, sync = 0, use = None):
        super().__init__(screenName, baseName, className, useTk, sync, use)

        #loggin object
        self.logger = logging.getLogger("Padification.root")
        #system Info
        
        ##System Information
        #self.screenWidth = screenWidth
        #self.screenHeight = screenHeight

        ##Relative Paths to resources.
        #currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        #self.pathResource = (os.path.dirname(os.path.dirname(currentdir)) + r"\Resource" )
        
        # Fix the Size of the Application
        self.minsize(width=1280, height=960)
        self.maxsize(width=1280, height=960)
        self.resizable(width=False, height=False)
        self.geometry('%dx%d+%d+%d' % (1280,960, 320, 10))

        self.title("PADification - The Ultimate in Puzzle and Dragons Organization.")

        
        #pypyodbc SQl Object
        self.PADsql = PADSQL.PADSQL()

        #screens
        self.MonsterBook = MonsterBook.MonsterBook(self)
        self.homeScreen = Home_Screen.HomeScreen(self)
        self.accountOptions = Account_Options_Screen.AccountOptions(self)
        self.playerCollection = PlayerCollection.PlayerCollection(self)
        self.teamBrowser = TeamBrowserScreen.TeamBrowser(self)
        self.editTeam = EditTeamScreen.EditTeam(self)
        self.monsterEdit = MonsterEditScreen.MonsterEdit(self)
        self.showHomeScreen()
        self.lower()

        LoginDialog(self,"LOGIN")
        if not self.PADsql.signedIn:
            self.destroy()

        super().mainloop()

    # Displays Edit Monster Screen.
    def showEditMonster(self):
        self.forgetAll()
        self.monsterEdit.monsteredit.grid()

    # Displays the home screen.
    def showHomeScreen(self):
        """Show Home Screen""" 
        self.forgetAll()
        self.homeScreen.mainwindow.grid()
        if self.PADsql.signedIn:
            self.homeScreen.update()

    # Displays the account options screen.
    def showAccountOptions(self):
        """Show Account Options Screen"""
        self.forgetAll()
        self.accountOptions.mainwindow.grid()
        self.accountOptions.updateLabel()

    # Displays the Monster Book screen.
    def showMonsterBook(self):
        self.forgetAll()
        self.MonsterBook.mainwindow.grid()
        self.MonsterBook.update()

    # Displays the Player Collection screen.
    def showPlayerCollection(self):
        """Show Player Collection Screen"""
        self.forgetAll()
        self.playerCollection.mainwindow.grid()
        self.playerCollection.pageOne()

    # Displays the team Browser screen.
    def showTeamBrowser(self):
        """Show Login Screen"""
        self.forgetAll()
        self.teamBrowser.loadUserTeams()
        self.teamBrowser.mainwindow.grid()
    
    # Displays the Edit team screen.
    def showEditTeamScreen(self):
        """Show Login Screen"""
        self.forgetAll()
        self.editTeam.mainwindow.grid()


    #Removes all frames from the screen
    def forgetAll(self):
        """Forgets all frames"""
        self.focus()
        self.MonsterBook.mainwindow.grid_forget()
        self.homeScreen.mainwindow.grid_forget()
        self.accountOptions.mainwindow.grid_forget()
        self.playerCollection.mainwindow.grid_forget()
        self.teamBrowser.mainwindow.grid_forget()
        self.editTeam.mainwindow.grid_forget()
        self.editTeam.mainwindow.grid_forget()
        self.monsterEdit.monsteredit.grid_forget()

    def updateProfile(self, builder):
        """Updates player profile image, username, collection and team counts"""
        if self.PADsql.ProfileImage != None:
            value = self.PADsql.ProfileImage
        else:
            value = 1

        self.ProfileImage = PhotoImage(file = RP.THUMBNAILS + '\\' + str(value) + ".png")
        builder.get_object("canProfileImage").create_image(2,2, image = self.ProfileImage, anchor = NW)

        #CustomFont_Label(self.builder.get_object('frmPlayerInfo'), text= self.PADsql.Username, font_path="Resource/PAD/Font/FOT-RowdyStd-EB.ttf", size=22).grid(row = 0, column = 1, sticky = NW)
        builder.get_object("lblUsername").config(text = self.PADsql.Username)
        builder.get_object("lblCollectionCount").config(text ="Monsters\t= " + str(len(self.PADsql.selectMonsterInstance())))
        builder.get_object("lblTeamCount").config(text ="Teams\t= " + str(len(self.PADsql.selectTeamInstance())))

    def quit(self):
        super().quit()
PADification()
