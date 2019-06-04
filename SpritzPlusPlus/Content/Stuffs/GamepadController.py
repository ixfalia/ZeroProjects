import Zero
import Events
import Property
import VectorMath
import PlayerController
import Keys

#Useful Variables
Keys = Zero.Keys
Vec3 = VectorMath.Vec3

class GamepadController:
    DebugMode = Property.Bool(default = False)
    deadzone = Property.Float(default = 0.2)
    MovementFrame = Vec3()
    Floating = False
    Timer = 0
    soundTimer = 0
    
    jumping = False
    DisableControlPad = Property.Bool(default = False)
    
    Gamepad = Zero.Gamepads.GetGamePad(0) # getting first player gamepad
    
    def Initialize(self, initializer):
        Zero.Connect( self.Space, Events.ButtonUp, self.onButtonUp )
        Zero.Connect( self.Space, Events.ButtonDown, self.onButtonDown )
        Zero.Connect( self.Space, Events.LogicUpdate, self.onUpdate )
        Zero.Connect(self.Space, "DisableControl", self.disable)
        
        if( self.Owner.PlayerController is None ):
            print( "GamepadController: A [PlayerController] component is require for this component to function" )
        #endif
        
        if(self.DebugMode is True):
                print("GamePadController: Initialze()")
        #endif
    #end
    
    def disable(self,Event):
        self.DisableControlPad = True
    
    def onUpdate(self, Event):
        self.MovementFrame = self.Gamepad.LeftStick
        
        #this is the speed we will move at
        self.speed = 2.0
        self.Timer += Event.Dt
        self.soundTimer += Event.Dt
        
        if self.DisableControlPad:
            #return
            pass
        
        #print(Event.Dt)
        
        if( self.Timer >= 0.03 ):
            if(self.Gamepad.LeftTrigger > 0):
                self.handleTrigger(self.Gamepad.LeftTrigger, False, Event.Dt)
            #endif        
            if(self.Gamepad.RightTrigger > 0):
                self.handleTrigger(self.Gamepad.RightTrigger, True, Event.Dt)
            else:
                self.handleRightStick( self.Gamepad.RightStick, Event.Dt )
            #endif
            
            if(self.Gamepad.IsButtonHeld(Zero.Buttons.B)):
                #self.Owner.Sprinkler.Shoot()
                pass
            elif(self.Gamepad.IsButtonHeld(Zero.Buttons.X)):
                #self.Owner.Sprinkler.Shoot()
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
            self.jump(2)
        elif(self.Gamepad.IsButtonReleased(Zero.Buttons.A)):
            self.endjump()
        #endif
        
        if(self.Gamepad.IsButtonPressed(Zero.Buttons.RightShoulder) or self.Gamepad.IsButtonPressed(Zero.Buttons.LeftShoulder)):
            #for some reason pressing A makes you jump higher, this number is to even them
            self.jump(1.425)
        elif(self.Gamepad.IsButtonReleased(Zero.Buttons.RightShoulder) or self.Gamepad.IsButtonReleased(Zero.Buttons.LeftShoulder)):
            self.endjump()
        #endif
        
        #Move with physics
        self.jumping = not self.Owner.DynamicController.OnGround
        
        
        if not self.Floating:
            self.MovementFrame.y = 0
        #endif
        self.Owner.DynamicController.MoveInDirection(self.MovementFrame * float(self.speed))
    #end onUpdate()
    
    def handleTrigger(self, TriggerValue, isRightTrigger, dt = 1):
        #if I want to I could differentiate between trigger behaviors
        #for now I'm going to treat them the same
        #self.Owner.PlayerController.Spray(TriggerValue)
        self.Owner.Sprinkler.ShootStick(Vec3(0,-1,0) * TriggerValue)
        
        self.playCue()
    #end handleTrigger()
    
    def handleRightStick(self, Rightstick, dt = 1):
        if( Rightstick.x > self.deadzone or Rightstick.x < -self.deadzone or
            Rightstick.y > self.deadzone or Rightstick.y < -self.deadzone ):
            self.Owner.Sprinkler.ShootStick(Rightstick)
            
            self.playCue()
        #endif
    #enddef
    
    def playCue(self, string = "Spray"):
        if self.soundTimer > 0.5 and not self.Owner.WaterTank.TankReplenishing:
                self.Owner.SoundEmitter.PlayCue("Spray")
                self.soundTimer = 0
    
    
    def jump(self, jumpPow = 1.0):
        if not self.jumping:
            self.Owner.DynamicController.AttemptJump(jumpPow)
            self.Owner.SoundEmitter.Play()
            self.jumping = True
    #enddef
    
    def endjump(self):
        self.Owner.DynamicController.EndJump()
        self.jumping = False
        
    
    def onButtonUp(self, event):
        if(self.DebugMode is True):
                print("GamepadController:onButtonDown()")
        #endif
    #end onKeyUp()
    
    def onButtonDown(self, ButtonEvent):
        if(self.DebugMode is True):
                print("GamepadController:onButtonDown()")
                
        if(event.Button == Zero.Buttons.Start):
            self.Space.TimeSpace.TogglePause()
        #endif
    #end onKeyDown()
#end class

Zero.RegisterComponent("GamepadController", GamepadController)