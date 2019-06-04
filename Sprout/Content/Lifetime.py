import Zero
import Events
import Property
import VectorMath

import Action

class Lifetime:
    Duration = Property.Float(default = 4)
    SendEvent = Property.String(default="")
    sendToHUDSpace = Property.Bool(default = True)
    sendToGameSpace = Property.Bool(default = False)
    sendToOwner = Property.Bool(default = False)
    
    def Initialize(self, initializer):
        self.HUDSpace = self.GameSession.FindSpaceByName("HUDSpace")
        self.GameSpace = self.GameSession.LevelManager.getGameSpace()
        
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        
        self.timer = 0
    
    def onUpdate(self, uEvent):
        self.timer += uEvent.Dt
        
        if not self.Owner:
            return
        
        if self.timer >= self.Duration:
            if self.Owner.SpriteParticleSystem and self.Owner.Fader:
                self.Owner.Fader.FadeOut()
                seq = Action.Sequence(self.Owner)
                Action.Delay(seq, self.Owner.Fader.FadeOutDuration)
                Action.Delay(seq, self.Owner.SphericalParticleEmitter.Lifetime)
                Action.Call(seq, self.sendEvent)
                Action.Call(seq, self.Owner.Destroy)
            elif self.Owner.SpriteParticleSystem:
                seq = Action.Sequence(self.Owner)
                #Action.Delay(seq, self.Duration)
                Action.Call(seq, self.deactivateParticles)
                Action.Delay(seq, self.Owner.SphericalParticleEmitter.Lifetime)
                Action.Call(seq, self.sendEvent)
                Action.Call(seq, self.Owner.Destroy)
            elif self.Owner.Fader:
                self.Owner.Fader.FadeOut()
                seq = Action.Sequence(self.Owner)
                Action.Delay(seq, self.Owner.Fader.FadeOutDuration)
                Action.Call(seq, self.sendEvent)
                Action.Call(seq, self.Owner.Destroy)
            else:
                self.sendEvent()
                self.Owner.Destroy()
    
    def deactivateParticles(self):
        if self.Owner.SpriteParticleSystem:
            self.Owner.SphericalParticleEmitter.Active = False
    
    def sendEvent(self):
        if self.SendEvent == "":
            return
            
        e = Zero.ScriptEvent()
        
        if self.sendToGameSpace:
            self.GameSpace = self.GameSession.LevelManager.getGameSpace()
            self.GameSpace.DispatchEvent(self.SendEvent, e)
        
        if self.sendToHUDSpace:
            self.HUDSpace = self.GameSession.FindSpaceByName("HUDSpace")
            if not self.HUDSpace:
                return
            
            self.HUDSpace.DispatchEvent(self.SendEvent, e)
        
        if self.sendToOwner:
            self.Owner.DispatchEvent(self.SendEvent, e)

Zero.RegisterComponent("Lifetime", Lifetime)