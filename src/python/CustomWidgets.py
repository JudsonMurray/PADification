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
    def __init__(self, master, monster):
        super().__init__(master)
        self.monster = monster
        self.portrait = None
        self.portraitImage = Image.open("Resource/PAD/Images/portraits/"+ str(self.monster.MonsterClassID) + ".jpg")
        self.portraitImage = self.portraitImage.resize((int(self.portraitImage.width / 1.33), int(self.portraitImage.height // 1.33)))
        self.portraitimg = ImageTk.PhotoImage(self.portraitImage, self.portrait)
        

    def showcontents(self):
        self.portrait = Label(self.tipwindow, image = self.portraitimg, justify=LEFT,
                      background="#ffffe0", relief=GROOVE, borderwidth=4)
        self.portrait.pack()

        self.name = CustomFont_Label(self.tipwindow, text= self.monster.MonsterName, font_path="Resource/PAD/Font/FOT-RowdyStd-EB.ttf", size=20)

        self.name.pack()

        self.stats = Label(self.tipwindow, text = "Level = " + str(self.monster.Level) + "\tHp = " + str(self.monster.TotalHP) +
                           "\tAtk = " + str(self.monster.TotalATK) + "\tRCV = " + str(self.monster.TotalRCV), 
                           justify=LEFT, relief=GROOVE, borderwidth=4, font='Yu')
        self.stats.pack()

    def schedule(self):
        self.unschedule()
        self.id = self.button.after(250, self.showtip)

    def showtip(self):
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