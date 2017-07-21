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
        self.TEAMRESULTSPERPAGE = 6
        self.PLAYERRESULTSPERPAGE = 9

        #Load GUI
        self.master = master
        self.builder = pygubu.Builder()
        self.builder.add_from_file('src/ui/HomeScreen.ui')
        self.mainwindow = self.builder.get_object('homePageFrame', master)
        self.builder.connect_callbacks(self)

        #Screen Widgets
        self.canProfileImage = self.builder.get_object('canProfileImage')
        self.lblUsername = self.builder.get_object('lblUsername')
        self.lblCollectionCount = self.builder.get_object('lblCollectionCount')
        self.lblTeamCount = self.builder.get_object('lblTeamCount')
        self.canTeamPreviewer = self.builder.get_object('canTeamPreviewer')
        self.TeamPreviews = []

        self.canFollow = self.builder.get_object('canFollow')
        self.FollowFrames = []
        self.Following = None
        self.Followers = None

        self.canPlayerSearch = self.builder.get_object('canPlayerSearch')
        self.PlayerSearchFrames = []

        self.entTeamSearch = self.builder.get_object("entSearchTeams")
        self.entPlayerSearch = self.builder.get_object("entPlayerSearch")
       

        #Pygubu Variables
        self.FollowSwitch = self.builder.get_variable("varFollowSwitch")
        self.TeamSearch = self.builder.get_variable("varTeamSearch")
        self.PlayerSearch = self.builder.get_variable("varPlayerSearch")

        #Screen Variables
        self.ProfileImage = None
        self.imgTitleImage = PhotoImage(file = "Resource/PAD/Images/Padification Logo.png")
        self.builder.get_object('lblTitleImage').config(image = self.imgTitleImage)
        self.firstLoad = True
        self.PlayerSearchResults = None
        self.TeamSearchResults = None

        for i in range( 0 , self.TEAMRESULTSPERPAGE ):
            self.TeamPreviews.append(TeamPreview(self.canTeamPreviewer, self))

        for i in range( 0 , self.PLAYERRESULTSPERPAGE ):
            self.FollowFrames.append(playerWidget(self.canFollow,self))
            self.PlayerSearchFrames.append(playerWidget(self.canPlayerSearch,self))

        self.AttributeImages = dict()
        for i in ["Fire","Water","Wood","Light","Dark"]:
            self.AttributeImages[i] = PhotoImage(file = 'Resource/PAD/Images/Attributes/' + i + "Symbol.png")
            self.builder.get_object("chkPri" + i).config(image = self.AttributeImages[i])
            ToolTip.ToolTip(self.builder.get_object("chkPri" + i) , i)



    def update(self):
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


        if self.firstLoad:
            self.updateFollowings()
            self.updateFrames(self.master.PADsql.selectAllTeamInstance(), self.TeamPreviews, rand = True)
            self.updateFrames(self.master.PADsql.selectUsers(), self.PlayerSearchFrames, rand = True)
            self.updateFrames(self.master.PADsql.selectFollowings(), self.FollowFrames, rand = False)
            self.firstLoad = False


    def updateFrames(self, sqlQuery, Frames, rand = False):
        Selected = []
        for i in Frames:
            i.mainFrame.grid_forget()
        if rand:
            if len(sqlQuery) >= len(Frames):
                while len(Selected) < len(Frames):
                    choice = random.choice(sqlQuery)
                    if choice not in Selected:
                        Selected.append(choice)
                count = 0
                for i in Frames:
                    i.update(Selected[count])
                    i.mainFrame.grid(row = count)
                    count += 1
            else:
                random.shuffle(sqlQuery)
                count = 0
                for i in Frames:
                    if count >= len(sqlQuery):
                        break
                    i.update(sqlQuery[count])
                    i.mainFrame.grid(row = count)
                    count +=1
        else:
            count=0
            for i in Frames:
                if count >= len(sqlQuery):
                    break
                i.update(sqlQuery[count])
                i.mainFrame.grid(row = count)
                count +=1

    def updateFollowFrame(self):
        if self.FollowSwitch.get() == "Followers":
            self.updateFrames(self.master.PADsql.selectFollowers(), self.FollowFrames, rand = False)
        else:
            self.updateFrames(self.master.PADsql.selectFollowings(), self.FollowFrames, rand = False)


    def updateFollowings(self):
        self.Followings = self.master.PADsql.selectFollowings()
        self.Followers = self.master.PADsql.selectFollowers()
        print("Followers:", self.Followers)
        print("Followings:", self.Followings)


    def onSearchTeamsClick(self):
        PriAttributes = []
        for i in ["PriFire", "PriWater", "PriWood", "PriLight", "PriDark"]:
            if self.builder.get_variable(i).get() != "" and self.builder.get_variable(i).get() != "0":
                PriAttributes.append(self.builder.get_variable(i).get())
        if len(PriAttributes) == 0:
            PriAttributes = ["Fire","Water","Wood","Light","Dark"]

        value = self.TeamSearch.get()
        
        if value and value != "Enter Team Name.":
            self.updateFrames(self.master.PADsql.selectTeamInstance(value, allUser = True), self.TeamPreviews)
        else:
            self.updateFrames(self.master.PADsql.selectAllTeamInstance(), self.TeamPreviews, True)


    def onSearchBarFocusIn(self, event):
        #Clears Search Bar on focus
        if event.widget == self.entTeamSearch:
            if self.TeamSearch.get() == "Enter Team Name.":
                self.TeamSearch.set("")
        elif event.widget == self.entPlayerSearch:
            if self.PlayerSearch.get() == "Enter a Username.":
                self.PlayerSearch.set("")

    def onSearchBarFocusOut(self, event):
        #Populates empty Search bar on focus out
        if event.widget == self.entTeamSearch:
            if self.TeamSearch.get() == "":
                self.TeamSearch.set("Enter Team Name.")
        elif event.widget == self.entPlayerSearch:
            if self.PlayerSearch.get() == "":
                self.PlayerSearch.set("Enter a Username.")

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

        #Widget Objects
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
        self.canIdentity = dict()

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

        self.monToolTips = []
        for i in range(0,5):
            self.monToolTips.append(MonsterStatTooltip(getattr(self, "canTeamSlot" + str(i+1))))

    def update(self, teamDict):
        self.objTeam = PADMonster.Team(teamDict)
        self.strUsername = self.toplevel.master.PADsql.selectUsers(teamDict["Email"])
        self.lblTeamUsername.config(text = self.strUsername)
        self.lblTeamName.config(text = teamDict["TeamName"])


        for i in range(0,5):
            self.canIdentity[getattr(self, "canTeamSlot" + str(i+1))] = str(i+1)
            setattr(self, "monTeamSlot" + str(i+1), None)
            setattr(self, "imgTeamSlot" + str(i+1), None)
            keys = ['LeaderMonster', 'SubMonsterOne', 'SubMonsterTwo', 'SubMonsterThree', 'SubMonsterFour']
            if teamDict[keys[i]] != None:
                setattr(self, "monTeamSlot" + str(i+1), PADMonster.Monster(self.toplevel.master.PADsql.selectMonsterInstance(teamDict[keys[i]], allUsers = True)[0]))
                setattr(self, "imgTeamSlot" + str(i+1), PhotoImage(file = "resource/PAD/images/thumbnails/" + str(getattr(self, "monTeamSlot" + str(i+1)).MonsterClassID) + ".png" ).subsample(2))
                getattr(self, "canTeamSlot" + str(i+1)).create_image(2,2, image = getattr(self, "imgTeamSlot" + str(i+1)), anchor = NW)
                self.monToolTips[i].update(getattr(self, "monTeamSlot" + str(i+1)))
            else:
                self.monToolTips[i].update()
                

    def onCanTeamSlotClick(self, event):
        if getattr(self, "monTeamSlot" + self.canIdentity[event.widget]) != None:
            print("you clicked", getattr(self, "monTeamSlot" + self.canIdentity[event.widget]).MonsterName)

