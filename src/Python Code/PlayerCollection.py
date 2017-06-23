#!/usr/bin/env python
#   Name:    Ryan Breau
#   Date:    06/23/17
#   Purpose: Functionality for the player collection screen
#   Note: If using this in a new project, either change the paths for the images and ui or add the image folders into the and the ui into the project 

from tkinter import *
import tkinter as tk
import pygubu
import random
import pypyodbc
import sys
import time


class MonsterFrame:
    def __init__(self, master, mastermaster, i):
        self.master = master
        self.mastermaster = mastermaster
        self.i = i
        self.builder = pygubu.Builder()
        self.builder.add_from_file('PlayerCollection.ui')
        self.monbut = self.builder.get_object('MonsFrame', self.master)
        self.builder.connect_callbacks(self)
        
    def clickMe(self, event):
        '''Occurs everytime a monster in the player collection is clicked'''

        #Creates globals to be used in method
        global monsterClassIDs
        global myMonsterList
        global connection
        global cursor

        #print("i by clicked")
        #print(monsterClassIDs[self.i])
        
        #Creates photoimages for neccessary 
        s = PhotoImage(file = "thumbnails/" + str(monsterClassIDs[self.i]) +'.png')
        #e = PhotoImage(file = 'godly.png')
        
        #Retrieves information from database
        h = int(monsterClassIDs[self.i])
        sql = "Select MonsterName From MonsterClass where MonsterClassID = {}".format(h)
        q = cursor.execute(sql)
        monsterName = q.fetchall()
        monsterName = str(monsterName).replace("(", "")
        monsterName = monsterName.replace(",)", "")
        monsterName = monsterName.replace("[", "")
        monsterName = monsterName.replace("]", "")
        monsterName = monsterName.replace("\'", "")


        #Populates fields with neccessary information
        self.mastermaster.get_object("canMonsterSummary").create_image(7,7, image = myMonsterList[self.i], anchor = tk.NW)
        self.mastermaster.get_object("lblName").config(text = "Monster Name: " + str(monsterName))
        
        #Failed attempts to add images for monster types
        #self.mastermaster.get_object("canType1").create_image(7,7, image = e, anchor = tk.NW)
        #canType1 = Label(self.mastermaster.get_object("frmTypes"), image = e)
        #canType1.pack()


        
class Testing:
    def __init__(self, master):
        #Creates globals
        global connection 
        global cursor
        global monsterClassIDs
        global myMonsterList

        #Connects to local database
        NotConnected = True
        while NotConnected:
            connection = pypyodbc.connect('Driver={SQL Server};' 
                                            'Server=localhost;'
                                            'Database=SWTS1103;' 
                                            'uid=PADmin;pwd=PADmin;')
            NotConnected = False
        cursor = connection.cursor()
        connection.commit()

        #Retrieves monster IDs from database
        sql = "SELECT MonsterClassID FROM monsterInstance WHERE PlayerID = 350520414 ORDER BY MonsterClassID ASC"

        playerTable = cursor.execute(sql)
        myMonsters = playerTable.fetchall()

        monsterClassIDs = []
        myMonsterList = []
        x=0

        #Populates lists with monsterIDs
        for i in myMonsters:
            myMonster = str(myMonsters[x]).replace("(", "")
            myMonster = myMonster.replace(",)", "")
            monsterClassIDs += myMonster,
            myMonster= tk.PhotoImage(file = 'thumbnails/'+ str(myMonster) + '.png').zoom(15)
            myMonster = myMonster.subsample(30)
            myMonsterList.append(myMonster)
            x+=1
        b = len(myMonsterList)

        self.master = master
        #1: Creates a builder
        self.builder = builder = pygubu.Builder()

        #2: Loads an ui file
        builder.add_from_file('PlayerCollection.ui')

        #3: Creates the widget using a master as parent
        self.mainwindow = builder.get_object('frmPlayerCollection')
        builder.connect_callbacks(self)

        self.container = self.builder.get_object('canMonsterList')

        #Creates a graphical list of monsters
        self.buttons = []
        for i in range(0,b):
            self.buttons.append(MonsterFrame(self.container, self.builder, i))
            #print('.', end = '')
            self.buttons[i].monbut.grid(row=i // 10,column = i % 10)
            self.buttons[i].builder.get_object('FrameLabel').create_image(2,2, image = myMonsterList[i], anchor = tk.NW)

        self.container.config(height=(len(self.container.grid_slaves()) // 2) * 30)


root = tk.Tk()
app = Testing(root)

root.mainloop()