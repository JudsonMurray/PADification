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
from PIL import Image
from PIL import ImageTk
import PADMonster

class MonsterEdit:
    def __init__(self, master):
        self.master  = master
        self.builder = pygubu.Builder()
        self.builder.add_from_file(r"src\ui\Monster Edit UI.ui")
        self.monsteredit = self.builder.get_object("Monster Edit")
        self.builder.connect_callbacks(self)
        self.image = None
        self.portrait = None

    def receiveInstanceID(self, InstanceID, Wishlist):
        self.instanceID = InstanceID
        self.extraSlot = self.builder.get_object("chkExtraSlot")
        self.maxSlots = self.builder.get_variable('maxSlots')
        self.monster = self.master.PADsql.selectMonsterInstance(self.instanceID, wishlist = Wishlist)
        self.monster = PADMonster.Monster(self.monster[0])
        self.latents = self.master.PADsql.getLatentAwokenSkills()

        if self.monster.LSListID != None:
            self.latentList = self.master.PADsql.getLatentAwokenSkillList(self.instanceID)
            if self.latentList[7]:
                self.extraSlot.select()
        else:
            self.extraSlot.deselect()
        self.image = Image.open("Resource/PAD/Images/portraits/" + str(self.monster.MonsterClassID) + ".jpg").resize((320,192))
        self.portrait = ImageTk.PhotoImage(self.image)
        self.builder.get_object("canPortrait").create_image(2, 2, image = self.portrait, anchor = NW)

        if self.monster.AssistMonsterID != None:
            self.assistMonster = self.master.PADsql.selectMonsterInstance(self.monster.AssistMonsterID, wishlist = Wishlist)
            self.assistMonster = PADMonster.Monster(self.assistMonster[0])
            self.__displayAssistInfo()
        else:
            self.builder.get_object("canAssistantThumb").delete('all')
            self.builder.get_object("lblAssistName").config(text = "Assist Name: None", justify = LEFT)
            self.builder.get_object("lblAssistID").config(text = "Assist ID: None", justify = LEFT)
            self.builder.get_object("lblAssistLvl").config(text = "Assist LvL: None", justify = LEFT)
            self.builder.get_object("lblAssistHP").config(text = "Assist HP: None", justify = LEFT)
            self.builder.get_object("lblAssistATK").config(text = "Assist ATK: None", justify = LEFT)
            self.builder.get_object("lblAssistRCV").config(text = "Assist RCV: None", justify = LEFT)
            self.assistHP = 0
            self.assistATK = 0
            self.assistRCV = 0

        self.builder.get_object("lstSelectedLatents").delete(0, END)

        self.__displayAwokenSkills()
        self.__displayMonsterIDentification()
        self.__displaySkillInfo()
        self.__displayStats()
        self.__displayLatentSkills()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--- Bindings -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def selectLatentAwokenSkill(self, event):
        self.latentSkills = self.builder.get_object("lstLatents")
        self.chosenLatent = self.latentSkills.get(ANCHOR)
        if self.chosenLatent != '' and self.usedSlots < self.maxSlots.get():
            self.builder.get_object("btnAddLS").config(state = NORMAL)
        self.builder.get_object("btnRemoveLS").config(state = DISABLED)
        pass

    def selectAssignedLASkill(self, event):
        self.latentSkillList = self.builder.get_object("lstSelectedLatents")
        self.chosenLatent = self.latentSkillList.get(ANCHOR)
        if self.chosenLatent != '':
            self.builder.get_object("btnRemoveLS").config(state = NORMAL)
        self.builder.get_object("btnAddLS").config(state = DISABLED)
        pass

    def selectExtraSlot(self, event):
        if self.maxSlots.get() == 5:
            self.builder.get_object("lblLatentSlots").config(text = "Latent Slots: " + str(self.usedSlots) + " / " + str(self.maxSlots.get() + 1))
        elif self.maxSlots.get() == 6:
            self.builder.get_object("lblLatentSlots").config(text = "Latent Slots: " + str(self.usedSlots) + " / " + str(self.maxSlots.get() - 1))
        
        pass

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--- Button Commands ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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
        pass

    def applyChanges(self):
        self.monster.setLevel(int(self.spnLevel.get()))
        self.monster.setPlusHP(int(self.spnHP.get()))
        self.monster.setPlusATK(int(self.spnATK.get()))
        self.monster.setPlusRCV(int(self.spnRCV.get()))
        self.monster.setSkillLevel(int(self.spnAwokenSkill.get()))
        self.monster.setSkillsAwoke(int(self.spnSkillLVL.get()))


        pass

    def cancel(self):
        for i in range(1, self.monster.Level):
            self.builder.get_object("spnLevel").invoke('buttondown')

        for i in range(0, self.monster.PlusHP):
            self.builder.get_object("spn+HP").invoke('buttondown')

        for i in range(0, self.monster.PlusATK):
            self.builder.get_object("spn+ATK").invoke('buttondown')

        for i in range(0, self.monster.PlusRCV):
            self.builder.get_object("spn+RCV").invoke('buttondown')

        for i in range(0, self.monster.SkillLevel):
            self.builder.get_object("spnSkillLvl").invoke('buttondown')

        for i in range(0, self.monster.SkillsAwoke):
            self.builder.get_object("spnAwokenSkill").invoke('buttondown')

        self.master.showPlayerCollection()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--- Displaying base information, performed when screen is opened from PlayerCollection -----------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __UpdateInfo(self):
        pass

    def __displayAssistInfo(self):
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
        pass

    def __displayLatentSkills(self):

        for i in self.latents:
            self.builder.get_object("lstLatents").insert(END, i[0])

        self.usedSlots = 0

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

        for i in range(1, self.monster.Level):
            self.spnLevel.invoke('buttonup')

        for i in range(0, self.monster.PlusHP):
            self.spnHP.invoke('buttonup')

        for i in range(0, self.monster.PlusATK):
            self.spnATK.invoke('buttonup')

        for i in range(0, self.monster.PlusRCV):
            self.spnRCV.invoke('buttonup')


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
            for i in range(1, self.monster.SkillLevel):
                self.spnSkillLVL.invoke('buttonup')
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
        if self.monster.SecAttribute is None:
            self.secAtt = None
        else:
            self.secAtt = PhotoImage(file = "Resource/PAD/Images/Attributes/" + str(self.monster.SecAttribute) +'Symbol.png')
        
        self.builder.get_object("canPriAtt").create_image(2,2, image = self.priAtt, anchor =NW) 
        self.builder.get_object("canSecAtt").create_image(2,2, image = self.secAtt, anchor =NW) 

        self.typeOne = PhotoImage(file = "Resource/PAD/Images/Types/" + str(self.monster.MonsterTypeOne) +'.png')

        self.builder.get_object("canTypeTwo").delete("all")
        self.builder.get_object("canTypeThree").delete("all")

        if not self.monster.MonsterTypeTwo is None:
            self.typeTwo = PhotoImage(file = "Resource/PAD/Images/Types/" + str(self.monster.MonsterTypeTwo) +'.png')
        else:
            self.typeTwo = None

        if not self.monster.MonsterTypeThree is None:
            self.typeThree = PhotoImage(file = "Resource/PAD/Images/Types/" + str(self.monster.MonsterTypeThree) +'.png')
        else:
            self.typeThree = None

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
            for i in range(0, self.monster.SkillsAwoke):
                self.spnAwokenSkill.invoke('buttonup')

            #Creates the photo image for the selected monster's awoken awoken skills
            self.aSList = self.master.PADsql.getAwokenSkillList(self.monster.MonsterClassID)
            self.aSListImg = []
            self.numAS = 0

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
        pass
