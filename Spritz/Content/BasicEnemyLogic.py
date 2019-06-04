import Zero
import Events
import Property
import VectorMath

class BasicEnemyLogic:
    DamageTimer = Property.Float(default = 2.0)
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.onCollision)
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        self.Timer = 0
        self.isDamageable = True
    #END INIT()
    
    def onCollision(self, collisionEvent):
        other = collisionEvent.OtherObject
        
        if other.SphereCollider:
            pass
        
        if other.Water:
            if self.isDamageable:
                self.Owner.RigidBody.ApplyLinearVelocity(VectorMath.Vec3(5,3,0))
                self.isDamageable = False
    
    def onUpdate(self, uEvent):
        self.Timer += uEvent.Dt
        
        if self.Timer >= self.DamageTimer:
            self.Timer = 0
            self.isDamageable = True

Zero.RegisterComponent("BasicEnemyLogic", BasicEnemyLogic)