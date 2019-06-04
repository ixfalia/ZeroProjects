import Zero
import Events
import Property
import VectorMath

Vec3 = VectorMath.Vec3
Vec4 = VectorMath.Vec2

class PlayerController:
    DebugMode = Property.Bool(default = False)
    Time = 0
    FireRate = Property.Float(default = 0.2)
    BulletSpeed = Property.Float(default = 30)
    
    xLim = Property.Float(default = 40)
    yLim = Property.Float(default = 40)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        Zero.Connect(self.Space, Events.LevelStarted, self.levelStart)
        Zero.Connect(self.Owner, "HealthEvent", self.onHealth)
        self.Owner.RigidBody.Static = True
        
    
    def levelStart(self,Event):
        self.Owner.LightTank.changeWeapon(0)
    
    def MoveInDirection(self, movement):
        self.Owner.Transform.Translation += 0.5* movement.normalized()
        
        transl = self.Owner.Transform.Translation
        
        if transl.x > self.xLim:
            xVal = self.xLim
        elif transl.x < -self.xLim:
            xVal = -self.xLim
        else:
            xVal = transl.x
        
        if transl.y > self.yLim:
            yVal = self.yLim
        elif transl.y < -self.yLim:
            yVal = -self.yVal
        else:
            yVal = transl.y
        
        self.Owner.Transform.Translation = Vec3(xVal, yVal, 0)
    #enddef
    
    def onUpdate(self,Event):
        self.Time += Event.Dt
        self.Owner.Transform.Translation *= Vec3(1,1,0)
    
    def onHealth(self, Event):
        if Event.CurrentHealth <= 0:
            HUD = self.Owner.UIMaker.getHUD()
            HUD.Destroy()
            self.Space.DestroyAllFromLevel()
            self.Space.LoadLevel("GameOver")
    
    def shiftColorRight(self):
        self.Owner.LightTank.shiftWeaponRight()
    
    def shiftColorLeft(self):
        self.Owner.LightTank.shiftWeaponLeft()
    
    def Fire(self, RightStick = None):
        if self.DebugMode:
            print( "PlayerController.Fire()" )
        
        if RightStick == None:
            velo = Vec3(0, 1, 0)
        else:
            #velo = RightStick
            velo = Vec3(0,1,0)
            pass
        
        if self.Time >= self.FireRate and self.Owner.LightTank.currentWeaponNotEmpty():
            weapon = self.Owner.LightTank.getCurrentWeapon()
            
            if weapon.Name == "Red":
                self.generateDoubleBullet()
                self.Owner.LightTank.depleteCurrent()
            elif weapon.Name == "Blue":
                self.generateDoubleBullet()
                self.generateDoubleBullet(Vec3(3,3,0), Vec3(1,1,0))
                self.generateDoubleBullet(Vec3(3,0,0), Vec3(1,0,0))
                self.generateDoubleBullet(Vec3(-3,3,0), Vec3(-1,1,0))
                self.Owner.LightTank.depleteCurrent()
                
                self.Owner.SoundEmitter.PlayCue("Splash")
            elif weapon.Name == "Green":
                self.generateDoubleBullet()
            else:
                self.generateDoubleBullet()
                self.Owner.LightTank.depleteCurrent()
                self.Owner.SoundEmitter.PlayCue("Shoot")
            #ENDIF
            
            
            self.Time = 0
        #enidf
        
        
        if not self.Owner.LightTank.currentWeaponNotEmpty():
            self.Owner.LightTank.changeWeapon(0)
    #enddef
    
    def generateBullet(self, positionOffset = Vec3(0,3,0), velocity = Vec3(0,1,0), bulletType = ""):
        weapon = None
        
        if bulletType == "":
            weapon = self.Owner.LightTank.getCurrentWeapon()
            bulletType = weapon.Bullet
        
        if type(bulletType) is int:
            weapon = self.Owner.LightTank.GetCertainWeapon(bulletType)
            bulleType = weapon.Bullet
        
        bullet = self.Space.CreateAtPosition("BasicBullet", self.Owner.Transform.Translation+positionOffset)
        
        bullet.RigidBody.Velocity = velocity * self.BulletSpeed
        bullet.Transform.RotateByAngles(Vec3(0,0,velocity.angleZ()))
        
        bullet.Sprite.Color = self.Owner.LightTank.getCurrentWeapon().Color
    #enddef generateBulley
    
    def generateDoubleBullet(self, positionOffset = Vec3(0,3,0), velocity = Vec3(0,1,0), bulletType = ""):
        self.generateBullet(positionOffset, velocity, bulletType)
        self.generateBullet(-positionOffset, -velocity, bulletType)
    #enddef generateBulley
    
    def SetShipColor(self, Color):
        self.Owner.Sprite.Color = Color

Zero.RegisterComponent("PlayerController", PlayerController)