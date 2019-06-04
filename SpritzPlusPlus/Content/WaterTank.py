import Zero
import Events
import Property
import VectorMath

class WaterTank:
    DebugMode = Property.Bool( default = False )
    Tank = Property.Float( default = 1 )
    MinimumWater = Property.Float( default = 0.1 )
    MaximumWater = Property.Float(default = 1)
    Replenishing =  Property.Bool(default = True)
    ReplenishingLimit = Property.Float(default = 0.21)
    UnlimitedWater = Property.Bool( default = False )
    Percent = 0
    TankReplenishing = False
    isHUDMade = False
    HUDSpace = None
    
    def Initialize(self, initializer):
        Zero.Connect( self.Space, Events.LogicUpdate, self.onUpdate )
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevelStarted)
        #Zero.Connect(self.Space, "HUDCreated", self.onHUDCreation)
        
        self.HUDSpace = Zero.Game.FindSpaceByName("HUDSpace")
        
        #self.updatePercent()
    #enddef
    
    def onLevelStarted(self, Event):
        self.updatePercent()
    #enddef
    
    def onHUDCreation(self, Event):
        self.isHUDMade = True
        self.HUDSpace = Event.HUDSpace
        
        if self.DebugMode:
            print("WaterTank: HUD is made: ", self.HUDSpace)
    #enddef
    
    def onUpdate(self, Event):
        NormalizedTime = Event.Dt 
        
        if not self.Replenishing:
            return
        
            #if the tank is less than 10% full, add 1 percent back up.
        if( self.Tank > self.MinimumWater and self.Tank < self.MinimumWater + self.ReplenishingLimit ):
            self.replenish( 0.05 * NormalizedTime)
            self.TankReplenishing = False
            self.updatePercent()
        elif( self.Tank < self.MinimumWater ):
            self.replenish( 0.05 * NormalizedTime)
            self.TankReplenshing = True
            self.updatePercent()
        elif( self.Tank > self.MinimumWater ):
            self.TankReplenishing = False
            self.updatePercent()
        #endif
    #enddef()
    
    def deplete(self, amount = 0.005):
        if(self.TankReplenishing is True ):
            return
        elif(self.UnlimitedWater is True ):
            return
        #endif
        
        
        self.Tank -= amount 
        
        if(self.Tank < 0):
            self.Tank = 0
            self.TankReplenishing = True
        #endif
        
        self.updatePercent()
    #enddef()
    
    def replenish(self, amount = 0.01):
        self.Tank += amount 
        
        if(self.Tank > self.MaximumWater):
            self.Tank = self.MaximumWater
        #endif
        
        self.updatePercent()
    #enddef
    
    def percentLeft(self):
        return self.updatePercent()
    #enddef()
    
    def ToggleUnlimitedWater(self):
        self.UnlimitedWater = not self.UnlimitedWater
        print("WaterTank: UnlimitedWater:", self.UnlimitedWater)
    
    def updatePercent(self):
        self.Percent = self.Tank * 100
        
        if( self.Tank <= 1 ):
            if self.DebugMode:
                print( "Remaining Water: ", self.Percent)
            #endif
            
            #player = self.Space.FindObjectByName("MainCharacter")
            #Sending Custom Message to HUDSpace                
            if self.DebugMode:
                print("WaterTank: sending event >>>", self.HUDSpace)
            #endif
            
            WaterTankEvent = Zero.ScriptEvent()
            
            WaterTankEvent.Percent = self.Percent
            WaterTankEvent.Tank    = self.Tank
            WaterTankEvent.isReplenishing = self.TankReplenishing
            WaterTankEvent.isUnlimitedWater = self.UnlimitedWater
            
            if self.Owner.HUDEventDispatcher:
                self.Owner.HUDEventDispatcher.DispatchHUDEvent("WaterTankEvent", WaterTankEvent)
            
            #if player:
                #player.UIGameHUD2.HUDSpace.DispatchEvent("WaterTankEvent", WaterTankEvent)
            #endif
        #endif
        
        return self.Percent
    #enddef()
    
    def isEmpty(self):
        if(self.TankReplenishing is True and self.DebugMode):
            print("WaterTank.isEmpty():Is replenishing")
            return True
        elif(self.Tank <= 0 or self.TankReplenishing is True):
            return True
        else:
            return False
        #endif
    #enddef()
    
    def isNotEmpty(self):
        if(self.TankReplenishing is True):
            return False
        elif(self.Tank >= 0 and self.TankReplenishing is False):
            return True
        else:
            return False
        #endif
    #enddef
    

Zero.RegisterComponent("WaterTank", WaterTank)
