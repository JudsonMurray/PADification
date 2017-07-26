#! usr/bin/env Python3
#
#
# Name: William Gale
# Date: 2017-07-04
# Purpose: Module Contains Custom Tkinter Widgets for Fun and glory.

import pygubu
from tkinter import messagebox as mb
from tkinter import simpledialog as sd
from tkinter import *
from PIL import Image, ImageFont, ImageDraw, ImageTk
from idlelib import ToolTip
import re
import logging

def truetype_font(font_path, size):
    return ImageFont.truetype(font_path, size)

class CustomFont_Label(Label):
    # Author: Miguel Martinez Lopez -- http://code.activestate.com/recipes/580778-tkinter-custom-fonts/
    def __init__(self, master, text, foreground="black", truetype_font=None, font_path=None, family=None, size=None, **kwargs):   
        self.logger = logging.getLogger("Padification.CustomWidgets.CustomFont_Label")
        if truetype_font is None:
            if font_path is None:
                raise ValueError("Font path can't be None")
                
            # Initialize font
            truetype_font = ImageFont.truetype(font_path, size)
        
        width, height = truetype_font.getsize(text)

        image = Image.new("RGBA", (width, height), color=(0,0,0,0))
        draw = ImageDraw.Draw(image)

        draw.text((0, 0), text, font=truetype_font, fill=foreground)
        
        self._photoimage = ImageTk.PhotoImage(image)
        Label.__init__(self, master, image=self._photoimage, **kwargs)

class CustomFont_Message(Label):
    # Author: Miguel Martinez Lopez -- http://code.activestate.com/recipes/580778-tkinter-custom-fonts/
    def __init__(self, master, text, width, foreground="black", truetype_font=None, font_path=None, family=None, size=None, **kwargs):   
        self.logger = logging.getLogger("Padification.CustomWidgets.CustomFont_Message")
        if truetype_font is None:
            if font_path is None:
                raise ValueError("Font path can't be None")
                
            # Initialize font
            truetype_font = ImageFont.truetype(font_path, size)
    
        lines = textwrap.wrap(text, width=width)

        width = 0
        height = 0
        
        line_heights = []
        for line in lines:
            line_width, line_height = truetype_font.getsize(line)
            line_heights.append(line_height)
            
            width = max(width, line_width)
            height += line_height

        image = Image.new("RGBA", (width, height), color=(0,0,0,0))
        draw = ImageDraw.Draw(image)

        y_text = 0
        for i, line in enumerate(lines):
            draw.text((0, y_text), line, font=truetype_font, fill=foreground)
            y_text += line_heights[i]

        self._photoimage = ImageTk.PhotoImage(image)
        Label.__init__(self, master, image=self._photoimage, **kwargs)

class ImageTooltip(ToolTip.ToolTipBase):
    def __init__(self, button, Photoimage):
        super().__init__(button)
        self.logger = logging.getLogger("Padification.CustomWidgets.ImageTooltip")
        self.PhotoImage = Photoimage
        self.label = None

    def showcontents(self):
        self.label = Label(self.tipwindow, image = self.PhotoImage, justify=LEFT,
                      background="#ffffe0", relief=GROOVE, borderwidth=8)

        self.label.pack()

