import Zero
import Events
import Property
import VectorMath

import Color
import Action

class LevelChangeButton:
    DebugMode = Property.Bool( default = False )
    LevelChange = Property.Level()
    useLevelTable = Property.Bool(default = False)
    loadNextLevel = Property.Bool(default = False)
    
    ChangeDelay = Property.Float(default = 0)
    
    def Initialize(self, initializer):
         # Hook up the mouse events that I'll receive from the Reactive component.
        #Zero.Connect(self.Owner, Events.MouseEnter, self.onMouseEnter)
        #Zero.Connect(self.Owner, Events.MouseExit, self.onMouseExit)
        #Zero.Connect(self.Owner, Events.MouseUp, self.onMouseUp)
        Zero.Connect(self.Owner, Events.MouseDown, self.onMouseDown)
        Zero.Connect(self.Owner, "ActivateButton", self.onActivate)
        #Zero.Connect(self.Owner, Events.LevelStarted, self.onLevel)
        #Zero.Connect(self.Space, "ActivateButton", self.onActivate)
        
        #if self.Owner.SpriteText:
            #self.Owner.SpriteText.Text += ": " + self.LevelChange.Name
        
    
    def onLevel(self, e):
        button = self.LevelChange
        
        index = Zero.Game.LevelManager.levelTable.FindIndexOfResource(button)
        data = Zero.Game.AccomplishmentDataManager.getLevelData(index)
        
        if data.Played:
            self.Owner.Sprite.Color = Color.CadetBlue
        else:
            self.Owner.Sprite.Color = Color.Firebrick
        
    def onMouseDown(self, Event):
        if(self.DebugMode):
            print("Mouse Down")
        
        if self.ChangeDelay > 0:
            seq = Action.Sequence(self.Owner)
            Action.Delay(seq, self.ChangeDelay)
            Action.Call(seq, self.loadLevel)
        else:
            self.loadLevel()
    
    def loadLevel(self):
        Zero.Game.LevelManager.loadLevelLevel(self.LevelChange)
        self.Space.Destroy()
    
    def activate(self):
        print( "LevelChangeButton.activate():\n\tLevel Changing to:", self.LevelChange.Name)
        if self.loadNextLevel:
            #raise
            Zero.Game.LevelManager.loadNextLevel()
            return
        elif self.useLevelTable:
            #raise
            Zero.Game.LevelManager.loadLevelLevel(self.LevelChange)
            return
        else:
            raise
            self.Space.LoadLevel(self.LevelChange)
            return
    
    def onActivate(self, aEvent):
        self.activate()
#end Class

Zero.RegisterComponent("LevelChangeButton", LevelChangeButton)