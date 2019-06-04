import Zero
import Events
import Property
import VectorMath
import random
import Action

Vec3 = VectorMath.Vec3

class FlowerSpin:
    DebugMode = Property.Bool( default = False )
    AngularVelocity = Property.Float( default = 0.75 )
    SpinCount = Property.Float( default = 0 )
    SpinLimit = Property.Float( default = 1.5 )
    Windback = Property.Bool( default = False )
    SoundCue = Property.SoundCue()
    
    muteWindingSound = Property.Bool(default = False)
    
    isUsed = Property.Bool( default = False )
    ChubbyFlower = Property.Bool(default = False)
    position =  None
    
    def Initialize(self, initializer):
        #Zero.Connect(self.Owner, Events.CollisionStarted, self.onCollision)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.onCollisionPersisted)
        #Zero.Connect(self.Owner, Events.CollisionEnded, self.onCollisionEnd)
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        
        self.position = self.Owner.Transform.Translation
        self.position *= Vec3(1,1,0)
        self.position += Vec3(0,0,-1.1)
        #self.Owner.Transform.Translation *= Vec3(1,1,0)
        #self.Owner.Transform.Translation += Vec3(0,0,-1)
        
        self.blocking = False
        self.playingSound = False
        
        player = self.Space.FindObjectByName("MainCharacter")
        
        if player and not self.ChubbyFlower:
            if player.HUDEventDispatcher:
                if self.DebugMode:
                    print("WaterSpin.Initialize()")
                flowerEvent = Zero.ScriptEvent()
                
                player.HUDEventDispatcher.DispatchHUDEvent("FlowerCountEvent", flowerEvent)
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
            
            if not self.SoundCue.Name == "DefaultCue":
                self.playSound()
            pass
        #else:
        other = Event.OtherObject
        
        if other.Water and self.isUsed and not self.blocking and not self.ChubbyFlower:
            self.blocking = True
            
            self.Owner.PutAnotherSprite.CreateNewSprite("FullFlowerHappy")
            
            seq = Action.Sequence(self.Owner)
            Action.Delay(seq, 0.5)
            Action.Call(seq, self.unBlock)
            Action.Call(seq, self.reset)
            
            #self.Owner.Sprite.CurrentFrame = 1
    #enddef
    
    def playSound(self):
        self.WaitTime = 0.25
        
        if self.muteWindingSound:
            return
        
        if not self.playingSound:
            self.playingSound = True
            self.Owner.SoundEmitter.Pitch += self.SpinCount / (self.SpinLimit*2.5)
            self.Owner.SoundEmitter.PlayCue("FlowerWind")
            
            seq = Action.Sequence(self.Owner)
            Action.Delay(seq, self.WaitTime)
            Action.Call(seq, self.resetSound)
    
    def resetSound(self):
            self.playingSound = False
    
    
    def unBlock(self):
        self.blocking = False
    
    def reset(self):
        self.Owner.PutAnotherSprite.CreateNewSprite("FlowerFace")
    
    def onCollisionEnd(self, Event):
        other = Event.OtherObject
        
        if other.Water and self.isUsed:
            self.Owner.PutAnotherSprite.CreateNewSprite("FlowerFace")
        
    
    def onUpdate(self, Event):
        self.Owner.Transform.Translation = self.position
        self.Owner.RigidBody.Velocity = VectorMath.Vec3()
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
        #FlowerEvent.Level = Zero.Ga
        
            #this function is used to edit the behavior of the flower spin remotely
        def myFunc(otherSelf):
            otherSelf.Owner.Rotator.RotatorZ = 1.5
            otherSelf.Owner.Rotator.SwayPeriod = 0.45
        #end myFunc()
        
        if self.ChubbyFlower:
            self.Owner.ChangeColor.ColorShifting = True
        
        FlowerEvent.fn =  myFunc
        
        if not self.SoundCue.Name == "DefaultCue":
            #seq = Action.Sequence(self.Owner)
            self.Owner.SoundEmitter.Pitch = 1
            self.Owner.SoundEmitter.PlayCue("Flower")
            #Action.Delay(seq, 0.4)
            #Action.Call(seq, self.Owner.SoundEmitter.PlayCue)
        
        player = self.Space.FindObjectByName("MainCharacter")
        
        if player:
            print("FlowerSpin.prizeSplode(): Sending FlowerGet to HUD")
            if player.HUDEventDispatcher and not self.ChubbyFlower:
                player.HUDEventDispatcher.DispatchHUDEvent("FlowerGet", FlowerEvent)
        self.Owner.DispatchEvent("FlowerGet", FlowerEvent)
        self.Space.DispatchEvent("FlowerGet", FlowerEvent)
        #Zero.Game.DispatchEvent("FlowerGet", FlowerEvent)
        #endfor
    #enddef()
#end class

Zero.RegisterComponent("FlowerSpin", FlowerSpin)