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

def truetype_font(font_path, size):
    return ImageFont.truetype(font_path, size)

class CustomFont_Label(Label):
    # Author: Miguel Martinez Lopez -- http://code.activestate.com/recipes/580778-tkinter-custom-fonts/
    def __init__(self, master, text, foreground="black", truetype_font=None, font_path=None, family=None, size=None, **kwargs):   
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
        self.PhotoImage = Photoimage
        self.label = None

    def showcontents(self):
        self.label = Label(self.tipwindow, image = self.PhotoImage, justify=LEFT,
                      background="#ffffe0", relief=GROOVE, borderwidth=8)

        self.label.pack()

class MonsterStatTooltip(ToolTip.ToolTipBase):
    def __init__(self, master):
        super().__init__(master)
        self.monster = None
        self.portrait = None
        self.portraitImage = None
        self.portraitimg = None
    
    def update(self, monster = None):

        if monster != None:
            self.monster = monster
            self.portraitImage = Image.open("Resource/PAD/Images/portraits/"+ str(self.monster.MonsterClassID) + ".jpg")
            self.portraitImage = self.portraitImage.resize((int(self.portraitImage.width / 1.66), int(self.portraitImage.height // 1.66)))
            self.portraitimg = ImageTk.PhotoImage(self.portraitImage, self.portrait)
        else:
            self.monster = monster
            self.portrait = None
            self.portraitImage = None
            self.portraitimg = None

    def showcontents(self):
        if self.monster != None:
            self.tipwindow.config(relief=GROOVE, borderwidth=10)
            self.portrait = Label(self.tipwindow, image = self.portraitimg, justify=LEFT,
                            background="#ffffe0")
            self.portrait.grid(row=1,column=0)


            self.name = CustomFont_Label(self.tipwindow, text= self.monster.MonsterName, font_path="Resource/PAD/Font/FOT-RowdyStd-EB.ttf", size=18, foreground="#800080")
            self.name.grid(row=0,column=0,columnspan=2)

            self.stats = Label(self.tipwindow, 
                               text = "  ID= " + str(self.monster.MonsterClassID) +
                               "\nLVL= " + str(self.monster.Level) + 
                               "\n  HP= " + str(self.monster.TotalHP) +
                                "\nATK= " + str(self.monster.TotalATK) + 
                                "\nRCV= " + str(self.monster.TotalRCV), 
                                justify=LEFT, font=('Yu', 14, 'bold'))
            self.stats.grid(row=0,column=1,rowspan=3)

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
            y = self.button.winfo_rooty() - 250
            self.tipwindow = tw = Toplevel(self.button)
            tw.wm_overrideredirect(1)
            tw.wm_geometry("+%d+%d" % (x, y))
            self.showcontents()

class LoginDialog(sd.Dialog):
    def __init__(self, parent, title = None):
        self.imgTitleImage = PhotoImage(file = "Resource/PAD/Images/Padification Logo.png").subsample(2)
        self.entEmail = None
        self.entPassword = None
        self.Email = StringVar(value = "Enter Email")
        self.Password = StringVar(value = "Enter Password")
        self.servertxt = StringVar(value = "Remote")
        self.server = BooleanVar(value = True)
        super().__init__(parent, title)
        

    def body(self, master):
        '''create dialog body.

        return widget that should have initial focus.
        This method should be overridden, and is called
        by the __init__ method.

        '''
        box = Frame(self)
        l = Label(box, image= self.imgTitleImage)
        l.pack()

        self.chkServer = Checkbutton(box, indicatoron=False, font="yu", onvalue=False, offvalue=True, textvariable=self.servertxt, variable=self.server)
        self.chkServer.bind("<1>", self.onServerClick)
        self.chkServer.pack(pady=5)
        self.entEmail = Entry(box, width=20, textvariable=self.Email,foreground="#c6caca", font="yu")
        self.entEmail.pack(pady=5)
        self.entPassword = Entry(box, width=20, textvariable=self.Password,foreground="#c6caca", font="yu")
        self.entPassword.pack(pady=5)
        self.entEmail.bind("<FocusIn>", self.onEmailFocusIn)
        self.entEmail.bind("<FocusOut>", self.onEmailFocusOut)
        self.entPassword.bind("<FocusIn>", self.onPasswordFocusIn)
        self.entPassword.bind("<FocusOut>", self.onPasswordFocusOut)
        box.pack()
    
    def buttonbox(self):
        '''add standard button box.

        override if you do not want the standard buttons
        '''

        box = Frame(self)

        w = Button(box, text="Login", width=15, command=self.onLoginClick, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)

        w = Button(box, text="Exit", width=15, command=self.master.quit)
        w.pack(side=LEFT, padx=5, pady=5)

        w = Button(box, text="Create Account", width=15, command=self.onCreateAccountClick)
        w.pack(padx=5, pady=5)

        self.bind("<Return>", self.onLoginClick)
        self.bind("<Escape>", self.master.quit)

        box.pack()

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
    def onServerClick(self, event):
        if self.server.get():
            self.servertxt.set("localhost")
        else:
            self.servertxt.set("Remote")

    def onCreateAccountClick(self, event  = None):
        """Occurs When Create Account Button Is Clicked"""
        self.master.showAccountCreation()

    def onLoginClick(self, event  = None):
        """Occurs When Login Button Is Clicked"""
        self.master.PADsql.remote = self.server.get()
        self.master.PADsql.login(self.Email.get(), self.Password.get())
        if self.master.PADsql.signedIn:
            self.master.showHomeScreen()
            self.destroy()
        else:
            mb.showwarning('Login Error', 'Email and Password Do not exist!')


    def onEmailFocusIn(self,event):
        """Clears Username Entry Field"""
        if self.Email.get() == ("Enter Email"):
            self.entEmail.config(foreground="#000000")
            self.Email.set("")

    def onEmailFocusOut(self,event):
        """Fills Empty Field with Enter Email"""
        if self.Email.get() == "":
            self.entEmail.config(foreground="#c6caca")
            self.Email.set("Enter Email")

    def onPasswordFocusIn(self,event):
        """Clears Password Entry Field"""
        if self.Password.get() == ("Enter Password"):
            self.entPassword.config(foreground="#000000")
            self.Password.set("")

    def onPasswordFocusOut(self,event):
        """Fills Password Entry Field with Enter Password"""
        if self.Password.get() == (""):
            self.entPassword.config(foreground="#c6caca")
            self.Password.set("Enter Password")