class playerWidget():
    def __init__(self, master, toplevel):
        self.toplevel = toplevel
        self.master = master
        self.builder = pygubu.Builder()
        self.builder.add_from_file('src/ui/HomeScreen.ui')
        self.mainFrame = self.builder.get_object('frmPlayerPF', master)

        #Widget Objects
        self.canPlayerPF = self.builder.get_object('canPlayerPF', master)
        self.lblUsernamePF = self.builder.get_object('lblUsernamePF', master)

        self.popup = Menu(self.mainFrame, tearoff=0)
        self.popup.add_command(label="Follow", font="Yu", command=self.onFollow)
        self.popup.add_command(label="View Profile", font="Yu", command=self.onViewProfile)

        #Bindings
        for i in self.mainFrame.children:
            self.mainFrame.children[i].bind("<1>", self.onPlayerClick)

        #Variables
        self.Username = None
        self.Email = None
        self.ProfileImage = None
        self.ProfileImageFile = None


    def update(self, playerDict):
        self.Username = playerDict['Username']
        self.Email = playerDict['Email']
        self.ProfileImage = playerDict['ProfileImage']

        self.lblUsernamePF.config(text = self.Username)
        #self.lblTeamCountPF.config()

        if self.ProfileImage != None:
            value = self.ProfileImage
        else:
            value = 1

        self.ProfileImageFile = PhotoImage(file = 'Resource/PAD/Images/thumbnails/' + str(value) + ".png").subsample(3)
        self.canPlayerPF.create_image(2,2, image = self.ProfileImageFile, anchor = NW)

        if self.master == self.toplevel.canPlayerSearch:
            pass
        elif self.toplevel.FollowSwitch.get() == "Following":
            self.popup.entryconfig(0, label="UnFollow", font="Yu", command=self.onUnFollow)
        else:
            self.popup.entryconfig(0, label="Follow Back", font="Yu", command=self.onFollow)

    def onPlayerClick(self, event):
        try:
            self.popup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup.grab_release()

    def onViewProfile(self):
        print("Viewed Profile")

    def onFollow(self):
        if self.toplevel.master.PADsql.followPlayer(self.Email):
            print("Followed")
            self.toplevel.updateFollowFrame()
        else:
            print("Not Followed/ Already Followed")

    def onUnFollow(self):
        self.toplevel.master.PADsql.unFollowPlayer(self.Email)
        print("Unfollowed")
        self.toplevel.updateFollowFrame()