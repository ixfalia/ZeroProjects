import Zero
import Events
import Property
import VectorMath

class LevelChangeButton:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        self.Active = Property.Bool(default = True)
        self.Level = Property.Level()
        pass

    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, Events.MouseDown, self.onMouseDown)
        pass

    def OnLogicUpdate(self, UpdateEvent):
        pass
    
    def onMouseDown(self, mEvent):
        self.changeLevel()
    
    def changeLevel(self):
        if not self.Active:
            return
        
        self.Space.DestroyAllFromLevel()
        self.Space.LoadLevel(self.Level)
    
    def changeTargetLevel(self, Level):
        
        self.Level = Level

Zero.RegisterComponent("LevelChangeButton", LevelChangeButton)