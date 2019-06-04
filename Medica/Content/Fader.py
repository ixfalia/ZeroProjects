import Zero
import Events
import Property
import VectorMath

import Action #Actions 

Vec4 = VectorMath.Vec4
Vec3 = VectorMath.Vec3

class Fader:
    DebugMode = Property.Bool(default = False)
    #defaultOpacity = Property.Float(default = 1)
    FadeInDuration = Property.Float(default = 1)
    FadeOutDuration = Property.Float(default = 1)
    FadeInOnCreation = Property.Bool(default = False)
    InvisibleOnCreation = Property.Bool(default = False)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevel)
        
        self.defaultOpacity = 1
        self.levelStarted = False
        
        if self.Owner.Sprite:
            self.defaultOpacity = self.Owner.Sprite.Color.a
        elif self.Owner.Hierarchy:
            for child in self.Owner.Hierarchy.Children:
                if child.Sprite:
                    self.defaultOpacity = child.Sprite.Color.a
                    break
        else:
            self.defaultOpacity = 1
        
        #clear any actions that might be lingering
        self.Owner.Actions.Clear()
        
        if self.Owner.Sprite:
            currentColor = self.Owner.Sprite.Color
            self.Owner.Sprite.Color = Vec4(currentColor.r, currentColor.g, currentColor.b, self.defaultOpacity)
        elif self.Owner.SpriteText:
            currentColor = self.Owner.SpriteText.Color
            self.Owner.SpriteText.Color = Vec4(currentColor.r, currentColor.g, currentColor.b, self.defaultOpacity)
        
        self.TargetFade = self.defaultOpacity
        
        if self.FadeInOnCreation:
            seq = Action.Sequence(self.Owner)
            Action.Delay(seq, 0.05)
            Action.Call(seq, self.FadeIn)
            #self.FadeIn()
            pass
        elif self.InvisibleOnCreation:
            #self.FadeOut(0)
            pass
    
    def onLevel(self, e):
        if self.FadeInOnCreation:
            self.FadeIn()
    
    def onUpdate(self, uEvent):
        pass
        
    #end onUpdate()
    
    def FadeOut(self, time = None):
        if time == None:
            time = self.FadeOutDuration
        
        if self.Owner.Hierarchy:
            self.FadeOutHierarchy()
            
        if self.Owner.Sprite:
            #self.Owner.Sprite.Visible = True
            #self.Owner.Sprite.Color *= VectorMath.Vec4(1,1,1,0)
            
            myObject = self.Owner.Sprite
            myColor = self.Owner.Sprite.Color
        elif self.Owner.SpriteText:
            #self.Owner.SpriteText.Visible = True
            #self.Owner.SpriteText.Color *= VectorMath.Vec4(1,1,1,0)
            
            myObject = self.Owner.SpriteText
            myColor = self.Owner.SpriteText.Color
        
        if self.Owner.Reactive:
            self.Owner.Reactive.Active = False
        #endif
        
        if self.Owner.ColorNexus:
            myColor = self.Owner.ColorNexus.BaseColor
        
        target = myObject
        current = myColor
        endColor = Vec4( current.r, current.g, current.b, 0)
        
        seq = Action.Group(self.Owner)
        Action.Property(seq, target, "Color",end=endColor, duration=time)
        
    def FadeIn(self, time = None):
        if not self.Owner:
            return
        
        if not time:
            time = self.FadeInDuration
        
        if self.Owner.Hierarchy:
            self.FadeInHierarchy()
        
        if self.Owner.Sprite:
            #self.Owner.Sprite.Visible = True
            self.Owner.Sprite.Color *= VectorMath.Vec4(1,1,1,0)
            
            myObject = self.Owner.Sprite
            myColor = self.Owner.Sprite.Color
        elif self.Owner.SpriteText:
            self.Owner.SpriteText.Visible = True
            self.Owner.SpriteText.Color *= VectorMath.Vec4(1,1,1,0)
            
            myObject = self.Owner.SpriteText
            myColor = self.Owner.SpriteText.Color
        
        if self.Owner.Reactive:
            if self.Owner.UIItem:
                if not self.Owner.UIItem.Name:
                    self.Owner.Reactive.Active = False
            else:
                self.Owner.Reactive.Active = True
        #endif
        
        if self.Owner.ColorNexus:
            myColor = self.Owner.ColorNexus.BaseColor
        
        target = myObject
        current = myColor
        
        self.defaultOpacity = 1
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
            #object.Sprite.Visible = True
            
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
    
    def FadeDestroy(self):
        seq = Action.Sequence(self.Owner)
        self.FadeOut()
        Action.Delay(seq, self.FadeOutDuration)
        Action.Call(seq, self.Destroy)
    
    def Destroy(self):
        self.Owner.Destroy()

Zero.RegisterComponent("Fader", Fader)