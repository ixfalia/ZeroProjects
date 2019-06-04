import Zero
import Events
import Property
import VectorMath

import Action #Actions 

Vec4 = VectorMath.Vec4
Vec3 = VectorMath.Vec3

class Fader:
    DebugMode = Property.Bool(default = False)
    defaultOpacity = Property.Float(default = 1)
    FadeInDuration = Property.Float(default = 1)
    FadeOutDuration = Property.Float(default = 1)
    FadeInOnCreation = Property.Bool(default = False)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        
        #clear any actions that might be lingering
        self.Owner.Actions.Clear()
        
        currentColor = self.Owner.Sprite.Color
        self.Owner.Sprite.Color = Vec4(currentColor.r, currentColor.g, currentColor.b, self.defaultOpacity)
        self.TargetFade = self.defaultOpacity
        
        if self.FadeInOnCreation:
            self.FadeIn()
        
    
    def onUpdate(self, uEvent):
        pass
        
    #end onUpdate()
    
    def FadeOut(self, time = None):
        if not time:
            time = self.FadeOutDuration
        
        if self.Owner.Hierarchy:
            self.FadeOutHierarchy()
        
        target = self.Owner.Sprite
        current = self.Owner.Sprite.Color
        endColor = Vec4( current.r, current.g, current.b, 0)
        
        seq = Action.Sequence(self.Owner)
        Action.Property(seq, target, "Color",end=endColor, duration=time)
        
    def FadeIn(self, time = None):
        if not self.Owner:
            return
        
        if not time:
            time = self.FadeInDuration
        
        if self.Owner.Hierarchy:
            self.FadeInHierarchy()
        
        if self.Owner.Sprite:
            self.Owner.Sprite.Visible = True
            self.Owner.Sprite.Color *= VectorMath.Vec4(1,1,1,0)
        #endif
        
        target = self.Owner.Sprite
        current = self.Owner.Sprite.Color
        endColor = Vec4( current.r, current.g, current.b, self.defaultOpacity)
        
        seq = Action.Group(self.Owner)
        
        Action.Property( seq, target, property="Color",end=endColor,duration=time )
    
    def FadeInHierarchy(self, time = None):
        if not time:
            time = self.FadeInDuration
        
        for cog in self.Owner.Hierarchy.Children:
            if cog.Sprite:
                self.FadeInObject(cog)
            if cog.SpriteText:
                self.FadeInObject(cog)
            
            if cog.Hierarchy:
                for child in cog.Hierarchy.Children:
                    self.FadeInObject(child)
    
    def FadeOutHierarchy(self, time = None):
        if not time:
            time = self.FadeInDuration
        
        for cog in self.Owner.Hierarchy.Children:
            if cog.Sprite:
                self.FadeOutObject(cog)
            if cog.SpriteText:
                self.FadeOutObject(cog)
            
            if cog.Hierarchy:
                for child in cog.Hierarchy.Children:
                    self.FadeOutObject(child)
    
    def FadeInObject(self, object, time = None):
        if not self.Owner:
            return
        if not time:
            time = self.FadeInDuration
        
        if object.Sprite:
            object.Sprite.Visible = True
            
            target = object.Sprite
            current = object.Sprite.Color
            endColor = Vec4( current.r, current.g, current.b, self.defaultOpacity)
            
            object.Sprite.Color *= Vec4(1,1,1,0)
            
            seq = Action.Group(object)
            Action.Property( seq, target, property="Color",end=endColor,duration=time )
        
        if object.SpriteText:
            object.SpriteText.Visible = True
            
            target = object.SpriteText
            current = object.SpriteText.Color
            endColor = Vec4( current.r, current.g, current.b, self.defaultOpacity)
            
            object.SpriteText.Color *= Vec4(1,1,1,0)
            
            seq = Action.Group(object)
            Action.Property( seq, target, property="Color",end=endColor,duration=time )
    
    def FadeOutObject(self, object, time = None):
        if not self.Owner:
            return
        if not time:
            time = self.FadeOutDuration
        
        if object.Sprite:
            target = object.Sprite
            current = object.Sprite.Color
            endColor = Vec4( current.r, current.g, current.b, 0)
            
            seq = Action.Sequence(object)
            Action.Property(seq, target, "Color",end=endColor, duration=time)
        
        if object.SpriteText:
            target = object.SpriteText
            current = object.SpriteText.Color
            endColor = Vec4( current.r, current.g, current.b, 0)
            
            seq = Action.Sequence(object)
            Action.Property(seq, target, "Color",end=endColor, duration=time)

Zero.RegisterComponent("Fader", Fader)