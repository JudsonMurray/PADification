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
from tkinter import simpledialog as sd

class AccountOptions:
    def __init__(self, master):
        self.logger = logging.getLogger("PADification.ui.AccountOptions")
        self.master = master
        self.builder = pygubu.Builder()

        self.builder.add_from_file("src/ui/Account Options UI.ui")
        self.mainwindow = self.builder.get_object("Account Options",master)       
        self.imgTitleImage = PhotoImage(file = "Resource/PAD/Images/Padification Logo.png")
        self.builder.get_object('lblTitleImage').config(image = self.imgTitleImage)
        self.canProfileImage = self.builder.get_object('canProfileImage')
        self.lblUsername = self.builder.get_object('lblUsername')
        self.lblCollectionCount = self.builder.get_object('lblCollectionCount')
        self.lblTeamCount = self.builder.get_object('lblTeamCount')

        self.builder.connect_callbacks(self)

        self.obj1 = self.builder.get_object('New Username',master)
        self.obj2 = self.builder.get_object('New Password',master)
        self.obj3 = self.builder.get_object("Confirm New Password",master)


    def onProfileImageClick(self, event):
        value = sd.askstring("Change Profile Image", "Enter Monster ID or Name:", parent=self.builder.get_object("canProfileImage"))
        if value is not None:
            if value.isnumeric():
                value = int(value)

            if self.master.PADsql.updateProfileImage(value):
                self.master.updateProfile(self.builder)
            else:
                mb.showinfo("Profile Image", "Monster ID Does Not Exist")

    def updateProfile(self):
        #print(self.master.PADsql.ProfileImage)
        if self.master.PADsql.ProfileImage != None:
            value = self.master.PADsql.ProfileImage
        else:
            value = 1

        self.ProfileImage = PhotoImage(file = 'Resource/PAD/Images/thumbnails/' + str(value) + ".png")
        self.builder.get_object("canProfileImage").create_image(2,2, image = self.ProfileImage, anchor = NW)

        #CustomFont_Label(self.builder.get_object('frmPlayerInfo'), text= self.master.PADsql.Username, font_path="Resource/PAD/Font/FOT-RowdyStd-EB.ttf", size=22).grid(row = 0, column = 1, sticky = NW)
        self.builder.get_object("lblUsername").config(text = self.master.PADsql.Username)
        self.builder.get_object("lblCollectionCount").config(text ="Monsters\t= " + str(len(self.master.PADsql.selectMonsterInstance())))
        self.builder.get_object("lblTeamCount").config(text ="Teams\t= " + str(len(self.master.PADsql.selectTeamInstance())))

    def updateLabel(self):
        self.updateProfile()
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
        if len(self.obj1.get()) >= 4 and len(self.obj1.get()) <= 15:
            changeUsername = True 

        elif self.obj1.get() == '':
            pass

        elif not len(self.obj1.get()) < 4 or len(self.obj1.get()) > 15:
                changeUsername = False
                return mb.showwarning("Invalid Username", "Input a Valid Username,\nMust be 4-15 characters long")

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