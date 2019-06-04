import Zero
import Events
import Property
import VectorMath

import math #allows access to standard mathematical functions

Vec3 = VectorMath.Vec3

class MovementController:
    DebugMode = Property.Bool(default = True)
    JumpStrength = Property.Float(default = 10.0)
    GroundForgiveness = Property.Float(default = 0.1) #how long you have to let you jump after you've landed
    MovementStrength = Property.Float(default = 10.0)
    
    def Initialize(self, initializer):
        if self.DebugMode:
            print("MovementController.Initialize()")
        
        self.OnGround = False
        self.Floating = False
        self.Jumping = False
        
        self.DT = 0.0
        self.GroundTimer = 0.0
        
        Zero.Connect(self.Space, Events.LogicUpdate, self.onLogicUpdate)
    #end Initialize()
    
    def onLogicUpdate(self, updateEvent):
        self.GroundTimer += updateEvent.Dt
        
        self.UpdateGroundState()
        self.DT = updateEvent.Dt
        
        if self.DebugMode:
            print("Can Jump: ", self.CanJump())
            
        
        if self.OnGround:
            self.Owner.DragEffect.Active = False
            self.Owner.GravityEffect.Strength = 0
            
            camera = self.Space.FindObjectByName("Camera")
            camera.CameraController.updateY()
        else:
            self.Owner.DragEffect.Active = True
            
            if self.Owner.RigidBody.Velocity.y < 0:
                self.Owner.GravityEffect.Strength = 10
    #enddef
    
    def Move(self, movementVector):
        if self.DebugMode:
            print("MovementController.Move(): Vector Found:", movementVector)
        #movementVector.normalize()
        
        movementForce = movementVector * self.MovementStrength
        
        if not self.Floating:
            movementForce.y = 0
        
        if self.DebugMode:
            print("\tMovement Strength calculated: ", movementForce)
        #endif
        self.Owner.RigidBody.ApplyLinearVelocity(movementForce * self.DT)
    #end def Move()
    
    def MoveNotNormalizing(self, movementVector):
        pass
    
    def CanJump(self):
        return self.OnGround or self.GroundTimer <= self.GroundForgiveness
    
    def CanFlutter(self):
        return True
    
    def Jump(self, JumpBy = None):
        if self.CanJump():
            if JumpBy:
                self.Owner.RigidBody.ApplyLinearImpulse(VectorMath.Vec3(0,1,0) * JumpBy)
            else:
                self.Owner.RigidBody.ApplyLinearImpulse(VectorMath.Vec3(0,1,0) * self.JumpStrength)
            
            self.OnGround = False
            self.PlayCue("Jump")
        #endif
        
    #end Jump()
    
    def Flutter(self, JumpBy = None):
        if self.CanFlutter():
            if JumpBy:
                self.Owner.RigidBody.ApplyLinearImpulse(VectorMath.Vec3(0,1,0) * JumpBy)
            else:
                self.Owner.RigidBody.ApplyLinearImpulse(VectorMath.Vec3(0,1,0) * JumpBy)
            
            self.PlayCue("Spray")
    #def Flutter()
    
    def EndJump(self):
        #self.Owner.DynamicController.EndJump()
        #self.Jumping = False
        pass
    #def EndJump()
    
    def HandleRightStick(self, rightStickVector, deadzone):
        if( rightStickVector.x > deadzone or rightStickVector.x < -deadzone or
            rightStickVector.y > deadzone or rightStickVector.y < -deadzone ):
            self.Owner.Sprinkler.ShootStick(rightStickVector)
            
            self.PlayCue()
        #endif
    #enddef
        pass
    #end HandleRightStick()
    
    def PlayCue(self, cueName = "Spray"):
        self.Owner.SoundManager.Play(cueName)
    
    def UpdateGroundState(self):
        self.OnGround = False
        
        for ContactHolder in self.Owner.Collider.Contacts:
            if ContactHolder.IsGhost:
                continue
            
            collidingObject = ContactHolder.OtherObject
            
            surfaceNormal = -ContactHolder.FirstPoint.WorldNormalTowardsOther
            
            if self.IsGround(surfaceNormal):
                self.OnGround = True
                self.Ground = 0.0
                #self.Owner.GravityEffect.Strength = 0
                return
            #endif
            return
        #end for
    #end UpdateGroundState()
    
    def IsGround(self, surfaceNormal):
        degrees = self.GetDegreeDifference(surfaceNormal)
        
        return degrees < 60.0
    #end IsGround()
    
    def GetDegreeDifference(self, surfaceNormal):
        upDirection = Vec3(0,1,0)
        
        cosTheta = surfaceNormal.dot(upDirection)
        cosTheta = min(max(cosTheta, -1.0), 1.0)
        radians = math.acos(cosTheta)
        degrees = math.degrees(radians)
        
        return degrees
    #end GetDegreeDifference()
#end class MovementController

Zero.RegisterComponent("MovementController", MovementController)