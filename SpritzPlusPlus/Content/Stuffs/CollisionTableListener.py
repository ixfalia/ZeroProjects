import Zero
import Events
import Property
import VectorMath

Vec3 = VectorMath.Vec3

class CollisionTableListener:
    def Initialize(self, initializer):
        Zero.Connect( self.Owner, "OnCollectibleAndPlayer", self.onCollectibleAndPlayer )
        Zero.Connect( self.Owner, "OnPlayerAndGoal", self.onPlayerAndGoal )
        Zero.Connect( self.Owner, "OnPlayerAndPool", self.onPlayerAndPool )
        Zero.Connect( self.Owner, "OnPlayerAndPoolPersist", self.onPlayerAndPoolPersist )
        Zero.Connect( self.Owner, "OnPlayerAndPoolEnd", self.onPlayerAndPoolEnd )
    #enddef()
    
    def onCollectibleAndPlayer(self, Event):
        pass
    #enddef()
    
    def onPlayerAndGoal(self, Event):
        print("GOAL!")
    #enddef()
    
    def onPlayerAndPool(self,Event):
        self.Owner.GravityEffect.Active = False
        self.Owner.GamepadController.Floating = True
            #used to make player float off ground while in water
        self.Owner.DynamicController.OnGround = False 
    #enddef()
    
    def onPlayerAndPoolPersist(self, Event):
        #self.Owner.DynamicController.ApplyForce(Vec3(0,0.5,0))
        self.Owner.DynamicController.OnGround = False
        self.Owner.WaterTank.replenish( 0.01 )
    #enddef
    
    def onPlayerAndPoolEnd(self, Event):
        self.Owner.GravityEffect.Active = True
        self.Owner.GamepadController.Floating = False
    #enddef
    
#end class

Zero.RegisterComponent("CollisionTableListener", CollisionTableListener)