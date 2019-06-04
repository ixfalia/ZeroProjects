import Zero
import Events
import Property
import VectorMath

class MouseController:
    Debug = Property.Bool(default = True)
    
    Disabled = Property.Bool(default=False)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.MouseDown, self.onMouseDown)
        Zero.Connect(self.Space, Events.RightMouseDown, self.onRightMouseDown)
        
        Zero.Connect(self.Space, "ReactiveEnter", self.onReactive)
        Zero.Connect(self.Space, "ReactiveExit", self.onReactiveExit)
        
        Zero.Connect(self.Space, "PauseEvent", self.onDisable)
        Zero.Connect(self.Space, "FreezeEvent", self.onDisable)
        Zero.Connect(self.Space, "UnpauseEvent", self.onEnble)
        Zero.Connect(self.Space, "UnfreezeEvent", self.onEnble)
        
        self.isMoveableTerrain = True
        self.Paused = False
    
    def onRightMouseDown(self, e):
        if self.isMoveableTerrain and not self.Paused:
            self.Owner.MovementController.onRightMouseDown(e)
    
    def onMouseDown(self, e):
        pass
    
    def onReactive(self, e):
        self.isMoveableTerrain = False
        
        if self.Debug:
            print("Hovering Mouse over Event Object.")
    
    def onReactiveExit(self, e):
        self.isMoveableTerrain = True
        
        if self.Debug:
            print("Mouse Entered Moveable Terrain.")
    
    def onDisable(self, e):
        self.disable()
    
    def onEnble(self, e):
        self.enable()
    
    def disable(self):
        self.Paused = True
    
    def enable(self):
        self.Paused = False
    
Zero.RegisterComponent("MouseController", MouseController)