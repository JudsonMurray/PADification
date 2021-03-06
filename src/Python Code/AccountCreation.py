#   Author:  Ryan Breau
#   Date:    06/26/17
#   Purpose: Base functionality for the account creation screen
#   V.1.0   RB  Created base functionality, changes needed are: Cancel brings user to home screen when confirmed, CreateAccount brings user to a 
#                                                               different screen when successful, conditions for each input need to be determined
#   Note:   Only works if PADification was created on your current device
from tkinter import *
import tkinter as tk
import pygubu
import pypyodbc
import sys

class Testing:
    def __init__(self, master):
        NotConnected = True
        while NotConnected:
            self.connection = pypyodbc.connect('Driver={SQL Server};' 
                                            'Server=localhost;'
                                            'Database=PADification;' 
                                            'uid=PADmin;pwd=PADmin;')
            NotConnected = False
        self.cursor = self.connection.cursor()
        self.connection.commit()


        self.master = master
        #1: Creates a builder
        self.builder = builder = pygubu.Builder()

        #2: Loads an ui file
        builder.add_from_file('Account Creation.ui')

        #3: Creates the widget using a master as parent
        self.mainwindow = builder.get_object('frmSignUp')
        builder.connect_callbacks(self)
        self.a = PhotoImage(file = 'PADification Title.png')

        self.passw = self.builder.get_object('entPassword')
        self.repassw = self.builder.get_object('entPasswordConfirm')
        self.canvas = self.builder.get_object('canBanner')
        self.canvas.create_image(0,0, image = self.a, anchor = tk.NW) 

        self.passw.config(show = '*')
        self.repassw.config(show = '*')

    def CreateAccount(self):
        '''Occurs whenever the create account button is clicked button'''

        #Creates a boolean variable to keep track of the validity of the account being created
        self.Account = True
        
        #Creates a variable to store the value entered into the player id entry box
        self.ID = self.builder.get_object('entPlayerID').get()
        #Checks whether the user entered anything into the entry box
        if self.ID == '':
            print('You must enter your player ID')
            self.Account = False
        #Checks whether the user entered a possible ID
        elif not self.ID.isnumeric():
            print('Player ID must be a numeric value')
            self.Account = False

        #Creates a variable to store the value entered into the username entry box
        self.Name = self.builder.get_object('entUsername').get()
        #Checks whether the user entered anything into the entry box
        if self.Name == '':
            print('You must enter your Username')
            self.Account = False
        
        #Creates a variable to store the value entered into the password entry box
        self.Password = self.passw.get()
        #Checks whether the user entered anything into the entry box
        if self.Password == '':
            print('You must enter your Password')
            self.Account = False

        #Creates a variable to store the value entered into the password confirmation entry box
        self.RePassword = self.repassw.get()
        #Checks whether the user entered anything into the entry box
        if self.RePassword == '':
            print('You must re-enter your Password')
            self.Account = False
        #Checks whether the user successfully entered the same password into the entry box
        elif not self.RePassword == self.Password:
            print('Passwords do not match')
            self.Account = False

        #Creates a variable to store the value entered into the email entry box
        self.Email = self.builder.get_object('entEmail').get()
        #Checks whether the user entered anything into the entry box
        if self.Email == '':
            self.Email = 'Null'

        #Creates the user's account if none of the fields are invalid
        if self.Account:
            sql = "Insert into Player(PlayerID, [Password], Email, Username) Values ('" + str(self.ID) +"', '" + str(self.Password) +"', '" + str(self.Email) +"', '" + str(self.Name) +"')"
            q = self.cursor.execute(sql)
            print('Account Created Successfully')
            self.connection.commit()

    def Cancel(self):
        '''Occurs when the cancel button is clicked'''
        #Ends the program, for now
        sys.exit()


root = tk.Tk()
app = Testing(root)

root.mainloop()