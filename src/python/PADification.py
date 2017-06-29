# !/usr/bin/env Python3

#   Name:   WILLIMAM GALE
#   Date:   JUNE 28TH 2017
#   Purpose: Main for Padification Application.

# v1.0 WG - Integrated Code from Zachs Test_Integration.py,

#3rd Party Modules
import pypyodbc
import tkinter as tk
from tkinter import *
import tkinter.messagebox as mb
import pygubu

#1st Party Modules
import PADSQL
import PADMonster
#import PlayerCollection
import MonsterEditScreen
import Monster_Info_Screen
import EditTeamScreen
import LoginScreen
import AccountCreation
import Home_Screen
import Account_Options_Screen
import MonsterBook

class PADification(tk.Tk):
    def __init__(self, screenName = None, baseName = None, className = 'Tk', useTk = 1, sync = 0, use = None):
        super().__init__(screenName, baseName, className, useTk, sync, use)
        # Fix the Size of the Application
        self.minsize(width=1280, height=960)
        self.resizable(width=False, height=False)
        
        #pypyodbc SQl Object
        self.PADsql = PADSQL.PADSQL()

        #screens
        self.MonsterBook = MonsterBook.MonsterBook(self)
        self.loginScreen = LoginScreen.LoginScreen(self)
        self.accountCreation = AccountCreation.AccountCreation(self)
        self.homeScreen = Home_Screen.HomeScreen(self)
        self.accountOptions = Account_Options_Screen.AccountOptions(self)
        #self.playerCollection = PlayeCollection.Testing(self)
        self.showLoginScreen()
        super().mainloop()

    #Displays the login screen
    def showLoginScreen(self):
        """Show Login Screen"""
        self.forgetAll()
        self.loginScreen.mainwindow.grid()

    #Displays the account creation screen
    def showAccountCreation(self):
        """Show Account Creation"""
        self.forgetAll()
        self.accountCreation.mainwindow.grid()

    #Displays the home screen
    def showHomeScreen(self):
        """Show Home Screen"""
        self.forgetAll()
        self.homeScreen.mainwindow.grid()

    #Displays the account options screen
    def showAccountOptions(self):
        """Show Account Options Screen"""
        self.forgetAll()
        self.accountOptions.mainwindow.grid()

    def showMonsterBook(self):
        self.forgetAll()
        self.MonsterBook.mainwindow.grid()
        self.MonsterBook.update()

    #def showPlayerCollection(self)
    #    """Show Player Collection Screen"""
    #    self.forgetAll()
    #    self.playerCollection.mainwindow.grid()

    #Removes all frames from the screen
    def forgetAll(self):
        """Forgets all frames"""
        self.MonsterBook.mainwindow.grid_forget()
        self.loginScreen.mainwindow.grid_forget()
        self.accountCreation.mainwindow.grid_forget()
        self.homeScreen.mainwindow.grid_forget()
        self.accountOptions.mainwindow.grid_forget()
        #self.playerCollection.mainwindow.grid_forget()

PADification()
