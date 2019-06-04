import Zero
import Events
import Property
import VectorMath

import math
import Color

# Declaractions
Vec3 = VectorMath.Vec3
Vec4 = VectorMath.Vec4

States = ["Idle", "Walking", "Falling", "Jumping"]
CharacterState = Property.DeclareEnum("CharacterState", States)

class CharacterController:
    Debug = Property.Bool(default = False)
    isActive = Property.Bool(default = True)
    
    UpVector = Property.Vector3(default = Vec3(0,1,0))
    MaxSpeed = Property.Float(default = 7.0)
    MovePower = Property.Float(default = 2.0)
    InAirControl = Property.Float(default = 0.2)
    
    WalkableSlopeAngle = Property.Float(default = 40.0)
    InitialJumpVelocity = Property.Float(default = 6.0)
    AdditiveJumpVelocity = Property.Float(default = 150)
    
    AdditiveJumpTime = Property.Float(default = 0.05)
    LateJumpTimer = Property.Float(0.23)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        
        self.Traction = 1.0
        self.isJumping = False
        self.isInAirFromJump = False
        
        self.OnGround = False
        self.TimeSinceLastDirectContact = 0.0
        self.VelocityOfGround = Vec3(0,0,0)
        #self.doubleJumpUsed = False
        
        self.CharacterState = CharacterState.Idle
    #end initialize()
    
    def getCurrentState(self):
        return self.CharacterState
    
    def onUpdate(self, uEvent):
        if not self.isActive:
            return
        # Update whether or not we are on ground, as well as getting 
        # the traction (slipperyness) of the surface we're on
        self.UpdateGroundState(uEvent.Dt)
        
        # All logic for jumping is contained in this function
        self.UpdateJumpState(uEvent.Dt)
        
        # Get our current control (value between 0-1)
        controlScalar = self.GetCurrentControlScalar()
        
        # We want to set the amount of force we can apply to reach our desired maximum speed
        # We're multiplying by the object's mass so that the character can easily be scaled
        # without having to re-adjust MovePower
        moveForce = self.MovePower * self.Owner.RigidBody.Mass
        # Apply the control scalar (air control / traction / etc...)
        moveForce *= controlScalar
        # Set the final force
        self.Owner.DynamicMotor.MaxMoveForce = moveForce
        
        # Get a movement direction from input
        movement = self.Owner.CharacterInput.GetMovementDirection()
        # We don't want any movement in the y
        movement.y = 0.0
        
        # Get our current max speed
        maxSpeed = self.GetMaxSpeed()
        
        # Move in the given direction with our current max speed
        self.Owner.DynamicMotor.MoveInDirection(movement * maxSpeed, self.UpVector)
        
        self.UpdateOrientation(movement)
        
        self.UpdateCurrentState(movement)
    #end def onUpdate()
    
    def UpdateOrientation(self, movement):
        if movement.x > 0:
            self.FaceRight()
        elif movement.x < 0:
            self.FaceLeft()
    #enddef UpdateOrientation
    
    def FaceRight(self):
        self.Owner.Sprite.FlipX = True
        return True
    
    def FaceLeft(self):
        self.Owner.Sprite.FlipX = False
        return False
    
    def UpdateCurrentState(self, movement):
        if self.Owner.Player.inDeath:
            return
        if self.OnGround:
            if self.isJumping:
                CharacterState.Jumping
                self.Owner.Sprite.SpriteSource = "DennisJump"
            else:
                speed = movement.length()
                if speed == 0.0:
                    self.CharacterState = CharacterState.Idle
                    self.Owner.Sprite.SpriteSource = "MainCharacter"
                    self.JumpTimer = 0
                    self.doubleJumpUsed = False
                else:
                    self.CharacterState = CharacterState.Walking
                    #self.Owner.Sprite.SpriteSource = "Denniswalkcycle"
                    self.Owner.Sprite.AnimationActive = True
                    self.JumpTimer = 0
                    self.doubleJumpUsed = False
                    #self.Owner.Sprite.Color = Color.Aqua
                #endif
            #endif
        else:
            if self.isJumping or self.Owner.CharacterInput.IsJumpHeld():
                self.CharacterState = CharacterState.Jumping
                self.Owner.Sprite.SpriteSource = "DennisJump"
            else:
                self.CharacterState = CharacterState.Falling
                self.Owner.Sprite.SpriteSource = "DennisJump"
            #endif
        #endif
    #end UpdateCurrentState()
    
    def GetCurrentControlScalar(self):
        # Use our current traction if we're on the ground
        if self.OnGround:
            return self.Traction
        # Otherwise, use the air control
        return self.InAirControl
    #end GetCurentControlScalar()
    
    def GetMaxSpeed(self):
        speed = self.MaxSpeed
        
        # If we're on the ground simply use the default max speed
        if self.OnGround:
            return speed
        
        # If we're in the air, we want to be able to move faster than the
        # specified MaxSpeed.  This allows objects to hit us and accelerate
        # us to faster speeds than the specified max
        # To accomplish this, we want to set our current maximum speed
        # to the maximum of the specified MaxSpeed and our current velocity
        # This way, the DynamicMotor will not try and slow us down to the max
        # specified speed while in the air, we will simply remain at whatever
        # speed we're currently at
        
        # Get our current velocity
        vel = self.Owner.RigidBody.Velocity
        
        # Project out the up vector (we only want velocity on our plane of movement)
        # In 2D, this could simply be: abs(self.Owner.RigidBody.Velocity.x)
        vel = vel - self.UpVector * vel.dot(self.UpVector)
        currSpeed = vel.length()
        
        # Return whichever is greater
        return max(speed, currSpeed)
    #end GetMaxSpeed()
    
    ############################################################
    ###                  Ground State Code
    ############################################################
    def UpdateGroundState(self, dt):
        # Update the timer for late jumps
        self.TimeSinceLastDirectContact += dt
        
        # We want to iterate through all objects we're in contact with in order
        # to determine whether or not we have any objects under us (ground)
        for ContactHolder in self.Owner.Collider.Contacts:
            # Ignore ghost objects
            if ContactHolder.IsGhost:
                continue
            
            # Get the object we're in contact with
            objectHit = ContactHolder.OtherObject
            
            # We need the normal of the surface (the normal that points from
            # the object hit to us) to determine whether or not it's walkable
            # FIXME - GetNormalPointingAt
            surfaceNormal = -ContactHolder.FirstPoint.WorldNormalTowardsOther
            
            # If the object is considered walkable
            if self.IsGround(surfaceNormal):
                # Contact is valid ground
                self.OnGround = True
                if not self.isJumping:
                    self.InAirFromJump = False
                
                self.TimeSinceLastDirectContact = 0.0
                
                # Set the reference frame to the object if it's valid
                if self.ShouldChangeReferenceFrame(objectHit):
                    self.Owner.DynamicMotor.SetReferenceFrameToObject(objectHit)
                
                # We want to store the object's velocity so that we can
                # jump with the object's velocity taken into account
                if objectHit.RigidBody:
                    self.VelocityOfGround = objectHit.RigidBody.Velocity
                
                # As an example, we read the traction from a 'Traction' component
                # This can be done in any way you want it
                if objectHit.Traction:
                    self.Traction = objectHit.Traction.Traction
                else:
                    # Default to full traction
                    self.Traction = 1.0
                #endif
            #endif
        #endfor
        
        if self.TimeSinceLastDirectContact > self.LateJumpTimer:
            # Reset all values
            self.OnGround = False
            self.VelocityOfGround = Vec3(0,0,0)
            
            # By default, always set our reference frame to the world
            # If we're in contact with another object that is considered walkable, 
            # we can change to its reference frame (see loop below)
            self.Owner.DynamicMotor.SetReferenceFrameToWorld()
        #endif
    #end UpdateGroundState()
    
    def ShouldChangeReferenceFrame(self, object):
        # For now, all objects are valid
        # You could only accept kinematic objects
        # You could only accept objects with a specific component (e.g. a Platform component)
        return True
    #end ShouldChangeReferenceFrame()
    
    def GetDegreeDifference(self, surfaceNormal):
        # Returns the angle between the surface normal and the up vector of the character
        cosTheta = surfaceNormal.dot(self.UpVector)
        radians = math.acos(cosTheta)
        degrees = math.degrees(radians)
        return degrees
    #end GetDefreeDifference()
    
    def IsGround(self, surfaceNormal):
        # If the angle of the surface's normal is less than the specified value,
        # we're considered to be on ground
        degrees = self.GetDegreeDifference(surfaceNormal)
        return degrees < self.WalkableSlopeAngle
    #end IsGround()
    
    ############################################################
    ###                 Jumping Code
    ############################################################
    def UpdateJumpState(self, dt):
        # If we're currently jumping, we want to continue adding an upward velocity while
        # they still have the jump action held down
        # This allows the player to hold the jump button longer to jump higher
        
        if self.CanJump() and self.Owner.CharacterInput.IsJumpPressed():
            self.Jump()
        
        if self.isJumping:
            # Keep adding the additive jump velocity while Jump is still held and until we
            # have reached the additive jump timer
            if self.Owner.CharacterInput.IsJumpHeld() and self.JumpTimer < self.AdditiveJumpTime:
                # Increment the timer
                self.JumpTimer += dt
                # Add to our velocity
                self.Owner.RigidBody.Velocity += self.Up * self.AdditiveJumpVelocity * dt
            else:
                # If the player has released the jump button or we've reached the
                # end of the timer, we're no longer jumping
                self.Jumping = False
            #endif
        # If we're not already jumping, check to see if we can jump and the Jump action was just pressed
        elif self.CanJump() and self.Owner.CharacterInput.IsJumpPressed():
            self.Jump()
        #endif
    #end UpdateJumpState()
    
    def CanJump(self):
        # We need to be on the ground to be allowed to jump
        # We could also add logic for jumping if we're holding
        # onto something like a rope or ledge
        #if not self.doubleJumpUsed and not self.CharacterState == CharacterState.Idle and self.Owner.CharacterInput.IsJumpPressed():
         #   self.doubleJumpUsed = True
          #  return True
        #else:
            #raise
        return self.OnGround
    #end CanJump()
    
    def Jump(self):
        # Get only horizontal element of our velocity (none in the direction of our Up vector)
        currVelocity = self.Owner.RigidBody.Velocity
        newVelocity = currVelocity - self.UpVector * currVelocity.dot(self.UpVector)
        
        # Add velocity upward by the initial jump strength
        newVelocity += self.UpVector * self.InitialJumpVelocity
        
        # We want to add the velocity of the surface we're currently on
        # This allows us to get an extra boost from jumping off moving objects (e.g. platforms moving upwards)
        newVelocity += self.UpVector * self.VelocityOfGround
        
        # Set the velocity
        self.Owner.RigidBody.Velocity = newVelocity
        
        # We're no longer on the ground
        self.OnGround = False
        
        # We're now jumping (used for the additive jump)
        self.Jumping = True
        #self.isJumping = True
        self.InAirFromJump = True
        
        # Set the additive jump timer to 0
        self.JumpTimer = 0.0
        
        # Because we're now off the ground, we want to attach ourselves back to the world
        self.Owner.DynamicMotor.SetReferenceFrameToWorld()
        
        self.Owner.SoundEmitter.PlayCue("Jump")
        self.Owner.Sprite.SpriteSource = "DennisJump"
    #end Jump()
#end class

Zero.RegisterComponent("CharacterController", CharacterController)