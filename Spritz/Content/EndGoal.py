import Zero
import Events
import Property
import VectorMath

import Action

class EndGoal:
    DetectEvent = Property.String()
    OwnerEvent = Property.Bool(default = True)
    SpaceEvent = Property.Bool(default = False)
    
    LevelTransitionDelay = Property.Float(default = 4.0)
    
    def Initialize(self, initializer):
        if not self.DetectEvent == "":
            if self.OwnerEvent:
                Zero.Connect(self.Owner, self.DetectEvent, self.onEvent)
                pass
            if self.SpaceEvent:
                Zero.Connect(self.Space, self.DetectEvent, self.onEvent)
                pass
            #endif
        #endif
        
        self.Space.CreateAtPosition("Celebration", self.Owner.Transform.Translation)
    #end init()
    
    def onEvent(self, eEvent):
        gSpace = Zero.Game.FindSpaceByName("GameSpace")
        #Zero.Game.LevelManager.loadNextLevel()
        
        EndEvent = Zero.ScriptEvent()
        self.Space.DispatchEvent("LevelEnd", EndEvent)
        
        player = self.Space.FindObjectByName("MainCharacter")
        player.HUDEventDispatcher.DispatchHUDEvent("LevelEnd", EndEvent)
        
        seq = Action.Sequence(self.Owner)
        Action.Delay(seq, self.LevelTransitionDelay)
        Action.Call(seq, Zero.Game.LevelManager.loadNextLevel)
        #gSpace.LevelManager.loadNextLevel()
        #raise
    #onEvent()

Zero.RegisterComponent("EndGoal", EndGoal)