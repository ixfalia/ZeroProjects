import Zero
import Events
import Property
import VectorMath

import Action
import random

class LightPulse:
    def DefineProperties(self):
        self.Active = Property.Bool(default = True)
        self.LightOn = Property.Float(default = 0.5)
        self.LightOff = Property.Float(default = 0.5)
        self.FadeTime = Property.Float(default = 0.5)
        self.defaultIntensity = Property.Float(default = -1)
        self.StartsOn = Property.Bool(default = True)
        pass

    def Initialize(self, initializer):
        self.Sequence = Action.Sequence(self.Owner)
        
        Zero.Connect(self.Owner, "PulseOnEvent", self.onPulse)
        Zero.Connect(self.Owner, "PulseOffEvent", self.onPulseOff)
        Zero.Connect(self.GameSession, Events.KeyUp, self.onKeyDown)
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
        if self.defaultIntensity < 0:
            self.defaultIntensity = self.Owner.Light.Intensity
        
        self.turnLightOn()
        pass

    def OnLogicUpdate(self, UpdateEvent):
        if not self.Active:
            self.onPulseOff(None)
        pass
    
    def turnLightOn(self, time = None):
        if not time:
            duration = self.LightOn
        else:
            duration = time
        
        if duration < 0:
            duration = random.random()
        if self.FadeTime < 0:
            fade = random.uniform(0, 0.75)
        else:
            fade = self.FadeTime
        
        target = self.Owner.Light
        seq = self.Sequence#Action.Sequence(self.Owner)
        self.Owner.Light.Intensity
        
        Action.Property(seq, target, "Intensity", end = self.defaultIntensity, duration = fade, ease = Action.Ease.SinInOut)
        Action.Delay(seq, duration)
        Action.Call(seq, self.turnLightOff)
    
    def onKeyDown(self, kEvent):
        raise
    
    def turnLightOff(self, time = None):
        if not time:
            duration = self.LightOff
        else:
            duration = time
        
        if duration < 0:
            duration = random.random()
        if self.FadeTime < 0:
            fade = random.uniform(0, 0.75)
        else:
            fade = self.FadeTime
        
        target = self.Owner.Light
        seq = self.Sequence#Action.Sequence(self.Owner)
        
        Action.Property(seq, target, "Intensity", end = 0, duration = fade, ease = Action.Ease.SinInOut)
        Action.Delay(seq, duration)
        Action.Call(seq, self.turnLightOn)
    
    def setDefaultIntensity(self, intensity):
        self.defaultIntensity = intensity
    
    def onPulse(self, pulseEvent):
        if self.StartsOn:
            self.turnLightOn()
        else:
            self.turnLightOff()
    
    def onPulseOff(self, pulseEvent):
        self.Sequence.Cancel()
        

Zero.RegisterComponent("LightPulse", LightPulse)