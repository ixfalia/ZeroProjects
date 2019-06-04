import Zero
import Events
import Property
import VectorMath

import Color

Vec3 = VectorMath.Vec3
Vec2 = VectorMath.Vec2

class BarController:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        self.CurrentValue = Property.Float(default = 0.0)
        
        self.MaxLength = Property.Float(default = 8.0)
        self.OtherAxisSize = Property.Float(default = 0.5)
        
        self.ApplyOnYAxisInstead = Property.Bool(default = False)
        self.ApplyColorModification = Property.Bool(default = False)
        self.LowColor = Property.Color()
        self.HighColor = Property.Color()
        pass

    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
        self.MinLength = 0.01
        self.Scale = self.Owner.Transform.Scale
        self.bleh = self.CurrentValue
        pass

    def OnLogicUpdate(self, UpdateEvent):
        #self.bleh += UpdateEvent.Dt / 2
        #self.setValue(self.bleh)
        
        self.updateBar()
        self.updateColor()
    
    def updateBar(self, value = None):
        if value == None:
            value = self.CurrentValue
        
        if not value:
            value = self.bleh
        
        if value > 1.0:
            value = 1.0
        
        scale = value * self.MaxLength
        
        if self.ApplyOnYAxisInstead:
            #self.Owner.Transform.Scale = Vec3(self.OtherAxisSize, scale, 0)
            self.Owner.Area.Size = Vec2(self.OtherAxisSize, scale)
        else:
            #self.Owner.Transform.Scale = Vec3(scale, self.OtherAxisSize, 0)
            self.Owner.Area.Size = Vec2(scale, self.OtherAxisSize)
    
    def updateColor(self, value = None):
        if not value:
            value = self.CurrentValue
        
        if value > 1.0:
            value = 1.0
        elif value < 0:
            value = 0
        
        color = self.LowColor.lerp(self.HighColor, value)
        
        self.Owner.Sprite.Color = color
    
    def setValue(self, value):
        self.CurrentValue = value

Zero.RegisterComponent("BarController", BarController)