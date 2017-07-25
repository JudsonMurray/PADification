#   Author:  Ryan Breau
#   Date:    06/26/17
#   Purpose: Base functionality for the account creation screen
#   V.1.0   RB  Created base functionality, changes needed are: Cancel brings user to home screen when confirmed, CreateAccount brings user to a 
#                                                               different screen when successful, conditions for each input need to be determined
#   Note:   Only works if PADification was created on your current device
#   V.1.1   WG  Integrated with PADification.py Using the SQL object within the Master.

from tkinter import *
import tkinter as tk
import pygubu

class AccountCreation:
    def __init__(self, master):

        self.master = master
        #1: Creates a builder
        self.builder = builder = pygubu.Builder()

        #2: Loads an ui file
        builder.add_from_file('src/ui/Account Creation.ui')

        #3: Creates the widget using a master as parent
        self.mainwindow = builder.get_object('frmSignUp')
        builder.connect_callbacks(self)
        self.a = PhotoImage(file = 'Resource/PAD/Images/PADification Title.png')

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

        #Creates the user's account if none of the fields are invalid [Username, Password, Email, PlayerID]
        if self.Account:
            self.master.PADsql.signup(self.Email, self.Password, self.Name, self.ID)
            self.master.showLoginScreen()

    def Cancel(self):
        '''Occurs when the cancel button is clicked'''
        self.master.showLoginScreen()


#root = tk.Tk()
#app = Testing(root)

#root.mainloop()