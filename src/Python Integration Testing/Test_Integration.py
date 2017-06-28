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

class PADification(tk.Tk):
    def __init__(self, screenName = None, baseName = None, className = 'Tk', useTk = 1, sync = 0, use = None):
        super().__init__(screenName, baseName, className, useTk, sync, use)
        

        self.loginScreen = LoginScreen.LoginScreen(self)
        self.accountCreation = AccountCreation.Testing(self)
        self.homeScreen = Home_Screen.HomeScreen(self)

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

    def showHomeScreen(self):
        self.forgetAll()
        self.homeScreen.mainwindow.grid()

    #Removes all frames from the screen
    def forgetAll(self):
        """Forgets all frames"""
        self.loginScreen.mainwindow.grid_forget()
        self.accountCreation.mainwindow.grid_forget()
        self.homeScreen.mainwindow.grid_forget()

PADification()