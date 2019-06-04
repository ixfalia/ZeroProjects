import Zero
import Events
import Property
import VectorMath

import Color

class HoverText:
    Text = Property.String()
    Archetype = Property.Archetype()
    BackColor = Property.Color(default = Color.White)
    HoverSize = Property.Float(default = 1.25)
    
    Offset = Property.Vector3(VectorMath.Vec3(0,2,0))
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.MouseEnter, self.onHover)
        Zero.Connect(self.Owner, Events.MouseExit, self.onExit)
        
        if not self.Text:
            self.Text = "Undefined String"
        if self.BackColor == Color.White:
            self.BackColor = Color.CadetBlue.lerp(Color.Black, 0.7)
            #self.BackColor = VectorMath.Vec4(0x0F,0x11,0x20, 1)
        
        if self.Archetype.Name ==  "DefaultArchetype":
            self.Archetype = "HoverText"
    
    def onHover(self, e):
        myTransl = self.Owner.Transform.Translation
        position = VectorMath.Vec3(myTransl.x, myTransl.y, 2)
        
        if self.Text.find("UI") >= 0:
            name = self.Owner.UIItem.Name
            
            if not name:
                name = "Undefined Item"
            self.Text = name
            #raise
        
        if self.Owner.MeshCollider:
            lSettings = self.Space.FindObjectByName("LevelSettings")
            pos = lSettings.CameraViewport.ScreenToWorldZPlane(e.Position, 2)
            pos = pos + self.Offset
            self.Created = self.Space.CreateAtPosition(self.Archetype, pos)
            #print(self.Created.Transform.Translation)
            #raise
        else:
            self.Created = self.Space.CreateAtPosition(self.Archetype, position+self.Offset)
        
        self.Created.Transform.Scale = VectorMath.Vec3(self.HoverSize, self.HoverSize, self.HoverSize)
        e = Zero.ScriptEvent()
        
        e.Name = self.Text
        self.Created.DispatchEvent("DetailEvent", e)
        
        self.Created.SpriteText.Text = self.Text
        
        for child in self.Created.Hierarchy.Children:
            if child.Sprite:
                child.Sprite.Color = self.BackColor
    
    def onExit(self, e):
        if self.Created:
            self.Created.Destroy()

Zero.RegisterComponent("HoverText", HoverText)