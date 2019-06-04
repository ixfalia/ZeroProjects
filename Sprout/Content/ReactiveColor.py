import Zero
import Events
import Property
import VectorMath

import Action
import myCustomEnums

sproutTypes = myCustomEnums.sproutTypes

Vec3 = VectorMath.Vec3
Vec4 = VectorMath.Vec4

class ReactiveColor:
    disableMouseEvents =  Property.Bool(default = False)
    
    DefaultColor = Property.Color(default=Vec4())
    HoverColor = Property.Color(default=Vec4(0.80, 0.80, 0.8, 1))
    DownColor = Property.Color(default=Vec4(0.45,0.45,0.45,1))
    
    hoverEvent = Property.String(default="UIState_Hover")
    resetEvent = Property.String(default="UIState_Default")
    activateEvent = Property.String(default="UIState_Activate")
    
    def Initialize(self, initializer):
        if not self.disableMouseEvents:
            Zero.Connect(self.Owner, self.resetEvent, self.onReset)
            Zero.Connect(self.Owner, self.hoverEvent, self.onHover)
            Zero.Connect(self.Owner, self.activateEvent, self.onActivate)
        #endif
        
        if self.Owner.Sprout:
            self.DefaultColor = self.Owner.Sprout.enumToColor()
        elif self.Owner.GridManipulator:
            self.DefaultColor = self.Owner.GridManipulator.setColorstoEffects()
        else:
        #elif self.DefaultColor == Vec4():
            self.DefaultColor = self.Owner.Sprite.Color
        
        if self.Owner.Sprite:
            self.Owner.Sprite.Color = self.DefaultColor
        
        self.Defaulta = self.DefaultColor.a
    #enddef
    
    def getDefaultColor(self):
        if self.Owner.Sprout:
            self.DefaultColor = self.Owner.Sprout.Manager.effectColors(self.Owner.Sprout.Type)
            self.Owner.ColorShifting.Active = False
            if self.Owner.Sprout.Type == sproutTypes.rainbow:
                self.Owner.ColorShifting.Active = True
        if self.Owner.GridManipulator:
            self.DefaultColor = self.Owner.GridManipulator.setColorstoEffects()
        return self.DefaultColor
    
    def onReset(self, mEvent):
        if self.Owner.Sprite:
            self.Owner.Sprite.Color = self.getDefaultColor()
            #self.Owner.Sprite.Color = self.Owner.Sprout.enumToColor()
        #endif
        
        pass
    #endef
    
    def onHover(self, mEvent):
        color = self.DefaultColor
        
        if self.Owner.Sprite:
            if self.Owner.Sprout:
                if not self.Owner.Sprout.Type == sproutTypes.blank:
                    return
                levelsetting = self.Space.FindObjectByName("LevelSettings")
                if levelsetting.ManipulatorManager.currentEffect == sproutTypes.rainbow:
                    self.Owner.ColorShifting.Active = True
                else:
                    self.Owner.ColorShifting.Active = False
                manager = self.Owner.Sprout.Manager
                a = 1#manager.effectColors().a
                self.Owner.Sprite.Color = manager.effectColors(manager.currentEffect)#self.Owner.Sprout.currentColor
                
                return
            if self.Owner.GridManipulator:
                self.DefaultColor = self.Owner.GridManipulator.setColorstoEffects()
                nuColor = self.HoverColor
                color = self.DefaultColor
                nuColor = color.lerp(self.HoverColor, 0.5)
                nuColor.w = 1
                self.Owner.Sprite.Color = nuColor
                return
            else:
                a = 1.0
            #endif
            
            nuColor = self.HoverColor
            #self.DefaultColor = self.Owner.Sprout.enumToColor()
            #nuColor = Vec4(self.HoverColor.r,self.HoverColor.g,self.HoverColor.b,a)
            #print(self.DefaultColor)
            #print(self.Owner.GridManipulator.currentEffect)
            nuColor = color.lerp(self.HoverColor, 0.5)
            nuColor.w = a
            
            self.Owner.Sprite.Color = nuColor
        #endif
        
        pass
    #endef
    
    def onActivate(self, mEvent):
        if self.Owner.Sprite:
            nuColor = self.DownColor.lerp(self.DefaultColor, 0.15)
            #self.Owner.Sprite.Color = nuColor
        #endif
        
        pass
    #enddef

Zero.RegisterComponent("ReactiveColor", ReactiveColor)