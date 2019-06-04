import Zero
import Events
import Property
import VectorMath

class LockAspect:
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevelStart)
        
    def onLevelStart(self, Event):
        Viewport = Event.Viewport
        Viewport.TargetAspectRatio =  1.5
        print("LockAspect.onLevelStart() Aspect Set to:", Viewport.TargetAspectRatio)

Zero.RegisterComponent("LockAspect", LockAspect)