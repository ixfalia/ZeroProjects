import Zero
import Events
import Property
import VectorMath
import Action
import random

Vec3 = VectorMath.Vec3

CollectibleList = ["twinkle", "replenish", "bubble", "coin"]
Collectibles = Property.DeclareEnum("Collectibles", CollectibleList)

class Collectible:
    DebugMode = Property.Bool( default = False )
    Type = Property.Enum(default = Collectibles.twinkle, enum = Collectibles)
    Type2 = Property.Enum
    PrizeStrength = Property.Float( default = 0.1 )
    Timing = Property.Float(default = 2)
    Lifetime = Property.Float(default = 0.0)
    Blinking = Property.Bool(default = True)
    BlinkDuration = Property.Float(default = 1.5)
    BlinkNumber = Property.Uint(default = 4)
    
    respawnOnEvent =  Property.String()
    
    timer = 0
    enoughTime = True
    
    def Initialize(self, initializer):
        Zero.Connect( self.Owner, Events.CollisionStarted, self.onCollision)
        #Zero.Connect( self.Owner, "OnCollectibleAndPlayer", self.onCollectibleAndPlayer)
        
        
        if not self.Lifetime <= 0:
            self.setLifetime()
        
        if self.Timing >= 0:
            Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        
        if not self.respawnOnEvent == "":
            Zero.Connect(self.Space, self.respawnOnEvent, self.onEvent)
        
        if self.DebugMode:
            print("Collectible.Initialize()")
        
        self.isTransparent = False
    #enddef()
    
    def onUpdate(self, Event):
        self.timer += Event.Dt
        return
        
        if self.timer >= self.Timing:
            if self.Type == "replenish" and not self.enoughTime:
                self.enoughTime = True
                self.Owner.Sprite.Color = VectorMath.Vec4(1,1,1,1)
                self.timer = 0
        #endif
        
        #if self.Owner.Transform.Translation.z > 0:
        #    self.Owner.Transform.Translation *= VectorMath.Vec3(1,1,0)
        
        #player = Space.FindObjectByName("MainCharacter")
        
        #if player:
            #player.HUDEventDispatcher()
    #enddef()
    
    def onCollectibleAndPlayer(self, Event):
        if self.DebugMode:
            print("Collectible.onCollectibleAndPlayer()")
    #enddef()
    
    def onCollision(self, CollisionEvent):
        other = CollisionEvent.OtherObject
        
        if not other:
            return
        
        if(other.Player):
            if( self.Type == "twinkle" ):
                self.Twinkle(other)
                other.SoundEmitter.PlayCue("Coin")
                TwinkleEvent = Zero.ScriptEvent()
                self.Space.DispatchEvent("TwinkleGet", TwinkleEvent)
                self.Owner.Destroy()
            elif( self.Type == "replenish" and self.enoughTime):
                #print("Collectible.onCollision(): Replenish Ding!")
                self.Replenish(other)
                other.SoundEmitter.PlayCue("Bubble")
                ReplenishEvent = Zero.ScriptEvent()
                self.Space.DispatchEvent("ReplenishGet", ReplenishEvent)
                self.Owner.Sprite.Color = VectorMath.Vec4(0.6, 0.6, 0.6, 0.75)
                self.enoughTime = False
                seq = Action.Sequence(self.Owner)
                Action.Delay(seq, self.Timing)
                Action.Call(seq, self.bubbleBack)
                
                self.Timer = 0
            elif( self.Type == "coin" ):
                print("coinget")
                self.Coin(other)
                
                CoinEvent = Zero.ScriptEvent()
                other.SoundEmitter.PlayCue("Coin")
                self.Space.DispatchEvent("CoinGet", CoinEvent)
                self.Owner.Destroy()
            #endif
            
            if self.DebugMode:
                print("Collectible Get! Type:", self.Type)
            
            #self.Owner.Destroy()
        elif(other.WaterSpin):
            if(other.WaterSpin.isUsed):
                return
        else:
            self.Owner.SphereCollider.Ghost = False
    #enddef
    
    def Twinkle(self, other):
        if( other.PointsCounter):
            other.PointsCounter.AddPoints(self.PrizeStrength)
            other.WaterTank.replenish(0.075)
        #endif
    #enddef()
    
    def Replenish(self, other):
        other.WaterTank.replenish( self.PrizeStrength )
    #enddef()
    
    def Coin(self, other):
        other.PointsCounter.AddPoints(self.PrizeStrength)
    
    def setLifetime(self):
        sequence = Action.Sequence(self.Owner)
        
        if not self.Lifetime <= 0:
            Action.Delay(sequence, self.Lifetime+random.random())
        
        if self.Blinking:
            self.setBlinking(sequence)
        
        Action.Call(sequence, self.Owner.Destroy)
    #end setLifetime()
    
    def setBlinking(self, sequence):
        timeslice = self.BlinkDuration / (self.BlinkNumber*2)
        
        Action.Call(sequence, self.toggleVisible)
        
        for i in range(0, self.BlinkNumber):
            nuSlice = timeslice# * (0.01+random.random())
            Action.Delay(sequence, nuSlice)
            Action.Call(sequence, self.toggleVisible)
            Action.Delay(sequence, nuSlice)
            Action.Call(sequence, self.toggleVisible)
        #endfor
    #end setBlinking()
    
    def toggleVisible(self):
        #self.Owner.Sprite.Visible = not self.Owner.Sprite.Visible
        self.isTransparent = not self.isTransparent
        if self.isTransparent:
            self.Owner.Sprite.Color *= VectorMath.Vec4(1,1,1,0.35)
        else:
            self.Owner.Sprite.Color = VectorMath.Vec4(1,1,1,1)
    
    def onEvent(self, eEvent):
        self.enoughTime = True
        self.Owner.Sprite.Color = VectorMath.Vec4(1,1,1,1)
    
    def bubbleBack(self):
        self.enoughTime = True
        self.Owner.Sprite.Color = VectorMath.Vec4(1,1,1,1)
#endclass

Zero.RegisterComponent("Collectible", Collectible)