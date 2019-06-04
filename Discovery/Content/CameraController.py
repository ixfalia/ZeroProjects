import Zero
import Events
import Property
import VectorMath

import math

class CameraController:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        self.Target = Property.Cog()
        self.Offset = Property.Vector3()
        
        pass

    def Initialize(self, initializer):
        self.Player = None
        self.TargetRadius = 5
        
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Space, "PlayerCreationEvent", self.onPlayer)
        
        cameraEvent = Zero.ScriptEvent()
        cameraEvent.Camera = self.Owner
        
        self.GameSession.DispatchEvent("CameraCreationEvent", cameraEvent)
        pass

    def OnLogicUpdate(self, UpdateEvent):
        if not self.Target:
            self.Target = self.Player
        
        targetPosition = self.Target.Transform.Translation
        position = self.Owner.Transform.Translation
        
        distance = self.distance(position, targetPosition)
        
        if False and distance > self.TargetRadius:
            ratio = self.TargetRadius / distance
            delta = targetPosition - position
            
            moveDistance = delta * (1-ratio)
            
            self.Owner.Transform.Translation =  VectorMath.Vec3(moveDistance.x, moveDistance.y, position.z)
            
            print("################")
            print("\t\tratio:{} delta:{} moveDistance:{} distance:{}".format(ratio, delta, moveDistance, distance))
            print("\tCameraPos: {} PlayerPos: {}".format(position, targetPosition))
            print("################")
        
        self.Owner.Transform.Translation = VectorMath.Vec3(targetPosition.x, targetPosition.y, position.z)
    
    def onPlayer(self, pEvent):
        self.Player = pEvent.Player
    
    def changeTarget(self, target, tweenTime = 0):
        self.Target = target
        self.DisableTracking = Tre
    
    def setTarget(self, target):
        self.Target = target
    
    def distance(self, p1, p2):
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

Zero.RegisterComponent("CameraController", CameraController)