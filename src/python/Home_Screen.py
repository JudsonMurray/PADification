#!/USR/BIN/ENV PYTHON 3.5
#   NAME:    KYLE GUNTON
#   DATE:    06/26/17
#   PURPOSE: FUNCTIONALITY FOR THE HOME SCREEN

#Version 0.0.1

import pygubu
import PADMonster
import random
from CustomWidgets import *
from tkinter import messagebox as mb
from tkinter import simpledialog as sd
from tkinter import *
from PIL import Image, ImageFont, ImageDraw, ImageTk

class HomeScreen():
    """Displays Home Screen Frame and widgets"""
    def __init__(self, master):
        self.RESULTSPERPAGE = 5
        #Load GUI
        self.master = master
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('src/ui/HomeScreen.ui')
        self.mainwindow = builder.get_object('homePageFrame', master)
        self.builder.connect_callbacks(self)

        #Screen Widgets
        self.canProfileImage = self.builder.get_object('canProfileImage')
        self.lblUsername = self.builder.get_object('lblUsername')
        self.lblCollectionCount = self.builder.get_object('lblCollectionCount')
        self.lblTeamCount = self.builder.get_object('lblTeamCount')
        self.canTeamPreviewer = self.builder.get_object('canTeamPreviewer')
        self.TeamPreviews = []

        #Screen Variables
        self.ProfileImage = None
        self.imgTitleImage = PhotoImage(file = "Resource/PAD/Images/Padification Logo.png")
        self.builder.get_object('lblTitleImage').config(image = self.imgTitleImage)

        for i in range( 0 , self.RESULTSPERPAGE ):
            self.TeamPreviews.append(TeamPreview(self.canTeamPreviewer, self))
            self.TeamPreviews[i].mainFrame.grid(row = i)

    def update(self):
        print(self.master.PADsql.ProfileImage)
        if self.master.PADsql.ProfileImage != None:
            value = self.master.PADsql.ProfileImage
        else:
            value = 1

        self.ProfileImage = PhotoImage(file = 'Resource/PAD/Images/thumbnails/' + str(value) + ".png")
        self.canProfileImage.create_image(2,2, image = self.ProfileImage, anchor = NW)

        #CustomFont_Label(self.builder.get_object('frmPlayerInfo'), text= self.master.PADsql.Username, font_path="Resource/PAD/Font/FOT-RowdyStd-EB.ttf", size=22).grid(row = 0, column = 1, sticky = NW)
 
   
        self.lblUsername.config(text = self.master.PADsql.Username)
        self.lblCollectionCount.config(text ="Monsters\t= " + str(len(self.master.PADsql.selectMonsterInstance())) )
        self.lblTeamCount.config(text ="Teams\t= " + str(len(self.master.PADsql.selectTeamInstance())))

        teams = self.master.PADsql.selectAllTeamInstance()
        teamset = []
        if len(teams) >= 5:
            while len(teamset) < 5:
                team = random.choice(teams)
                if team not in teamset:
                    teamset.append(team)

            count = 0
            for i in self.TeamPreviews:
                i.update(teamset[count])
                count += 1
        else:
            random.shuffle(teams)
            count = 0
            for i in self.TeamPreviews:
                if len(teams) < count:
                    break
                i.update(teams[count])
                count +=1

    def onProfileImageClick(self, event):
        value = sd.askstring("Change Profile Image", "Enter Monster ID or Name:", parent=self.canProfileImage)
        if value is not None:
            if value.isnumeric():
                value = int(value)

            if self.master.PADsql.updateProfileImage(value):
                self.update()
            else:
                mb.showinfo("Profile Image", "Monster ID Does Not Exist")

    def onHomeClick(self,event):
            self.master.showHomeScreen()

    def onCollectionClick(self,event):
        self.master.showPlayerCollection()

    def onBookClick(self,event):
        self.master.showMonsterBook()

    def onTeamsClick(self,event):
        self.master.showTeamBrowser()

    def onCommunityClick(self,event):
        pass

    def onTeamRankingClick(self,event):
        pass

    def onOptionsClick(self,event):
        self.master.showAccountOptions()

class TeamPreview():
    def __init__(self, master, toplevel):
        self.toplevel = toplevel
        self.master = master
        self.builder = pygubu.Builder()
        self.builder.add_from_file('src/ui/HomeScreen.ui')
        self.mainFrame = self.builder.get_object('frmTeamPreview', master)
        self.canTeamSlot1 = self.builder.get_object('canTeamSlot1')
        self.canTeamSlot2 = self.builder.get_object('canTeamSlot2')
        self.canTeamSlot3 = self.builder.get_object('canTeamSlot3')
        self.canTeamSlot4 = self.builder.get_object('canTeamSlot4')
        self.canTeamSlot5 = self.builder.get_object('canTeamSlot5')
        self.lblTeamUsername = self.builder.get_object('lblTeamUsername')
        self.lblTeamName = self.builder.get_object('lblTeamName')
        self.builder.connect_callbacks(self)

        #Variables
        self.objTeam = None
        self.strUsername = None
        

        self.imgTeamSlot1 = None
        self.imgTeamSlot2 = None
        self.imgTeamSlot3 = None
        self.imgTeamSlot4 = None
        self.imgTeamSlot5 = None

        self.imgTeamportrait1 = None
        self.imgTeamportrait2 = None
        self.imgTeamportrait3 = None
        self.imgTeamportrait4 = None
        self.imgTeamportrait5 = None

        self.monTeamSlot1 = None
        self.monTeamSlot2 = None
        self.monTeamSlot3 = None
        self.monTeamSlot4 = None
        self.monTeamSlot5 = None

    def update(self, teamDict):
        self.objTeam = PADMonster.Team(teamDict)
        self.strUsername = self.toplevel.master.PADsql.selectUsers(teamDict["Email"])
        self.lblTeamUsername.config(text = self.strUsername)
        self.lblTeamName.config(text = teamDict["TeamName"])

        for i in range(0,5):
            keys = ['LeaderMonster', 'SubMonsterOne', 'SubMonsterTwo', 'SubMonsterThree', 'SubMonsterFour']
            if teamDict[keys[i]] != None:
                setattr(self, "monTeamSlot" + str(i+1), PADMonster.Monster(self.toplevel.master.PADsql.selectMonsterInstance(teamDict[keys[i]], allUsers = True)[0]))
                setattr(self, "imgTeamSlot" + str(i+1), PhotoImage(file = "resource/PAD/images/thumbnails/" + str(getattr(self, "monTeamSlot" + str(i+1)).MonsterClassID) + ".png" ))
                getattr(self, "canTeamSlot" + str(i+1)).create_image(2,2, image = getattr(self, "imgTeamSlot" + str(i+1)), anchor = NW)

    def onCanTeamSlotClick(self, event):
        print("you clicked me")