import Zero
import Events
import Property
import VectorMath
import random
import Action

Vec3 = VectorMath.Vec3

class WaterSpin:
    DebugMode = Property.Bool( default = False )
    AngularVelocity = Property.Float( default = 0.75 )
    SpinCount = Property.Float( default = 0 )
    SpinLimit = Property.Float( default = 1.5 )
    Windback = Property.Bool( default = False )
    SoundCue = Property.SoundCue()
    
    isUsed = Property.Bool( default = False )
    position =  None
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.onCollision)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.onCollisionPersisted)
        Zero.Connect(self.Owner, Events.CollisionEnded, self.onCollisionEnd)
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        
        self.position = self.Owner.Transform.Translation
        
    #endef()
        
    
    def onCollision(self, Event):
        self.Owner.Transform.Translation = self.position
        self.Owner.RigidBody.Velocity = Vec3()
    
    def onCollisionPersisted(self, Event):
        #print("Spin spin")
        self.Owner.Transform.Translation = self.position
        self.Owner.RigidBody.Velocity = Vec3()
        if not self.isUsed:
            self.Owner.RigidBody.ApplyAngularVelocity(Vec3(0,0,self.AngularVelocity))
        #else:
        other = Event.OtherObject
        
        if other.Water and self.isUsed:
            self.Owner.PutAnotherSprite.CreateNewSprite("FullFlowerHappy")
            #self.Owner.Sprite.CurrentFrame = 1
    #enddef
    
    def onCollisionEnd(self, Event):
        other = Event.OtherObject
        
        if other.Water and self.isUsed:
            self.Owner.PutAnotherSprite.CreateNewSprite("FlowerFace")
        
    
    def onUpdate(self, Event):
        self.Owner.Transform.Translation = self.position
        self.Owner.RigidBody.Velocity = Vec3()
        #print( self.Owner.Transform.Rotation.z )
        #print( self.Owner.RigidBody.AngularVelocity )
        
        velocity = self.Owner.RigidBody.AngularVelocity.z
        Pi = 6.2831
        
            #Turns the angular velocity into steps that I can keep track of
        self.SpinCount += (velocity*Event.Dt)/Pi
        
        if( self.DebugMode == True ):
            print(self.Owner.Name, " Spin Count: ",self.SpinCount)
        #endif
        
        if( self.SpinCount >= self.SpinLimit and not self.isUsed ):
            self.prizeSplode()
            self.isUsed = True
        #endif
        
        #self.Owner.RigidBody.
    #enddef
    
    def prizeSplode(self):
        if(self.Owner.Prizebox):
            self.Owner.Prizebox.prizeSplode()
        
        if(self.Owner.Key):
            self.Owner.Key.broadCastKey()
        
        print("flowerget")
        FlowerEvent = Zero.ScriptEvent()
        
            #this function is used to edit the behavior of the flower spin remotely
        def myFunc(otherSelf):
            otherSelf.Owner.Rotator.RotatorZ = 1.5
            otherSelf.Owner.Rotator.SwayPeriod = 0.45
        #end myFunc()
        
        FlowerEvent.fn =  myFunc
        
        if not self.SoundCue.Name == "DefaultCue":
            self.Owner.SoundEmitter.PlayCue(self.SoundCue)
        
        #endfor
    #enddef()
#end class

Zero.RegisterComponent("WaterSpin", WaterSpin)