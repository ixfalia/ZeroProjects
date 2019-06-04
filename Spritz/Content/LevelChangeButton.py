import Zero
import Events
import Property
import VectorMath

class LevelChangeButton:
    DebugMode = Property.Bool( default = False )
    LevelChange = Property.Level()
    useLevelTable = Property.Bool(default = False)
    
    def Initialize(self, initializer):
         # Hook up the mouse events that I'll receive from the Reactive component.
        Zero.Connect(self.Owner, Events.MouseEnter, self.onMouseEnter)
        Zero.Connect(self.Owner, Events.MouseExit, self.onMouseExit)
        Zero.Connect(self.Owner, Events.MouseUp, self.onMouseUp)
        Zero.Connect(self.Owner, Events.MouseDown, self.onMouseDown)
    
    def onMouseEnter(self, Event):
        if(self.DebugMode):
            print("Mouse Enter")
    
    def onMouseExit(self, Event):
        if(self.DebugMode):
            print("Mouse Exit")
        
    def onMouseUp(self, Event):
        if(self.DebugMode):
            print("Mouse Up")
    
    def onMouseDown(self, Event):
        if(self.DebugMode):
            print("Mouse Down")
        
        self.Space.LoadLevel( self.LevelChange )
        
    def activate(self):
        if not self.useLevelTable:
            self.Space.LoadLevel(self.LevelChange)
        else:
            Zero.Game.LevelManager.loadNextLevel()
#end Class

Zero.RegisterComponent("LevelChangeButton", LevelChangeButton)