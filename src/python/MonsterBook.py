#!/USR/BIN/ENV PYTHON 3.5
#   NAME:    Billy Gale 
#   DATE:    06/28/17
#   PURPOSE: MonsterBook Functionality

from PADMonster import Monster
import tkinter as tk
import pygubu
from tkinter import messagebox as mb
from tkinter import *


class MonsterFrame():
    def __init__(self, master, monster):
        self.count = 0
        self.monster = monster
        self.master = master
        self.builder = pygubu.Builder()

        self.builder.add_from_file('src/ui/MonsterBook.ui')
        self.frame = self.builder.get_object('MonsFrame', master)
        self.thumbnail = PhotoImage(file = 'Resource/PAD/Images/thumbnails/' + str(self.monster.MonsterClassID) + ".png")
        self.FrameLabel = self.builder.get_object('FrameLabel')
        self.FrameLabel.create_image(2,2, image = self.thumbnail, anchor = tk.NW)

    def onFrameClick(self, event):
        print('hello')

class MonsterBook():
    """Displays Home Screen Frame and widgets"""
    def __init__(self, master):
        self.master = master
        self.MonsterResults = []
        self.MonsterFrames = []
        self.builder = builder = pygubu.Builder()


        builder.add_from_file('src/ui/MonsterBook.ui')
        self.mainwindow = builder.get_object('frmMonsterBook', master)
        self.resultsFrame = builder.get_object('canMonsterList')
        self.builder.connect_callbacks(self)
        

    def update(self, search = None):
        self.MonsterResults = []
        self.MonsterFrames = []
        for i in self.resultsFrame.grid_slaves():
            i.grid_forget()
            i.destroy()

        monsters = self.master.PADsql.selectMonsterClass(search)
        for i in monsters:
            self.MonsterResults.append(Monster(i))


        for i in range(0,100 if len(self.MonsterResults) > 100 else len(self.MonsterResults)):
            self.MonsterFrames.append(MonsterFrame(self.resultsFrame, self.MonsterResults[i]))
            self.MonsterFrames[-1].frame.grid(row = i)
            
    def onSearchClick(self, event):
        search = self.builder.get_variable("SearchBar").get()
        try:
            search = int(search)
        except:
            pass
        self.update(search)
        #print('Search Click')
