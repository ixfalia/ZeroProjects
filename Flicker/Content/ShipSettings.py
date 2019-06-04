import Zero
import Events
import Property
import VectorMath

Vec4 = VectorMath.Vec4

#This class is very much like a statemachine. It aggregates important data about the state of
#the ship the player's utilizing. Probably will be upgraded to a more legit state manager
class ShipSettings:
    DebugMode = Property.Bool(default = True)
    
    ShipType = Property.String(default = "")
    WeaponType = Property.String(default = "gray")
    
    Spectrum = Property.Vector4(default = Vec4())
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        
    def onUpdate(self, Event):
        pass
    
    def textToColor(self, text):
        if text == "gray":
            return Vec4( 0.61, 0.61, 0.61, 1)
        if text == "red":
            return Vec4( 1, 0, 0, 1)
        if text == "green":
            return Vec4(0, 1, 0, 1)
        if text == "blue":
            return Vec4(0, 0, 1, 1)
    
    def getColor(self):
        return self.Spectrum
        
    def getColorNormalized(self):
        return self.Spectrum.normalize()
    
    def shiftLeft(self):
        
        pass
    
    def shiftRight(self):
        pass

Zero.RegisterComponent("ShipSettings", ShipSettings)