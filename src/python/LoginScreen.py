# !/usr/bin/env Python3

#   Author: ZACHARY BLUE
#   Date:   JUNE 21ST 2017
#   Purpose:MAKE THE LOGIN SCREEN FOR PADification WORK

# V1.4 - WG - Integration of SQL Login check.

import tkinter as tk
from tkinter import *
import tkinter.messagebox as mb
import pygubu

class LoginScreen:
    def __init__(self, master):
        self.master = master
        #Create builder
        self.builder = pygubu.Builder()

        #Load UI file
        self.builder.add_from_file("src/ui/Login UI.ui")

        #Create widget and add title image
        self.mainwindow = self.builder.get_object('Login Screen',master)
        self.image1 = PhotoImage(file = 'Resource/PAD/Images/PADification Title.png')
        item = self.builder.get_object('TitleCanvas').create_image(10,0,image = self.image1,anchor = NW,tag="Title")
        self.builder.connect_callbacks(self)

        self.obj1 = self.builder.get_object('Username',master)
        self.obj2 = self.builder.get_object('Password',master)
        self.isUsername = self.obj1.get()
        self.isPassword = self.obj2.get()

    #Activates next screen when button is clicked
    def onCreateAccountClick(self, event):
        """Occurs When Create Account Button Is Clicked"""
        self.master.showAccountCreation()

    def onLoginClick(self, event):
        """Occurs When Login Button Is Clicked"""
        self.master.PADsql.login(self.builder.get_variable('Username').get(), self.builder.get_variable('Password').get())
        if self.master.PADsql.signedIn:
            self.master.showHomeScreen()
        else:
            mb.showwarning('Login Error', 'Username and Password Do not exist!')

    def onUsernameFocusIn(self,event):
        """Clears Username Entry Field"""
        if self.obj1.get() == self.isUsername:
            self.obj1.delete(0,END)

    def onUsernameFocusOut(self,event):
        """Clears Username Entry Field"""
        if self.obj1.get() == "":
            self.obj1.insert(0,"Username")

    def onPasswordFocusIn(self,event):
        """Clears Password Entry Field"""
        if self.obj2.get() == self.isPassword:
            self.obj2.delete(0,END)

    def onPasswordFocusOut(self,event):
        """Clears Password Entry Field"""
        if self.obj2.get() == "":
            self.obj2.insert(0,"Password")