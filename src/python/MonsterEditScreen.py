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


class MonsterFrame:
    def __init__(self, master, assistant):
        self.master = master
        self.assistant = assistant
        self.builder = pygubu.Builder()
        self.builder.add_from_file(r"src\ui\Monster Edit UI.ui")
        self.monbut = self.builder.get_object('MonsFrame', self.master.builder.get_object("canSelectAssist"))
        self.myMonster = tk.PhotoImage(file = "Resource/PAD/Images/thumbnails/" + str(assistant.MonsterClassID) + '.png').subsample(2)
        self.builder.get_object("FrameLabel").create_image(2,2, image = self.myMonster, anchor = tk.NW)
        self.builder.connect_callbacks(self)

    def clickMe(self, event):
        for i in range(0, (len(self.master.buttons))):
            self.master.buttons[i].monbut.config(relief = FLAT)
        self.monbut.config(relief = SUNKEN)


        for i in range(0, len(self.master.assistants)):
            if self.master.assistants[i] == self.master.monster.AssistMonsterID:
                self.master.assistants.pop(i)

        self.master.monster.AssistMonsterID = None

        self.master.monster.AssistMonsterID = self.assistant.InstanceID

        self.master.displayAssistInfo()
        pass

class MonsterEdit:
    def __init__(self, master):
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
        self.startMonster = 0
        
        self.currentPage = 1
        self.builder.get_object("btnNext").config(state = NORMAL)
        self.builder.get_object("btnPrev").config(state = DISABLED)
        self.wishlist = Wishlist
        self.extraSlot = self.builder.get_object("chkExtraSlot")
        self.maxSlots = self.builder.get_variable('maxSlots')
        self.monster = self.master.PADsql.selectMonsterInstance(self.instanceID, wishlist = self.wishlist)
        self.monster = PADMonster.Monster(self.monster[0])
        self.latents = self.master.PADsql.getLatentAwokenSkills()
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
            if self.chosenLatent != '' and self.usedSlots < self.maxSlots.get():
                self.builder.get_object("btnAddLS").config(state = NORMAL)
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
        self.master.playerCollection.buttons[self.master.playerCollection.k].clickMe(self)
        self.master.PADsql.saveMonster(self.monster.getSaveDict())
        self.master.showPlayerCollection()
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
        self.__displayPossibleAssistants()

    def prev(self):
        self.builder.get_object("btnNext").config(state = NORMAL)
        self.currentPage -= 1
        self.startMonster = 16 * (self.currentPage-1)
        if self.currentPage == 1:
            self.builder.get_object("btnPrev").config(state = DISABLED)
        self.__displayPossibleAssistants()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--- Displaying base information, performed when screen is opened from PlayerCollection -----------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __displayPossibleAssistants(self):

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

        for i in self.builder.get_object("canSelectAssist").grid_slaves():
            i.grid_forget()

        self.buttons = []
        self.count = 0
        display = True

        if self.asist:
            for i in self.pAssistants:
                try:
                    if self.startMonster < 16 * self.currentPage and ((self.startMonster >= 16 * (self.currentPage - 1)) and not(self.startMonster == len(self.pAssistants))) or self.count != 16:
                        if self.pAssistants[self.startMonster].InstanceID != self.monster.InstanceID and self.pAssistants[self.startMonster].AssistMonsterID is None:
                            for a in self.assistants:
                                if a == self.pAssistants[self.startMonster].InstanceID:
                                    display = False
                                else:
                                    display = True

                                
                                
                                if a == self.formarAsisID:
                                    display = True
                            teams = self.pds.selectTeamInstance()
                            for selectedMonster in self.pAssistants:
                                        for i in range(0,len(teams)):
                                            self.SelectedTeam = PADMonster.Team(self.pds, (teams[i]))

                                            if self.SelectedTeam.LeaderMonster == selectedMonster.InstanceID:
                                                display = False
                                                break
                                            if self.SelectedTeam.SubMonsterOne == selectedMonster.InstanceID:
                                                display = False
                                                break
                                            if self.SelectedTeam.SubMonsterTwo == selectedMonster.InstanceID:
                                                display = False
                                                break
                                            if self.SelectedTeam.SubMonsterThree == selectedMonster.InstanceID:
                                                display = False
                                                break
                                            if self.SelectedTeam.SubMonsterFour == selectedMonster.InstanceID:
                                                display = False
                                                break
                                            display = True

                            if display:
                                self.buttons.append(MonsterFrame(self, self.pAssistants[self.startMonster]))
                                self.buttons[self.count].monbut.grid(row=self.count // 8,column = self.count % 8)
                                if self.pAssistants[self.startMonster].InstanceID == self.monster.AssistMonsterID:
                                    self.buttons[self.count].monbut.config(relief = SUNKEN)
                                else:
                                    self.buttons[self.count].monbut.config(relief = FLAT)
                                self.buttons[self.count].builder.get_object('lblMonsterBrief').config(text = 'LVL:' + str(self.pAssistants[self.startMonster].Level)+ '\nID: ' + str(self.pAssistants[self.startMonster].MonsterClassID))
                                self.count += 1
                        
                        self.startMonster += 1
                except:
                    pass

        self.pages = (len(self.pAssistants) // 16) + 1
        if len(self.pAssistants) == 0:
            self.pages = 1
        elif len(self.pAssistants) % 16 == 0:
            self.pages -= 1

        if self.pages == 1:
            self.builder.get_object('btnNext').config(state = DISABLED)
        else:
            self.builder.get_object('btnNext').config(state = NORMAL)
        self.builder.get_object('lblCurPage').config(text = "Page " + str(self.currentPage) + "/" + str(self.pages))

        pass


    def displayAssistInfo(self):
        self.assistMonster = self.master.PADsql.selectMonsterInstance(self.monster.AssistMonsterID, wishlist = self.wishlist)
        self.assistMonster = PADMonster.Monster(self.assistMonster[0])

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
        if self.monster.ASListID is None:
            self.spnAwokenSkill.config(state = DISABLED)
        else:
            self.spnAwokenSkill.config(state = NORMAL)
            self.spnAwokenSkill.config(state = 'readonly')

            self.builder.get_variable("spnAwokenSkill").set(str(self.monster.SkillsAwoke))

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