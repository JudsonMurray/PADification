#Version 1.0 - Created Module - Kyle
#Version 1.1 - Added player Name to Class constructors, Added playerMaxHp, playerLevel, Made monsters inherite Monster class, added monsterMaxHp, monsterSpd
#Version 1.2 - Added image variables to monsters
#            - Added Widigo, Goblin, SamuraiTortise, Cthulu, Missingno Monster Classes
#Version 1.3 - added accessors
#            - trashed fighter class
import random
class Player():
    def __init__(self):
        self.playerName = ''
        self.playerMaxHp = -1
        self.playerHp = self.playerMaxHp
        self.playerAtk = 0
        self.playerDef = 0
        self.playerLevel = 0
        self.potions = 0
        self.hasWon = False
        self.playerImage = ""

    def addPotions(self, amount):
        self.potions += amount
        return

    def minusPotions(self, amount):
        self.potions -= amount
        return

    def addHp(self, amount):
        self.playerHp += amount
        if self.playerHp > self.playerMaxHp:
            self.playerHp = self.playerMaxHp

    def minusHp(self, amount):
        self.playerHp -= amount

    def getHp(self):
        return self.playerHp

    def getAtk(self):
        return self.playerAtk

    def getDef(self):
        return self.playerDef

    def getPots(self):
        return self.potions

class Adventurer(Player):
    def __init__(self, name):
        super().__init__()
        self.playerLevel = 1
        self.playerName = name
        self.playerMaxHp = 110
        self.playerHp = self.playerMaxHp
        self.playerAtk = 17
        self.playerDef = 1
        self.potions = 10
        self.playerImage = "DTDresource/Adventurer.gif"

class Fighter(Player):
    def __init__(self, name):
        super().__init__()
        self.playerLevel = 1
        self.playerName = name
        self.playerMaxHp = 60 
        self.playerHp = self.playerMaxHp
        self.playerAtk = 17000 # changed for quick kills
        self.playerDef = 8
        self.potions = 1
        self.playerImage = "DTDresource/Fighter.gif"

class Rogue(Player):
    def __init__(self, name):
        super().__init__()
        self.playerLevel = 1
        self.playerName = name
        self.playerMaxHp = 45
        self.playerHp = self.playerMaxHp
        self.playerAtk = 23
        self.playerDef = 3
        self.potions = 2
        self.playerImage = "DTDresource/Rogue.gif"

class Mage(Player):
    def __init__(self, name):
        super().__init__()
        self.playerLevel = 1
        self.playerName = name
        self.playerMaxHp = 30
        self.playerHp = self.playerMaxHp
        self.playerAtk = 28
        self.playerDef = 1
        self.potions = 10
        self.playerImage = "DTDresource/Mage.gif"

class Explorer(Player):##
    def __init__(self, name):
        super().__init__()
        self.playerLevel = 1
        self.playerName = name
        self.playerMaxHp = 310
        self.playerHp = self.playerMaxHp
        self.playerAtk = 37
        self.playerDef = 10
        self.potions = 60
        self.playerImage = "DTDresource/Explorer.gif"

class Gladiator(Player):##
    def __init__(self, name):
        super().__init__()
        self.playerLevel = 1
        self.playerName = name
        self.playerMaxHp = 278
        self.playerHp = self.playerMaxHp
        self.playerAtk = 42
        self.playerDef = 12
        self.potions = 30
        self.playerImage = "DTDresource/Gladiator.gif"

class Assassin(Player):##
    def __init__(self, name):
        super().__init__()
        self.playerLevel = 1
        self.playerName = name
        self.playerMaxHp = 180
        self.playerHp = self.playerMaxHp
        self.playerAtk = 23
        self.playerDef = 13
        self.potions = 25
        self.playerImage = "DTDresource/Assassin.gif"

class GrandMage(Player):##
    def __init__(self, name):
        super().__init__()
        self.playerLevel = 1
        self.playerName = name
        self.playerMaxHp = 140
        self.playerHp = self.playerMaxHp
        self.playerAtk = 53
        self.playerDef = 7
        self.potions = 100
        self.playerImage = "DTDresource/Grand Mage.gif"



