# !/usr/bin/env Python3

#   Name:   ZACHARY BLUE
#   Date:   JUNE 23RD 2017
#   Purpose:THE MONSTER EDIT SCREEN FOR THE PADification APPLICATION
#   V.1.0   RB  Display the information for the Monster Edit Screen

import tkinter as tk
from tkinter import *
import tkinter.messagebox as mb
import pygubu
import math
from idlelib import ToolTip
from PIL import Image
from PIL import ImageTk
import PADMonster
import logging
import CustomWidgets
from PADMonster import Monster

class EvoFrame:
    def __init__(self, master, nextMon):
        #logger
        #self.logger = logging.getLogger("Padification.ui.MonsterEditScreen.EvoFrame")
        self.master = master
        self.nextMon = nextMon
        self.builder = pygubu.Builder()
        self.builder.add_from_file(r"src\ui\Monster Edit UI.ui")
        self.evos = self.builder.get_object('frmEvos', self.master.container)
        self.availEvo = tk.PhotoImage(file = "Resource/PAD/Images/thumbnails/" + str(self.nextMon[0]) + '.png').zoom(4).subsample(5)
        self.builder.get_object("canNextMon").create_image(7,7, image = self.availEvo, anchor = tk.NW)
        self.evos.config(highlightthickness = 5)
        self.check = self.nextMon[0]

        self.check = Monster((self.master.master.PADsql.selectMonsterClass(self.check))[0])

        self.evos.config(highlightbackground = 'Red')

        if self.nextMon[7]:
            self.evos.config(highlightbackground = 'Blue')

        if self.master.m.MonsterClassID > self.nextMon[0]:
            self.evos.config(highlightbackground = 'Yellow')
        self.builder.connect_callbacks(self)
        return
    def clickMe(self, event):
        self.master.builder.get_object('btnConfirmEvo').config(state=NORMAL)
        self.master.monClass = self.master.master.PADsql.selectMonsterClass(self.nextMon[0])
        #self.master.master.monsterEdit.applyChanges()

