import Zero
import Events
import Property
import VectorMath
import Keys

Keys = Zero.Keys
Vec3 = VectorMath.Vec3

class GamepadController:
    DebugMode = Property.Bool(default = True)
    Paused = Property.Bool(default = False)
    deadzone = Property.Float(default = 0.2)
    disableControlPad = Property.Bool(default = False)
    detectEvents = Property.Bool(default = True)
    
    Timer = 0
    soundTimer = 0
    MovementFrame = Vec3()
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.onLogicUpdate)
        
        if self.detectEvents:
            Zero.Connect(self.Space, "DisableControl", self.disable)
            Zero.Connect(self.Space, "EnableControl", self.enable)
        
        for i in range(0,3):
            self.Gamepad = Zero.Gamepads.GetGamePad(i)
            
            if self.Gamepad:
                break
        
        if not self.Gamepad:
            print("GamepadController.Initialize(): Gamepad not detected")
    #end def Initialize()
    
    def onLogicUpdate(self, UpdateEvent):
        checkloops = False
        
        if self.DebugMode and checkloops:
            print("GamepadController.onLogicUpdate(): Called")
        
        #self.grabPlayerInput(UpdateEvent.Dt)
        #self.applyMovement()
        #self.applyInput()
        
        self.inputOctopus(UpdateEvent.Dt)
    #end def OnLogicUpdate
    
    def enableEventDetection(self):
        if self.detectEvents:
            return
        
        self.detectEvents = True
        
        Zero.Connect(self.Space, "DisableControl", self.disable)
        Zero.Connect(self.Space, "EnableControl", self.enable)
    
    def disableEventDetection(self):
        if not self.detectEvents:
            return
        
        self.detectEvents = False
        
        Zero.Disconnect(self.Space, "DisableControl", self.disable)
        Zero.Disconnect(self.Space, "EnableControl", self.enable)
    
    def grabPlayerInput(self, DT):
        #Movement set
        self.moveLeft = self.Gamepad.IsButtonPressed(Zero.Buttons.DpadLeft)
        self.moveRight = self.Gamepad.IsButtonPressed(Zero.Buttons.DpadRight)
        
        self.checkIfActive(self.moveLeft, "Left Dpad Button")
        self.checkIfActive(self.moveRight, "Right Dpad Button")
        
        #jump set
        rightShoulder = self.Gamepad.IsButtonPressed(Zero.Buttons.RightShoulder)
        leftShoulder = self.Gamepad.IsButtonPressed(Zero.Buttons.LeftShoulder)
        
        self.checkIfActive(rightShoulder, "Right Shoulder")
        self.checkIfActive(leftShoulder, "Left Shoulder")
        
        #checking the jump inputs
        self.jump = self.Gamepad.IsButtonPressed(Zero.Buttons.A) or leftShoulder or rightShoulder
        
        self.checkIfActive(self.jump, "Jump")
        
        #Interaction set
        self.interact = self.Gamepad.IsButtonPressed(Zero.Buttons.DpadDown)
        self.lookUp = self.Gamepad.IsButtonPressed(Zero.Buttons.DpadUp)
        
        self.checkIfActive(self.interact, "Dpad Down")
        self.checkIfActive(self.lookUp, "Dpad Up")
        
        #Water Set
        rightTriggerStrength = self.Gamepad.RightTrigger
        leftTriggerStrength = self.Gamepad.LeftTrigger
        
        triggerStrength = max(rightTriggerStrength, leftTriggerStrength)
        
        if abs(triggerStrength) > 0.2:
            #self.Owner.Sprinkler.Shoot()
            self.HandleTrigger(triggerStrength, DT)
            pass
        self.waterPressure = triggerStrength
        
        pass
    #end def grabPlayerInput()
    
    def applyMovement(self):
        
        Leftstick = self.Gamepad.LeftStick
        
        usingLeftStick = Leftstick.x > self.deadzone or Leftstick.x < -self.deadzone or Leftstick.y > self.deadzone or Leftstick.y < -self.deadzone
        
        if usingLeftStick:
            if self.DebugMode:
                print("GamepadController.applyMovement(): Using the Left stick")
            #endif
        else:
            if self.moveLeft:
                self.Owner.MovementController.Move(VectorMath.Vec3(-1,0,0))
            if self.moveRight:
                self.Owner.MovementController.Move(VectorMath.Vec3(1,0,0))
        #endif
        
        pass
    #end def applyMovement
    
    def applyInput(self):
        Rightstick = self.Gamepad.RightStick
        
        if self.waterPressure > 0.08:
            if self.DebugMode:
                print("GamepadController.applyInput(): calling WaterTank")
            self.Owner.Sprinkler.Shoot(self.waterPressure) #perhaps spend time to make this more message based
        
        usingRightStick = Rightstick.x > self.deadzone or Rightstick.x < -self.deadzone or Rightstick.y > self.deadzone or Rightstick.y < -self.deadzone
        
        if usingRightStick:
            self.Owner.Sprinkler.ShootStick(Rightstick)
            pass
        pass
    #end def applyInput()
    
    def checkIfActive(self, isActive, name):
        if self.DebugMode:
            if isActive:
                print("GamepadController.checkIfActive(): The " + name + " button is Active.")
    #end def checkIfActive()
    
    def inputOctopus(self, DT):
        self.MovementFrame = self.Gamepad.LeftStick
        
        #this is the speed we will move at
        #self.speed = 2.0
        self.Timer += DT
        self.soundTimer += DT
        
        if self.disableControlPad:
            return
            pass
        
        #print(Event.Dt)
        
        if( self.Timer >= 0.03 ):
            if(self.Gamepad.LeftTrigger > 0):
                self.HandleTrigger(self.Gamepad.LeftTrigger, DT)
            #endif        
            if(self.Gamepad.RightTrigger > 0):
                self.HandleTrigger(self.Gamepad.RightTrigger, DT)
            else:
                self.Owner.MovementController.HandleRightStick( self.Gamepad.RightStick, self.deadzone )
            #endif
            
            if(self.Gamepad.IsButtonHeld(Zero.Buttons.Y)):
                self.HandleTrigger(0.9, DT)
                pass
            elif(self.Gamepad.IsButtonHeld(Zero.Buttons.X)):
                self.HandleTrigger(0.9, DT)
                pass
            #endif
            
            self.Timer = 0
        #endif
        
        ### Movement Code ###
        #####################
        if( self.MovementFrame.x < 0 ):
            self.Owner.Sprite.FlipX = False
        elif( self.MovementFrame.x > 0 ):
            self.Owner.Sprite.FlipX = True
        #endif
        
        if(self.Gamepad.IsButtonPressed(Zero.Buttons.A)):
            self.Owner.MovementController.Jump()
        elif(self.Gamepad.IsButtonReleased(Zero.Buttons.A)):
            self.Owner.MovementController.EndJump()
        #endif
        
        if(self.Gamepad.IsButtonPressed(Zero.Buttons.B)):
            self.Owner.MovementController.Jump()
        elif(self.Gamepad.IsButtonReleased(Zero.Buttons.B)):
            self.Owner.MovementController.EndJump()
        #endif
        
        if(self.Gamepad.IsButtonPressed(Zero.Buttons.RightShoulder) or self.Gamepad.IsButtonPressed(Zero.Buttons.LeftShoulder)):
            #for some reason pressing A makes you jump higher, this number is to even them
            self.Owner.MovementController.Jump()
        elif(self.Gamepad.IsButtonReleased(Zero.Buttons.RightShoulder) or self.Gamepad.IsButtonReleased(Zero.Buttons.LeftShoulder)):
            self.Owner.MovementController.EndJump()
        #endif
        
        #Move with physics
        #self.jumping = not self.Owner.DynamicController.OnGround
        
        #endif
        #self.Owner.DynamicController.MoveInDirection(self.MovementFrame * float(self.speed))
        if self.MovementFrame.x != 0 and self.MovementFrame.y != 0:
            self.Owner.MovementController.Move(self.MovementFrame)
    #end inputOctopus()
    
    def HandleTrigger(self, triggerStrength, DT):
        #if I want to I could differentiate between trigger behaviors
        #for now I'm going to treat them the same
        #self.Owner.PlayerController.Spray(TriggerValue)
        self.Owner.Sprinkler.ShootStick(Vec3(0,-1,0) * triggerStrength)
    #end HandleTrigger()
    
    def disable(self):
        print("GamepadController.Disable()")
        self.disableControlPad = True
    
    def enable(self):
        print("GamepadController.enable()")
        self.disableControlPad = False
    
#end class GamepadController

Zero.RegisterComponent("GamepadController", GamepadController)