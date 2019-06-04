import Zero
import Events
import Property
import VectorMath

import Action
Vec2 = VectorMath.Vec2

class MouseResponse:
    SimpleDarken = Property.Bool(default = False)
    MergeColors = Property.Bool(default = True)
    mergePercent = Property.Float(default = 0.75)
    
    mouseSlide = Property.Vector2(default = Vec2())
    
    hoverColor = Property.Color()
    downColor = Property.Color()
    
    defaultOpacity = Property.Float(default = 1)
    hoverSound = Property.SoundCue()
    downSound = Property.SoundCue()
    
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.MouseEnter, self.setHover)
        Zero.Connect(self.Owner, Events.MouseExit, self.onExit)
        #Zero.Connect(self.Owner, "MouseActivateEvent", self.setDown)
        Zero.Connect(self.Owner, Events.MouseDown, self.setDown)
        Zero.Connect(self.Owner, Events.MouseUp, self.onUp)
        
        self.SpriteText = False
        self.hovering = False
        self.seq = Action.Group(self.Owner)
        
        #if not self.Owner.MouseBox:
            #print("[[MouseResponse Error]] Module requires MouseBox")
            #raise
        
        if self.Owner.Sprite:
            color = self.Owner.Sprite.Color
            color = VectorMath.Vec4(color.r, color.g, color.b, self.defaultOpacity)
            #self.defaultColor = VectorMath.Vec4(color.x, color.y, color.z, 1)
            self.defaultColor = color
            self.startingColor = color
            
        elif self.Owner.SpriteText:
            color = self.Sprite.Color
            self.defaultColor = VectorMath.Vec4(color.r, color.g, color.b, self.defaultOpacity)
            self.startingColor = VectorMath.Vec4(color.r, color.g, color.b, self.defaultOpacity)
            self.SpriteText = True
        else:
            raise
        
        if self.mouseSlide == Vec2(0,0):
            self.mouseSlide = None
        else:
            self.startingPosition = self.Owner.Transform.Translation
            self.endPosition = self.Owner.Transform.Translation + self.mouseSlide
    
    def setHover(self, e):
        #print("hover")
        self.setColor(self.hoverColor)
        self.hovering = True
        
        if not self.hoverSound.Name == "DefaultCue":
            if self.Owner.Parent and self.Owner.Parent.SoundEmitter:
                self.Owner.Parent.SoundEmitter.PlayCue(self.hoverSound)
            elif self.Owner.SoundEmitter:
                self.Owner.SoundEmitter.PlayCue(self.hoverSound)
        
        self.mouseSlideOut()
    
    def setDefault(self, e):
        if self.hovering:
            color = self.getColor(self.hoverColor)
        else:
            color = self.defaultColor
        
        if self.SpriteText:
            self.Owner.SpriteText.Color = color
        else:
            self.Owner.Sprite.Color = color
        
        if not self.hovering:
            self.mouseSlideBack()
            pass
    
    def setDown(self, e):
        self.setColor(self.downColor)
        
        if not self.downSound.Name == "DefaultCue":
            if self.Owner.Parent and self.Owner.Parent.SoundEmitter:
                self.Owner.Parent.SoundEmitter.PlayCue(self.downSound)
            elif self.Owner.SoundEmitter:
                self.Owner.SoundEmitter.PlayCue(self.downSound)
    
    def onExit(self, e):
        self.hovering = False
        self.setDefault(e)
    
    def onUp(self, e):
        self.setDefault(e)
    
    def setColor(self, color):
        if self.SpriteText:
            self.setTextColor(color)
        else:
            self.setSpriteColor(color)
    
    def setSpriteColor(self, color):
        if self.MergeColors:
            color = self.getColor(color)
        self.Owner.Sprite.Color = color
    
    def setTextColor(self, color):
        if self.MergeColors:
            color = self.getColor(color)
        
        self.Owner.SpriteText.Color = color
    
    def getColor(self, color):
        if self.MergeColors:
            return self.defaultColor.lerp(color, self.mergePercent)
        else:
            return color
    
    def setDefaultColor(self, color, setSprite = False):
        self.defaultColor = color
        
        if setSprite:
            self.setColor(color)
    
    def resetColor(self, setSprite = False):
        self.defaultColor = self.startingColor
        
        if setSprite:
            self.setColor(self.defaultColor)
    
    def mouseSlideOut(self):
        if self.mouseSlide:
            self.seq.Cancel()
            self.seq = Action.Group(self.Owner)
            position = self.Owner.Transform.Translation + self.mouseSlide
            
            sE = Zero.ScriptEvent()
            sE.Name = "Slide"
            self.Owner.Parent.Space.DispatchEvent("PlaySound", sE)
            
            Action.Property(self.seq, self.Owner.Transform, "Translation", self.endPosition, 0.25)
    
    def mouseSlideBack(self):
        if self.mouseSlide:
            self.seq.Cancel()
            self.seq = Action.Group(self.Owner)
            
            position = self.startingPosition
            Action.Property(self.seq, self.Owner.Transform, "Translation", position, 0.25)

Zero.RegisterComponent("MouseResponse", MouseResponse)