#!/USR/BIN/ENV PYTHON 3.5
#   NAME:    KYLE GUNTON
#   DATE:    06/26/17
#   PURPOSE: FUNCTIONALITY FOR THE EDIT TEAM SCREEN 

#   -V. 0.0.1 -Created base functionality of selection monsters in player collection.

import pygame
import tkinter as tk
import pygubu
from tkinter import messagebox
from tkinter import *
import tkinter as tk
import pypyodbc
import sys

class MonsterFrame:
    def __init__(self, master, mastermaster, i):
        self.master = master
        self.mastermaster = mastermaster
        self.i = i
        self.builder = pygubu.Builder()
        self.builder.add_from_file('ui/PlayerCollection.ui')
        self.monbut = self.builder.get_object('MonsFrame', self.master)
        self.builder.connect_callbacks(self)
        
    def clickMe(self, event):
        '''Method for selection of a monster in the player collection'''

        #Call globals to be used in method
        global monsterClassIDs
        global myMonsterList
        global connection
        global cursor
        global rowFull
        global teamCanvasWidth 
        global teamCanvasHeight 
        
        #Retrieves information from database and removes excess string content
        h = int(monsterClassIDs[self.i])
        sql = "Select MonsterName From MonsterClass where MonsterClassID = {}".format(h)
        y = cursor.execute(sql)
        monsterName = y.fetchall()
        monsterName = str(monsterName).replace("(", "")
        monsterName = monsterName.replace(",)", "")
        monsterName = monsterName.replace("[", "")
        monsterName = monsterName.replace("]", "")
        monsterName = monsterName.replace("\'", "")

        self.builder.add_from_file('ui/HomeScreen.ui')

        #Adds monster collection buttons to monster collection
        teamCanvas = self.mastermaster.get_object('Canvas_3')
        teamCanvas.create_image(teamCanvasWidth, teamCanvasHeight, image = myMonsterList[self.i], anchor = tk.NW)
        rowFull+=1
        if rowFull % 7 == 0 :
            teamCanvasWidth = 7
            teamCanvasHeight += 80
            if (rowFull // 7+1) * 80 > 520:
                teamCanvas.config(height=(rowFull//7+1)*80)
        else:
            teamCanvasWidth += 80

class EditTeam():
    """Displays Edit Team Frame and Widgets"""
    def __init__(self, master):

        #Declare Globals
        global monsterClassIDs
        global myMonsterList
        global connection 
        global cursor
        global rowFull
        global teamCanvasWidth 
        global teamCanvasHeight 

        rowFull = 0
        teamCanvasWidth = 7
        teamCanvasHeight = 7

        #Create GUI and add title image
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('ui/EditTeam.ui')
        self.mainwindow = builder.get_object('EditTeamFrame', master)    
        self.titleImg = tk.PhotoImage(file = 'C:/Users/kyleg/Documents/Visual Studio 2015/SWTS1102/Home Screen/PADification Title.png')
        self.builder.get_object('titleImage').create_image(0,0, image =self.titleImg , anchor = tk.NW, tag = "pic")
        self.canvas = builder.get_object('Canvas_2')
        self.teamCanvas = builder.get_object('Canvas_3')


        #Connect to Database
        NotConnected = True
        while NotConnected:
            try:
                connection = pypyodbc.connect('Driver={SQL Server};' 
                                              'Server=localhost;'
                                              'Database=SWTS1103;' 
                                              'uid=PADmin;pwd=PADmin;')
                NotConnected = False
            except:
                pass

        cursor = connection.cursor()

        #Retrieves monster IDs from database
        sql = "SELECT MonsterClassID FROM monsterInstance WHERE PlayerID = 350520414"
        playerTable = cursor.execute(sql)
        myMonsters = playerTable.fetchall()
        connection.commit()

        #create a collection of resized monster thumbnails
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

        
        #Creates a list of buttons for the monsters in a players collection
        self.buttons = []
        self.canvas
        b = len(myMonsterList)

        for i in range(0,b):
            self.buttons.append(MonsterFrame(self.canvas, self.builder, i))
            self.buttons[i].monbut.grid(row=i // 10,column = i % 10)
            self.buttons[i].builder.get_object('FrameLabel').create_image(2,2, image = myMonsterList[i], anchor = tk.NW)
        self.canvas.config(height=(len(self.canvas.grid_slaves()) // 2) * 30)
        self.builder.connect_callbacks(self)



if __name__ == '__main__':
    root = tk.Tk()
    app = EditTeam(root)
    root.mainloop()