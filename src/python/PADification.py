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

#1st Party Modules
import PADSQL
import PADMonster
import PlayerCollection
import MonsterEditScreen
import Monster_Info_Screen
import EditTeamScreen
#import LoginScreen
#import AccountCreation
import Home_Screen
import Account_Options_Screen
import MonsterBook
import TeamBrowserScreen

from CustomWidgets import *

logging.basicConfig(filename='log/' + '{:%Y-%m-%d %H-%M-%S}'.format(datetime.datetime.now()) + '.log', level=logging.WARN , format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())
logging.info("Application Start")

class PADification(tk.Tk):
    def __init__(self, screenName = None, baseName = None, className = 'Tk', useTk = 1, sync = 0, use = None):
        super().__init__(screenName, baseName, className, useTk, sync, use)

        #Logging object
        self.logger = logging.getLogger("Padification.root")

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
        #self.loginScreen = LoginScreen.LoginScreen(self)
        #self.accountCreation = AccountCreation.AccountCreation(self)
        self.homeScreen = Home_Screen.HomeScreen(self)
        self.accountOptions = Account_Options_Screen.AccountOptions(self)
        self.playerCollection = PlayerCollection.PlayerCollection(self)
        self.teamBrowser = TeamBrowserScreen.TeamBrowser(self)
        self.editTeam = EditTeamScreen.EditTeam(self)
        self.monsterEdit = MonsterEditScreen.MonsterEdit(self)
        #self.showLoginScreen()
        self.showHomeScreen()
        self.lower()

        LoginDialog(self,"LOGIN")
        if not self.PADsql.signedIn:
            self.destroy()

        super().mainloop()

    #Displays the login screen
    #def showLoginScreen(self):
    #    """Show Login Screen"""
    #    self.forgetAll()
    #    self.loginScreen.mainwindow.grid()

    def showEditMonster(self):
        self.forgetAll()
        self.monsterEdit.monsteredit.grid()

    #Displays the account creation screen
    #def showAccountCreation(self):
    #    """Show Account Creation"""
    #    self.forgetAll()
    #    self.accountCreation.mainwindow.grid()

    #Displays the home screen
    def showHomeScreen(self):
        """Show Home Screen""" 
        self.forgetAll()
        self.homeScreen.mainwindow.grid()
        if self.PADsql.signedIn:
            self.homeScreen.update()

    #Displays the account options screen
    def showAccountOptions(self):
        """Show Account Options Screen"""
        self.forgetAll()
        self.accountOptions.mainwindow.grid()
        self.accountOptions.updateLabel()

    def showMonsterBook(self):
        self.forgetAll()
        self.MonsterBook.mainwindow.grid()
        self.MonsterBook.update()

    def showPlayerCollection(self):
        """Show Player Collection Screen"""
        self.forgetAll()
        self.playerCollection.mainwindow.grid()
        self.playerCollection.pageOne()

    def showTeamBrowser(self):
        """Show Login Screen"""
        self.forgetAll()
        self.teamBrowser.loadUserTeams()
        self.teamBrowser.mainwindow.grid()

    def showEditTeamScreen(self):
        """Show Login Screen"""
        self.forgetAll()
        self.editTeam.mainwindow.grid()


    #Removes all frames from the screen
    def forgetAll(self):
        """Forgets all frames"""
        self.MonsterBook.mainwindow.grid_forget()
        #self.loginScreen.mainwindow.grid_forget()
        #self.accountCreation.mainwindow.grid_forget()
        self.homeScreen.mainwindow.grid_forget()
        self.accountOptions.mainwindow.grid_forget()
        self.playerCollection.mainwindow.grid_forget()
        self.teamBrowser.mainwindow.grid_forget()
        self.editTeam.mainwindow.grid_forget()
        self.editTeam.mainwindow.grid_forget()
        self.monsterEdit.monsteredit.grid_forget()

    def updateProfile(self, builder):
        """Updates player profile image, username, collection and team counts"""
        #print(self.PADsql.ProfileImage)
        if self.PADsql.ProfileImage != None:
            value = self.PADsql.ProfileImage
        else:
            value = 1

        self.ProfileImage = PhotoImage(file = 'Resource/PAD/Images/thumbnails/' + str(value) + ".png")
        builder.get_object("canProfileImage").create_image(2,2, image = self.ProfileImage, anchor = NW)

        #CustomFont_Label(self.builder.get_object('frmPlayerInfo'), text= self.PADsql.Username, font_path="Resource/PAD/Font/FOT-RowdyStd-EB.ttf", size=22).grid(row = 0, column = 1, sticky = NW)
        builder.get_object("lblUsername").config(text = self.PADsql.Username)
        builder.get_object("lblCollectionCount").config(text ="Monsters\t= " + str(len(self.PADsql.selectMonsterInstance())))
        builder.get_object("lblTeamCount").config(text ="Teams\t= " + str(len(self.PADsql.selectTeamInstance())))

    def quit(self):
        super().quit()
PADification()