class Monster:
    def __init__(self):
        self.monsterName = ''
        self.monsterMaxHp = 0
        self.monsterHp = self.monsterMaxHp
        self.monsterAtk = 0
        self.monsterDef = 0
        self.monsterSpd = random.randint(2,4)
        self.monsterImg = ""

    def addMonsterHp(self, amount):
        self.monsterHp += amount
        if self.monsterHp > self.monsterMaxHp:
            self.monsterHp = self.monsterMaxHp
        return

    def minusMonsterHp(self, amount):
        self.monsterHp -= amount
        if self.monsterHp <= 0:
            self.monsterHp = 0
        return

    def monsterDificultyMultiplier(self, amount):
        self.monsterMaxHp *= amount
        self.monsterHp *= amount
        self.monsterAtk *= amount
        self.monsterDef *= amount

    def monsterLvlMultiplier(self, amount):
        self.monsterMaxHp += int(self.monsterMaxHp * (amount * 0.08))
        self.monsterHp = self.monsterMaxHp
        self.monsterAtk += int(self.monsterAtk * (amount * 0.08))
        self.monsterDef += int(self.monsterDef * (amount * 0.08))

class Gremlin(Monster):
    def __init__(self):
        super().__init__()
        self.monsterName = 'Gremlin'
        self.monsterMaxHp = 50
        self.monsterHp = self.monsterMaxHp
        self.monsterAtk = 12
        self.monsterDef = 7
        self.monsterImg = "Gremlin.gif"

class Gargoyle(Monster):
    def __init__(self):
        super().__init__()
        self.monsterName = 'Gargoyle'
        self.monsterMaxHp = 30
        self.monsterHp = self.monsterMaxHp
        self.monsterAtk = 8
        self.monsterDef = 16
        self.monsterImg = "Gargoyle.gif"

class Pikachu(Monster):
    def __init__(self):
        super().__init__()
        self.monsterName = 'Pikachu!'
        self.monsterMaxHp = 42
        self.monsterHp = self.monsterMaxHp
        self.monsterAtk = 17
        self.monsterDef = 1
        self.monsterImg = "Pikachu.gif"

class AVeryPowerfulMonster(Monster):
    def __init__(self):
        super().__init__()
        self.monsterName = 'This Name Is Pointlessly Long And Propably Will Not Fit Into The Screen However It Will Be There Anyway'
        self.monsterMaxHp = 190
        self.monsterHp = self.monsterMaxHp
        self.monsterAtk = 1
        self.monsterDef = -5
        self.monsterImg = "AVeryPowerfulMonster.gif"

class Ogre(Monster):
    def __init__(self):
        super().__init__()
        self.monsterName = 'The Ogre'
        self.monsterMaxHp = 230
        self.monsterHp = self.monsterMaxHp
        self.monsterAtk = 20
        self.monsterDef = 6
        self.monsterImg = "Ogre.gif"

class Goblin(Monster):
    def __init__(self):
        super().__init__()
        self.monsterName = 'Goblin'
        self.monsterMaxHp = 55
        self.monsterHp = self.monsterMaxHp
        self.monsterAtk = 12
        self.monsterDef = 7
        self.monsterImg = "Goblin.gif"

class Wendigo(Monster):
    def __init__(self):
        super().__init__()
        self.monsterName = 'Wendigo'
        self.monsterMaxHp = 40
        self.monsterHp = self.monsterMaxHp
        self.monsterAtk = 21
        self.monsterDef = 2
        self.monsterImg = "wendigo.gif"

class Cthulu(Monster):
    def __init__(self):
        super().__init__()
        self.monsterName = 'Cthulu'
        self.monsterMaxHp = 133
        self.monsterHp = self.monsterMaxHp
        self.monsterAtk = 20
        self.monsterDef = 6
        self.monsterImg = "Cthulu.gif"

class SamuraiTortise(Monster):
    def __init__(self):
        super().__init__()
        self.monsterName = 'Giant Turtle'
        self.monsterMaxHp = 12
        self.monsterHp = self.monsterMaxHp
        self.monsterAtk = 7
        self.monsterDef = 10000
        self.monsterImg = "Sword Gator.gif"


class Missingno(Monster):
    def __init__(self):
        super().__init__()
        self.monsterName = 'Missingno'
        self.monsterMaxHp = 27
        self.monsterHp = self.monsterMaxHp
        self.monsterAtk = 16
        self.monsterDef = 16
        self.monsterImg = "MissingNo.gif"


class KyleHasCome(Monster):
    def __init__(self):
        super().__init__()
        self.monsterName = "Kyle The Destroyer Of All Things Or AT Least He Would Be If He Wern't Too Lazy To Do So"
        self.monsterMaxHp = 450
        self.monsterHp = self.monsterMaxHp
        self.monsterAtk = 0
        self.monsterDef = 50
        self.monsterImg = "theDestroyer.gif"
