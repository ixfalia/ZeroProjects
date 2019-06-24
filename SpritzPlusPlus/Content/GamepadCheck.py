import Zero
import Events
import Property
import VectorMath

import Action

class GamepadCheck:
    DebugMode = Property.Bool(default = True)
    WaitTime = Property.Float(default = 2)
    
    def Initialize(self, initializer):
        self.Gamepad = None
        self.controllerFound = False
        self.Timer = 0
        self.Waiting = True
        
        self.startup()
        #Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
    
    def startup(self):
        detected = self.detectController()
        
        if detected:
            Zero.Connect(self.Space, "myGamepadEvent", self.onGamepad)
        
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
    
    def onUpdate(self, uEvent):
        self.Timer += uEvent.Dt
        
        if self.Timer >= self.WaitTime:
            detected = self.detectController()
            
            if detected and self.Waiting:
                print("waiting:", self.Waiting)
                self.Timer = 0
                self.WaitTime = self.Owner.Fader.FadeOutDuration
                self.Waiting = False
                self.FadeOut()
                #self.controllerDetected()
            elif detected and not self.Waiting:
                self.NextLevel()
    
    def onGamepad(self, gEvent):
        self.NextLevel()
    
    def controllerDetected(self):
        print("ControllerFound:", self.controllerFound)
        if self.controllerFound:
            return
        
        self.controllerFound = True
        transitionTime = 0#1.5
        fadeTime = self.Owner.Fader.FadeOutDuration
        
        if self.DebugMode:
            print("GamepadCheck.controllerDetected(): Entering next level in", transitionTime+fadeTime, "seconds")
            print("ControllerFound: ", self.controllerFound)
        
        #seq = Action.Sequence(self.Owner)
        
        Action.Delay(self.seq, transitionTime)
        #self.Owner.Fader.FadeOut()
        #Action.Call(seq, self.Owner.Fader.FadeOut)
        Action.Delay(self.seq, fadeTime)
        #Action.Call(seq, self.NextLevel)
        Action.Call(self.seq, self.Owner.Destroy)
    
    def FadeOut(self):
        self.Owner.Fader.FadeOut()
    
    def NextLevel(self):
        self.GameSession.LevelManager.loadNextLevel()
    
    def detectController(self):
        for i in range(0,3):
            self.Gamepad = Zero.Gamepads.GetGamePad(i)
            
            if self.Gamepad:
                break
            #endif
        #end for
        
        if self.Gamepad:
            return True
        else:
            return False
    #enddef

Zero.RegisterComponent("GamepadCheck", GamepadCheck)