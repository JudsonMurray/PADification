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
        self.image1 = PhotoImage(file = 'Resource/PAD/Images/PADification Title.png')
        item = self.builder.get_object('TitleCanvas').create_image(10,0,image = self.image1,anchor = NW,tag="Title")

        self.builder.connect_callbacks(self)

        self.obj1 = self.builder.get_object('New Username',master)
        self.obj2 = self.builder.get_object('New Password',master)
        self.obj3 = self.builder.get_object("Confirm New Password",master)

    def onMainMenuClick(self):
        """Displays Main Menu"""
        self.master.showHomeScreen()

    def onMonsterBookClick(self, event):
        self.master.showMonsterBook()

    def onMyMonstersClick(self):
        self.master.showPlayerCollection()

    def onMyTeamsClick(self, event):
        self.master.showTeamBrowser()

    def onUsernameFocusIn(self,event):
        """Clears New Username Entry Field"""
        if self.obj1.get() == "New Username":
            self.obj1.delete(0,END)

    def onUsernameFocusOut(self,event):
        """Repopulates New Username Entry Field"""
        if self.obj1.get() == "":
            self.obj1.insert(0,"New Username")

    def onPasswordFocusIn(self,event):
        """Clears New Password Entry Field"""
        if self.obj2.get() == "New Password":
            self.obj2.delete(0,END)

    def onPasswordFocusOut(self,event):
        """Repopulates New Password Entry Field"""
        if self.obj2.get() == "":
            self.obj2.insert(0,"New Password")

    def onNewPassFocusIn(self,event):
        """Clears New Password Confirmation Entry Field"""
        if self.obj3.get() == "Confirm New Password":
            self.obj3.delete(0,END)

    def onNewPassFocusOut(self,event):
        """Repopulates New Password Confirmation Entry Field"""
        if self.obj3.get() == "":
            self.obj3.insert(0,"Confirm New Password")