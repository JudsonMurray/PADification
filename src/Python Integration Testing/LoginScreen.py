# !/usr/bin/env Python3

#   Author: ZACHARY BLUE
#   Date:   JUNE 21ST 2017
#   Purpose:MAKE THE LOGIN SCREEN FOR PADification WORK
import tkinter as tk
from tkinter import *
import tkinter.messagebox as mb
import pygubu
import pypyodbc
class LoginScreen:
    def __init__(self, master):
        self.master = master

        #Create builder
        self.builder = pygubu.Builder()

        #Load UI file
        self.builder.add_from_file(r"C:\Users\Tester\Documents\PADification\src\ui\Login UI.ui")

        #Create widget and add title image
        self.mainwindow = self.builder.get_object('Login Screen',master)
        #self.PICTURES = 'PADification Title.png'
        self.builder.connect_callbacks(self)
        self.image1 = PhotoImage(file = 'PADification Title.png')
        item = self.builder.get_object('TitleCanvas').create_image(10,0,image = self.image1,anchor = NW,tag="Title")

    #Activates next screen when button is clicked
    def onCreateAccountClick(self):
        """Occurs When Create Account Button Is Clicked"""
        self.master.showAccountCreation()
    def onLoginClick(self, event):
        """Occurs When Login Button Is Clicked"""
        self.master.showHomeScreen()