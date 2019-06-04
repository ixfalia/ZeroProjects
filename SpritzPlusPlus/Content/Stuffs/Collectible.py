import Zero
import Events
import Property
import VectorMath
import Action

Vec3 = VectorMath.Vec3

class Collectible:
    DebugMode = Property.Bool( default = False )
    Type =  Property.String( default = "" )
    PrizeStrength = Property.Float( default = 0.1 )
    
    timer = 0
    enoughTime = False
    
    def Initialize(self, initializer):
        Zero.Connect( self.Owner, Events.CollisionStarted, self.onCollision)
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        #Zero.Connect( self.Owner, "OnCollectibleAndPlayer", self.onCollectibleAndPlayer)
    #enddef()
    
    def onUpdate(self, Event):
        self.timer += Event.Dt
        
        if self.timer >= 2:
            if self.Type == "replenish":
                self.enoughTime = True
                self.Owner.Sprite.Color = VectorMath.Vec4(1,1,1,1)
            self.timer = 0
        #endif
    #enddef()
    
    def onCollectibleAndPlayer(self, Event):
        if self.DebugMode:
            print("Collectible.onCollectibleAndPlayer()")
    #enddef()
    
    def onCollision(self, CollisionEvent):
        other = CollisionEvent.GetOtherObject(self.Owner)
        
        if not other:
            return
        
        if(other.PlayerController):
            if( self.Type == "twinkle" ):
                self.Twinkle(other)
                other.SoundEmitter.PlayCue("Coin")
                TwinkleEvent = Zero.ScriptEvent()
                self.Space.DispatchEvent("TwinkleGet", TwinkleEvent)
                self.Owner.Destroy()
            elif( self.Type == "replenish" and self.enoughTime):
                self.Replenish(other)
                other.SoundEmitter.PlayCue("Bubble")
                ReplenishEvent = Zero.ScriptEvent()
                self.Space.DispatchEvent("ReplenishGet", ReplenishEvent)
                self.Owner.Sprite.Color = VectorMath.Vec4(0.6, 0.6, 0.6, 0.6)
                
                self.enoughTime = False
                self.Timer = 0
            elif( self.Type == "coin" ):
                print("coinget")
                self.Coin(other)
                
                CoinEvent = Zero.ScriptEvent()
                other.SoundEmitter.PlayCue("Coin")
                self.Space.DispatchEvent("CoinGet", CoinEvent)
                self.Owner.Destroy()
            #endif
            
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
#endclass

Zero.RegisterComponent("Collectible", Collectible)