import Zero
import Events
import Property
import VectorMath

import Action

Vec4 = VectorMath.Vec4
Vec3 = VectorMath.Vec3

class Fader:
    def DefineProperties(self):
        self.FadeChildren = Property.Bool(default = True)
        self.FadeInOnStart = Property.Bool(default = False)
        
        self.FadeInTime = Property.Float(default = 0.25)
        self.FadeOutTime = Property.Float(default = 0.25)
        self.startingAlpha = Property.Float()
        pass

    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        self.startingColor = self.getColor()
        self.startingAlpha = self.startingColor.a
        
        print(self.Owner.Name, self.startingColor, self.startingAlpha)
        
        if self.FadeInOnStart:
            self.FadeIn()
        pass
    
    def FadeIn(self, time = None):
        if time == None:
            time = self.FadeInTime
        
        self.setAlpha(0)
        self.fadeToAlpha(time, self.startingAlpha)
        
        if self.FadeChildren:
            self.fadeChildrenIn(time)
            #raise
    
    def Fadeout(self, time = None):
        if time == None:
            time = self.FadeOutTime
        
        self.fadeToAlpha(time, 0)
        
        if self.FadeChildren:
            self.fadeChildrenOut(time)
    
    def fadeChildrenIn(self, time = None):
        for child in self.Owner.Children:
            if child.Fader:
                child.Fader.FadeIn(time)
    
    def fadeChildrenOut(self, time = None):
        for child in self.Owner.Children:
            if child.Fader:
                child.Fader.FadeOut(time)

    def setAlpha(self, set):
        color = self.getColor()
        
        nuColor = Vec4(color.r, color.g, color.b, set)
        
        if self.Owner.Sprite:
            self.Owner.Sprite.Color = nuColor
        elif self.Owner.SpriteText:
            self.Owner.SpriteText.Color = nuColor
    
    def getColor(self):
        if self.Owner.Sprite:
            returner = self.Owner.Sprite.Color
        elif self.Owner.SpriteText:
            returner = self.Owner.SpriteText.Color
        else:
            raise
        
        return returner
    
    def fadeToAlpha(self, time, alpha):
        color = self.getColor()
        nuColor = Vec4(color.r, color.g, color.b, alpha)
        
        self.fadeToColor(time, nuColor)
    
    def fadeToColor(self, time, color):
        seq = Action.Sequence(self.Owner)
        Action.Group(seq)
        
        if self.Owner.Sprite:
            Action.Property(seq, self.Owner.Sprite, "Color", color, time, Action.Ease.QuadIn)
        if self.Owner.SpriteText:
            Action.Property(seq, self.Owner.SpriteText, "Color", color, time, Action.Ease.QuadIn)

Zero.RegisterComponent("Fader", Fader)