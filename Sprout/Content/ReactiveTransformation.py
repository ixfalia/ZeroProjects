import Zero
import Events
import Property
import VectorMath

class ReactiveTransformation:
    hoverEvent = Property.String(default="UIState_Hover")
    resetEvent = Property.String(default="UIState_Default")
    activateEvent = Property.String(default="UIState_Activate")
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, self.resetEvent, self.onReset)
        Zero.Connect(self.Owner, self.hoverEvent, self.onHover)
        Zero.Connect(self.Owner, self.activateEvent, self.onActivate)
            
        pass
    
    def onReset(self, mEvent):
        pass
    
    def onHover(self, mEvent):
        pass
    
    def onActivate(self, mEvent):
        pass
    
    def TranslationAction(self, end, duration = None):
        if not duration:
            duration = 0.15
        
        target = self.Owner.Transform
        
        group = Action.Sequence(self.Owner)
        #end = end + self.Owner.Transform.Translation
        
        Action.Property(group, target, "Translation", end, duration)

Zero.RegisterComponent("ReactiveTransformation", ReactiveTransformation)