# !/usr/bin/env Python3

#   Author: ZACHARY BLUE
#   Date:   JUNE 21ST 2017
#   Purpose:MAKE THE LOGIN SCREEN FOR PADification WORK
import tkinter as tk
from tkinter import *
import tkinter.messagebox as mb
import pygubu

class LoginScreen:
    def __init__(self, master):
        self.master = master
        self.builder = pygubu.Builder()

        self.builder.add_from_file(r"C:\Users\Tester\Documents\PADification Python stuff\PADification UI\Login UI.ui")
        self.loginscreen = self.builder.get_object('Login Screen',master)
        self.PICTURES = r'C:\Users\Tester\Documents\PADification Python stuff\LoginScreen\pictures/'
        self.builder.connect_callbacks(self)
        self.image1 = PhotoImage(file = self.PICTURES + 'PADificationTitle.gif')
        item = self.builder.get_object('TitleCanvas').create_image(10,0,image = self.image1,anchor = NW,tag="Title")

class PADification(tk.Tk):
    def __init__(self, screenName = None, baseName = None, className = 'Tk', useTk = 1, sync = 0, use = None):
        super().__init__(screenName, baseName, className, useTk, sync, use)

        self.loginscreen = LoginScreen(self)

        super().mainloop()

PADification()