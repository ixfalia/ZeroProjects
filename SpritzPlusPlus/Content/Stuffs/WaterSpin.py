import Zero
import Events
import Property
import VectorMath
import random
import Action

Vec3 = VectorMath.Vec3

class WaterSpin:
    DebugMode = Property.Bool( default = False )
    AngularVelocity = Property.Float( default = 0.4 )
    SpinCount = Property.Float( default = 0 )
    SpinLimit = Property.Float( default = 3 )
    Windback = Property.Bool( default = True )
    SoundCue = Property.String( default = "" )
    
    isUsed = Property.Bool( default = False )
    position =  None
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.onCollision)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.onCollisionPersisted)
        #Zero.Connect(self.Owner, Events.CollisionEnded, self.onCollisionEnd)
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
            #self.Owner.PutAnotherSprite.CreateNewSprite("FullFlowerHappy")
            #self.Owner.Transform.Scale *= Vec3(1.01,1.01,1.01)
    #enddef
    
    def onCollisionEnd(self, Event):
        other = Event.GetOtherObject(self.Owner)
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
        
        if not self.SoundCue == "":
            self.Owner.SoundEmitter.PlayCue(self.SoundCue)
        
        player = self.Space.FindObjectByName("MainCharacter")
        if player:
            if player.WaterTank:
                player.WaterTank.HUDSpace.DispatchEvent("FlowerGet", FlowerEvent)
        self.Owner.DispatchEvent("FlowerGet", FlowerEvent)
        self.Space.DispatchEvent("FlowerGet", FlowerEvent)
        #endfor
    #enddef()
#end class

Zero.RegisterComponent("WaterSpin", WaterSpin)