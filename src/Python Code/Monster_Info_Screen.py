# !/usr/bin/env Python3

#   Name:   ZACHARY BLUE
#   Date:   JUNE 22ND 2017
#   Purpose:THE MONSTER INFO SCREEN FOR THE PADification APPLICATION

import tkinter as tk
from tkinter import *
import tkinter.messagebox as mb
import pygubu

class MonsterInfo:
    def __init__(self, master):
        self.master = master
        self.builder = pygubu.Builder()

        self.builder.add_from_file(r"C:\Users\Tester\Documents\PADification Python stuff\PADification UI\Monster Info UI.ui")
        self.monsterinfo = self.builder.get_object('Monster Info',master)

class PADification(tk.Tk):
    def __init__(self, screenName = None, baseName = None, className = 'Tk', useTk = 1, sync = 0, use = None):
        super().__init__(screenName, baseName, className, useTk, sync, use)

        self.monsterinfo = MonsterInfo(self)

        super().mainloop()

PADification()