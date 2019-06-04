import Zero
import Events
import Property
import VectorMath

import math

class FollowTarget:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        self.Active = Property.Bool(default = True)
        self.InitialTarget = Property.Cog()
        self.FollowMouse = Property.Bool(default = False)
        self.TargetRadius = Property.Float(default = 1)
        self.moveSpeed = Property.Float(default = 4.0)
        pass

    def Initialize(self, initializer):
        self.moveSpeed = 4.0
        self.Player = None
        #self.TargetRadius = 1
        self.Target = self.InitialTarget
        
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Space, "PlayerCreationEvent", self.onPlayer)
        pass
    
    def OnLogicUpdate(self, UpdateEvent):
        if not self.Active:
            return
        
        if self.FollowMouse:
            self.Target = self.Space.FindObjectByName("Mousebee")
        elif not self.Target:
            self.Target = self.Player
        if not self.Target:
            return
        
        targetPosition = self.Target.Transform.Translation
        position = self.Owner.Transform.Translation
        distance = self.distance(position, targetPosition)
        
        #desiredPosition = VectorMath.Vec3(targetPosition.x, targetPosition.y, position.z)
        if distance > self.TargetRadius:
            delta = targetPosition - position
            delta *= UpdateEvent.Dt
            
            self.Owner.Transform.Translation += delta * self.moveSpeed
    
    def onPlayer(self, pEvent):
        self.Player = pEvent.Player
    
    def distance(self, p1, p2):
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
    
    def changeTarget(self, cog):
        self.Target = cog
    
    def getMouseWorldPosition(self, zPos = 1):
        mouse = Zero.Mouse
        viewport = self.Space.FindObjectByName("LevelSettings").CameraViewport
        worldposition = viewport.ScreenToWorldZPlane(mouse.ScreenPosition, zPos)
        
        return worldposition

Zero.RegisterComponent("FollowTarget", FollowTarget)