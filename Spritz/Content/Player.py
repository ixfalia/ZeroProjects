import Zero
import Events
import Property
import VectorMath

import Action

class Player:
    DeathLength =  Property.Float(default = 3.0)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "onPlayerAndDeathMaker", self.onDeath)
        Zero.Connect(self.Owner, "PlayerDeath", self.onDeath)
        Zero.Connect(self.Owner, "LevelEnd", self.onLevelEnd)
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        Zero.Connect(self.Space, "myGamepadEvent", self.onGamepad)
        Zero.Connect(self.Space, Events.KeyDown, self.onKey)
        
        self.deathTimer = 0
        self.inDeath = False
        self.DeathFallStrength = 10
    #def initialize()
    
    def onUpdate(self, uEvent):
        #print("Player.onUpdate():",self.deathTimer)
        #self.deathTimer += uEvent.Dt
        #print(self.deathTimer)
        
        #if self.deathTimer >= self.DeathLength:
            #print("Player.onUpdate(): no Longer in Death", self.deathTimer, self.DeathLength)
        #    self.deathTimer = 0.0
        #    self.inDeath = False
        velocity = self.Owner.RigidBody.Velocity
        velocityLimit = 20.0
        if velocity.y >= velocityLimit:
            self.Owner.RigidBody.Velocity = VectorMath.Vec3(velocity.x, velocityLimit, velocity.z)
    
    def onGamepad(self, gEvent):
        pass
    
    def onKey(self, kEvent):
        if kEvent.Key == Keys.Tilde:
            #enter cheat state
            pass
        
        if kEvent.Key == Keys.Minus:
            pass
            e = Zero.ScriptEvent()
        
    
    def onDeath(self, dEvent):
        if not self.inDeath:
            print("Player.onUpdate(): inDeath now === True")
            
            self.inDeath = True
            #self.deathTimer = 0.0
            #raise
            self.Owner.GamepadController.disable()
            self.disableCamera()
            self.Owner.SoundManager.Play("Death")
            self.Owner.CapsuleCollider.Ghost = True
            self.Owner.RigidBody.Velocity = VectorMath.Vec3()
            self.Owner.RigidBody.ApplyLinearVelocity(VectorMath.Vec3(0,15,0))
            self.Owner.GravityEffect.Strength = self.DeathFallStrength
            self.Owner.Sprite.SpriteSource = "DennisDeath"
            
            deathEvent = Zero.ScriptEvent()
            self.Space.DispatchEvent("DeathEvent", deathEvent)
            
            transl = self.Owner.Transform.Translation
            self.Owner.Transform.Translation = VectorMath.Vec3(transl.x,transl.y, 0.1)
            
            sequence = Action.Sequence(self.Owner)
            Action.Call(sequence, self.Owner.MovementController.Jump, (200))
            
            Action.Delay(sequence, self.DeathLength)
            Action.Call(sequence, self.onRespawn)
            Action.Call(sequence, self.Owner.Teleport.GoToCheckpoint)
    #end onDeath()
    
    def disableCamera(self):
        camera = self.Space.FindObjectByName("myCamera")
        
        camera.CameraController.FreezeCamera(True)
    
    def enableCamera(self):
        camera = self.Space.FindObjectByName("myCamera")
        
        camera.CameraController.FreezeCamera(False)
    
    def onRespawn(self):
        print("Player.onRespawn(): Player Respawned")
        self.Owner.CapsuleCollider.Ghost = False
        self.enableCamera()
        self.Owner.GamepadController.enable()
        self.Owner.GravityEffect.Strength = 1
        self.Owner.Sprite.SpriteSource = "MainCharacter"
        self.inDeath = False
        
        if self.Owner.WaterTank:
            TankSet = self.Owner.WaterTank.MaximumWater * 0.35
            if self.Owner.WaterTank.Tank < TankSet:
                self.Owner.WaterTank.Tank = TankSet
        #self.deathTimer = 0.0
        
        respawnEvent = Zero.ScriptEvent()
        self.Space.DispatchEvent("RespawnEvent", respawnEvent)
        
        transl = self.Owner.Transform.Translation
        self.Owner.Transform.Translation *= VectorMath.Vec3(transl.x,transl.y,0)
        
        #print("unGhost()")
        pass
    
    def onLevelEnd(self, lEvent):
        pass

Zero.RegisterComponent("Player", Player)