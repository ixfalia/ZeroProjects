import Zero
import Events
import Property
import VectorMath
import random

Vec3 = VectorMath.Vec3
Vec4 = VectorMath.Vec4
class BasicEnemy:
    DebugMode = Property.Bool(default = False)
    OriginalPosition = Property.Vector3(default = VectorMath.Vec3())
    EnemyDrops = Property.Resource("WeightedTable")
    ContactDamage = Property.Float(default = 25)
    VisionRange = Property.Float(default = 1024)
    OriginalColor = Property.Vector4(default = Vec4())
    
    def Initialize(self, initializer):
        #print("initialized")
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.onCollision)
        Zero.Connect(self.Owner, "HealthEvent", self.onHealth)
        
        self.currentTarget = self.findTarget()
        self.Owner.FollowTarget.ChangeTarget(self.currentTarget.Name)
        self.Owner.Transform.Translation *= Vec3(1,1,0)
        
        self.OriginalColor = self.Owner.Sprite.Color
    
    def onUpdate(self, Event):
        self.Owner.RigidBody.Velocity *= 0
        self.Owner.Transform.Translation *= Vec3(1,1,0)
        
        Target = self.findTarget()
        if not Target == self.currentTarget:
            if self.DebugMode:
                print("BasicEnemy.onUpdate() Target Changed to", Target.Name)
            self.currentTarget = Target
            self.Owner.FollowTarget.ChangeTarget(Target.Name)
    
    def onCollision(self, Event):
        other = Event.GetOtherObject(self.Owner)
        
        if other.Bullet:
            if self.DebugMode:
                print("BasicEnemy.onCollision(): Bullet Detected")
            self.takeDamage(other.Bullet.getDamage())
            other.Destroy()
        
        if other.Beacon:
            if self.DebugMode:
                print("BasicEnemy.onCollision() Beacon Colliding")
            other.Health.takeDamage(self.ContactDamage)
            self.Owner.Destroy()
        
        if other.PlayerController:
            if self.DebugMode:
                print("BasicEnemy.onCollision() Player Collision")
            other.Health.takeDamage(self.ContactDamage)
            self.Owner.Destroy()
    #end
    
    def onHealth(self, Event):
        if self.DebugMode:
            print("BasicEnemy.onHealth():")
        if Event.CurrentHealth <= 0:
            pass
            #WeightedTable = Zero.GetResource(self.EnemyDrops)
            #ArchetypeName = WeightedTable.Sample(random.random(),random.random())
            
            #if(ArchetypeName != "Nothing"):
                #self.Space.CreateAtPosition(ArchetypeName, self.Owner.Transform.Translation)
            
            #power = self.Space.CreateAtPosition("BasicPowerup", self.Owner.Transform.Translation)
            #power.RigidBody.ApplyLinearVelocity(Vec3(0, -10, 0))
            #power.Transform.Scale *= 1
            death = Zero.ScriptEvent()
            self.Owner.DispatchEvent("OnDeath", death)
            
            death = Zero.ScriptEvent()
            self.Owner.DispatchEvent("DropPrize", death)
            
            print(self.Owner.Name, "Died")
            
            player = self.Space.FindObjectByName("MainCharacter")
            player.SoundEmitter.PlayCue("EnemyDeath")
            self.Owner.Destroy()
    #end
    
    def takeDamage(self, damage = 10 ):
        #self.Owner.Timer.registerTimer("DamageBlink", 0.1, self.setRegularColor, False)
        self.setDamageColor()
        self.Owner.Health.takeDamage(damage)
    
    def setDamageColor(self):
        oc = self.OriginalColor
        self.Owner.Sprite.Color = VectorMath.Vec4(oc.x,self.Owner.Health.normalizedHealth()*oc.y,self.Owner.Health.normalizedHealth()*oc.z,1)
    
    def setRegularColor(self):
        self.Owner.Sprite.Color = Vec4(0.8,0.8,0.8)
    
    def getDistance(self, other):
        if not other:
            return None
        
        pos = self.Owner.Transform.Translation
        otherpos = other.Transform.Translation
        
        distance = (pos.x - otherpos.x)*(pos.x - otherpos.x) + (pos.y - otherpos.y)*(pos.y - otherpos.y)
        
        return distance
    
    def findTarget(self):
        beacon1 = self.Space.FindObjectByName("Beacon1")
        beacon2 = self.Space.FindObjectByName("Beacon2")
        player = self.Space.FindObjectByName("MainCharacter")
        
        closest = self.getDistance(beacon1)
        target = beacon1
        
        
        if beacon2 and closest > self.getDistance(beacon2):
            closest = self.getDistance(beacon2)
            target = beacon2
            
        if not beacon2.Beacon.isActive:
            closest = self.getDistance(beacon1)
            target = beacon1
        
        if not beacon1.Beacon.isActive:
            closest = self.getDistance(beacon2)
            target = beacon2
        
        if self.getDistance(beacon1) == self.getDistance(beacon2):
            random.seed(None)
            result = random.randint(0,1)
            
            if result == 0:
                target = beacon1
            else:
                target = beacon2
        #endif
        
        if not beacon1.Beacon.isActive and not beacon2.Beacon.isActive:
            closest = self.getDistance(player)
            target = player
        
        playerDist = self.getDistance(player)
        #print("findTarget()", playerDist)
        eve = Zero.ScriptEvent()
        eve.String = str(playerDist)
        player.UIMaker.DispatchToHUDSpace("PlayerPos", eve)
        
        if player and closest > self.getDistance(player) and self.getDistance(player) < self.VisionRange:
            closest = self.getDistance(player)
            target = player
        
        if self.DebugMode:
            #print( "BasicEnemy.findTarget() Target is: ", target.Name)
            pass
        return target
    #enddef

Zero.RegisterComponent("BasicEnemy", BasicEnemy)