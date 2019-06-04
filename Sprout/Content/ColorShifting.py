import Zero
import Events
import Property
import VectorMath

import random
import time
import Color
import math
import colorsys
import Action

class ColorShifting:
    Debug = Property.Bool(default = False)
    Active = Property.Bool(default = True)
    RandomShift = Property.Bool(default = True)
    ShiftTime = Property.Float(default = 1.0)
    SpriteShift = Property.Bool(default = True)
    TextShift = Property.Bool(default = False)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevel)
        random.seed(time.clock())
        
        if self.Owner.Sprite:
            self.StartingColor = self.Owner.Sprite.Color
        elif self.Owner.SpriteText:
            self.StartingColor = self.Owner.SpriteText.Color
        else:
            self.StartingColor = Color.Blue
        self.NewColor = Color.Blue
        
        self.RandomShiftColor = self.RandomHue(self.NewColor)
        self.timer = 0.0
    
    def onLevel(self, lEvent):
        if self.Owner.EffectTracker:
            self.NewColor = self.Owner.EffectTracker.getCurrentEffectColor()
    
    def onUpdate(self, updateEvent):
        if not self.Active:
            return
        
        if self.Debug:
            print("ChangeColor.onUpdate():")
            print("\tCurrent Color:", self.Owner.Sprite.Color)
            print("\tEnd Color:", self.RandomShiftColor)
            print("\tDelta Time:", updateEvent.Dt)
        #endif
        
        deltaColor = self.getCurrentColor() - self.RandomShiftColor
        deltaTime = updateEvent.Dt / self.ShiftTime
        self.timer += updateEvent.Dt
        #interpolatedColor = self.Owner.Sprite.Color * deltaTime + self.RandomShiftColor * (1 - deltaTime)
        interpolatedColor = self.getCurrentColor() + deltaTime * (self.RandomShiftColor - self.getCurrentColor())
        
        if self.SpriteShift:
            self.Owner.Sprite.Color = interpolatedColor
        
        if self.TextShift:
            self.Owner.SpriteText.Color = interpolatedColor
        
        if self.Debug:
            print("\tUpdated Color:", self.Owner.Sprite.Color)
        
        if self.timer >= self.ShiftTime:
            self.RandomShiftColor = self.RandomHue(self.NewColor)
            
            self.timer = 0.0
            
            if self.Debug:
                print("\Color Changed to:", self.RandomShiftColor)
                #i = 2 /0
        #endif
        #endif
    #end
    
    def shiftColor(self, color = None):
        if color == None:
            #print("ChangeColorChangeColor()")
            hue = self.RandomHue(self.StartingColor)
            #print("\tOldColor:", self.StartingColor)
            #print("\t", hue)
            self.RandomShiftColor = hue#self.RandomHue(self.NewColor)
            #self.colorChange = True
            return
        else:
            self.RandomShiftColor = color
            seq = Action.Sequence(self.Owner)
            Action.Property(seq, self.Owner.Sprite, "Color", color, self.ShiftTime, Action.Ease.Linear)
            
        #endif
    #end ChangeColor()
    
    def RandomHue(self, currentColor = None):
        if not currentColor:
            currentColor = self.StartingColor
        
        random.seed(time.time())
        
        convertedColor = colorsys.rgb_to_hsv(currentColor.x, currentColor.y, currentColor.z)
        newColor = colorsys.hsv_to_rgb(random.random(), convertedColor[1], convertedColor[2])
        
        return VectorMath.Vec4(newColor[0], newColor[1], newColor[2], 1)
    #end RandomHue()
    
    def RGBtoH(self):
        saturation = 0
        hue = 0
        value = 0
        
        minimum = min(self.StartingColor.r, self.StartingColor.g, self.StartingColor.b)
        maximum = max(self.StartingColor.r, self.StartingColor.g, self.StartingColor.b)
        
        value = maximum
        
        delta = max - min
        
        if not max == 0:
            saturation = delta / maximum
        else:
            saturation = 0
            hue = -1
            return hue
        
        if self.StartingColor.r == maximum:
            hue = (self.StartingColor.g - self.StartingColort.b) / delta
        elif self.StartingColor.g == maximum:
            hue = 2 + (self.StartingColor.b - self.StartingColort.r) / delta
        else:
            hue = 4 + (self.StartingColor.r - self.StartingColort.g) / delta
        #endif
        
        hue *=  60
        
        if (hue < 0):
            hue += 360
        
        return hue
    #end RGBtoH()
    
    def HtoRGB(self, hsv):
        hi = math.floor(h / 60.0) % 6
        f =  (h / 60.0) - math.floor(h / 60.0)
        p = v * (1.0 - s)
        q = v * (1.0 - (f*s))
        t = v * (1.0 - ((1.0 - f) * s))
        return {
            0: (v, t, p),
            1: (q, v, p),
            2: (p, v, t),
            3: (p, q, v),
            4: (t, p, v),
            5: (v, p, q),
        }[hi]
    
    def getCurrentColor(self):
        if self.Owner.Sprite:
            color = self.Owner.Sprite.Color
        else:# self.Owner.SpriteText:
            color = self.Owner.SpriteText.Color
        return color

Zero.RegisterComponent("ColorShifting", ColorShifting)