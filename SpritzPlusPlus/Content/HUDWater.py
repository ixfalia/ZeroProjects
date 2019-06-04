import Zero
import Events
import Property
import VectorMath

class HUDWater:
    DebugMode = Property.Bool(default = True)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, "WaterTankEvent", self.onWaterTank)
        
        self.StartingPosition = self.Owner.Transform.Translation
        self.DefaultTankSize = self.Owner.Transform.Scale.y#7.0
        
        self.lastState = False
        
        if self.DebugMode:
            print("HUDWater.Initialize()")
    
    def onWaterTank(self, waterEvent):
        if self.DebugMode:
            print("WaterTankEvennt received, levels at ", waterEvent.Tank)
        
        currentScale = self.Owner.Transform.Scale
        currentPos = self.Owner.Transform.Translation
        
        if self.lastState == True and waterEvent.isReplenishing == False:
            self.Owner.SoundEmitter.Play()
        
        if waterEvent.isReplenishing:
            self.Owner.Model.Material = "RedTankWater"
        else:
            self.Owner.Model.Material = "Water"
        
        self.Owner.BoxParticleEmitter.Active = waterEvent.isUnlimitedWater
        
        self.lastState = waterEvent.isReplenishing
        
        self.Owner.Transform.Scale = VectorMath.Vec3(currentScale.x, self.DefaultTankSize * waterEvent.Tank, currentScale.z)
        #self.Owner.Transform.Translation = VectorMath.Vec3(self.StartingPosition.x, currentPos.y, currentPos.z)

Zero.RegisterComponent("HUDWater", HUDWater)