class MonsterStatTooltip(ToolTip.ToolTipBase):
    def __init__(self, master):
        super().__init__(master)
        self.logger = logging.getLogger("Padification.CustomWidgets.MonsterStatTooltip")
        self.monster = None
        self.portrait = None
        self.portraitImage = None
        self.portraitimg = None
        self.portraitBanner = None
        self.portraitBannerImage = None
        self.portraitBannerPI = None
    
    def update(self, monster = None):

        if monster != None:
            self.monster = monster
            truetype_font = ImageFont.truetype("Resource/PAD/Font/FOT-RowdyStd-EB.ttf", 22)
            baseimg = Image.open("Resource/PAD/Images/PortraitBanner.jpg")
            portimg = Image.open("Resource/PAD/Images/portraits/"+ str(self.monster.MonsterClassID) + ".jpg")
            thumbimg = Image.open("Resource/PAD/Images/thumbnails/"+ str(self.monster.MonsterClassID) + ".png")
            baseimg.paste(portimg, (0,75))
            baseimg.paste(thumbimg,(11,472))
            draw = ImageDraw.Draw(baseimg)
            shadowcolor = "#000000"

            #draw Mon ID
            self.shadowText(draw, 10, 15, "No." + str(self.monster.MonsterClassID), truetype_font, shadowcolor)
            draw.text((10, 15), "No." + str(self.monster.MonsterClassID), font=truetype_font, fill="#ffffff")
            #draw Mon Name
            self.shadowText(draw, 10, 35, self.monster.MonsterName, truetype_font, shadowcolor)
            draw.text((10, 35), self.monster.MonsterName, font=truetype_font, fill="#ffffff")
            #draw Mon LVL
            self.shadowText(draw, 340, 475, "Lv."+str(self.monster.Level), truetype_font, shadowcolor)
            draw.text((340, 475), "Lv."+str(self.monster.Level), font=truetype_font, fill="#ffffff")
            #draw Mon Max LVL
            self.shadowText(draw, 340, 500, "Max Lv."+str(self.monster.MaxLevel), truetype_font, shadowcolor)
            draw.text((340, 500), "Max Lv."+str(self.monster.MaxLevel), font=truetype_font, fill="#ffffff")
            #draw Mon PLUSHP
            self.shadowText(draw, 260, 470, "(+" + str(self.monster.PlusHP) + ")", truetype_font, shadowcolor)
            draw.text((260, 470), "(+" + str(self.monster.PlusHP) + ")", font=truetype_font, fill="#fbfc19")
            #draw Mon PLUSATK
            self.shadowText(draw, 260, 503, "(+" + str(self.monster.PlusATK) + ")", truetype_font, shadowcolor)
            draw.text((260, 503), "(+" + str(self.monster.PlusATK) + ")", font=truetype_font, fill="#fbfc19")
            #draw Mon PLUSRCV
            self.shadowText(draw, 260, 537, "(+" + str(self.monster.PlusRCV) + ")", truetype_font, shadowcolor)
            draw.text((260, 537), "(+" + str(self.monster.PlusRCV) + ")", font=truetype_font, fill="#fbfc19")
            #draw Mon Cost
            self.shadowText(draw, 580, 480, str(self.monster.MonsterCost), truetype_font, shadowcolor)
            draw.text((580, 480), str(self.monster.MonsterCost), font=truetype_font, fill="#ffffff")
            #draw Mon Skill
            if self.monster.ActiveSkillName != None:
                self.shadowText(draw, 105, 585, str(self.monster.ActiveSkillName), truetype_font, shadowcolor)
                draw.text((105, 585), str(self.monster.ActiveSkillName), font=truetype_font, fill="#7cb4ee")

                self.shadowText(draw, 420, 545, "Lv." + str(self.monster.SkillLevel) + " Turn(s): " + str(self.monster.ActiveSkillMaxCoolDown - self.monster.SkillLevel + 1 ),
                                 truetype_font, shadowcolor)
                draw.text((420, 545), "Lv." + str(self.monster.SkillLevel) + " Turn(s): " + str(self.monster.ActiveSkillMaxCoolDown - self.monster.SkillLevel + 1 ),
                            font=truetype_font, fill="#ffffff")

            if self.monster.LeaderSkillName != None:
                self.shadowText(draw, 197, 700, str(self.monster.LeaderSkillName), truetype_font, shadowcolor)
                draw.text((197, 700), str(self.monster.LeaderSkillName), font=truetype_font, fill="#86ee7b")

            #Resize font
            truetype_font = ImageFont.truetype("Resource/PAD/Font/FOT-RowdyStd-EB.ttf", 26)
            #draw Mon HP
            self.shadowText(draw, 178, 470, str(self.monster.TotalHP), truetype_font, shadowcolor)
            draw.text((178, 470), str(self.monster.TotalHP), font=truetype_font, fill="#ffffff")
            #draw Mon ATK
            self.shadowText(draw, 178, 503, str(self.monster.TotalATK), truetype_font, shadowcolor)
            draw.text((178, 503), str(self.monster.TotalATK), font=truetype_font, fill="#ffffff")
            #draw Mon RCV
            self.shadowText(draw, 178, 537, str(self.monster.TotalRCV), truetype_font, shadowcolor)
            draw.text((178, 537), str(self.monster.TotalRCV), font=truetype_font, fill="#ffffff")

            values = ["One", "Two", "Three"]
            for i in range(0,3):
                if getattr(self.monster, "MonsterType" + values[i]) != None:
                    img = Image.open("Resource/PAD/Images/Types/" + getattr(self.monster, "MonsterType" + values[i]) + ".png")
                    baseimg.paste(img, (10 + ( i * 40 ), 80 ))

            img = Image.open("Resource/PAD/Images/RarityStar.png")
            for i in range(0,self.monster.Rarity):
                baseimg.paste(img, (250 + ( i * 30 ), 12 ))

            values = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
            for i in range(0,9):
                if getattr(self.monster, "AwokenSkill" + values[i]) != None:
                        if i < self.monster.SkillsAwoke:
                            img = Image.open("Resource/PAD/Images/Awoken Skills/" + getattr(self.monster, "AwokenSkill" + values[i]) + ".png")
                        else:
                            img = Image.open("Resource/PAD/Images/Awoken Skills/not " + getattr(self.monster, "AwokenSkill" + values[i]) + ".png")
                        baseimg.paste(img, (590, 80 + ((i) * 40)))
            #count = 0
            #for i in ["One", "Two", "Three", "Four", "Five", "Six"]:
            #    if getattr(self.monster, "LatentSkill" + values[i]) != None:
            #        #img = Image.open("Resource/PAD/Images/Awoken Skills/" + getattr(self.monster, "AwokenSkill" + values[i]) + ".png")

            self.portraitImage = baseimg
            self.portraitImage = self.portraitImage.resize((int(self.portraitImage.width / 1.5), int(self.portraitImage.height / 1.5 )), Image.ANTIALIAS)
            self.portraitimg = ImageTk.PhotoImage(self.portraitImage, self.portrait)

        else:
            self.monster = monster
            self.portrait = None
            self.portraitImage = None
            self.portraitimg = None

    def shadowText(self, drawer, x, y, text, font, color):
        drawer.text((x+2, y+2), text, font=font, fill=color)

    def showcontents(self):
        if self.monster != None:
            self.tipwindow.config(relief=GROOVE, borderwidth=10, background="#000000")
            self.portrait = Label(self.tipwindow, image = self.portraitimg, justify=LEFT,
                            background="#000000")
            self.portrait.grid(row=0, column=0, sticky=NW)

    def schedule(self):
        self.unschedule()
        self.id = self.button.after(250, self.showtip)

    def showtip(self):
        if self.monster != None:
            if self.tipwindow:
                return
            # The tip window must be completely outside the button;
            # otherwise when the mouse enters the tip window we get
            # a leave event and it disappears, and then we get an enter
            # event and it reappears, and so on forever :-(
            x = self.button.winfo_rootx() + self.button.winfo_width() + 1
            y = 250
            self.tipwindow = tw = Toplevel(self.button)
            tw.wm_overrideredirect(1)
            tw.wm_geometry("+%d+%d" % (x, y))
            self.showcontents()

