import Zero
import Events
import Property
import VectorMath

#Do not use this class to determine movement. It merely works for single button presses
class GamepadDispatcher:
    DebugMode = Property.Bool(default = False)
    DisableControl = Property.Bool(default = False)
    UIDispatcher = Property.Bool(default = False)
    #DetectWhilePaused = Property.Bool(default = False)
    
    deadzone = Property.Float(default = 0.8)
    Gamepad = Zero.Gamepads.GetGamePad(0) # getting first player gamepad
    Timer = 0
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        Zero.Connect(self.Space, "DisableControl", self.disable)
        
    def disable(self, Event):
        self.DisableControl = True
    
    def onUpdate(self, Event):
        if self.DisableControl:
            return
        
        self.Timer += Event.Dt
        
        if( self.Timer >= 0.15 ):
            stick = self.Gamepad.LeftStick
            
            if( stick.y > self.deadzone):
                myGamepadEvent = Zero.ScriptEvent()
                
                myGamepadEvent.Gamepad = self.Gamepad
                myGamepadEvent.Button = Zero.Buttons.DpadUp
                myGamepadEvent.String = "LeftStick:Up"
                
                self.Space.DispatchEvent("myGamepadEvent", myGamepadEvent)
            #endif
            
            if( stick.y < -self.deadzone):
                myGamepadEvent = Zero.ScriptEvent()
                
                myGamepadEvent.Gamepad = self.Gamepad
                myGamepadEvent.Button = Zero.Buttons.DpadDown
                myGamepadEvent.String = "LeftStick:Down"
                
                self.Space.DispatchEvent("myGamepadEvent", myGamepadEvent)
            #endif
            
            if( stick.x > self.deadzone):
                myGamepadEvent = Zero.ScriptEvent()
                
                myGamepadEvent.Gamepad = self.Gamepad
                myGamepadEvent.Button = Zero.Buttons.DpadRight
                myGamepadEvent.String = "LeftStick:Right"
                
                self.Space.DispatchEvent("myGamepadEvent", myGamepadEvent)
            #endif
            if( stick.x < -self.deadzone):
                myGamepadEvent = Zero.ScriptEvent()
                
                myGamepadEvent.Gamepad = self.Gamepad
                myGamepadEvent.Button = Zero.Buttons.DpadLeft
                myGamepadEvent.String = "LeftStick:Left"
                
                self.Space.DispatchEvent("myGamepadEvent", myGamepadEvent)
            #endif
            self.Timer = 0
        #endif
        
        if(self.Gamepad.IsButtonPressed(Zero.Buttons.DpadUp)):
            myGamepadEvent = Zero.ScriptEvent()
            
            myGamepadEvent.Gamepad = self.Gamepad
            myGamepadEvent.Button = Zero.Buttons.DpadUp
            myGamepadEvent.String = "Up"
            
            self.Space.DispatchEvent("myGamepadEvent", myGamepadEvent)
        #endif
        if(self.Gamepad.IsButtonPressed(Zero.Buttons.DpadDown)):
            myGamepadEvent = Zero.ScriptEvent()
            
            myGamepadEvent.Gamepad = self.Gamepad
            myGamepadEvent.Button = Zero.Buttons.DpadDown
            myGamepadEvent.String = "Down"
            
            self.Space.DispatchEvent("myGamepadEvent", myGamepadEvent)
        #endif
        if(self.Gamepad.IsButtonPressed(Zero.Buttons.DpadLeft)):
            myGamepadEvent = Zero.ScriptEvent()
            
            myGamepadEvent.Gamepad = self.Gamepad
            myGamepadEvent.Button = Zero.Buttons.DpadLeft
            myGamepadEvent.String = "Left"
            
            self.Space.DispatchEvent("myGamepadEvent", myGamepadEvent)
        #endif
        if(self.Gamepad.IsButtonPressed(Zero.Buttons.DpadRight)):
            myGamepadEvent = Zero.ScriptEvent()
            
            myGamepadEvent.Gamepad = self.Gamepad
            myGamepadEvent.Button = Zero.Buttons.DpadRight
            myGamepadEvent.String = "Right"
            
            self.Space.DispatchEvent("myGamepadEvent", myGamepadEvent)
        #endif
        if(self.Gamepad.IsButtonPressed(Zero.Buttons.A)):
            myGamepadEvent = Zero.ScriptEvent()
            
            myGamepadEvent.Gamepad = self.Gamepad
            myGamepadEvent.Button = Zero.Buttons.A
            myGamepadEvent.String = "A"
            
            self.Space.DispatchEvent("myGamepadEvent", myGamepadEvent)
        #endif
        if(self.Gamepad.IsButtonPressed(Zero.Buttons.B)):
            myGamepadEvent = Zero.ScriptEvent()
            
            myGamepadEvent.Gamepad = self.Gamepad
            myGamepadEvent.Button = Zero.Buttons.B
            myGamepadEvent.String = "B"
            
            self.Space.DispatchEvent("myGamepadEvent", myGamepadEvent)
        #endif
        if(self.Gamepad.IsButtonPressed(Zero.Buttons.X)):
            myGamepadEvent = Zero.ScriptEvent()
            
            myGamepadEvent.Gamepad = self.Gamepad
            myGamepadEvent.Button = Zero.Buttons.X
            myGamepadEvent.String = "X"
            
            self.Space.DispatchEvent("myGamepadEvent", myGamepadEvent)
        #endif
        if(self.Gamepad.IsButtonPressed(Zero.Buttons.Y)):
            myGamepadEvent = Zero.ScriptEvent()
            
            myGamepadEvent.Gamepad = self.Gamepad
            myGamepadEvent.Button = Zero.Buttons.Y
            myGamepadEvent.String = "Y"
            
            self.Space.DispatchEvent("myGamepadEvent", myGamepadEvent)
        #endif
        if(self.Gamepad.IsButtonPressed(Zero.Buttons.LeftShoulder)):
            myGamepadEvent = Zero.ScriptEvent()
            
            myGamepadEvent.Gamepad = self.Gamepad
            myGamepadEvent.Button = Zero.Buttons.LeftShoulder
            myGamepadEvent.String = "LeftShoulder"
            
            self.Space.DispatchEvent("myGamepadEvent", myGamepadEvent)
        #endif
        if(self.Gamepad.IsButtonPressed(Zero.Buttons.RightShoulder)):
            myGamepadEvent = Zero.ScriptEvent()
            
            myGamepadEvent.Gamepad = self.Gamepad
            myGamepadEvent.Button = Zero.Buttons.RightShoulder
            myGamepadEvent.String = "RightShoulder"
            
            self.Space.DispatchEvent("myGamepadEvent", myGamepadEvent)
        #endif
        if(self.Gamepad.IsButtonPressed(Zero.Buttons.Start)):
            myGamepadEvent = Zero.ScriptEvent()
            
            myGamepadEvent.Gamepad = self.Gamepad
            myGamepadEvent.Button = Zero.Buttons.Start
            myGamepadEvent.String = "Start"
            
            self.Space.DispatchEvent("myGamepadEvent", myGamepadEvent)
        #endif
        if(self.Gamepad.IsButtonPressed(Zero.Buttons.Back)):
            myGamepadEvent = Zero.ScriptEvent()
            
            myGamepadEvent.Gamepad = self.Gamepad
            myGamepadEvent.Button = Zero.Buttons.Back
            myGamepadEvent.String = "Back"
            
            self.Space.DispatchEvent("myGamepadEvent", myGamepadEvent)
        #endif
    #enddef
#endclass

Zero.RegisterComponent("GamepadDispatcher", GamepadDispatcher)