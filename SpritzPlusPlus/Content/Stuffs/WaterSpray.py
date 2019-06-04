import Zero
import Events
import Property
import VectorMath

Vec3 = VectorMath.Vec3

class Sprinkler:
    DebugMode = Property.Bool(default = False)
    def Initialize(self, initializer):
        pass
        
    def Shoot(self):
        spritz = self.ShootStick(Vec3(0.7,0.7,0))
        
        #if(self.Owner.Sprite.FlipX is true):
        
        if not spritz:
            print("bul not found")
    #enddef Shoot()
    
    def ShootStick(self, Rightstick):
        if( self.Owner.WaterTank.isEmpty() ):
            return
        #endif
        
        self.Owner.WaterTank.deplete(0.01)
        spritz = self.Space.CreateAtPosition("WaterSpray", self.Owner.Transform.Translation + Vec3(0, 1, 0))
        #spritz.Transform.Translation = self.Owner.Transform.Translation
        spritz.RigidBody.Velocity = Rightstick * 15
        
        
        if(self.Owner.PlayerController):
            VelocityLimit = 5
                #if the right stick is pointed down apply some sort of pushing force
            if(Rightstick.y < -self.Owner.GamepadController.deadzone and not self.Owner.WaterTank.isEmpty()):
                if(self.Owner.RigidBody.Velocity.y < VelocityLimit):
                    v = self.Owner.RigidBody.Velocity
                    self.Owner.RigidBody.Velocity = Vec3(v.x, min( v.y + Rightstick.y * -0.55, VelocityLimit ), v.z )
                    #self.Owner.RigidBody.ApplyLinearVelocity( Vec3(0, Rightstick.y * -0.55, 0) )
                    self.Owner.DynamicController.AttemptJump(Rightstick.y * 0.1)
                    self.Owner.DynamicController.OnGround = False
            else:
                if self.DebugMode:
                    print("Sprinkler.ShootStick(): jumpended")
                    
                self.Owner.DynamicController.OnGround = True
                self.Owner.DynamicController.EndJump()
            #endif
        #endif
        
        if not spritz:
            print("bul not found")
        #endif
        return spritz
    #endef ShootStick()
#endclass

Zero.RegisterComponent("Sprinkler", Sprinkler)