class LoginDialog(sd.Dialog):
    def __init__(self, parent, title = None):
        self.logger = logging.getLogger("Padification.CustomWidgets.LoginDialog")
        # Screen State Constants
        self.LOGIN = 0
        self.CREATE = 1
        self.RECOVER = 2
        self.FGCOLOR = "#999999"
        self.imgTitleImage = PhotoImage(file = "Resource/PAD/Images/Padification Logo.png").subsample(2)

        self.varEmail = StringVar(value = "Enter Email")
        self.varPassword = StringVar(value = "Enter Password")
        self.varVerifyPassword = StringVar(value = "Confirm Password")
        self.varUsername = StringVar(value = "Enter Username")
        self.varPlayerID = StringVar(value = "Enter PlayerID")

        self.server = BooleanVar(value = True)
        self.servertxt = StringVar(value = "Remote")

        self.screenState = self.LOGIN

        #Frame Widgets
        self.frmbodyBox = None
        self.frmButtonBox = None

        #Login Widgets vars
        self.chkServerSelect = None
        self.entEmail = None
        self.entPassword = None

        #Create Account Widgets
        self.entUsername = None
        self.entPlayerID = None
        self.entVerifyPassword = None

        #Buttons Vars
        self.btnLogin = None
        self.btnCreateAccount = None
        self.btnExit = None
        self.btnRecover = None
        self.btnCancel = None
        self.btnCreate = None

        super().__init__(parent, title)

    def body(self, master):
        '''create dialog body.

        return widget that should have initial focus.
        This method should be overridden, and is called
        by the __init__ method.

        '''
        t = Frame(self)
        l = Label(t, image= self.imgTitleImage)
        l.pack()
        self.chkServerSelect = Checkbutton(t, indicatoron=False, font="yu", onvalue=False, offvalue=True, textvariable=self.servertxt, variable=self.server)
        self.chkServerSelect.bind("<1>", self.onServerClick)
        self.chkServerSelect.pack(pady=5)
        t.pack()

        self.frmbodyBox = box = Frame(self)

        
        self.entEmail = Entry(box, width=20, textvariable=self.varEmail,foreground=self.FGCOLOR, font="yu")
        self.entEmail.bind("<FocusIn>", self.onFocusIn)
        self.entEmail.bind("<FocusOut>", self.onFocusOut)

        self.entPassword = Entry(box, width=20, textvariable=self.varPassword,foreground=self.FGCOLOR, font="yu")
        self.entPassword.bind("<FocusIn>", self.onFocusIn)
        self.entPassword.bind("<FocusOut>", self.onFocusOut)
        
        self.entVerifyPassword = Entry(box, width=20, textvariable=self.varVerifyPassword,foreground=self.FGCOLOR, font="yu")
        self.entVerifyPassword.bind("<FocusIn>", self.onFocusIn)
        self.entVerifyPassword.bind("<FocusOut>", self.onFocusOut)

        self.entUsername = Entry(box, width=20, textvariable=self.varUsername,foreground=self.FGCOLOR, font="yu")
        self.entUsername.bind("<FocusIn>", self.onFocusIn)
        self.entUsername.bind("<FocusOut>", self.onFocusOut)

        self.entPlayerID = Entry(box, width=20, textvariable=self.varPlayerID,foreground=self.FGCOLOR, font="yu")
        self.entPlayerID.bind("<FocusIn>", self.onFocusIn)
        self.entPlayerID.bind("<FocusOut>", self.onFocusOut)

        self.entEmail.pack(pady=5)
        self.entPassword.pack(pady=5)

        box.pack()

    def buttonbox(self):
        '''add standard button box.
        override if you do not want the standard buttons
        '''

        self.frmButtonBox = box = Frame(self)
        self.btnLogin = Button(box, text="Login", width=15, command=self.onLoginClick, default=ACTIVE, font="yu")
        self.btnCreateAccount = Button(box, text="Create Account", width=15, command=self.onCreateAccountClick, font="yu")
        self.btnExit = Button(box, text="Exit", width=15, command=self.onExit, font="yu")
        self.btnRecover = Button(box, text="Recover Password", width=15, command=self.onRecoverClick, font="yu")
        self.btnCancel = Button(box, text="Cancel", width=15, command=self.onCancelClick, font="yu")


        self.btnLogin.grid(row=0, column = 0, padx=5, pady=5)
        self.btnExit.grid(row=0, column = 1, padx=5, pady=5)
        self.btnCreateAccount.grid(row=1, column = 0, padx=5, pady=5)
        self.btnRecover.grid(row=1, column = 1, padx=5, pady=5)

        self.bind("<Return>", self.onLoginClick)

        box.pack()

    def clearWidgets(self):
        self.focus()
        for i in self.frmbodyBox.pack_slaves():
            i.config(foreground=self.FGCOLOR)
            i.pack_forget()
        for i in self.frmButtonBox.grid_slaves():
            i.grid_forget()

        self.entPassword.config(show='')
        self.entVerifyPassword.config(show='')
        self.varEmail.set("Enter Email")
        self.varPassword.set("Enter Password")
        self.varVerifyPassword.set("Confirm Password")
        self.varUsername.set("Enter Username")
        self.varPlayerID.set("Enter PlayerID")

    def showLogin(self):
        self.clearWidgets()
        self.screenState = self.LOGIN

        # Entry Fields
        self.entEmail.pack(pady=5)
        self.entPassword.pack(pady=5)

        # Buttons
        self.btnLogin.grid(row=0, column = 0, padx=5, pady=5)
        self.btnExit.grid(row=0, column = 1, padx=5, pady=5)
        self.btnCreateAccount.grid(row=1, column = 0, padx=5, pady=5)
        self.btnRecover.grid(row=1, column = 1, padx=5, pady=5)

    def showCreateAccount(self):
        self.clearWidgets()
        self.screenState = self.CREATE

        # Entry Fields
        self.entEmail.pack(pady=5)
        self.entPassword.pack(pady=5)
        self.entVerifyPassword.pack(pady=5)
        self.entUsername.pack(pady=5)
        self.entPlayerID.pack(pady=5)

        # Buttons
        self.btnCreateAccount.grid(row=0, column = 0, padx=5, pady=5)
        self.btnCancel.grid(row=0, column = 1, padx=5, pady=5)

    def showRecovery(self):
        self.clearWidgets()
        self.screenState = self.RECOVER

        self.entEmail.pack(pady=5)
        self.btnRecover.grid(row=0, column = 0, padx=5, pady=5)
        self.btnCancel.grid(row=0, column = 1, padx=5, pady=5)

    def onRecoverClick(self):
        if self.screenState == self.LOGIN:
            self.showRecovery()
        elif self.screenState == self.RECOVER:
            if self.master.PADsql.retrievePassword(self.varEmail.get()):
                mb.showwarning("Email Recovery", "Password Sent to Email",parent=self)
            else:
                mb.showwarning("Email Recovery", "No such Email Exists",parent=self)
        pass

    def onCancelClick(self):
        self.showLogin()

    def onServerClick(self, event):
        if self.server.get():
            self.servertxt.set("localhost")
        else:
            self.servertxt.set("Remote")

    def onCreateAccountClick(self, event  = None):
        """Occurs When Create Account Button Is Clicked"""
        if self.screenState == self.LOGIN:
            self.showCreateAccount()
        elif self.screenState == self.CREATE:

            if not re.match(r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[A-Za-z]*$', self.varEmail.get() ):
                return mb.showwarning("invalid email", "input a valid email",parent=self)

            if not re.match(r'[A-Za-z0-9@#$%^&+=]*$',self.varPassword.get()) or len(self.varPassword.get()) < 8 or len(self.varPassword.get()) > 10:
                return mb.showwarning("Invalid Password", "Input a Valid Password,\nMust be 8-10 characters long,\nand can contain A-Z a-z 0-9 @#$%^&+=",parent=self)

            if not self.varPassword.get() == self.varVerifyPassword.get():
                return mb.showwarning("Entry Error", "Passwords do not Match",parent=self)

            if not re.match(r'[A-Za-z0-9 ]*$' , self.varUsername.get() ) or self.varUsername.get() == "Enter Username" or len(self.varUsername.get()) < 4 or len(self.varUsername.get()) > 15:
                return mb.showwarning("Invalid Username", "Input a Valid Username,\nMust be 4-15 characters long,\nand can contain A-Z a-z 0-9.",parent=self)

            if not re.match(r'[0-9]*$' ,self.varPlayerID.get() ) or len(self.varPlayerID.get()) != 9:
                return mb.showwarning("Invalid PlayerID", "Input a Valid PlayerID,\nMust be 9 Digits long.",parent=self)

            self.master.PADsql.remote = self.server.get()
            if self.master.PADsql.signup(self.varEmail.get(), self.varPassword.get(), self.varUsername.get(), self.varPlayerID.get()):
                mb.showwarning("Account Created!", "Account has been successfully Created." , parent=self)
            else:
                mb.showwarning("Account already exists!", "An account with this Email already exists." , parent=self)
            self.showLogin()

    def onLoginClick(self, event  = None):
        """Occurs When Login Button Is Clicked"""
        if self.screenState == self.LOGIN:
            self.master.PADsql.remote = self.server.get()
            self.master.PADsql.login(self.varEmail.get(), self.varPassword.get())
            if self.master.PADsql.signedIn:
                self.master.showHomeScreen()
                self.destroy()
            else:
                mb.showwarning('Login Error', 'Email and Password Do not exist!',parent=self)

    def onExit(self):
        self.destroy()

    def onFocusIn(self, event):
        """Focus in behavior"""
        color = "#000000"
        if event.widget == self.entEmail:
            if self.varEmail.get() == ("Enter Email"):
                self.entEmail.config(foreground=color)
                self.varEmail.set("")

        elif event.widget == self.entPassword:
            if self.varPassword.get() == ("Enter Password"):
                self.entPassword.config(foreground=color, show='*')
                self.varPassword.set("")

        elif event.widget == self.entVerifyPassword:
            if self.varVerifyPassword.get() == ("Confirm Password"):
                self.entVerifyPassword.config(foreground=color, show='*')
                self.varVerifyPassword.set("")

        elif event.widget == self.entPlayerID:
            if self.varPlayerID.get() == ("Enter PlayerID"):
                self.entPlayerID.config(foreground=color)
                self.varPlayerID.set("")

        elif event.widget == self.entUsername:
            if self.varUsername.get() == ("Enter Username"):
                self.entUsername.config(foreground=color)
                self.varUsername.set("")

    def onFocusOut(self, event):
        """Focus out behavior"""
        color = self.FGCOLOR
        if event.widget == self.entEmail:
            if self.varEmail.get() == (""):
                self.entEmail.config(foreground=color)
                self.varEmail.set("Enter Email")

        elif event.widget == self.entPassword:
            if self.varPassword.get() == (""):
                self.entPassword.config(foreground=color, show='')
                self.varPassword.set("Enter Password")

        elif event.widget == self.entVerifyPassword:
            if self.varVerifyPassword.get() == (""):
                self.entVerifyPassword.config(foreground=color, show='')
                self.varVerifyPassword.set("Confirm Password")

        elif event.widget == self.entPlayerID:
            if self.varPlayerID.get() == (""):
                self.entPlayerID.config(foreground=color)
                self.varPlayerID.set("Enter PlayerID")

        elif event.widget == self.entUsername:
            if self.varUsername.get() == (""):
                self.entUsername.config(foreground=color)
                self.varUsername.set("Enter Username")

    def validate(self):
        '''validate the data

        This method is called automatically to validate the data before the
        dialog is destroyed. By default, it always validates OK.
        '''
        return 1 # override

    def apply(self):
        '''process the data

        This method is called automatically to process the data, *after*
        the dialog is destroyed. By default, it does nothing.
        '''
        pass