#class Evolve()
class EvolutionFrame(tk.Toplevel):
    def __init__(self, master, masterbuilder):
        #logger
        #self.logger = logging.getLogger("Padification.ui.MonsterEditScreen.EvolutionFrame")
        tk.Toplevel.__init__(self, master)
        self.master = master
        self.masterbuilder = masterbuilder
        self.builder = pygubu.Builder()
        self.builder.add_from_file('src/ui/Monster Edit UI.ui')
        self.mainwidow = self.builder.get_object('frmEvoTree', self)
        self.container = self.builder.get_object('canEvoTree', self.mainwidow)
        self.monClass = None
        self.transient(master) #set to be on top of the main window
        self.grab_set() #hijack all commands from the master (clicks on the main window are ignored)
        self.evos = self.master.PADsql.getEvolutions(self.master.monsterEdit.monster.MonsterClassID)
        self.evoFrames = []
        
        self.builder.get_object('btnConfirmEvo').config(state=DISABLED)
        self.count = 0
        
        w = 526 #width for the Tk root
        h = 335 #height for the Tk root
        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen
        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.geometry('%dx%d+%d+%d' % (w,h, x, y))
        self.m = self.master.monsterEdit.monster
        for i in self.evos:
            self.evoFrames.append(EvoFrame(self, i))
            self.evoFrames[self.count].evos.grid(row=self.count // 4,column = self.count % 4, padx = 8, pady = 10)
            self.count += 1
        self.builder.connect_callbacks(self)

    def confirmEvo(self):
        
        self.m.MonsterClassID = self.monClass[0]['MonsterClassID']
        self.m.MonsterName = self.monClass[0]['MonsterName']
        self.m.Rarity = self.monClass[0]['Rarity']
        self.m.PriAttribute = self.monClass[0]['PriAttribute']
        self.m.SecAttribute = self.monClass[0]['SecAttribute']
        self.m.MonsterTypeOne = self.monClass[0]['MonsterTypeOne']
        self.m.MonsterTypeTwo = self.monClass[0]['MonsterTypeTwo']
        self.m.MonsterTypeThree = self.monClass[0]['MonsterTypeThree']
        self.m.ExpCurve = self.monClass[0]['ExpCurve']
        self.m.MaxLevel = self.monClass[0]['MaxLevel']
        self.m.MonsterCost = self.monClass[0]['MonsterCost']
        self.m.ASListID = self.monClass[0]['ASListID']
        self.m.LeaderSkillName = self.monClass[0]['LeaderSkillName']
        self.m.ActiveSkillName = self.monClass[0]['ActiveSkillName']
        self.m.MaxHP = self.monClass[0]['MaxHP']
        self.m.MinHP = self.monClass[0]['MinHP']
        self.m.GrowthRateHP = self.monClass[0]['GrowthRateHP']
        self.m.MaxATK = self.monClass[0]['MaxATK']
        self.m.MinATK = self.monClass[0]['MinATK']
        self.m.GrowthRateATK = self.monClass[0]['GrowthRateATK']
        self.m.MaxRCV = self.monClass[0]['MaxRCV']
        self.m.MinRCV = self.monClass[0]['MinRCV']
        self.m.GrowthRateRCV = self.monClass[0]['GrowthRateRCV']
        self.m.CurSell = self.monClass[0]['CurSell']
        self.m.CurFodder = self.monClass[0]['CurFodder']
        self.m.MonsterPointValue = self.monClass[0]['MonsterPointValue']
        self.m.ActiveSkillDesc = self.monClass[0]['ActiveSkillDesc']
        self.m.LeaderSkillDesc = self.monClass[0]['LeaderSkillDesc']
        self.m.updateStats()
        self.master.monsterEdit.updateMonsterPage()
        self.destroy()
        pass

    def cancelEvo(self):
        self.builder.get_object('btnConfirmEvo').config(state=DISABLED)
        self.monClass = None
        self.destroy()
class MonsterFrame:
    def __init__(self, master, assistant):
        self.logger = logging.getLogger("Padification.ui.MonsterEditScreen.MonsterFrame")
        self.master = master
        self.assistant = assistant
        self.builder = pygubu.Builder()
        self.builder.add_from_file(r"src\ui\Monster Edit UI.ui")
        self.monbut = self.builder.get_object('MonsFrame', self.master.builder.get_object("canSelectAssist"))
        self.myMonster = tk.PhotoImage(file = "Resource/PAD/Images/thumbnails/" + str(assistant.MonsterClassID) + '.png').subsample(2)
        self.builder.get_object("FrameLabel").create_image(2,2, image = self.myMonster, anchor = tk.NW)
        self.builder.connect_callbacks(self)

    def clickMe(self, event):
        self.master.builder.get_object('btnRemoveAssist').config(state = NORMAL)
        for i in range(0, (len(self.master.buttons))):
            self.master.buttons[i].monbut.config(relief = FLAT)
        self.monbut.config(relief = SUNKEN)


        for i in range(0, len(self.master.assistants)):
            if self.master.assistants[i] == self.master.monster.AssistMonsterID:
                self.master.assistants.pop(i)
                break

        self.master.monster.AssistMonsterID = None

        self.master.monster.AssistMonsterID = self.assistant.InstanceID

        self.master.displayAssistInfo()
        pass

class MonsterEdit:
    def __init__(self, master):
        #logger
        self.logger = logging.getLogger("Padification.ui.MonsterEditScreen.MonsterEdit")

        self.master  = master
        self.builder = pygubu.Builder()
        self.builder.add_from_file(r"src\ui\Monster Edit UI.ui")
        self.monsteredit = self.builder.get_object("Monster Edit")
        self.builder.connect_callbacks(self)
        self.image = None
        self.portrait = None
        self.AttOne = ToolTip.ToolTip(self.builder.get_object("canPriAtt"), None)
        self.AttTwo = ToolTip.ToolTip(self.builder.get_object("canSecAtt"), None)
        self.TypeOne = ToolTip.ToolTip(self.builder.get_object("canTypeOne"), None)
        self.TypeTwo = ToolTip.ToolTip(self.builder.get_object("canTypeTwo"), None)
        self.TypeThree = ToolTip.ToolTip(self.builder.get_object("canTypeThree"), None)
        self.ASOne = ToolTip.ToolTip(self.builder.get_object("canAwokenSkillOne"), None)
        self.ASTwo = ToolTip.ToolTip(self.builder.get_object("canAwokenSkillTwo"), None)
        self.ASThree = ToolTip.ToolTip(self.builder.get_object("canAwokenSkillThree"), None)
        self.ASFour = ToolTip.ToolTip(self.builder.get_object("canAwokenSkillFour"), None)
        self.ASFive = ToolTip.ToolTip(self.builder.get_object("canAwokenSkillFive"), None)
        self.ASSix = ToolTip.ToolTip(self.builder.get_object("canAwokenSkillSix"), None)
        self.ASSeven = ToolTip.ToolTip(self.builder.get_object("canAwokenSkillSeven"), None)
        self.ASEight = ToolTip.ToolTip(self.builder.get_object("canAwokenSkillEight"), None)
        self.ASNine = ToolTip.ToolTip(self.builder.get_object("canAwokenSkillNine"), None)
        

    def receiveInstanceID(self, InstanceID, Wishlist):
        self.instanceID = InstanceID
        self.wishlist = Wishlist
        self.monster = self.master.PADsql.selectMonsterInstance(self.instanceID, wishlist = self.wishlist)
        self.monster = PADMonster.Monster(self.monster[0])
        self.updateMonsterPage()

    def updateMonsterPage(self):
        self.latents = self.master.PADsql.getLatentAwokenSkills()
        self.startMonster = 0
        self.pAssistants = None
        self.displayList = []
        self.currentPage = 1
        self.builder.get_object("btnNext").config(state = NORMAL)
        self.builder.get_object("btnPrev").config(state = DISABLED)
        self.extraSlot = self.builder.get_object("chkExtraSlot")
        self.maxSlots = self.builder.get_variable('maxSlots')
        self.formarAsisID = self.monster.AssistMonsterID
        if self.monster.LSListID != None:
            self.latentList = self.master.PADsql.getLatentAwokenSkillList(self.instanceID)
            if self.latentList[7]:
                self.extraSlot.select()
        else:
            self.extraSlot.deselect()
        self.image = Image.open("Resource/PAD/Images/portraits/" + str(self.monster.MonsterClassID) + ".jpg").resize((320,192))
        self.portrait = ImageTk.PhotoImage(self.image)
        self.builder.get_object("canPortrait").create_image(8, 8, image = self.portrait, anchor = NW)

        if self.monster.AssistMonsterID != None:
            self.displayAssistInfo()
        else:
            self.builder.get_object('btnRemoveAssist').config(state = DISABLED)
            self.builder.get_object("canAssistantThumb").delete('all')
            self.builder.get_object("lblAssistName").config(text = "Assist Name: None", justify = LEFT)
            self.builder.get_object("lblAssistID").config(text = "Assist ID: None", justify = LEFT)
            self.builder.get_object("lblAssistLvl").config(text = "Assist LvL: None", justify = LEFT)
            self.builder.get_object("lblAssistHP").config(text = "Assist HP: None", justify = LEFT)
            self.builder.get_object("lblAssistATK").config(text = "Assist ATK: None", justify = LEFT)
            self.builder.get_object("lblAssistRCV").config(text = "Assist RCV: None", justify = LEFT)
            self.builder.get_object("lblAssistSkillName").config(text = "Assist Skill: None", anchor = W)
            self.builder.get_object("lblAssistSkillDesc").config(text = "N/A")
            self.builder.get_object("lblAssistSkillLvl").config(text = "LvL: N/A")
            self.builder.get_object("lblAssistSkillCD").config(text = "Cooldown: N/A")
            self.assistHP = 0
            self.assistATK = 0
            self.assistRCV = 0

        self.latentSkillList = self.builder.get_object("lstSelectedLatents")
        self.latentSkillList.delete(0, END)

        self.latentSkills = self.builder.get_object("lstLatents")

        self.__displayAwokenSkills()
        self.__displayMonsterIDentification()
        self.__displaySkillInfo()
        self.__displayStats()
        self.__displayLatentSkills()
        self.__displayPossibleAssistants()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--- Bindings -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def selectLatentAwokenSkill(self, event):
        
        if str(self.latentSkills['state']) == 'normal':
            self.chosenLatent = self.latentSkills.get(ANCHOR)
            count = 0
            for i in ('Attacker Killer','Dragon Killer', 'God Killer', 'Balanced Killer', 'Devil Killer', 'Machine Killer', 'Physical Killer', 'Healer Killer'):
                if self.chosenLatent == i:
                    if self.monster.MonsterTypeOne == "Balanced" or self.monster.MonsterTypeTwo == "Balanced" or self.monster.MonsterTypeThree == "Balanced":
                        break
                    if (count == 0 or count == 1) and (self.monster.MonsterTypeOne != "Healer" and self.monster.MonsterTypeTwo != "Healer" and self.monster.MonsterTypeThree != "Healer"):
                        self.chosenLatent = ''
                        break
                    if count == 2 and (self.monster.MonsterTypeOne != "Machine" and self.monster.MonsterTypeTwo != "Machine" and self.monster.MonsterTypeThree != "Machine" and self.monster.MonsterTypeOne != "Devil" and self.monster.MonsterTypeTwo != "Devil" and self.monster.MonsterTypeThree != "Devil"):
                        self.chosenLatent = ''
                        break
                    if count == 3  and (self.monster.MonsterTypeOne != "Machine" and self.monster.MonsterTypeTwo != "Machine" and self.monster.MonsterTypeThree != "Machine"):
                        self.chosenLatent = ''
                        break
                    if count == 4 and (self.monster.MonsterTypeOne != "Attacker" and self.monster.MonsterTypeTwo != "Attacker" and self.monster.MonsterTypeThree != "Attacker" and self.monster.MonsterTypeOne != "God" and self.monster.MonsterTypeTwo != "God" and self.monster.MonsterTypeThree != "God"):
                        self.chosenLatent = ''
                        break
                    if count == 5 and (self.monster.MonsterTypeOne != "Physical" and self.monster.MonsterTypeTwo != "Physical" and self.monster.MonsterTypeThree != "Physical" and self.monster.MonsterTypeOne != "Dragon" and self.monster.MonsterTypeTwo != "Dragon" and self.monster.MonsterTypeThree != "Dragon"):
                        self.chosenLatent = ''
                        break
                    if count == 6  and (self.monster.MonsterTypeOne != "Attacker" and self.monster.MonsterTypeTwo != "Attacker" and self.monster.MonsterTypeThree != "Attacker"):
                        self.chosenLatent = ''
                        break
                    if count == 7 and (self.monster.MonsterTypeOne != "Physical" and self.monster.MonsterTypeTwo != "Physical" and self.monster.MonsterTypeThree != "Physical" and self.monster.MonsterTypeOne != "Dragon" and self.monster.MonsterTypeTwo != "Dragon" and self.monster.MonsterTypeThree != "Dragon"):
                        self.chosenLatent = ''
                        break
                count += 1

            if self.chosenLatent != '' and self.usedSlots < self.maxSlots.get():
                self.builder.get_object("btnAddLS").config(state = NORMAL)
            else:
                self.builder.get_object("btnAddLS").config(state = DISABLED)
            self.builder.get_object("btnRemoveLS").config(state = DISABLED)
        pass

    def selectAssignedLASkill(self, event):
        
        if str(self.latentSkillList['state']) == 'normal':
            self.chosenLatent = self.latentSkillList.get(ANCHOR)
            if self.chosenLatent != '':
                self.builder.get_object("btnRemoveLS").config(state = NORMAL)
            self.builder.get_object("btnAddLS").config(state = DISABLED)
        pass

    def selectExtraSlot(self, event):
        if str(self.extraSlot['state']) != 'disabled':
            if self.maxSlots.get() == 5:
                if str(self.latentSkills['state']) == 'disabled':
                    self.latentSkills.config(state = NORMAL)
                self.builder.get_object("lblLatentSlots").config(text = "Latent Slots: " + str(self.usedSlots) + " / " + str(self.maxSlots.get() + 1))
            elif self.maxSlots.get() == 6:
                if self.usedSlots == 5:
                    self.latentSkills.config(state = DISABLED)
                self.builder.get_object("lblLatentSlots").config(text = "Latent Slots: " + str(self.usedSlots) + " / " + str(self.maxSlots.get() - 1))

            a = self.builder.get_object("lstSelectedLatents").get(0, END)

            self.LSList = []

            for i in range(0 , 6):
                if i >= len(a):
                    self.LSList.append(None)
                else:
                    self.LSList.append(a[i])

            if self.maxSlots.get() == 5:
                self.eS = 1
            else:
                self.eS = 0

            self.master.PADsql.saveLatentAwokenSkillList(self.monster.InstanceID, self.LSList[0], self.LSList[1], self.LSList[2], self.LSList[3], self.LSList[4], self.LSList[5], self.eS)

            if self.monster.LSListID is None:
                self.monster.LSListID = self.monster.InstanceID
        
        pass

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--- Button Commands ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def changeLevel(self):
        self.monster.setLevel(int(self.spnLevel.get()))
        self.monster.updateStats()

        self.lblCurrentLevel.config(text = "Current Level: " + str(self.monster.Level))
        self.lblCurrentEXP.config(text = "Current EXP: " + str(self.monster.CurrentExperience))
        self.lblBaseHP.config(text = "Base HP: " + str(self.monster.HP))
        self.lblBaseATK.config(text = "Base ATK: " + str(self.monster.ATK))
        self.lblBaseRCV.config(text = "Base RCV: " + str(self.monster.RCV))
        self.lblTotalHP.config(text = "Total HP: " + str(self.monster.TotalHP + self.assistHP))
        self.lblTotalATK.config(text = "Total ATK: " + str(self.monster.TotalATK + self.assistATK))
        self.lblTotalRCV.config(text = "Total RCV: " + str(self.monster.TotalRCV+ self.assistRCV))
        pass

    def changeHP(self):
        self.monster.setPlusHP(int(self.spnHP.get()))
        self.bonusHP = self.monster.PlusHP * 10
        self.lblBonusHP.config(text = "Bonus HP: " + str(self.bonusHP + self.assistHP))
        self.lblTotalHP.config(text = "Total HP: " + str(self.monster.TotalHP + self.assistHP))
        pass

    def changeATK(self):
        self.monster.setPlusATK(int(self.spnATK.get()))
        self.bonusATK = self.monster.PlusATK * 5
        self.lblBonusATK.config(text = "Bonus ATK: " + str(self.bonusATK + self.assistATK))
        self.lblTotalATK.config(text = "Total ATK: " + str(self.monster.TotalATK + self.assistATK))
        pass

    def changeRCV(self):
        self.monster.setPlusRCV(int(self.spnRCV.get()))
        self.bonusRCV = self.monster.PlusRCV * 3
        self.lblBonusRCV.config(text = "Bonus RCV: " + str(self.bonusRCV + self.assistRCV))
        self.lblTotalRCV.config(text = "Total RCV: " + str(self.monster.TotalRCV+ self.assistRCV))
        pass

    def changeSkillLevel(self):
        self.monster.setSkillLevel(int(self.spnSkillLVL.get()))
        self.monster.updateStats()
        self.lblSkillCooldown.config(text = "Cooldown: " + str(self.monster.ActiveSkillCoolDown))
        pass

    def changeSkillsAwoke(self):
        self.monster.setSkillsAwoke(int(self.spnAwokenSkill.get()))
        self.aSListImg = []
        for i in range(1, len(self.aSList)):
                if i <= self.monster.SkillsAwoke:
                    if self.aSList[i] is not None:
                        self.aSListImg.append(PhotoImage(file = "Resource/PAD/Images/Awoken Skills/" + str(self.aSList[i]) +'.png'))
                        self.numAS += 1
                    else:
                        self.aSListImg.append(None)
                else:
                    if self.aSList[i] is not None:
                        self.aSListImg.append(PhotoImage(file = "Resource/PAD/Images/Awoken Skills/not " + str(self.aSList[i]) +'.png'))
                        self.numAS += 1
                    else:
                        self.aSListImg.append(None)

        self.builder.get_object("canAwokenSkillOne").delete("all")
        self.builder.get_object("canAwokenSkillTwo").delete("all")
        self.builder.get_object("canAwokenSkillThree").delete("all")
        self.builder.get_object("canAwokenSkillFour").delete("all")
        self.builder.get_object("canAwokenSkillFive").delete("all")
        self.builder.get_object("canAwokenSkillSix").delete("all")
        self.builder.get_object("canAwokenSkillSeven").delete("all")
        self.builder.get_object("canAwokenSkillEight").delete("all")
        self.builder.get_object("canAwokenSkillNine").delete("all")

        self.builder.get_object("canAwokenSkillOne").create_image(2,2, image = self.aSListImg[0], anchor = tk.NW)
        self.builder.get_object("canAwokenSkillTwo").create_image(2,2, image = self.aSListImg[1], anchor = tk.NW)
        self.builder.get_object("canAwokenSkillThree").create_image(2,2, image = self.aSListImg[2], anchor = tk.NW)
        self.builder.get_object("canAwokenSkillFour").create_image(2,2, image = self.aSListImg[3], anchor = tk.NW)
        self.builder.get_object("canAwokenSkillFive").create_image(2,2, image = self.aSListImg[4], anchor = tk.NW)
        self.builder.get_object("canAwokenSkillSix").create_image(2,2, image = self.aSListImg[5], anchor = tk.NW)
        self.builder.get_object("canAwokenSkillSeven").create_image(2,2, image = self.aSListImg[6], anchor = tk.NW)
        self.builder.get_object("canAwokenSkillEight").create_image(2,2, image = self.aSListImg[7], anchor = tk.NW)
        self.builder.get_object("canAwokenSkillNine").create_image(2,2, image = self.aSListImg[8], anchor = tk.NW)
        pass

    def addLatentAwokenSkill(self):
        for i in self.latents:
            if self.chosenLatent == i[0]:
                if self.usedSlots + int(i[2]) <= self.maxSlots.get():
                    self.builder.get_object("lstSelectedLatents").config(state = NORMAL)
                    self.builder.get_object("lstSelectedLatents").insert(END, self.chosenLatent)
                    self.usedSlots += i[2]
                    self.builder.get_object("lblLatentSlots").config(text = "Latent Slots: " + str(self.usedSlots) + " / " + str(self.maxSlots.get()))
                    break
        self.builder.get_object('btnAddLS').config(state = DISABLED)
        if self.usedSlots == self.maxSlots.get():
            self.latentSkills.config(state = DISABLED)
            if self.maxSlots.get() == 6:
                self.builder.get_object('chkExtraSlot').config(state = DISABLED)

        a = self.builder.get_object("lstSelectedLatents").get(0, END)

        self.LSList = []

        for i in range(0 , 6):
            if i >= len(a):
                self.LSList.append(None)
            else:
                self.LSList.append(a[i])

        if self.maxSlots.get() == 6:
            self.eS = 1
        else:
            self.eS = 0

        self.master.PADsql.saveLatentAwokenSkillList(self.monster.InstanceID, self.LSList[0], self.LSList[1], self.LSList[2], self.LSList[3], self.LSList[4], self.LSList[5], self.eS)

        if self.monster.LSListID is None:
            self.monster.LSListID = self.monster.InstanceID
        print(a)

        pass

    def removeLatentAwokenSkill(self):
        for i in self.latents:
            if i[0] == self.chosenLatent:
                self.usedSlots -= i[2]
                break
        self.builder.get_object("btnRemoveLS").config(state = DISABLED)
        self.builder.get_object("lstLatents").config(state = NORMAL)
        self.builder.get_object("lblLatentSlots").config(text = "Latent Slots: " + str(self.usedSlots) + " / " + str(self.maxSlots.get()))
        self.builder.get_object("lstSelectedLatents").delete(ANCHOR)
        if self.usedSlots <= 0:
            self.latentSkillList.config(state = DISABLED)

        a = self.builder.get_object("lstSelectedLatents").get(0, END)
        self.builder.get_object('chkExtraSlot').config(state = NORMAL)
        self.LSList = []

        for i in range(0 , 6):
            if i >= len(a):
                self.LSList.append(None)
            else:
                self.LSList.append(a[i])

        if self.maxSlots.get() == 6:
            self.eS = 1
        else:
            self.eS = 0

        self.master.PADsql.saveLatentAwokenSkillList(self.monster.InstanceID, self.LSList[0], self.LSList[1], self.LSList[2], self.LSList[3], self.LSList[4], self.LSList[5], self.eS)

        if self.monster.LSListID is None:
            self.monster.LSListID = self.monster.InstanceID
        pass

    def applyChanges(self):
        global k
        self.master.PADsql.saveMonster(self.monster.getSaveDict())
        self.master.showPlayerCollection()
        self.master.playerCollection.buttons[self.master.playerCollection.k].clickMe(self)
        pass

    def cancel(self):
        self.builder.get_variable("spnLevel").set(str(self.monster.Level))
        self.builder.get_variable("spn+HP").set(str(self.monster.PlusHP))
        self.builder.get_variable("spn+ATK").set(str(self.monster.PlusATK))
        self.builder.get_variable("spn+RCV").set(str(self.monster.PlusRCV))
        self.builder.get_variable("spnSkillLvl").set(str(self.monster.SkillLevel))
        self.builder.get_variable("spnAwokenSkill").set(str(self.monster.SkillsAwoke))
        self.master.showPlayerCollection()

    def next(self):
        self.builder.get_object("btnPrev").config(state = NORMAL)
        self.currentPage += 1
        if self.currentPage == self.pages:
            self.builder.get_object("btnNext").config(state = DISABLED)
        self.startMonster = (self.currentPage - 1) * 16
        self.__displayPossibleAssistants()

    def prev(self):
        self.builder.get_object("btnNext").config(state = NORMAL)
        self.currentPage -= 1
        self.startMonster = 16 * (self.currentPage-1)
        if self.currentPage == 1:
            self.builder.get_object("btnPrev").config(state = DISABLED)
        self.__displayPossibleAssistants()

    def removeAssistant(self):
        
        self.builder.get_object("canAssistantThumb").delete('all')
        self.builder.get_object("lblAssistName").config(text = "Assist Name: None", justify = LEFT)
        self.builder.get_object("lblAssistID").config(text = "Assist ID: None", justify = LEFT)
        self.builder.get_object("lblAssistLvl").config(text = "Assist LvL: None", justify = LEFT)
        self.builder.get_object("lblAssistHP").config(text = "Assist HP: None", justify = LEFT)
        self.builder.get_object("lblAssistATK").config(text = "Assist ATK: None", justify = LEFT)
        self.builder.get_object("lblAssistRCV").config(text = "Assist RCV: None", justify = LEFT)
        self.builder.get_object("lblAssistSkillName").config(text = "Assist Skill: None", anchor = W)
        self.builder.get_object("lblAssistSkillDesc").config(text = "N/A")
        self.builder.get_object("lblAssistSkillLvl").config(text = "LvL: N/A")
        self.builder.get_object("lblAssistSkillCD").config(text = "Cooldown: N/A")
        self.assistHP = 0
        self.assistATK = 0
        self.assistRCV = 0
        self.count = 0
        self.builder.get_object('btnRemoveAssist').config(state = DISABLED)
        for i in range(0, len(self.displayList)):
            if self.displayList[i].InstanceID == self.monster.AssistMonsterID and self.count < 16:
                self.buttons[self.count].monbut.config(relief = FLAT)
                break
            else:
                self.count += 1
        self.monster.AssistMonsterID = None
        self.__displayStats()
        pass

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--- Displaying base information, performed when screen is opened from PlayerCollection -----------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def btnEvolutionClick(self, event):
        dialog = EvolutionFrame(self.master, self.builder)
    def __displayPossibleAssistants(self):

        if self.pAssistants is None:

            self.pAssistants = []
            if self.monster.WishList:
                self.wishlist = 1
            else:
                self.wishlist = 0

            self.assistList = self.master.PADsql.selectMonsterInstance(wishlist = self.wishlist)

            for i in range(0, len(self.assistList)):
                self.pAssistants.append(PADMonster.Monster(self.assistList[i]))

            self.assistants = []
            for i in self.pAssistants:
                if self.monster.InstanceID == i.AssistMonsterID:
                    self.asist = False
                    break
                else:
                    if i.AssistMonsterID != None:
                        self.assistants.append(i.AssistMonsterID)
                    self.asist = True

            self.myMonsterList = []

            
            self.count = 0
            self.teamins =[]
            teams = self.master.PADsql.selectTeamInstance()
            for x in range(0,len(teams)):
                self.teamins.append( PADMonster.Team(self.master.PADsql, (teams[x])))

            self.displayList = []
            if self.asist:
                for l in range(0, len(self.pAssistants)):
                    print('.')
                    display = True
                    i = self.pAssistants[l + self.startMonster]
                    try:
                        if i.InstanceID != self.monster.InstanceID and i.AssistMonsterID is None:
                            for a in self.assistants:
                                if a == i.InstanceID and a != self.formarAsisID:
                                    display = False
                                    break
                                else:
                                    display = True

                            if display:
                                for self.SelectedTeam in self.teamins:
                                    if self.SelectedTeam.LeaderMonster == i.InstanceID:
                                        display = False
                                        break
                                    if self.SelectedTeam.SubMonsterOne == i.InstanceID:
                                        display = False
                                        break
                                    if self.SelectedTeam.SubMonsterTwo == i.InstanceID:
                                        display = False
                                        break
                                    if self.SelectedTeam.SubMonsterThree == i.InstanceID:
                                        display = False
                                        break
                                    if self.SelectedTeam.SubMonsterFour == i.InstanceID:
                                        display = False
                                        break
                            if display:
                                self.displayList.append(i)
                                pass
                    except:
                        pass

        for i in self.builder.get_object("canSelectAssist").grid_slaves():
                i.grid_forget()

        self.buttons = []
        self.count = 0

        if self.displayList != None:
            for i in self.displayList:
                if self.startMonster < 16 * self.currentPage and ((self.startMonster >= 16 * (self.currentPage - 1)) and (self.startMonster != len(self.displayList))) or self.count != 16:
                    if self.startMonster < self.currentPage * 16 and self.startMonster < len(self.displayList):
                        self.buttons.append(MonsterFrame(self, self.displayList[self.startMonster]))
                        #self.buttons[self.count].monbut.config(padx = 8, pady = 10)
                        self.buttons[self.count].monbut.grid(row=self.count // 8,column = self.count % 8, padx = 8, pady = 10)
                        if self.displayList[self.startMonster].InstanceID == self.monster.AssistMonsterID:
                            self.buttons[self.count].monbut.config(relief = SUNKEN)
                        else:
                            self.buttons[self.count].monbut.config(relief = FLAT)
                        self.buttons[self.count].builder.get_object('lblMonsterBrief').config(text = 'LVL:' + str(self.displayList[self.startMonster].Level)+ '\nID: ' + str(self.displayList[self.startMonster].MonsterClassID))
                        self.count += 1
                        self.startMonster += 1
                else:
                    break

            self.pages = (len(self.displayList) // 16) + 1

            if len(self.displayList) == 0:
                self.pages = 1
            elif len(self.displayList) % 16 == 0:
                self.pages -= 1

            if self.pages == 1:
                self.builder.get_object('btnNext').config(state = DISABLED)
            self.builder.get_object('lblCurPage').config(text = "Page " + str(self.currentPage) + "/" + str(self.pages))

        pass


    def displayAssistInfo(self):
        self.assistMonster = self.master.PADsql.selectMonsterInstance(self.monster.AssistMonsterID, wishlist = self.wishlist)
        self.assistMonster = PADMonster.Monster(self.assistMonster[0])
        self.builder.get_object('btnRemoveAssist').config(state = NORMAL)
        self.assistHP = 0
        self.assistATK = 0
        self.assistRCV = 0
        if self.monster.PriAttribute == self.assistMonster.PriAttribute:
            self.assistHP = int(math.ceil(self.assistMonster.TotalHP * 0.1))
            self.assistATK = int(math.ceil(self.assistMonster.TotalATK * 0.05))
            self.assistRCV = int(math.ceil(self.assistMonster.TotalRCV * 0.15))

        self.AssistImage = PhotoImage(file = "Resource/PAD/Images/thumbnails/" + str(self.assistMonster.MonsterClassID) + ".png")
        self.builder.get_object("canAssistantThumb").create_image(7, 7, image = self.AssistImage, anchor = NW)
        self.builder.get_object("lblAssistName").config(text = "Assist Name: " + self.assistMonster.MonsterName, justify = LEFT)
        self.builder.get_object("lblAssistID").config(text = "Assist ID: " + str(self.assistMonster.MonsterClassID), justify = LEFT)
        self.builder.get_object("lblAssistLvl").config(text = "Assist LvL: " + str(self.assistMonster.Level), justify = LEFT)
        self.builder.get_object("lblAssistHP").config(text = "Assist HP: " + str(self.assistHP), justify = LEFT)
        self.builder.get_object("lblAssistATK").config(text = "Assist ATK: " + str(self.assistATK), justify = LEFT)
        self.builder.get_object("lblAssistRCV").config(text = "Assist RCV: " + str(self.assistRCV), justify = LEFT)
        self.builder.get_object("lblAssistSkillName").config(text = "Assist Skill: " + str(self.assistMonster.ActiveSkillName), anchor = W)
        if len(self.master.PADsql.getActiveSkillDesc(self.assistMonster.ActiveSkillName)) > 40:
            count = 0
            spaces = []
            self.desc = ''
            for i in self.master.PADsql.getActiveSkillDesc(self.assistMonster.ActiveSkillName):
                if i == ' ':
                    spaces.append(count)
                self.desc += i
                count += 1
                if count % 39 == 0:
                    j = spaces[len(spaces) - 1]
                    self.desc = self.desc[0 : j] + '\n' + self.desc[j + 1 :]
            self.builder.get_object("lblAssistSkillDesc").config(text = str(self.desc))
        else:
            self.builder.get_object("lblAssistSkillDesc").config(text = str(self.master.PADsql.getActiveSkillDesc(self.assistMonster.ActiveSkillName)))
        self.builder.get_object("lblAssistSkillLvl").config(text = "LvL: " + str(self.assistMonster.SkillLevel), justify = LEFT)
        self.builder.get_object("lblAssistSkillCD").config(text = "Cooldown: " + str(self.assistMonster.ActiveSkillCoolDown), justify = LEFT)

        self.__displayStats()
        pass

    def __displayLatentSkills(self):
        self.builder.get_object("lstLatents").delete(0,END)
        for i in self.latents:
            self.builder.get_object("lstLatents").insert(END, i[0])

        self.usedSlots = 0
        self.extraSlot.config(state = NORMAL)

        if self.monster.LSListID != None:
            self.latentList = self.master.PADsql.getLatentAwokenSkillList(self.instanceID)
            if self.latentList[7]:
                self.extraSlot.select()
                print(self.usedSlots)
            else:
                self.extraSlot.deselect()
                self.extraSlot.config(state = NORMAL)
            for i in self.latentList:
                if i != self.monster.InstanceID and i != 0 and i != 1:
                    for a in self.latents:
                        if a[0] == i:
                            self.usedSlots += int(a[2])
                            break
                    self.builder.get_object("lstSelectedLatents").insert(END, i)
        if self.usedSlots >= 6:
            self.extraSlot.config(state= DISABLED)

        if self.usedSlots == self.maxSlots.get():
            self.latentSkills.config(state = DISABLED)

        self.builder.get_object("lblLatentSlots").config(text = "Latent Slots: " + str(self.usedSlots) + " / " + str(self.maxSlots.get()))

    def __displayStats(self):
        self.lblCurrentLevel = self.builder.get_object("lblCurrentLevel")
        self.lblCurrentLevel.config(text = "Current Level: " + str(self.monster.Level))

        self.lblCurrentEXP = self.builder.get_object("lblCurrentEXP")
        self.lblCurrentEXP.config(text = "Current EXP: " + str(self.monster.CurrentExperience))

        self.lblBaseHP = self.builder.get_object("lblBaseHP")
        self.lblBaseHP.config(text = "Base HP: " + str(self.monster.HP))

        self.lblBaseATK = self.builder.get_object("lblBaseATK")
        self.lblBaseATK.config(text = "Base ATK: " + str(self.monster.ATK))

        self.lblBaseRCV = self.builder.get_object("lblBaseRCV")
        self.lblBaseRCV.config(text = "Base RCV: " + str(self.monster.RCV))

        self.bonusHP = self.monster.PlusHP * 10
        self.bonusATK = self.monster.PlusATK * 5
        self.bonusRCV = self.monster.PlusRCV * 3

        self.lblBonusHP = self.builder.get_object("lblBonusHP")
        self.lblBonusHP.config(text = "Bonus HP: " + str(self.bonusHP + self.assistHP))

        self.lblBonusATK = self.builder.get_object("lblBonusATK")
        self.lblBonusATK.config(text = "Bonus ATK: " + str(self.bonusATK + self.assistATK))

        self.lblBonusRCV = self.builder.get_object("lblBonusRCV")
        self.lblBonusRCV.config(text = "Bonus RCV: " + str(self.bonusRCV + self.assistRCV))

        self.lblTotalHP = self.builder.get_object("lblTotalHP")
        self.lblTotalHP.config(text = "Total HP: " + str(self.monster.TotalHP + self.assistHP))

        self.lblTotalATK = self.builder.get_object("lblTotalATK")
        self.lblTotalATK.config(text = "Total ATK: " + str(self.monster.TotalATK + self.assistATK))

        self.lblTotalRCV = self.builder.get_object("lblTotalRCV")
        self.lblTotalRCV.config(text = "Total RCV: " + str(self.monster.TotalRCV+ self.assistRCV))

        

        self.spnLevel = self.builder.get_object("spnLevel")
        self.spnLevel.config(state = NORMAL)

        if self.monster.MaxLevel > 1:
            self.spnLevel.config(from_ = 1, to = self.monster.MaxLevel, state = 'readonly')
        else:
            self.spnLevel.config(from_ = 1, to = self.monster.MaxLevel, state = DISABLED)

        self.spnHP = self.builder.get_object("spn+HP")
        self.spnHP.config(state = 'readonly')

        self.spnATK = self.builder.get_object("spn+ATK")
        self.spnATK.config(state = 'readonly')

        self.spnRCV = self.builder.get_object("spn+RCV")
        self.spnRCV.config(state = 'readonly')
        
        self.builder.get_variable("spnLevel").set(str(self.monster.Level))
        self.builder.get_variable("spn+HP").set(str(self.monster.PlusHP))
        self.builder.get_variable("spn+ATK").set(str(self.monster.PlusATK))
        self.builder.get_variable("spn+RCV").set(str(self.monster.PlusRCV))
        self.builder.get_variable("spnSkillLvl").set(str(self.monster.SkillLevel))
        self.builder.get_variable("spnAwokenSkill").set(str(self.monster.SkillsAwoke))

    def __displaySkillInfo(self):
        if self.monster.ActiveSkillName is None:
            self.builder.get_object("lblSkillName").config(text = "Skill Name: No Skill", justify = LEFT)
            self.builder.get_object("spnSkillLvl").config(state = DISABLED)
            self.builder.get_object("lblSkillCooldown").config(text = "Cooldown: N/A")
        else:
            self.builder.get_object("lblSkillName").config(text = "Skill Name: " + self.monster.ActiveSkillName, justify = LEFT)
            if len(self.master.PADsql.getActiveSkillDesc(self.monster.ActiveSkillName)) > 40:
                count = 0
                spaces = []
                self.desc = ''
                for i in self.master.PADsql.getActiveSkillDesc(self.monster.ActiveSkillName):
                    if i == ' ':
                        spaces.append(count)
                    self.desc += i
                    count += 1
                    if count % 39 == 0:
                        j = spaces[len(spaces) - 1]
                        self.desc = self.desc[0 : j] + '\n' + self.desc[j + 1 :]
                self.builder.get_object("lblSkillDesc").config(text = str(self.desc))
            else:
                self.builder.get_object("lblSkillDesc").config(text = str(self.master.PADsql.getActiveSkillDesc(self.monster.ActiveSkillName)))
            self.spnSkillLVL = self.builder.get_object("spnSkillLvl")
            self.spnSkillLVL.config(from_ = 1, to = self.monster.ActiveSkillMaxLevel, state = NORMAL)
            self.spnSkillLVL.config(state = 'readonly')
            self.builder.get_variable("spnSkillLvl").set(str(self.monster.SkillLevel))

            self.lblSkillCooldown = self.builder.get_object("lblSkillCooldown")
            self.lblSkillCooldown.config(text = "Cooldown: " + str(self.monster.ActiveSkillCoolDown))
        pass

    def __displayMonsterIDentification(self):
        if len(self.monster.MonsterName) > 26:
            count = 0
            spaces = []
            self.name = ''
            self.nom = ''
            for i in self.monster.MonsterName:
                if i == ' ':
                    spaces.append(count)
                self.name += i
                count += 1
                if count % 25 == 0:
                    j = spaces[len(spaces) - 1]
                    self.name = self.name[0 : j] + '\n' + self.name[j + 1 :]
                    
            self.builder.get_object("lblPrintName").config(justify = LEFT, text = self.name)
        else:
            self.builder.get_object("lblPrintName").config(justify = LEFT, text = self.monster.MonsterName)
        self.builder.get_object("lblPrintID").config(justify = LEFT, text = self.monster.MonsterClassID)

        self.priAtt = PhotoImage(file = "Resource/PAD/Images/Attributes/" + str(self.monster.PriAttribute) +'Symbol.png')
        self.AttOne.text = self.monster.PriAttribute
        if self.monster.SecAttribute is None:
            self.secAtt = None
        else:
            self.secAtt = PhotoImage(file = "Resource/PAD/Images/Attributes/" + str(self.monster.SecAttribute) +'Symbol.png')
            self.AttTwo.text = self.monster.SecAttribute
        
        self.builder.get_object("canPriAtt").create_image(2,2, image = self.priAtt, anchor =NW) 
        self.builder.get_object("canSecAtt").create_image(2,2, image = self.secAtt, anchor =NW) 

        self.typeOne = PhotoImage(file = "Resource/PAD/Images/Types/" + str(self.monster.MonsterTypeOne) +'.png')
        self.TypeOne.text = self.monster.MonsterTypeOne

        self.builder.get_object("canTypeTwo").delete("all")
        self.builder.get_object("canTypeThree").delete("all")

        if not self.monster.MonsterTypeTwo is None:
            self.typeTwo = PhotoImage(file = "Resource/PAD/Images/Types/" + str(self.monster.MonsterTypeTwo) +'.png')
            self.TypeTwo.text = self.monster.MonsterTypeTwo
        else:
            self.typeTwo = None
            self.TypeTwo.text = None

        if not self.monster.MonsterTypeThree is None:
            self.typeThree = PhotoImage(file = "Resource/PAD/Images/Types/" + str(self.monster.MonsterTypeThree) +'.png')
            self.TypeThree.text = self.monster.MonsterTypeThree
        else:
            self.typeThree = None
            self.TypeThree.text = None

        self.builder.get_object("canTypeOne").create_image(2,2, image = self.typeOne, anchor =NW) 
        self.builder.get_object("canTypeTwo").create_image(2,2, image = self.typeTwo, anchor =NW) 
        self.builder.get_object("canTypeThree").create_image(2,2, image = self.typeThree, anchor =NW)

        pass

    def __displayAwokenSkills(self):
        self.spnAwokenSkill = self.builder.get_object("spnAwokenSkill")
        #Removes all the previously selected monster's, if there was one, awoken awoken skills
        self.builder.get_object("canAwokenSkillOne").delete("all")
        self.builder.get_object("canAwokenSkillTwo").delete("all")
        self.builder.get_object("canAwokenSkillThree").delete("all")
        self.builder.get_object("canAwokenSkillFour").delete("all")
        self.builder.get_object("canAwokenSkillFive").delete("all")
        self.builder.get_object("canAwokenSkillSix").delete("all")
        self.builder.get_object("canAwokenSkillSeven").delete("all")
        self.builder.get_object("canAwokenSkillEight").delete("all")
        self.builder.get_object("canAwokenSkillNine").delete("all")

        if self.monster.ASListID is None:
            self.builder.get_variable("spnAwokenSkill").set(0)
            self.spnAwokenSkill.config(state = DISABLED)
        else:
            self.spnAwokenSkill.config(state = NORMAL)
            self.builder.get_variable("spnAwokenSkill").set(str(self.monster.SkillsAwoke))
            self.spnAwokenSkill.config(state = 'readonly')

            #Creates the photo image for the selected monster's awoken awoken skills
            self.aSList = self.master.PADsql.getAwokenSkillList(self.monster.MonsterClassID)
            self.aSListImg = []
            self.numAS = 0
            self.awokenSkills = []

            for i in range(1, len(self.aSList)):
                if i <= self.monster.SkillsAwoke:
                    if self.aSList[i] is not None:
                        self.awokenSkills.append(self.aSList[i])
                        self.aSListImg.append(PhotoImage(file = "Resource/PAD/Images/Awoken Skills/" + str(self.aSList[i]) +'.png'))
                        self.numAS += 1
                    else:
                        self.awokenSkills.append(None)
                        self.aSListImg.append(None)
                else:
                    if self.aSList[i] is not None:
                        self.awokenSkills.append(self.aSList[i])
                        self.aSListImg.append(PhotoImage(file = "Resource/PAD/Images/Awoken Skills/not " + str(self.aSList[i]) +'.png'))
                        self.numAS += 1
                    else:
                        self.awokenSkills.append(None)
                        self.aSListImg.append(None)

            self.spnAwokenSkill.config(to = self.numAS)


            self.builder.get_object("canAwokenSkillOne").create_image(2,2, image = self.aSListImg[0], anchor = tk.NW)
            self.builder.get_object("canAwokenSkillTwo").create_image(2,2, image = self.aSListImg[1], anchor = tk.NW)
            self.builder.get_object("canAwokenSkillThree").create_image(2,2, image = self.aSListImg[2], anchor = tk.NW)
            self.builder.get_object("canAwokenSkillFour").create_image(2,2, image = self.aSListImg[3], anchor = tk.NW)
            self.builder.get_object("canAwokenSkillFive").create_image(2,2, image = self.aSListImg[4], anchor = tk.NW)
            self.builder.get_object("canAwokenSkillSix").create_image(2,2, image = self.aSListImg[5], anchor = tk.NW)
            self.builder.get_object("canAwokenSkillSeven").create_image(2,2, image = self.aSListImg[6], anchor = tk.NW)
            self.builder.get_object("canAwokenSkillEight").create_image(2,2, image = self.aSListImg[7], anchor = tk.NW)
            self.builder.get_object("canAwokenSkillNine").create_image(2,2, image = self.aSListImg[8], anchor = tk.NW)

            if self.awokenSkills[0] is None:
                self.ASOne.text = None
                self.ASTwo.text = None
                self.ASThree.text = None
                self.ASFour.text = None
                self.ASFive.text = None
                self.ASSix.text = None
                self.ASSeven.text = None
                self.ASEight.text = None
                self.ASNine.text = None
            else:
                self.ASOne.text = self.awokenSkills[0]

            if self.awokenSkills[1] is None:
                self.ASTwo.text = None
                self.ASThree.text = None
                self.ASFour.text = None
                self.ASFive.text = None
                self.ASSix.text = None
                self.ASSeven.text = None
                self.ASEight.text = None
                self.ASNine.text = None
            else:
                self.ASTwo.text = self.awokenSkills[1]

            if self.awokenSkills[2] is None:
                self.ASThree.text = None
                self.ASFour.text = None
                self.ASFive.text = None
                self.ASSix.text = None
                self.ASSeven.text = None
                self.ASEight.text = None
                self.ASNine.text = None
            else:
                self.ASThree.text = self.awokenSkills[2]

            if self.awokenSkills[3] is None:
                self.ASFour.text = None
                self.ASFive.text = None
                self.ASSix.text = None
                self.ASSeven.text = None
                self.ASEight.text = None
                self.ASNine.text = None
            else:
                self.ASFour.text = self.awokenSkills[3]

            if self.awokenSkills[4] is None:
                self.ASFive.text = None
                self.ASSix.text = None
                self.ASSeven.text = None
                self.ASEight.text = None
                self.ASNine.text = None
            else:
                self.ASFive.text = self.awokenSkills[4]

            if self.awokenSkills[5] is None:
                self.ASSix.text = None
                self.ASSeven.text = None
                self.ASEight.text = None
                self.ASNine.text = None
            else:
                self.ASSix.text = self.awokenSkills[5]

            if self.awokenSkills[6] is None:
                self.ASSeven.text = None
                self.ASEight.text = None
                self.ASNine.text = None
            else:
                self.ASSeven.text = self.awokenSkills[6]

            if self.awokenSkills[7] is None:
                self.ASEight.text = None
                self.ASNine.text = None
            else:
                self.ASEight.text = self.awokenSkills[7]

            if self.awokenSkills[8] is None:
                self.ASNine.text = None
            else:
                self.ASNine.text = self.awokenSkills[8]
            pass