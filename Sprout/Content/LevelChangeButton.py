import Zero
import Events
import Property
import VectorMath

import Action

class LevelChangeButton:
    DebugMode = Property.Bool( default = False )
    LevelChange = Property.Level()
    useLevelTable = Property.Bool(default = False)
    PlaySoundOnPress = Property.SoundCue()
    
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
        
        #self.Space.LoadLevel( self.LevelChange )
        self.activate()
        
    def activate(self):
        Playsound = False
        print(self.PlaySoundOnPress.Name)
        if not self.PlaySoundOnPress.Name == "DefaultCue":
            self.Owner.SoundEmitter.PlayCue(self.PlaySoundOnPress)
            Playsound = True
            #raise
        
        seq=Action.Sequence(self.Owner)
        Action.Delay(seq, 1.5)
        
        if not self.useLevelTable:
            if Playsound:
                Action.Call(seq, self.Space.LoadLevel,(self.LevelChange))
                
            else:
                if self.LevelChange.Name == "TitleScreen":
                    self.GameSession.LevelManager.loadLevelName(self.LevelChange.Name)
                else:
                    self.Space.LoadLevel(self.LevelChange)
                
        else:
            if Playsound:
                Action.Call(seq, self.GameSession.LevelManager.loadNextLevel)
                
            else:
                self.GameSession.LevelManager.loadNextLevel()
#end Class

Zero.RegisterComponent("LevelChangeButton", LevelChangeButton)