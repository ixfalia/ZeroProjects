import Zero
import Events
import Property
import VectorMath

Vec3 = VectorMath.Vec3
Vec4 = VectorMath.Vec4

class Weapon:
    def __init__(self, Owner, Name, TankLimit = 255, StartingAmount = 0, isUnlimited = False, isReplenishing = False, Color = Vec4(1,1,1,1), Bullet = "BasicBullet", Minimum = 0):
        self.Name = Name
        self.Owner = Owner
        self.Bullet = Bullet
        self.TankLimit = TankLimit
        self.Tank = int(StartingAmount)
        self.isReplenishing = isReplenishing #does this thing replenish over time?
        self.Minimum = Minimum  #if it does replenish how much is the minimum
        self.isUnlimited = isUnlimited
        self.Color = Color
        
        self.Timer = 0
        self.TimeCycle = 0.5
        
        if self.isUnlimited:
            self.Tank = self.TankLimit
            
        if self.isReplenishing:
            Zero.Connect(self.Owner.Space, Events.LogicUpdate, self.onUpdate)
        pass
    #end init()
    
    def onUpdate(self, Event):
        Timer += Event.Dt
        
        if self.Timer > self.TimeCycle:
            if self.Tank < self.Minimum:
                self.Tank += 1
        #endif
    
    def deplete(self, amount = 1):
        if self.isUnlimited:
            return
        
        self.Tank -= amount
        
        if self.Tank < 0:
            self.Tank = 0
        pass
    
    def replenish(self, amount = 15):
        if self.isUnlimited:
            return
        
        self.Tank += int(amount)
        
        if self.Tank > self.TankLimit:
            self.Tank = self.TankLimit
        pass
    
    def isNotEmpty(self):
        if self.isUnlimited:
            return True
        else:
            return self.Tank > 0
    
    def isEmpty(self):
        if self.isUnlimited:
            return False
        else:
            return self.Tank <= 0
#end class

