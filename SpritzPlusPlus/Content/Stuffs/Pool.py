import Zero
import Events
import Property
import VectorMath

Vec3 = VectorMath.Vec3

class Pool:
    Floatiness = Property.Float(default = 0.5)
    
    def Initialize(self, initializer):        
        Zero.Connect(self.Owner, Events.CollisionPersisted, self.onCollisionPersist)
        
    def onCollisionPersist(self, CollisionEvent):
        other = CollisionEvent.GetOtherObject(self.Owner)
        
        
        if( other.Water ):
            return
        
        if( other.RigidBody and not other.RigidBody.Static ):
            other.RigidBody.ApplyForce( Vec3( 0, self.Floatiness, 0 ) )
            
        if(other.RigidBody and other.Collectible):
            other.RigidBody.ApplyForce( Vec3( 0, self.Floatiness, 0 ) )
#endclass
Zero.RegisterComponent("Pool", Pool)