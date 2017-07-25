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
        self.builder.get_object('entPassword').bind('<Return>', self.onLoginClick)
        self.builder.get_object('entEmail').bind('<Return>', self.onLoginClick)
        self.Email = self.builder.get_variable('varEmail')
        self.Password = self.builder.get_variable('varPassword')
        self.Passw = self.builder.get_object('entPassword')

    #Activates next screen when button is clicked
    def onCreateAccountClick(self, event):
        """Occurs When Create Account Button Is Clicked"""
        self.master.showAccountCreation()

    def onLoginClick(self, event):
        """Occurs When Login Button Is Clicked"""
        self.master.PADsql.login(self.Email.get(), self.Password.get())
        if self.master.PADsql.signedIn:
            self.master.showHomeScreen()
        else:
            mb.showwarning('Login Error', 'Email and Password Do not exist!')

    def onEmailFocusIn(self,event):
        """Clears Username Entry Field"""
        if self.Email.get() == ("Enter Email"):
            self.builder.get_object('entEmail').config(foreground="#000000")
            self.Email.set("")

    def onEmailFocusOut(self,event):
        """Fills Empty Field with Enter Email"""
        if self.Email.get() == "":
            self.builder.get_object('entEmail').config(foreground="#c6caca")
            self.Email.set("Enter Email")

    def onPasswordFocusIn(self,event):
        """Clears Password Entry Field"""
        if self.Password.get() == ("Enter Password"):
            self.builder.get_object('entPassword').config(foreground="#000000")
            self.Password.set("")
            self.Passw.config(show="*")

    def onPasswordFocusOut(self,event):
        """Fills Password Entry Field with Enter Password"""
        if self.Password.get() == (""):
            self.builder.get_object('entPassword').config(foreground="#c6caca")
            self.Password.set("Enter Password")
            self.Passw.config(show="")