class LightTank:
    DebugMode = Property.Bool(default = False)
    RedTank = Property.Float(default = 0)
    GreenTank = Property.Float(default = 0)
    BlueTank = Property.Float(default = 0)
    
    TankLimit = Property.Float(default = 255)
    TankScale = Property.Float(default = 255)
    StartingAmount = Property.Uint(default = 0)
    
    CurrentWeapon = Property.Uint(default = 0)
    
    def Initialize(self, initializer):
        #Name, TankLimit = 255, StartingAmount = 0, isUnlimited = False, isReplenishing = False, Minimum = 0
        Gray = Weapon(self.Owner, "Gray", self.TankLimit, self.StartingAmount, True, False, Vec4(0.5,0.5,0.5,1))
        Red = Weapon(self.Owner, "Red", self.TankLimit, self.StartingAmount, False, False, Vec4(1,0,0,1))
        Green = Weapon(self.Owner, "Green", self.TankLimit, self.StartingAmount, False, False, Vec4(0,1,0,1))
        Blue = Weapon(self.Owner, "Blue", self.TankLimit, self.StartingAmount, False, False, Vec4(0,0,1,1))
        
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevel)
        
        self.CurrentWeapon = 0
        
        self.Weapons = [Gray, Red, Green, Blue]
        self.WeaponLength = len(self.Weapons)
        
        if self.DebugMode:
            print("LightTank.Initialize() ", self.Weapons)
        pass
    
    def onLevel(self, Event):
        for i in self.Weapons:
            print(i.Name)
            self.sendColorMessage("", i.Name, i.Tank)
    
    def replenish(self, amount, color):
        weapon = self.GetCertainWeapon(color)
        weapon.replenish(amount)
        
        self.sendColorMessage("", color, weapon.Tank)
        return
        
        #deprecate code
        if color == "Red":
            self.RedTank += amount / self.TankLimit
            self.sendColorMessage("", "Red", self.RedTank*self.TankLimit)
            
            if self.DebugMode:
                self.printTankStrength(color, self.RedTank)
            pass
        elif color == "Blue":
            self.BlueTank += (amount / self.TankLimit)
            self.sendColorMessage("", "Blue", self.BlueTank*self.TankLimit)
            
            if self.DebugMode:
                self.printTankStrength(color, self.BlueTank)
            pass
        elif color == "Green":
            self.GreenTank += (amount / self.TankLimit)
            self.sendColorMessage("", "Green", self.GreenTank*self.TankLimit)
            
            if self.DebugMode:
                self.printTankStrength(color, self.GreenTank)
            pass
        else:
            print("LightTank.replenish(): Color parameter implemented is unknown")
            
        #self.sendColorMessage(color+"Update", color, amount)
    
    def depleteCurrent(self, amount = 1):
        if self.CurrentWeapon == 0:
            return
        elif not self.CurrentWeapon >= self.WeaponLength or not self.CurrentWeapon < 0:
            weapon = self.Weapons[self.CurrentWeapon]
            
            weapon.deplete(amount)
            self.sendColorMessage("", weapon.Name, weapon.Tank)
            pass
        else:
            print("LightTank.depleteCurrent() self.CurrentWeapon is an unviable value")
            return
    
    def deplete(self, amount, color):
        weapon = self.GetCertainWeapon(color)
        print("LightTank.deplete()", weapon.Name, "Tank", weapon.Tank)
        weapon.deplete(amount)
        
        self.sendColorMessage("", color, weapon.Tank)
        return
        
        #deprecated code
        if color == "Red":
            self.RedTank -= amount / self.TankLimit
            self.sendColorMessage("", "Red", self.RedTank*self.TankLimit)
            
            if self.DebugMode:
                self.printTankStrength(color, self.RedTank)
            pass
        elif color == "Blue":
            self.BlueTank -= (amount / self.TankLimit)
            self.sendColorMessage("", "Blue", self.BlueTank*self.TankLimit)
            
            if self.DebugMode:
                self.printTankStrength(color, self.BlueTank)
            pass
        elif color == "Green":
            self.GreenTank -= (amount / self.TankLimit)
            self.sendColorMessage("", "Green", self.GreenTank*self.TankLimit)
            
            if self.DebugMode:
                self.printTankStrength(color, self.GreenTank)
            pass
        else:
            print("LightTank.replenish(): Color parameter implemented is unknown")
            
        #self.sendColorMessage(color+"Update", color, amount)
    
    def getCurrentWeapon(self):
        return self.Weapons[self.CurrentWeapon]
    
    def GetCertainWeapon(self, weapon):
        if type(weapon) is str:
            for i in self.Weapons:
                if i.Name == weapon:
                    return i
            #end for
            
            return None #we didn't find it after looking through the whole thing
        elif type(weapon) is int:
            return self.Weapons[self.weapon]
        #endif
    
    def sendColorMessage(self, MessageType, Color, Amount):
        if self.DebugMode:
            print(Color + " Message sent:", Amount)
        
        myEvent = Zero.ScriptEvent()
        myEvent.Type = MessageType
        myEvent.String = int(Amount)
        myEvent.Function = None
        
        self.Owner.UIMaker.DispatchToHUDSpace(Color + "Update", myEvent)
    
    def printTankStrength(self, Color, Amount):
        print("LightTank:", Color+" Tank At:", Amount*100)
    
    def shiftWeaponLeft(self):
        newColor = self.CurrentWeapon - 1
        
        if self.CurrentWeapon < 0:
            newColor = self.WeaponLength -1
        
        self.changeWeapon(newColor)
    
    def shiftWeaponRight(self):
        newColor = self.CurrentWeapon - 1
        
        if self.CurrentWeapon < 0:
            newColor = self.WeaponLength-1
        
        self.changeWeapon(newColor)
    
    def changeWeapon(self, WeaponID):
        
        self.CurrentWeapon = WeaponID
        weapon = self.Weapons[self.CurrentWeapon]
        
        self.Owner.Sprite.Color = weapon.Color
        self.Owner.SpriteParticleSystem.Tint = weapon.Color
        return weapon
    
    def setWeaponLogic(self):
        pass #do the stuff that needs to happen
    
    def currentWeaponNotEmpty(self):
        currentColor = self.Weapons[self.CurrentWeapon]
        
        return currentColor.isNotEmpty()

Zero.RegisterComponent("LightTank", LightTank)