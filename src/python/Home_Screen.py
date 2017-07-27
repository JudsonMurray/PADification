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
import math
import logging

class HomeScreen():
    """Displays Home Screen Frame and widgets"""
    def __init__(self, master):
        self.logger = logging.getLogger("Padification.ui.HomeScreen")
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

        #Search and page Variables
        self.TeamSearchResults = None
        self.TeamCurPage = 1
        self.TeamMaxPage = 1
        self.entTeamPage = self.builder.get_variable("varTeamPageEnt")

        self.PlayerSearchResults = None
        self.PlayerCurPage = 1
        self.PlayerMaxPage = 1
        self.entPlayerPage = self.builder.get_variable("varPlayerSearchPg")

        self.FollowResults = None
        self.FollowCurPage = 1
        self.FollowMaxPage = 1
        self.entFollowPage = self.builder.get_variable("varFollowPg")

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
        # Called When switching to home and Updated Profile image.
        if self.master.PADsql.ProfileImage != None:
            value = self.master.PADsql.ProfileImage
        else:
            value = 1

        self.ProfileImage = PhotoImage(file = 'Resource/PAD/Images/thumbnails/' + str(value) + ".png")
        self.canProfileImage.create_image(2,2, image = self.ProfileImage, anchor = NW)
        self.lblUsername.config(text = self.master.PADsql.Username)
        self.lblCollectionCount.config(text ="Monsters\t= " + str(len(self.master.PADsql.selectMonsterInstance())) )
        self.lblTeamCount.config(text ="Teams\t= " + str(len(self.master.PADsql.selectTeamInstance())))

        if self.firstLoad: # Load Frames first time opened.
            self.onSearchTeamsClick()
            self.onPlayerSearch()
            self.updateFollowFrame()
            self.firstLoad = False

    def updateFrames(self, sqlQuery, Frames):
        #Update Frames with Results
        Selected = []
        for i in Frames:
            i.mainFrame.grid_forget()

        count=0
        for i in Frames:
            if count >= len(sqlQuery):
                break
            i.update(sqlQuery[count])
            i.mainFrame.grid(row = count)
            count +=1

    def updateFollowFrame(self):
        #Gets results for Followers and Followings and populates the frame
        if self.FollowSwitch.get() == "Followers":
            self.FollowResults = self.master.PADsql.selectFollowers()
        else:
            self.FollowResults = self.master.PADsql.selectFollowings()
        #Setup Page
        self.FollowCurPage = 1
        self.FollowMaxPage = math.ceil(len(self.FollowResults) / self.PLAYERRESULTSPERPAGE)
        if self.FollowMaxPage == 0:
            self.FollowMaxPage = 1
        self.entFollowPage.set(self.FollowCurPage)
        self.builder.get_object("lblFollowpg").config(text = " / " + str(self.FollowMaxPage))
        self.updateFollowPage()

    def updateFollowPage(self):
        #updates follow frams with results
        min = (self.FollowCurPage - 1) * self.PLAYERRESULTSPERPAGE
        self.updateFrames(self.FollowResults[min : min + self.PLAYERRESULTSPERPAGE ], self.FollowFrames)

    def onFollowPrev(self):
        if self.FollowCurPage > 1:
            self.FollowCurPage -= 1
        else:
            return
        self.entFollowPage.set(self.FollowCurPage)
        self.updateFollowPage()

    def onFollowNext(self):
        if self.FollowCurPage < self.FollowMaxPage:
            self.FollowCurPage += 1
        else:
            return
        self.entFollowPage.set(self.FollowCurPage)
        self.updateFollowPage()

    def onPlayerSearch(self, event = None):
        value = self.PlayerSearch.get()
        if value and value != "Enter a Username.":
            self.PlayerSearchResults = self.master.PADsql.selectUsers(Username = value)
        else:
            self.PlayerSearchResults = self.master.PADsql.selectUsers()
            random.shuffle(self.PlayerSearchResults)
            #Setup Page
        count = 0
        for i in self.PlayerSearchResults:
            if i["Email"].lower() == self.master.PADsql.Email.lower():
                self.PlayerSearchResults.pop(count)
            count += 1

        self.PlayerCurPage = 1
        self.PlayerMaxPage = math.ceil(len(self.PlayerSearchResults) / self.PLAYERRESULTSPERPAGE)
        self.entPlayerPage.set(self.PlayerCurPage)
        self.builder.get_object("lblPlayerSearchPg").config(text = " / " + str(self.PlayerMaxPage))

        #update Page Results
        self.updatePlayerSearch()

    def updatePlayerSearch(self):
        """Feeds update Frames a Page of results"""
        min = (self.PlayerCurPage - 1) * self.PLAYERRESULTSPERPAGE
        self.updateFrames(self.PlayerSearchResults[min : min + self.PLAYERRESULTSPERPAGE ], self.PlayerSearchFrames)

    def onPlayerNext(self):
        """Next Page of Team Results"""
        if self.PlayerCurPage < self.PlayerMaxPage:
            self.PlayerCurPage += 1
        else:
            return
        self.entPlayerPage.set(self.PlayerCurPage)
        self.updatePlayerSearch()

    def onPlayerPrev(self):
        """Next Page of Team Results"""
        if self.PlayerCurPage > 1:
            self.PlayerCurPage -= 1
        else:
            return
        self.entPlayerPage.set(self.PlayerCurPage)
        self.updatePlayerSearch()

    def onSearchTeamsClick(self, event = None):
        """Grab Search Results on Teams, Or Return all on Random."""
        ############################
        ##### GRAB ALL FILTERS #####
        ############################
        PriAttributes = []
        for i in ["PriFire", "PriWater", "PriWood", "PriLight", "PriDark"]:
            if self.builder.get_variable(i).get() != "" and self.builder.get_variable(i).get() != "0":
                PriAttributes.append(self.builder.get_variable(i).get())
        if len(PriAttributes) == 0:
            PriAttributes = ["Fire","Water","Wood","Light","Dark"]
        
        ###################################
        ##### GRAB ALL SEARCH RESULTS #####
        ###################################
        value = self.TeamSearch.get()
        if value and value != "Enter Team Name.":
            self.TeamSearchResults = self.master.PADsql.selectTeamInstance(value, allUser = True)
        else:
            self.TeamSearchResults = self.master.PADsql.selectTeamInstance(allUser = True, exlcudeUser = True)
            random.shuffle(self.TeamSearchResults)

        if len(PriAttributes) < 5:
            TeamFilteredResults = []
            for i in self.TeamSearchResults:
                if i["LeaderMonster"] != None:
                    query = self.master.PADsql.selectMonsterInstance(i["LeaderMonster"], allUsers = True)
                    if query:
                        testing = PADMonster.Monster(query[0])
                        if testing.PriAttribute in PriAttributes:
                            TeamFilteredResults.append(i)

            self.TeamSearchResults = TeamFilteredResults


        #Setup Page
        self.TeamCurPage = 1
        self.TeamMaxPage = math.ceil(len(self.TeamSearchResults) / self.TEAMRESULTSPERPAGE)
        self.entTeamPage.set(self.TeamCurPage)
        self.builder.get_object("lblPageNumber").config(text = "       / " + str(self.TeamMaxPage))
        self.builder.get_object("lblResults").config(text = str(len(self.TeamSearchResults)) + " Results.")
        #update Page Results
        self.updateTeamPage()

    def updateTeamPage(self):
        """Feeds update Frames a Page of results"""
        min = (self.TeamCurPage - 1) * self.TEAMRESULTSPERPAGE
        self.updateFrames(self.TeamSearchResults[min : min + self.TEAMRESULTSPERPAGE ], self.TeamPreviews)
    
    def onTeamNextPage(self):
        """Next Page of Team Results"""
        if self.TeamCurPage < self.TeamMaxPage:
            self.TeamCurPage += 1
        else:
            return
        self.entTeamPage.set(self.TeamCurPage)
        self.updateTeamPage()

    def onTeamPrevPage(self):
        """Next Page of Team Results"""
        if self.TeamCurPage > 1:
            self.TeamCurPage -= 1
        else:
            return
        self.entTeamPage.set(self.TeamCurPage)
        self.updateTeamPage()

    def onTeamPageEnter(self, event):
         pgnum = int(self.entTeamPage.get())
         if pgnum >= 1 and pgnum <= self.TeamMaxPage:
             self.TeamCurPage = pgnum
             self.updateTeamPage()

    def validatePageEntry(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        if text in "0123456789\b" and len(value_if_allowed) < 4:
            return True
        else:
            return False

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
        self.logger = logging.getLogger("Padification.ui.MonsterBook.TeamPreview")
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
        self.btnTeamVoteUp = self.builder.get_object('btnTeamUpVote')
        self.btnTeamVoteDown = self.builder.get_object('btnTeamDownVote')
        self.lblTeamRank = self.builder.get_object('lblTeamRank')

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
        self.TeamInstanceID = teamDict["TeamInstanceID"]

        self.updateVotes()

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
                
    def updateVotes(self):
        votes = self.toplevel.master.PADsql.getVotes(self.TeamInstanceID)
        self.voteCount = votes[0]

        self.lblTeamRank.config(text="%+d" % self.voteCount)
        if votes[1]== None:
            pass
        elif votes[1]:
            self.btnTeamVoteUp.config(foreground="#3DDE47")
            self.btnTeamVoteDown.config(foreground="#000000")
        else:
            self.btnTeamVoteDown.config(foreground="#DE1A18")
            self.btnTeamVoteUp.config(foreground="#000000")

    def onCanTeamSlotClick(self, event):
        if getattr(self, "monTeamSlot" + self.canIdentity[event.widget]) != None:
            print("you clicked", getattr(self, "monTeamSlot" + self.canIdentity[event.widget]).MonsterName)

    def onVoteUp(self):
        self.toplevel.master.PADsql.teamVote(self.TeamInstanceID, True)
        self.updateVotes()

    def onVoteDown(self):
        self.toplevel.master.PADsql.teamVote(self.TeamInstanceID, False)
        self.updateVotes()

class playerWidget():
    def __init__(self, master, toplevel):
        self.logger = logging.getLogger("Padification.ui.PlayerWidget")
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