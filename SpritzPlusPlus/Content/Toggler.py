import Zero
import Events
import Property
import VectorMath

import Action

#toggles visibles and traits on and off
class Toggler:
    onEvent = Property.String()
    Duration = Property.Float(default = 3.0)
    def Initialize(self, initializer):
        if self.onEvent == "":
            raise
        
        self.Active = False
        Zero.Connect(self.Space, self.onEvent, self.onKeyEvent)
    
    def onKeyEvent(self, kEvent):
        print("Toggler.onKeyEvent:", kEvent.Name, "received")
        if not kEvent.Toggle == None:
            if kEvent.Toggle == False:
                self.toggleOff()
                return
        
        if self.Owner.Sprite:
            self.Owner.Sprite.Visible = True
        
        if self.Owner.SpriteText:
            self.Owner.SpriteText.Visible = True
        
        if self.Owner.SoundEmitter:
            self.Owner.SoundEmitter.Play()
        
        e =  Zero.ScriptEvent()
        self.Owner.DispatchEvent("ActivateEvent", e)
        
        if self.Duration >= 0:
            seq = Action.Sequence(self.Owner)
            
            Action.Delay(seq, self.Duration)
            Action.Call(seq, self.toggleOff)
    
    def onKeyEventAlt(self, kEvent):
        print("Toggler.onKeyEvent:", kEvent, "received")
        
        if not kEvent.Toggle == None:
            self.Active = kEvent.Toggle
        else:
            self.Active = not self.Active
        
        if self.Owner.Sprite:
            self.Owner.Sprite.Visible = self.Active
        
        if self.Owner.SpriteText:
            self.Owner.SpriteText.Visible = self.Active
        
        if self.Owner.SoundEmitter:
            self.Owner.SoundEmitter.Play()
        
        e =  Zero.ScriptEvent()
        self.Owner.DispatchEvent("ActivateEvent", e)
        
        if self.Duration >= 0:
            seq = Action.Sequence(self.Owner)
            
            Action.Delay(seq, self.Duration)
            Action.Call(seq, self.toggleOff)
    
    def toggleOff(self):
        if self.Owner.Sprite:
            self.Owner.Sprite.Visible = False
        
        if self.Owner.SpriteText:
            self.Owner.SpriteText.Visible = False
        
        if self.Owner.PathFollower:
            self.Owner.PathFollower.Reset()
            self.Owner.PathFollower.Paused = True
        
        self.Active = False
    #END TOGGLEOFF()
    
    

Zero.RegisterComponent("Toggler", Toggler)