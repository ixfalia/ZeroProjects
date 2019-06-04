import Zero
import Events
import Property
import VectorMath
Vec3 = VectorMath.Vec3

class Bullet:
    DebugMode = Property.Bool(default = False)
    BulletType = Property.String(default = "BasicBullet")
    TimeToLive = Property.Float(default = 2)
    
    isHoming = Property.Bool(default = False)
    Timer = 0
    isUsed = Property.Bool(default = False)
    currentTarget = None
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.onCollision)
        
    
    def onCollision(self, Event):
        other = Event.GetOtherObject(self.Owner)
        
        if other.Bullet or other.BasicPowerup or other.PlayerController:
            return
        
        if not other.PlayerController and not other.BasicPowerup or not other.Bullet:
            self.Owner.Destroy()
    
    def onUpdate(self, Event):
        if self.isUsed:
            return
        
        self.Owner.Transform.Translation *= Vec3(1, 1, 0)
        
        self.Timer += Event.Dt
        
        if self.isHoming:
            self.FindTarget()
        
        if self.Timer >= self.TimeToLive:
            self.Death()
            self.Timer = 0
    #enddef
    
    def getDamage(self):
        if self.BulletType == "BasicBullet":
            return 30
            
    def Death(self):
        self.isUsed = True
        self.Owner.Destroy()
    
    def FindTarget(self):
        Target = self.checkForTarget()
        
        if not Target == self.currentTarget:
            if self.DebugMode:
                print("Bullet.onUpdate() Target Changed to", Target.Name)
            self.currentTarget = Target
            self.Owner.FollowTarget.ChangeTarget(Target.Name)
    
    def checkForTarget(self):
        pass

Zero.RegisterComponent("Bullet", Bullet)