# !/usr/bin/env Python3

#   Author: ZACHARY BLUE
#   DATE:   JANUARY 12TH 2017
#   PURPOSE:CLAIM THE TITLE YOU RIGHTFULLY DESERVE

#   HISTORY:
#   v0.1: ZB - Gave functionality to main menu and game over buttons.
#   v0.2: BG - Renamed files for intergration. Changed classes to use Init
#   v0.3: ZB - Resized the font of title. Made title and game over into labels on a canvas
#   v0.4: ZB - Finally made text scroll!
#   v0.5: KG - Added images
#   v2.0: ZB - Text scrolls on canvas but game over needs fixing
#   V2.1: EG - added method for endless floors (line 59) incomplete
#   V2.2: EG - added the EndlessOver class for losing at endless floors mode
#   V2.3: KG - added Easter egg

from tkinter import *
from tkinter import messagebox
import pygubu

class Title:
    def __init__(self, master):
        self.master = master
        #Create Builder
        self.builder = builder = pygubu.Builder()

        #Load a ui file
        builder.add_from_file('DTDui/ZacksMenu.ui')

        #Create the widget
        self.mainwindow = builder.get_object('MainMenu', master) 

        self.builder.connect_callbacks(self)
        self.image1 = PhotoImage(file = self.master.RESOURCEDIR + 'Hydra.gif')
        self.image2 = PhotoImage(file = self.master.RESOURCEDIR + 'Knight.gif')
        builder.get_object('hydraCanvas').create_image(0,-40,image = self.image1,anchor = NW)
        builder.get_object('knightCanvas').create_image(30,120,image = self.image2)

        self.image3 = PhotoImage(file = self.master.RESOURCEDIR + 'Title.gif')
        item = builder.get_object('titleCanvas').create_image(-60,25,image = self.image3,anchor = NW)
        item2 = builder.get_object('titleCanvas').create_image(-795,25,image = self.image3,anchor = NW)
        def next_image(event=None):
            maxwidth = self.builder.get_object('titleCanvas').winfo_width()
            x0,y0 = self.builder.get_object('titleCanvas').coords(item)
            x1,y1 = self.builder.get_object('titleCanvas').coords(item2)
            if x0 > maxwidth:
                self.builder.get_object('titleCanvas').coords(item, (-795,y0))
                
            elif x1 > maxwidth:
                self.builder.get_object('titleCanvas').coords(item2, (-795,y0))
            else:
                self.builder.get_object('titleCanvas').move(item, 10, 0)
                self.builder.get_object('titleCanvas').move(item2, 10, 0)
            #self.builder.get_object('titleCanvas').move(item, 10, 0)
            self.builder.get_object('titleCanvas').after(1000 // 15, next_image)
        self.master.destroyerAtk = 0
        self.builder.get_object('titleCanvas').bind("<Button-3>", self.destroyerAtkUp)
        next_image()


    def destroyerAtkUp(self, event):
        self.master.destroyerAtk += 20
        print(self.master.destroyerAtk)

    def onNewGameClick(self):
        self.master.gameMode = 'normal'
        self.master.showNewGame()

    def onEndlessModeClick(self):
        self.master.gameMode = 'endless'
        self.master.showNewGame()

    def onLoadClick(self):
        #self.builder.get_object('MainMenu').grid_forget()
        self.master.showLoadFrame()

    def onCreditClick(self):
        self.master.showCreditsFrame()

    def onQuitClick(self):
        self.mainwindow.quit()


class GameOver:
    def __init__(self, master):
        self.master = master
        #Create Builder
        self.builder = builder = pygubu.Builder()

        #Load a ui file
        builder.add_from_file('DTDui/ZacksMenu.ui')

        #Create the widget
        self.mainwindow = builder.get_object('GameOver', master) 

        self.builder.connect_callbacks(self)

        self.image4 = PhotoImage(file = self.master.RESOURCEDIR + 'GameOver.gif')
        self.image5 = PhotoImage(file = self.master.RESOURCEDIR + 'GameOver.gif')
        item = builder.get_object('gameOverCanvas').create_image(-2600,25,image = self.image4,anchor = NW)
        item2 = builder.get_object('gameOverCanvas').create_image(0,25,image = self.image5,anchor = NW)
        def next_image(event=None):
            maxwidth = self.builder.get_object('gameOverCanvas').winfo_width()
            x0,y0 = self.builder.get_object('gameOverCanvas').coords(item)
            x1,y1 = self.builder.get_object('gameOverCanvas').coords(item2)
            if x0 > maxwidth:
                self.builder.get_object('gameOverCanvas').coords(item, (-640,y0))
                
            elif x1 > maxwidth:
                self.builder.get_object('gameOverCanvas').coords(item2, (-640,y1))
            else:
                self.builder.get_object('gameOverCanvas').move(item, 10, 0)
                self.builder.get_object('gameOverCanvas').move(item2, 10, 0)
            #self.builder.get_object('titleCanvas').move(item, 10, 0)
            self.builder.get_object('gameOverCanvas').after(1000 // 15, next_image)
        next_image()
    def onMenuClick(self):
        self.master.showMainMenu()
        #message = messagebox.askokcancel('Go To Menu','Do you really want to wipe progress and go to main menu?') 
        #if message == True:
        #    self.builder.get_object('GameOver').grid_forget
        #    self.builder.get_object('MainMenu')
        #elif message == False:
        #    pass

    def onNewGameClick(self):
        self.master.gameMode = 'normal'
        self.master.showNewGame()

    def onQuitClick(self):
        self.mainwindow.quit()


#-----------------------------------Endless floors game over-------------------------------------
class EndlessOVer:
    def __init__(self, master):
        self.master = master
        print('success from endlessOver')

        #create builder
        self.builder = builder = pygubu.Builder()

        #select file
        builder.add_from_file('DTDui/ZacksMenu.ui')

        #get screen
        self.endlessOver = builder.get_object('endlessOver', master)

        #callbacks 
        builder.connect_callbacks(self)
        
        self.image4 = PhotoImage(file = self.master.RESOURCEDIR + 'GameOver.gif')
        self.image5 = PhotoImage(file = self.master.RESOURCEDIR + 'GameOver.gif')
        item = builder.get_object('endlessOverCanvas').create_image(-2600,25,image = self.image4,anchor = NW)
        item2 = builder.get_object('endlessOverCanvas').create_image(0,25,image = self.image5,anchor = NW)
        def next_image(event=None):
            maxwidth = self.builder.get_object('endlessOverCanvas').winfo_width()
            x0,y0 = self.builder.get_object('endlessOverCanvas').coords(item)
            x1,y1 = self.builder.get_object('endlessOverCanvas').coords(item2)
            if x0 > maxwidth:
                self.builder.get_object('endlessOverCanvas').coords(item, (-640,y0))
                
            elif x1 > maxwidth:
                self.builder.get_object('endlessOverCanvas').coords(item2, (-640,y1))
            else:
                self.builder.get_object('endlessOverCanvas').move(item, 10, 0)
                self.builder.get_object('endlessOverCanvas').move(item2, 10, 0)
            #self.builder.get_object('titleCanvas').move(item, 10, 0)
            self.builder.get_object('endlessOverCanvas').after(1000 // 15, next_image)
        next_image()

        #Add data to endlessOver.ui
    def endlessOverUpdate(self):
        playername = self.builder.get_variable('playerHolder')
        playername.set(str(self.master.player.playerName))

        playerattack = self.builder.get_variable('atkHolder')
        playerattack.set(str(self.master.player.attacks))

        playerfloor = self.builder.get_variable('floHolder')
        playerfloor.set(str(self.master.player.floorsBeat))

        playerdd = self.builder.get_variable('ddHolder')
        playerdd.set(str(self.master.player.bossKills))

    def onMenuClick(self):
        self.master.showMainMenu()

    def onQuitClick(self):
        self.endlessOver.quit()



#if __name__ == '__main__':
#    root = Tk()
#    app = Title(root)
#    app.run()