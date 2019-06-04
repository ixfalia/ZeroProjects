import Zero
import Events
import Property
import VectorMath

import Action

class LevelTransitionButton:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)s
        self.Active = Property.Bool(default = True)
        self.Level = Property.Level()
        self.Delay = Property.Float(default = 0)
        self.OnEvent = Property.String(default = "")
        self.ResourceTable = Property.ResourceTable()
        pass

    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.MouseDown, self.onEvent)
        if not self.OnEvent == "":
            Zero.Connect(self.Space, self.OnEvent, self.onEvent)
        pass

    def onEvent(self, Event):
        #if Event.Level:
         #   self.Level = self.ResourceTable.FindResource(Event.Level)
        self.Activate()
    
    def Activate(self):
        if not self.Active:
            return
        
        seq = Action.Sequence(self.Owner)
        Action.Delay(seq, self.Delay)
        Action.Call(seq, self.ChangeLevel)
    
    def ChangeLevel(self):
        #self.GameSession.GameStateTracker.UpdateGameData()
        #self.Space.Destroy()
        self.Space.LoadLevel(self.Level)
        
        LevelEvent = Zero.ScriptEvent()
        LevelEvent.Level = self.Level
        print("Changing to new Level:", self.Level)
        self.Space.DispatchEvent("LevelChanged", LevelEvent)
        self.GameSession.DispatchEvent("LevelChanged", LevelEvent)
        pass

Zero.RegisterComponent("LevelTransitionButton", LevelTransitionButton)