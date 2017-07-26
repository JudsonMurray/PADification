# !usr/bin/env Python3

#   Name:   ZACHARY BLUE
#   Date:   JUNE 27TH 2017
#   Purpose:THE ACCOUNT OPTIONS SCREEN

import logging
import tkinter as tk
from tkinter import *
import tkinter.messagebox as mb
import pygubu
import re 


class AccountOptions:
    def __init__(self, master):
        self.logger = logging.getLogger("PADification.ui.AccountOptions")
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



    def updateLabel(self):
        x = self.master.PADsql.PlayerID
        self.lab1 = self.builder.get_object("IDNum")
        self.lab2 = self.builder.get_object("AccName")
        self.lab3 = self.builder.get_object("AccEmail")
        self.lab1.config(text = self.master.PADsql.PlayerID)
        self.lab2.config(text = self.master.PADsql.Username)
        self.lab3.config(text = self.master.PADsql.Email)

    def applyChanges(self):
        changePassword = None
        changeUsername = None 

        self.onNewPassFocusIn(self)
        self.onPasswordFocusIn(self)
        self.onUsernameFocusIn(self)
        #Update Password
        if re.match(r'[A-Za-z0-9@#$%^&+=]*$',self.obj2.get()) and len(self.obj2.get()) >= 8 and len(self.obj2.get()) <= 10 and self.obj2.get() == self.obj3.get():
            changePassword = True

        elif self.obj2.get() == '':
            pass

        elif not re.match(r'[A-Za-z0-9@#$%^&+=]*$',self.obj2.get()) or len(self.obj2.get()) < 8 or len(self.obj2.get()) > 10 or self.obj2.get() != self.obj3.get():
            changePassword = False
            return mb.showwarning("Invalid Password", "Input a Valid Password,\nMust be 8-10 characters long,\nand can contain A-Z a-z 0-9 @#$%^&+=")
        #Update Username
        if self.obj1.get() != '' and not self.obj1.get().isspace() :
            changeUsername = True 

        elif self.obj1.get() == '':
            pass

        else:
            mb.showerror("Update Error","Incorrect username format!")
            changeUsername = False
        if (changePassword == True and changeUsername == True) or (changePassword == True and changeUsername == None) or (changePassword == None and changeUsername == True):
            if changePassword == True:
                mb.showinfo("Successful Update","Password was updated")
                self.master.PADsql.updatePassword(self.obj2.get())
            if changeUsername == True:
                mb.showinfo("Successful Update","Username was updated!")
                self.master.PADsql.updateUsername(self.obj1.get())
        if (changePassword == None and changeUsername == None):
            mb.showinfo("No Changes","No changes were implemented")
        self.onNewPassFocusOut(self)
        self.onPasswordFocusOut(self)
        self.onUsernameFocusOut(self)
    def onHomeClick(self, event):
        """Displays Main Menu"""
        self.master.showHomeScreen()

    def onBookClick(self, event):
        self.master.showMonsterBook()

    def onCollectionClick(self, event):
        self.master.showPlayerCollection()

    def onTeamsClick(self, event):
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