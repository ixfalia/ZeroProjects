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
    Timer = 0
    soundTimer = 0
    
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
        self.DisableControlPad = not self.DisableControlPad
    
    def onUpdate(self, Event):
        self.MovementFrame = self.Gamepad.LeftStick
        
        #this is the speed we will move at
        self.speed = 1
        self.Timer += Event.Dt
        self.soundTimer += Event.Dt
        
        if self.DisableControlPad:
            #return
            pass
        
        #print(Event.Dt)
        
        if( self.Timer >= 0.2 ):
            if(self.Gamepad.LeftTrigger > 0):
                self.handleTrigger(self.Gamepad.LeftTrigger, False, Event.Dt)
            #endif        
            if(self.Gamepad.RightTrigger > 0):
                self.handleTrigger(self.Gamepad.RightTrigger, True, Event.Dt)
            
            self.handleRightStick( self.Gamepad.RightStick, Event.Dt )
            
            #endif
            
            if(self.Gamepad.IsButtonHeld(Zero.Buttons.B)):
                #self.Owner.Sprinkler.Shoot()
                pass
            elif(self.Gamepad.IsButtonHeld(Zero.Buttons.X)):
                #self.Owner.Sprinkler.Shoot()
                pass
            #endif
            
            #if self.Gamepad.IsButtonHeld(Zero.Buttons.A):
            #    self.Owner.PlayerController.Fire()
            
            self.Timer = 0
        #endif
        
        ### Movement Code ###
        #####################
        if( self.MovementFrame.x < 0 ):
            pass
            #self.Owner.Sprite.FlipX = False
        elif( self.MovementFrame.x > 0 ):
            pass
            #self.Owner.Sprite.FlipX = True
        #endif
        
        if(self.Gamepad.IsButtonPressed(Zero.Buttons.A)):
            self.Owner.PlayerController.Fire()
            pass
        elif(self.Gamepad.IsButtonReleased(Zero.Buttons.A)):
            pass
        #endif
        if self.Gamepad.IsButtonHeld(Zero.Buttons.A):
            self.Owner.PlayerController.Fire()
        
        if(self.Gamepad.IsButtonPressed(Zero.Buttons.RightShoulder)):
            self.Owner.PlayerController.shiftColorRight()
            pass
        if(self.Gamepad.IsButtonPressed(Zero.Buttons.LeftShoulder)):
            self.Owner.PlayerController.shiftColorLeft()
            pass
        #Move with physics
        self.Owner.PlayerController.MoveInDirection(self.MovementFrame * float(self.speed))
    #end onUpdate()
    
    def handleTrigger(self, TriggerValue, isRightTrigger, dt = 1):
        #if I want to I could differentiate between trigger behaviors
        #for now I'm going to treat them the same
        #self.Owner.PlayerController.Spray(TriggerValue)
        #self.Owner.Sprinkler.ShootStick(Vec3(0,-1,0) * TriggerValue)
        
        self.playCue()
    #end handleTrigger()
    
    def handleRightStick(self, Rightstick, dt = 1):
        if( Rightstick.x > self.deadzone or Rightstick.x < -self.deadzone or
            Rightstick.y > self.deadzone or Rightstick.y < -self.deadzone ):
            #self.Owner.Sprinkler.ShootStick(Rightstick)
            
            self.Owner.PlayerController.Fire(Rightstick)
        #endif
    #enddef
    
    def playCue(self, string = "Default"):
        self.Owner.SoundEmitter.PlayCue(string)
        self.soundTimer = 0
    
    
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