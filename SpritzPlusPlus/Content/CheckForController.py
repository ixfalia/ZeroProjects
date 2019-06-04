import Zero
import Events
import Property
import VectorMath

class CheckForController:
    gamepad = Zero.Gamepads.GetGamePad(0)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.update)
    
    def update(self, Event):
        gamepad = Zero.Gamepads.GetGamePad(0)
        print("getgamepad")
        if self.gamepad == None:
            print("no gamepad")

Zero.RegisterComponent("CheckForController", CheckForController)