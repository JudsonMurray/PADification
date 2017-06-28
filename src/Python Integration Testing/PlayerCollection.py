#!/usr/bin/env python
#   Name:    Ryan Breau
#   Date:    06/23/17
#   Purpose: Functionality for the player collection screen
#   V.1.0   RB  Created base functionality for the player collection screen, known bugs are monster summary image is wrongly sized and type images not showing up
#   V.1.1   RB  Monster summary image now sized correctly and type images are now being displayed
#
#   Note: If using this in a new project, either change the paths for the images and ui or add the image folders into the and the ui into the project
#   Note: Most of the select queries will be changed from MonsterClass to MonsterInstance

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
        
        #Creates photoimages for neccessary 
        self.s = PhotoImage(file = "thumbnails/" + str(monsterClassIDs[self.i]) +'.png')
        
        #Retrieves monster information from database
        h = int(monsterClassIDs[self.i])
        sql = "Select MonsterName, Rarity, MaxHP, MaxATK, MaxRCV, MonsterTypeOne, MonsterTypeTwo, MonsterTypeThree From MonsterClass where MonsterClassID = {}".format(h)
        q = cursor.execute(sql)
        monster = q.fetchall()

        #Types
        self.e = PhotoImage(file = str(monster[0][5]) + '.png')

        self.mastermaster.get_object("canType2").delete("all")
        self.mastermaster.get_object("canType3").delete("all")

        if not monster[0][6] is None:
            self.f = PhotoImage(file = str(monster[0][6]) + '.png')
        else:
            self.f = None

        if not monster[0][7] is None:
            self.g = PhotoImage(file = str(monster[0][7]) + '.png')
        else:
            self.g = None

        #Populates fields with neccessary information
        self.mastermaster.get_object("canMonsterSummary").create_image(7,7, image = self.s, anchor = tk.NW)
        self.mastermaster.get_object("lblName").config(text = "Monster Name: " + str(monster[0][0]))
        self.mastermaster.get_object("lblRarity").config(text = "Rarity: " + str(monster[0][1]))
        self.mastermaster.get_object("lblHP").config(text = "HP: " + str(monster[0][2]))
        self.mastermaster.get_object("lblATK").config(text = "ATK: " + str(monster[0][3]))
        self.mastermaster.get_object("lblRCV").config(text = "RCV: " + str(monster[0][4]))
        self.mastermaster.get_object("lblID").config(text = "Monster ID: " + str(h))
        self.mastermaster.get_object("canType1").create_image(2,2, image = self.e, anchor = tk.NW)
        self.mastermaster.get_object("canType2").create_image(2,2, image = self.f, anchor = tk.NW)
        self.mastermaster.get_object("canType3").create_image(2,2, image = self.g, anchor = tk.NW)

class Testing:
    def __init__(self, master):
        #Creates globals
        global connection 
        global cursor
        global monsterClassIDs
        global myMonsterList
        global monsterInstance

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

        #sql = "Select InstanceID From MonsterInstance Where PlayerID = 350520414 Order By MonsterClassID ASC"
        #a = cursor.execute(sql)
        #monsterInstance = a.fetchall()

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
            self.buttons[i].monbut.grid(row=i // 10,column = i % 10)
            self.buttons[i].builder.get_object('FrameLabel').create_image(2,2, image = myMonsterList[i], anchor = tk.NW)

        self.container.config(height=(len(self.container.grid_slaves()) // 2) * 30)


root = tk.Tk()
app = Testing(root)

root.mainloop()