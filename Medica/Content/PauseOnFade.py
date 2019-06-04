import Zero
import Events
import Property
import VectorMath

class PauseOnFade:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "FadeInEvent", self.onFadeIn)
        Zero.Connect(self.Owner, "FadeOutEvent", self.onFadeOut)
    
    def onFadeIn(self, fEvent):
        e = Zero.ScriptEvent()
        
        spaceDispatcher = Zero.Game.GameSpaceEventDispatcher
        spaceDispatcher.DispatchGameSpaceEvent("FreezeEvent", e)
        
        self.Space.DispatchEvent("PauseEvent", e)
        
    def onFadeOut(self, fEvent):
        e = Zero.ScriptEvent()
        
        spaceDispatcher = Zero.Game.GameSpaceEventDispatcher
        spaceDispatcher.DispatchGameSpaceEvent("UnfreezeEvent", e)
        
        self.Space.DispatchEvent("UnpauseEvent", e)

Zero.RegisterComponent("PauseOnFade", PauseOnFade)