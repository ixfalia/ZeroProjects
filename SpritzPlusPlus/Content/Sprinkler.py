import Zero
import Events
import Property
import VectorMath

import Action

Vec3 = VectorMath.Vec3

class Sprinkler:
    DebugMode = Property.Bool(default = False)
    SpraySpeed = Property.Float(default = 0.025)
    AutoSpray = Property.Bool(default = False)
    SprayDuration = Property.Float(default = 0.5)
    SprayDelay = Property.Float(default = 1.5)
    SprayInDirection = Property.Vector2(default = VectorMath.Vec2(1,1))
    
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        
        self.SprayTimer = 0.0
        self.AutoTimer = 0.0
        self.canSpray = False
        self.AutoWaiting = False
    
    def onUpdate(self, updateEvent):
        self.SprayTimer += updateEvent.Dt
        
        if self.SprayTimer >= self.SpraySpeed:
            self.canSpray = True
            self.SprayTimer = 0.0
        
        if self.AutoSpray and not self.AutoWaiting:
            self.AutoTimer += updateEvent.Dt
            self.ShootStick(self.SprayInDirection.normalized())
        
        if self.AutoTimer >= self.SprayDuration:
            self.AutoTimer = 0
            self.AutoWaiting = True
            
            seq = Action.Sequence(self.Owner)
            Action.Delay(seq, self.SprayDelay)
            Action.Call(seq, self.wait)
    
    def wait(self):
        self.AutoWaiting = False
    def Shoot(self, waterPressure = None):
        
        if waterPressure:
            spritz = self.ShootStick(Vec3(waterPressure, waterPressure, waterPressure))
        else:
            spritz = self.ShootStick(Vec3(0.7,0.7,0))
        
        if not spritz:
            print("bul not found")
    #enddef Shoot()
    
    def ShootStick(self, Rightstick):
        if( self.Owner.WaterTank.isEmpty() ):
            return
        #endif
        
        if not self.canSpray:
            return
        
        if self.Owner.SprayFlower:
            self.Owner.SoundManager.Play("Spray")
        
        self.Owner.WaterTank.deplete(0.01)
        spritz = self.Space.CreateAtPosition("WaterSpray", self.Owner.Transform.Translation + Vec3(0, 1, 0))
        #spritz.Transform.Translation = self.Owner.Transform.Translation
        spritz.RigidBody.Velocity = Rightstick * 15
        
        if(self.Owner.MovementController):
            VelocityLimit = 5
                #if the right stick is pointed down apply some sort of pushing force
            if(Rightstick.y < -self.Owner.GamepadController.deadzone and not self.Owner.WaterTank.isEmpty()):
                if(self.Owner.RigidBody.Velocity.y < VelocityLimit):
                    v = self.Owner.RigidBody.Velocity
                    self.Owner.RigidBody.Velocity = Vec3(v.x, min( v.y + Rightstick.y * -0.55, VelocityLimit ), v.z )
                    #self.Owner.RigidBody.ApplyLinearVelocity( Vec3(0, Rightstick.y * -0.55, 0) )
                    self.Owner.MovementController.Flutter(Rightstick.y * 0.1)
            else:
                if self.DebugMode:
                    print("Sprinkler.ShootStick(): jumpended")
                    
                self.Owner.MovementController.EndJump()
            #endif
        #endif
        
        if not spritz:
            print("bul not found")
        #endif
        
        self.canSpray = False
        return spritz
    #endef ShootStick()
    
    def shootUnlimited(self, Rightstick):
        self.Owner.WaterTank.deplete(0.01)
        spritz = self.Space.CreateAtPosition("WaterSpray", self.Owner.Transform.Translation + Vec3(0, 1, 0))
        #spritz.Transform.Translation = self.Owner.Transform.Translation
        spritz.RigidBody.Velocity = Rightstick * 15
        
        if(self.Owner.MovementController):
            VelocityLimit = 5
                #if the right stick is pointed down apply some sort of pushing force
            if(Rightstick.y < -self.Owner.GamepadController.deadzone and not self.Owner.WaterTank.isEmpty()):
                if(self.Owner.RigidBody.Velocity.y < VelocityLimit):
                    v = self.Owner.RigidBody.Velocity
                    self.Owner.RigidBody.Velocity = Vec3(v.x, min( v.y + Rightstick.y * -0.55, VelocityLimit ), v.z )
                    #self.Owner.RigidBody.ApplyLinearVelocity( Vec3(0, Rightstick.y * -0.55, 0) )
                    self.Owner.MovementController.Flutter(Rightstick.y * 0.1)
            else:
                if self.DebugMode:
                    print("Sprinkler.ShootStick(): jumpended")
                    
                self.Owner.MovementController.EndJump()
                #endif
            #endif
            
            if not spritz:
                print("bul not found")
#endclass

Zero.RegisterComponent("Sprinkler", Sprinkler)