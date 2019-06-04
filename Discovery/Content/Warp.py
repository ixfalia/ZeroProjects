import Zero
import Events
import Property
import VectorMath

class Warp:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        self.ToPosition = Property.Bool(default = False)
        self.Position = Property.Vector2()
        self.ToObject = Property.Bool(default = True)
        self.Object = Property.Cog()
        
        self.Offset = Property.Vector2(default = VectorMath.Vec2(0, -2))
    
    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        pass

    def OnLogicUpdate(self, UpdateEvent):
        pass
    
    def WarpMe(self, object):
        if self.ToObject and not self.Object:
            raise
        elif self.ToObject:
            target = self.Object.Transform.Translation
        if self.ToPosition and not self.Position:
            raise
        elif self.ToPosition:
            target = self.Position
        
        otherZ = object.Transform.Translation.z
        
        object.Transform.Translation = VectorMath.Vec3(target.x + self.Offset.x, target.y + self.Offset.y, otherZ)

Zero.RegisterComponent("Warp", Warp)