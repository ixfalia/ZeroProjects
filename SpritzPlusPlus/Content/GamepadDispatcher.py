import Zero
import Events
import Property
import VectorMath

#Do not use this class to determine movement. It merely works for single button presses
class GamepadDispatcher:
    DebugMode = Property.Bool(default = False)
    DisableControl = Property.Bool(default = False)
    DetectControlEvents = Property.Bool(default = True)
    #DetectWhilePaused = Property.Bool(default = False)
    
    spaceEvents = Property.Bool(default = True)
    ownerEvents = Property.Bool(default = False)
    
    deadzone = Property.Float(default = 0.8)
    #Gamepad = Zero.Gamepads.GetGamePad(0) # getting first player gamepad
    Timer = 0
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        Zero.Connect(self.Space, "myGamepadEvent", self.onGamepad)
        Zero.Connect(self.Owner, "myGamepadEvent", self.onGamepad)
        print("GamepadDispatcher.Initialize()")
        
        if self.DetectControlEvents:
            Zero.Connect(self.Space, "DisableControl", self.disable)
        
        self.controllerDetected = self.detectController()
        
        if not self.controllerDetected:
            print("Controller not detected")
            self.Space.CreateAtPosition("Menu_ControllerPlugin", VectorMath.Vec3())
    #enddef
    
    def onGamepad(self, e):
        if self.DebugMode:
            print("GamepadDispatcher:", e.String, "button")
    
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
    
    def onAnyButton(self, gEvent = None):
        print("boop")
        obj = self.Space.FindObjectByName("controllerPlug")
        obj.Destroy()
    
    def disable(self, Event):
        self.DisableControl = True
    
    def detectControlEvents(self):
        if self.DetectControlEvents:
            return
        
        self.DetectControlEvents = True
        Zero.Connect(self.Space, "DisableControl", self.disable)
    
    def disableControlEvents(self):
        if not self.DetectControlEvents:
            return
        
        self.DetectControlEvents = False
        Zero.Disconnect(self.Space, "DisableControl", self.disable)
    
    def onUpdate(self, Event):
        if self.DisableControl:
            return
        
        self.Timer += Event.Dt
        
        if not self.controllerDetected:
            self.controllerDetected = self.detectController()
            
            if self.controllerDetected:
                self.onAnyButton()
        
        if( self.Timer >= 0.15 ):
            stick = self.Gamepad.LeftStick
            self.CheckStick(stick, "Left")
            
            stick = self.Gamepad.RightStick
            self.CheckStick(stick, "Right")
            
            self.Timer = 0
        #endif
        
        if(self.Gamepad.IsButtonPressed(Zero.Buttons.DpadUp)):
            myGamepadEvent = Zero.ScriptEvent()
            
            myGamepadEvent.Gamepad = self.Gamepad
            myGamepadEvent.Button = Zero.Buttons.DpadUp
            myGamepadEvent.String = "Up"
            
            #self.Space.DispatchEvent("myGamepadEvent", myGamepadEvent)
            self.dispatchEvents("myGamepadEvent", myGamepadEvent)
        #endif
        if(self.Gamepad.IsButtonPressed(Zero.Buttons.DpadDown)):
            myGamepadEvent = Zero.ScriptEvent()
            
            myGamepadEvent.Gamepad = self.Gamepad
            myGamepadEvent.Button = Zero.Buttons.DpadDown
            myGamepadEvent.String = "Down"
            
            #self.Space.DispatchEvent("myGamepadEvent", myGamepadEvent)
            self.dispatchEvents("myGamepadEvent", myGamepadEvent)
        #endif
        if(self.Gamepad.IsButtonPressed(Zero.Buttons.DpadLeft)):
            myGamepadEvent = Zero.ScriptEvent()
            
            myGamepadEvent.Gamepad = self.Gamepad
            myGamepadEvent.Button = Zero.Buttons.DpadLeft
            myGamepadEvent.String = "Left"
            
            #self.Space.DispatchEvent("myGamepadEvent", myGamepadEvent)
            self.dispatchEvents("myGamepadEvent", myGamepadEvent)
        #endif
        if(self.Gamepad.IsButtonPressed(Zero.Buttons.DpadRight)):
            myGamepadEvent = Zero.ScriptEvent()
            
            myGamepadEvent.Gamepad = self.Gamepad
            myGamepadEvent.Button = Zero.Buttons.DpadRight
            myGamepadEvent.String = "Right"
            
            #self.Space.DispatchEvent("myGamepadEvent", myGamepadEvent)
            self.dispatchEvents("myGamepadEvent", myGamepadEvent)
        #endif
        if(self.Gamepad.IsButtonPressed(Zero.Buttons.A)):
            myGamepadEvent = Zero.ScriptEvent()
            
            myGamepadEvent.Gamepad = self.Gamepad
            myGamepadEvent.Button = Zero.Buttons.A
            myGamepadEvent.String = "A"
            
            #self.Space.DispatchEvent("myGamepadEvent", myGamepadEvent)
            self.dispatchEvents("myGamepadEvent", myGamepadEvent)
        #endif
        if(self.Gamepad.IsButtonPressed(Zero.Buttons.B)):
            myGamepadEvent = Zero.ScriptEvent()
            
            myGamepadEvent.Gamepad = self.Gamepad
            myGamepadEvent.Button = Zero.Buttons.B
            myGamepadEvent.String = "B"
            
            #self.Space.DispatchEvent("myGamepadEvent", myGamepadEvent)
            self.dispatchEvents("myGamepadEvent", myGamepadEvent)
        #endif
        if(self.Gamepad.IsButtonPressed(Zero.Buttons.X)):
            myGamepadEvent = Zero.ScriptEvent()
            
            myGamepadEvent.Gamepad = self.Gamepad
            myGamepadEvent.Button = Zero.Buttons.X
            myGamepadEvent.String = "X"
            
            #self.Space.DispatchEvent("myGamepadEvent", myGamepadEvent)
            self.dispatchEvents("myGamepadEvent", myGamepadEvent)
        #endif
        if(self.Gamepad.IsButtonPressed(Zero.Buttons.Y)):
            myGamepadEvent = Zero.ScriptEvent()
            
            myGamepadEvent.Gamepad = self.Gamepad
            myGamepadEvent.Button = Zero.Buttons.Y
            myGamepadEvent.String = "Y"
            
            #self.Space.DispatchEvent("myGamepadEvent", myGamepadEvent)
            self.dispatchEvents("myGamepadEvent", myGamepadEvent)
        #endif
        if(self.Gamepad.IsButtonPressed(Zero.Buttons.LeftShoulder)):
            myGamepadEvent = Zero.ScriptEvent()
            
            myGamepadEvent.Gamepad = self.Gamepad
            myGamepadEvent.Button = Zero.Buttons.LeftShoulder
            myGamepadEvent.String = "LeftShoulder"
            
            #self.Space.DispatchEvent("myGamepadEvent", myGamepadEvent)
            self.dispatchEvents("myGamepadEvent", myGamepadEvent)
        #endif
        if(self.Gamepad.IsButtonPressed(Zero.Buttons.RightShoulder)):
            myGamepadEvent = Zero.ScriptEvent()
            
            myGamepadEvent.Gamepad = self.Gamepad
            myGamepadEvent.Button = Zero.Buttons.RightShoulder
            myGamepadEvent.String = "RightShoulder"
            
            #self.Space.DispatchEvent("myGamepadEvent", myGamepadEvent)
            self.dispatchEvents("myGamepadEvent", myGamepadEvent)
        #endif
        if(self.Gamepad.IsButtonPressed(Zero.Buttons.Start)):
            myGamepadEvent = Zero.ScriptEvent()
            
            myGamepadEvent.Gamepad = self.Gamepad
            myGamepadEvent.Button = Zero.Buttons.Start
            myGamepadEvent.String = "Start"
            
            #self.Space.DispatchEvent("myGamepadEvent", myGamepadEvent)
            self.dispatchEvents("myGamepadEvent", myGamepadEvent)
        #endif
        if(self.Gamepad.IsButtonPressed(Zero.Buttons.Back)):
            myGamepadEvent = Zero.ScriptEvent()
            
            myGamepadEvent.Gamepad = self.Gamepad
            myGamepadEvent.Button = Zero.Buttons.Back
            myGamepadEvent.String = "Back"
            
            #self.Space.DispatchEvent("myGamepadEvent", myGamepadEvent)
            self.dispatchEvents("myGamepadEvent", myGamepadEvent)
        #endif
    #enddef
    
    def CheckStick(self, stick, name):
        if( stick.y > self.deadzone):
                myGamepadEvent = Zero.ScriptEvent()
                
                myGamepadEvent.Gamepad = self.Gamepad
                myGamepadEvent.Button = Zero.Buttons.DpadUp
                myGamepadEvent.String = "{0}Stick:Up".format(name)
                
                #self.Space.DispatchEvent("myGamepadEvent", myGamepadEvent)
                self.dispatchEvents("myGamepadEvent", myGamepadEvent)
            #endif
        
        if( stick.y < -self.deadzone):
            myGamepadEvent = Zero.ScriptEvent()
            
            myGamepadEvent.Gamepad = self.Gamepad
            myGamepadEvent.Button = Zero.Buttons.DpadDown
            myGamepadEvent.String = "{0}Stick:Down".format(name)
            
            #self.Space.DispatchEvent("myGamepadEvent", myGamepadEvent)
            self.dispatchEvents("myGamepadEvent", myGamepadEvent)
        #endif
        
        if( stick.x > self.deadzone):
            myGamepadEvent = Zero.ScriptEvent()
            
            myGamepadEvent.Gamepad = self.Gamepad
            myGamepadEvent.Button = Zero.Buttons.DpadRight
            myGamepadEvent.String = "{0}Stick:Right".format(name)
            
            #self.Space.DispatchEvent("myGamepadEvent", myGamepadEvent)
            self.dispatchEvents("myGamepadEvent", myGamepadEvent)
        #endif
        if( stick.x < -self.deadzone):
            myGamepadEvent = Zero.ScriptEvent()
            
            myGamepadEvent.Gamepad = self.Gamepad
            myGamepadEvent.Button = Zero.Buttons.DpadLeft
            myGamepadEvent.String = "{0}Stick:Left".format(name)
            
            #self.Space.DispatchEvent("myGamepadEvent", myGamepadEvent)
            self.dispatchEvents("myGamepadEvent", myGamepadEvent)
        #endif
        
        if( stick.x < -self.deadzone or stick.y < -self.deadzone or stick.x > self.deadzone or stick.y > self.deadzone):
            myGamepadEvent = Zero.ScriptEvent()
            
            myGamepadEvent.Gamepad = self.Gamepad
            myGamepadEvent.Button = None
            myGamepadEvent.String = "{0}Stick".format(name)
            
            self.dispatchEvents("myGamepadEvent", myGamepadEvent)
    #enddef
    
    def dispatchEvents(self, name, Event):
        if self.ownerEvents:
            self.Owner.DispatchEvent(name, Event)
        if self.spaceEvents:
            self.Space.DispatchEvent(name, Event)
#endclass

Zero.RegisterComponent("GamepadDispatcher", GamepadDispatcher)