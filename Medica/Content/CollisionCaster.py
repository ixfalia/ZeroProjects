import Zero
import Events
import Property
import VectorMath

import Color
import math
import DebugDraw

Vec3 = VectorMath.Vec3
Vec4 = VectorMath.Vec4

class CollisionCaster:
    DebugMode = Property.Bool(default = True)
    def Initialize(self, initializer):
        self.StartingPoint = self.Owner.Transform.Translation
        self.useOtherStartingPoint = False
    
    def setStartingPoint(self, point = None):
        if not point:
            point = self.Owner.Transform.Translation
            self.StartingPoint = point
            
            self.useOtherStartingPoint = False
        else:
            self.StartingPoint = point
            self.useOtherStartingPoint = True
    #enddef
    
    #Returns first object cast
    def CastRay(self, direction, length = 80, penetration = 1, color = Color.Yellow):
        ray = VectorMath.Ray()
        
        if self.useOtherStartingPoint:
            ray.Start = self.StartingPoint
        else:
            ray.Start = self.Owner.Transform.Translation
        #endif
        
        ray.Direction = direction
        #ray.Distance = length
        #ray.Color = color
        
        if self.DebugMode:
            self.rayDebugDraw(ray, length, color)
        
        return self.Space.PhysicsSpace.CastRayResults(ray, penetration)
    #end CastRay()
    
    def rayDebugDraw(self, ray, distance, arrowColor = None):
        endPoint = ray.Start + ray.Direction * distance
        
        if not arrowColor:
            arrowColor = ray.Color
        
        DebugDraw.DrawArrow(ray.Start, endPoint, 0.25, arrowColor)
    
    def CastSphere(self, radius = None, color = Color.Crimson):
        if not radius:
            radius = 10.0
        
        position = self.Owner.Transform.Translation
        
        if self.DebugMode:
            self.circleDebugDraw(radius)
        
        return self.Space.PhysicsSpace.CastSphereResults(position, radius, 20, self.Space.PhysicsSpace.CreateDefaultCastFilter())
    
    def circleDebugDraw(self, radius, color = Color.Crimson):
        position = self.Owner.Transform.Translation
        
        DebugDraw.DrawSphere(position, radius, color)

Zero.RegisterComponent("CollisionCaster", CollisionCaster)