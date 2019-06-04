import Zero
import Events
import Property
import VectorMath

Vec3 = VectorMath.Vec3;

# Enum for input type
InputType = Property.DeclareEnum("InputType", ["Keyboard", "Gamepad", "Both"]);

#----------------------------------------------------- Character Input Component
class CharacterInput:
    # Whether or not to use the keyboard or the gamepad
    InputType = Property.String(enum = InputType);
    
    # Which gamepad to use (if gamepad is selected as the InputType)
    GamepadIndex = Property.Uint(0);
    
    def Initialize(self, initializer):
        # Attempt to get the gamepad at the given index
        self.Gamepad = Zero.Gamepads.GetGamePad(self.GamepadIndex);
        
        # TEMPORARY - Set the camera to follow us
        #cam = self.Space.FindObjectByName("Camera");
        #cam.CameraGroupFocuser.AddObject(self.Owner);
        
    def GetMovementDirection(self):
        # If we're using the keyboard, get movement from WASD
        if(self.InputType == InputType.Keyboard):
            return self.GetKeyboardMovement();
        # If we're using the gamepad, get movement from the left stick
        # First make sure that the gamepad exists
        elif(self.InputType == InputType.Both):
            keyboard = self.GetKeyboardMovement()
            gPad = self.GetGamepadMovement()
            
            if keyboard.length() > gPad.length():
                return keyboard
            else:
                return gPad
        elif(self.Gamepad):
            return self.GetGamepadMovement();
        
        # If the gamepad doesn't exist, return that there was no movement
        return Vec3(0,0,0);
        
    def IsJumpPressed(self):
                
        # If we're using the keyboard, check the space bar
        if(self.InputType == InputType.Keyboard):
            return Zero.Keyboard.KeyIsPressed(Zero.Keys.W) or Zero.Keyboard.KeyIsPressed(Zero.Keys.Space);
        # If we're using the gamepad, check the A button
        elif(self.InputType == InputType.Both):
            return Zero.Keyboard.KeyIsPressed(Zero.Keys.W) or Zero.Keyboard.KeyIsDown(Zero.Keys.Space) or self.Gamepad.IsButtonPressed(Zero.Buttons.A)
        elif(self.Gamepad):
            return self.Gamepad.IsButtonPressed(Zero.Buttons.A);
            
            
        # If the gamepad doesn't exist, return that it is was not pressed
        return False;
        
    def IsJumpHeld(self):
        # If we're using the keyboard, check the space bar
        if(self.InputType == InputType.Keyboard):
            return Zero.Keyboard.KeyIsDown(Zero.Keys.W) or Zero.Keyboard.KeyIsDown(Zero.Keys.Space);
        # If we're using the gamepad, check the A button
        elif(self.InputType == InputType.Both):
            Zero.Keyboard.KeyIsDown(Zero.Keys.W) or Zero.Keyboard.KeyIsDown(Zero.Keys.Space) or self.Gamepad.IsButtonHeld(Zero.Buttons.A)
        elif(self.Gamepad):
            return self.Gamepad.IsButtonHeld(Zero.Buttons.A);
            
        # If the gamepad doesn't exist, return that it was not pressed
        return False;
    
    #--------------------------------------------------- Internal Implementation
    def GetKeyboardMovement(self):
        dir = Vec3(0,0,0);
        
        if(Zero.Keyboard.KeyIsDown(Zero.Keys.A)):
            dir += Vec3(-1,0,0);
        if(Zero.Keyboard.KeyIsDown(Zero.Keys.D)):
            dir += Vec3(1,0,0);
        if(Zero.Keyboard.KeyIsDown(Zero.Keys.W) or Zero.Keyboard.KeyIsDown(Zero.Keys.Space)):
            dir += Vec3(0,1,0);
            #raise
            #pass
        if(Zero.Keyboard.KeyIsDown(Zero.Keys.S)):
            dir += Vec3(0,-1,0);
        
        return dir;
        
    def GetGamepadMovement(self):
        # Remove the y axis from the stick location
        dir = self.Gamepad.LeftStick
        return dir;

Zero.RegisterComponent("CharacterInput", CharacterInput)