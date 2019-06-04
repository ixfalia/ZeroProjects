import Zero
import Events
import Property
import VectorMath
import Action

class GamePauser:
    def Initialize(self, initializer):
        Zero.Connect(self.Space, "GamePauseEvent", self.onGamePause)
        Zero.Connect(self.Space, "LevelBegin", self.onLevel)
        Zero.Connect(self.Space, "myGamepadEvent", self.onGamepad)
        
        self.Paused = False
        self.OtherSpace = None
        self.HowToPlay = self.Space.FindObjectByName("HowToPlay")
        self.Active = False
    
    def onGamePause(self, gEvent):
        self.OtherSpace = gEvent.Space
    
    def onGamepad(self, gEvent):
        if gEvent.Button == Zero.Buttons.Start:
            self.togglePause()
            
            self.Owner.SoundEmitter.PlayCue("Pause")
        
        if self.Paused:
            if gEvent.Button == Zero.Buttons.Back:
                self.togglePause()
                Zero.Game.LevelManager.loadLevelSelect()
                return
                EndEvent = Zero.ScriptEvent()
                self.Space.DispatchEvent("LevelEnd", EndEvent)
                seq = Action.Sequence(self.Owner)
                Action.Delay(seq, 1)
                Action.Call(seq, Zero.Game.LevelManager.loadLevelSelect)
    
    def onLevel(self, lEvent):
        self.Active = True
    
    def togglePause(self):
        if not self.Active:
            return
        
        self.Paused = not self.Paused
        
        self.updatePause()
    
    def updatePause(self):
        self.OtherSpace.TimeSpace.Paused = self.Paused
        self.Owner.SpriteText.Visible = self.Paused
        self.HowToPlay.Sprite.Visible = self.Paused

Zero.RegisterComponent("GamePauser", GamePauser)