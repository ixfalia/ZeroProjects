import Zero
import Events
import Property
import VectorMath

#python modules
import random
import math
import colorsys #rgbTohsv
import time #time

class ChangeColor:
    DebugMode = Property.Bool(default = True)
    
    NewColor = Property.Color()
    RandomColor = Property.Bool(default = False)
    RandomColorAtStart = Property.Bool(default = False)
    ColorShifting = Property.Bool(default = False)
    ShiftTime = Property.Float(default = 1.0)
    AnotherSprite = Property.SpriteSource() #a total hack need to have both modules listen for message in Body space
    DetectEventType = Property.String(default = "")
    SpaceEvent = Property.Bool(default = False)
    OwnerEvent = Property.Bool(default = True)
    
    def Initialize(self, initializer):
        #print("ChangeOnActivation.Init()")
        if self.RandomColor and self.RandomColorAtStart:
            self.Owner.Sprite.Color = self.RandomHue(self.NewColor)
        
        self.StartingColor = self.Owner.Sprite.Color
        random.seed(time.clock())
        
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        
        if not self.DetectEventType == "":
            #print(self.DetectEventType, "Event connected to this component.")
            if self.OwnerEvent:
                Zero.Connect(self.Owner, self.DetectEventType, self.OnActivation)
            elif self.SpaceEvent:
                Zero.Connect(self.Space, self.DetectEventType, self.OnActivation)
        else:
            Zero.Connect(self.Owner, "FlowerGet", self.OnActivation)
        #endif
        
        if self.ColorShifting:
            self.RandomShiftColor = self.RandomHue(self.NewColor)
            self.timer = 0.0
        else:
            self.RandomShiftColor = self.StartingColor
            self.timer = 0.0
        
        self.colorChange = False
    #end initialize()
    
    def onUpdate(self, updateEvent):
        if self.ColorShifting:
            if self.DebugMode:
                print("ChangeColor.onUpdate():")
                print("\tCurrent Color:", self.Owner.Sprite.Color)
                print("\tEnd Color:", self.RandomShiftColor)
                print("\tDelta Time:", updateEvent.Dt)
            #endif
            
            deltaColor = self.Owner.Sprite.Color - self.RandomShiftColor
            deltaTime = updateEvent.Dt / self.ShiftTime
            self.timer += updateEvent.Dt
            #interpolatedColor = self.Owner.Sprite.Color * deltaTime + self.RandomShiftColor * (1 - deltaTime)
            interpolatedColor = self.Owner.Sprite.Color + deltaTime * (self.RandomShiftColor - self.Owner.Sprite.Color)
            
            self.Owner.Sprite.Color = interpolatedColor
            
            if self.DebugMode:
                print("\tUpdated Color:", self.Owner.Sprite.Color)
            
            if self.timer >= self.ShiftTime:
                self.RandomShiftColor = self.RandomHue(self.NewColor)
                self.timer = 0.0
                
                if self.DebugMode:
                    print("\Color Changed to:", self.RandomShiftColor)
                    #i = 2 /0
            #endif
        #endif
        
        if self.colorChange:
            deltaColor = self.Owner.Sprite.Color - self.RandomShiftColor
            deltaTime = updateEvent.Dt / self.ShiftTime
            self.timer += updateEvent.Dt
            #interpolatedColor = self.Owner.Sprite.Color * deltaTime + self.RandomShiftColor * (1 - deltaTime)
            interpolatedColor = self.Owner.Sprite.Color + deltaTime * (self.RandomShiftColor - self.Owner.Sprite.Color)
            
            self.Owner.Sprite.Color = interpolatedColor
        #event
    #end onUpdate()
    
    def OnActivation(self, Event):
        if self.RandomColor:
            self.Owner.Sprite.Color = self.RandomHue(self.NewColor)
            return
        
        self.Owner.Sprite.Color = self.NewColor
        
        if not self.AnotherSprite == "":
            self.Owner.PutAnotherSprite.CreateNewSprite(self.AnotherSprite)
    #end OnActivation()
    
    def ChangeColor(self, color = None):
        if color == None:
            print("ChangeColorChangeColor()")
            hue = self.RandomHue(self.StartingColor)
            print("\tOldColor:", self.StartingColor)
            print("\t", hue)
            self.Owner.Sprite.Color = hue#self.RandomHue(self.NewColor)
            #self.colorChange = True
            return
        else:
            self.RandomShiftColor = color
            self.colorChange = True
        #endif
    #end ChangeColor()
    
    def RandomHue(self, currentColor):
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
#end class ChangeColor

Zero.RegisterComponent("ChangeColor", ChangeColor)