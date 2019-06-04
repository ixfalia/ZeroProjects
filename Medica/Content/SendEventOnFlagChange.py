import Zero
import Events
import Property
import VectorMath

class SendEventOnFlagChange:
    Flag = Property.String()
    State = Property.String()
    
    EventToSend = Property.String()
    
    OwnerEvent = Property.Bool(default = True)
    SpaceEvent = Property.Bool(default = False)
    GameEvent = Property.Bool(default = False)
    
    def Initialize(self, initializer):
        Zero.Connect(Zero.Game, "DataFlagEvent", self.onFlag)
        
        self.State = eval(self.State)
        
    
    def onFlag(self, fEvent):
        Name = fEvent.FlagName
        State = fEvent.State
        
        print("SendEventOnFlagChange:", Name, State, self.State)
        
        
        if Name == self.Flag and self.State == State:
            self.sendEvent()
    
    def sendEvent(self):
        e = Zero.ScriptEvent()
        
        if self.OwnerEvent:
            self.Owner.DispatchEvent(self.EventToSend, e)
        if self.SpaceEvent:
            self.Space.DispatchEvent(self.EventToSend, e)
        if self.GameEvent:
            Zero.Game.DispatchEvent(self.EventToSend, e)

Zero.RegisterComponent("SendEventOnFlagChange", SendEventOnFlagChange)