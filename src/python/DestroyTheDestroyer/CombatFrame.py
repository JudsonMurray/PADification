#!usr/bin/env python3
#
#   Name :      WILLIAM GALE
#   Date :      January 12th
#   Purpose:    DestroyingTheDestroyer CombatFrame

# History:  
#      BG - jan 12TH 2017 - V 0.1 initial coding 
#      BG - jan 13TH 2017 - V 0.11 So much integration
#      BG - jan 16TH 2017 - V 0.2 Changed layout, Loaded potion images.
#      KG - jan 18TH 2017 - V 0.3 Added hasWon = True if the player clears floor 10
#      BG - jan 18TH 2017 - Worked on audio
#      BG - Jan 19TH 2017 - intergrated Builders into combat frame
#                           Mass clean up of code, added delays to battle win and lose
#      BG - Jan 20TH 2017 - Fixed Switch scene and clicking on file menu bug
#      KG - Jan 20TH 2017 - Added easter egg

import winsound
import tkinter as tk
import tkinter.messagebox as mb
import pygubu

class CombatFrame:
    def __init__(self, master):
        # sets up Window
        self.master = master

        self.builder = pygubu.Builder()
        self.builder.add_from_file('DTDui/CombatFrame.ui')
        self.combatFrame = self.builder.get_object('root', master)

        self.potionpic = tk.PhotoImage(file = "DTDresource/Health potion.gif")
        self.builder.get_object("potPic").config(image = self.potionpic)
        self.builder.get_object("CombatLog").tag_config("death",background="black", foreground="red", underline=1)
        self.builder.get_object("CombatLog").tag_config("win", foreground="purple")
        self.builder.get_object("CombatLog").tag_config("hit", foreground="red")
        self.builder.get_object("CombatLog").tag_config("attack", foreground="blue")
        self.builder.get_object("CombatLog").tag_config("save", foreground="green", underline=1)
        self.builder.connect_callbacks(self)
        
        # Local Variables
        self.diff = 1
        self.turn = 0
        self.currentFloor = None
        self.deadImage = tk.PhotoImage(file = "DTDresource/dead.gif")
        self.fighting = False
        

    def onAttack(self, event):
        """ Process Attack of player and monsters and updates Labels """
        if self.fighting:
            selection = self.builder.get_variable("monsterSelection").get()

            if selection >= 0 and selection <= 2:
                self.turn += 1
                self.hitMonster(self.master.player.playerAtk, selection)
                self.monsterAttack()
                self.playAttackSound()
                self.updateMonsters()
                self.updatePlayer()
                self.master.player.attacks += 1

                if self.currentFloor.checkWin():
                    if self.master.player.floorNum >= 10 and self.master.gameMode == self.master.NORMAL:
                        self.master.player.hasWon = True
                        self.combatLogPrint("\nYOU  HAVE FELLED THE DESTROYER!!!","win")
                        self.master.player.floorNum = 1
                        self.master.player.floorsBeat += 1
                        self.master.player.bossKills += 1
                        self.master.save()
                        self.master.switch = self.master.after(2000, self.master.showWinScreen)
                        return

                    self.master.player.floorNum += 1
                    self.master.player.floorsBeat += 1
                    self.combatLogPrint("\nTHE CORPSES PILE UP, YOU WIN!","win")
                    self.fighting = False
                    #Switch to Level UP
                    self.master.switch = self.master.after(2000, self.master.showLevelUp)
                    #self.master.showLevelUp()
            else:
                self.combatLogPrint("Select a Monster!")

    def onPotion(self, event):
        """Heals Player if potions available, counts as a turn so you might get attacked"""
        if self.fighting:
            if self.master.player.hasPotions():
                if self.master.player.isFullHp():
                    self.combatLogPrint("Hp Already Full!")
                    return

                self.combatLogPrint(self.master.player.usePotion())
                self.playPotionSound()
                self.turn += 1
                self.monsterAttack()
                self.updatePlayer()
            else:
                self.combatLogPrint("No Potions")
        

    def onFlee(self, event):
        """Flee to the difficulty screen keeping your hero but starting at floor 1"""
        if self.fighting:
            self.playFleeSound()
            self.combatLogPrint("Fleed for your life!!")
            self.master.player.floorNum = 1
            self.combatFrame.grid_forget()
            self.master.player.fullHeal()
            self.master.showDifficultyFrame()
            self.master.playMusic()

    def monsterAttack(self):
        """ Process the monster attack on player, if playered is killed, trigger game over. """

        for i in self.currentFloor.monsters:
            if self.turn % i.monsterSpd == 0 and i.monsterHp > 0:
                # Minimun Damge monster can do is 1.
                damage = i.monsterAtk - self.master.player.playerDef if i.monsterAtk - self.master.player.playerDef > 0 else 1
                self.master.player.minusHp(damage)

                self.combatLogPrint(str(i.monsterName) + " Attacked " + str(self.master.player.playerName) + " for " + str(damage), "hit")
            
            if self.master.player.playerHp <= 0:
                self.combatLogPrint("A horrific death of pain and agony becomes you.", "death")
                self.master.after(5000, self.builder.get_object("CombatLog").delete, 1.0, tk.END) #(1.0, tk.END)
                self.floorLevel = 1
                self.fighting = False
                self.master.deleteSave()
                #switch to Game Over
                if self.master.gameMode == self.master.NORMAL:
                    self.master.switch = self.master.after(3000, self.master.showGameOver)
                else:
                    self.master.switch = self.master.after(3000, self.master.showEndlessScoreFrame)
                break

    def combatLogPrint(self, text, tag = None):
        """Print to combat log"""
        self.builder.get_object("CombatLog").config(state = tk.NORMAL)
        self.builder.get_object("CombatLog").insert(tk.END,"\n")
        self.builder.get_object("CombatLog").insert(tk.END, text, tag)
        self.builder.get_object("CombatLog").see(tk.END)
        self.builder.get_object("CombatLog").config(state = tk.DISABLED)

    def updateMonsters(self):
        """Updates monster Labels"""
        # Disables dead monsters and moves to alive monsters
        for i in range(0,3):
            if self.currentFloor.monsters[i].monsterHp <= 0:
                self.builder.get_object("Radio_" + str(i + 1)).config(state = tk.DISABLED)
                if i == self.builder.get_variable("monsterSelection").get():
                    for i in range(0,3):
                        if self.currentFloor.monsters[i].monsterHp > 0:
                            self.builder.get_variable("monsterSelection").set(i)
                            break
            else:
                self.builder.get_object("Radio_" + str(i + 1)).config(state = tk.NORMAL)
        
        # Updates Monster Labels and images
        count = 0
        for i in ("mOne", "mTwo", "mThree"):
            self.builder.get_variable(i + "Name").set(self.currentFloor.monsters[count].monsterName)
            self.builder.get_variable(i + "Level").set(self.master.player.floorNum)
            self.builder.get_variable(i + "HPValue").set(self.currentFloor.monsters[count].monsterHp)
            self.builder.get_variable(i + "MaxHP").set(self.currentFloor.monsters[count].monsterMaxHp)
            self.builder.get_object(i).delete("pic")

            

            if self.currentFloor.monsters[count].monsterHp > 0:
                self.builder.get_object(i).create_image(13,15, image = self.currentFloor.monsters[count].photoImage, anchor = tk.NW, tag = "pic")
            else:
                self.builder.get_object(i).create_image(18,15, image = self.deadImage, anchor = tk.NW, tag = "pic")
            count += 1

    def updatePlayer(self):
        """Updates Player Labels"""
        if self.master.gameMode == self.master.NORMAL:
            self.builder.get_object('Label_1').config(text = "/ 10")
        else:
            self.builder.get_object('Label_1').config(text = "")
        self.builder.get_variable("floorVar").set(self.master.player.floorNum)
        self.builder.get_variable("playerName").set(self.master.player.playerName)
        self.builder.get_variable("playerLevel").set(self.master.player.playerLevel)
        self.builder.get_variable("playerMaxHP").set(self.master.player.playerMaxHp)
        self.builder.get_variable("playerHPValue").set(self.master.player.playerHp)
        self.builder.get_object("potionCount").config(text = str(self.master.player.potions))

    def generateFloor(self):
        """Generates Monsters for killing"""
        self.combatLogPrint("\nYOU ENTER FLOOR " + str(self.master.player.floorNum) + "\n")
        self.turn = 0
        self.fighting = True
        self.currentFloor = self.master.levelBuilder.build(self.master.player.floorNum)
        self.master.playMusic(self.currentFloor.floorMusic)
        for i in self.currentFloor.monsters:
            i.monsterDificultyMultiplier(self.diff)
            i.monsterLvlMultiplier(self.master.player.floorNum)
            
            if i.monsterName == "Kyle The Destroyer":
                i.monsterAtk = self.diff * self.master.destroyerAtk + self.master.player.floorNum * 5

    def hitMonster(self, damage, monster):
        """ Damage selected Monster """
        dealtDamage = damage - self.currentFloor.monsters[monster].monsterDef if damage - self.currentFloor.monsters[monster].monsterDef > 0 else 1 
        self.combatLogPrint(str(self.master.player.playerName) + " Attacked " + str(self.currentFloor.monsters[monster].monsterName) + " for " + str(dealtDamage), "attack")
        self.currentFloor.monsters[monster].minusMonsterHp(dealtDamage)
        if self.currentFloor.monsters[monster].monsterHp <= 0:
            self.master.player.monsterKills += 1

    def canvasSelection(self, event):
        """ Select a monster by clicking on canvas"""
        if event.widget == self.builder.get_object("mOne"):
            if self.currentFloor.monsters[0].monsterHp > 0:
                self.builder.get_variable("monsterSelection").set(0)
        if event.widget == self.builder.get_object("mTwo"):
            if self.currentFloor.monsters[1].monsterHp > 0:
                self.builder.get_variable("monsterSelection").set(1)
        if event.widget == self.builder.get_object("mThree"):
            if self.currentFloor.monsters[2].monsterHp > 0:
                self.builder.get_variable("monsterSelection").set(2)

    def playAttackSound(self):
        winsound.PlaySound(self.master.RESOURCEDIR + "attack.wav", winsound.SND_ASYNC | winsound.SND_FILENAME)

    def playPotionSound(self):
        winsound.PlaySound(self.master.RESOURCEDIR + "potionDrink.wav", winsound.SND_ASYNC | winsound.SND_FILENAME)

    def playFleeSound(self):
        winsound.PlaySound(self.master.RESOURCEDIR + "runaway.wav", winsound.SND_ASYNC | winsound.SND_FILENAME)
        