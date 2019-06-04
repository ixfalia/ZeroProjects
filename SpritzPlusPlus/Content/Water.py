import Zero
import Events
import Property
import VectorMath
import TimerManager
import Action

Timer = TimerManager.Timer

class Water:
    Lifetime = 0
    Lifelimit = Property.Float( default = 1 )
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.onCollisionStarted )
        
        #self.Space.TimerManager.addTimer( "water", self.Lifelimit, self.Owner.Destroy )
    #enddef
    
    def __del__(self):
        ("Water deleted.")
        pass
    #enddef()
    
    def onUpdate(self, Event):
        self.Lifetime += Event.Dt
        
        if( self.Lifetime > self.Lifelimit ):
            self.Owner.Destroy()
        #endif
    #enddef
    
    def onCollisionStarted(self, CollisionEvent):
        other = CollisionEvent.OtherObject
        
        if not other:
            print("other not detected")
            return
        #endif
        
        if( other.Water ):
            #return
            pass
        elif( other.WaterTank ):
            #return
            pass
        else:
            self.Lifetime += 0.3
            self.Owner.SphereCollider.Ghost = False
        #endif
    #enddef()
    
#endclass

Zero.RegisterComponent("Water", Water)