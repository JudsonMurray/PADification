# !/usr/bin/env Python3

#   Name:   ZACHARY BLUE
#   Date:   JUNE 27TH 2017
#   Purpose:INTEGRATE THE LOGIN AND ACCOUNT CREATION SCREENS FOR PADification

import tkinter as tk
from tkinter import *
import tkinter.messagebox as mb
import pygubu
import LoginScreen
import AccountCreation
import pypyodbc
import Home_Screen
import Account_Options_Screen
class PADification(tk.Tk):
    def __init__(self, screenName = None, baseName = None, className = 'Tk', useTk = 1, sync = 0, use = None):
        super().__init__(screenName, baseName, className, useTk, sync, use)
        

        self.loginScreen = LoginScreen.LoginScreen(self)
        self.accountCreation = AccountCreation.Testing(self)
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

    #def showPlayerCollection(self)
    #    """Show Player Collection Screen"""
    #    self.forgetAll()
    #    self.playerCollection.mainwindow.grid()

    #Removes all frames from the screen
    def forgetAll(self):
        """Forgets all frames"""
        self.loginScreen.mainwindow.grid_forget()
        self.accountCreation.mainwindow.grid_forget()
        self.homeScreen.mainwindow.grid_forget()
        self.accountOptions.mainwindow.grid_forget()
        #self.playerCollection.mainwindow.grid_forget()

PADification()