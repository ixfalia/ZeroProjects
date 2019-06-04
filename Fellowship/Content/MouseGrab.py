import Zero
import Events
import Property
import VectorMath

import math
vec3 = VectorMath.Vec3

class MouseGrab:
    def DefineProperties(self):
        self.Debug = Property.Bool(default = False)
        
        self.Offset = Property.Vector3(default = vec3(0,0,0))
        self.FollowingDistance = Property.Float(4)
        self.MoveSpeed = Property.Float(default = 5.0)

    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.MouseDown, self.onMouseDown)
        Zero.Connect(self.Space, Events.MouseUp, self.onMouseUp)
        Zero.Connect(self.Owner, Events.MouseEnter, self.onMouseEnter)
        Zero.Connect(self.Owner, Events.MouseExit, self.onMouseExit)
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        Zero.Connect(self.Owner, Events.MouseUpdate, self.onMouseUpdate)
        
        self.Viewport = self.Space.FindObjectByName("LevelSettings")
        self.Viewport = self.Viewport.CameraViewport
        self.isGrabbing = False
        self.UsedMouseButton = Zero.MouseButtons.Right
        self.ZValue = 0
        
        self.StartingPos = None
        self.TimeGrabbed = 0
        self.CurrentDT = 0
        
        if not self.Viewport:
            raise

    def onUpdate(self, UpdateEvent):
        if self.isGrabbing:
            self.moveToMouse(UpdateEvent.Dt)
            self.TimeGrabbed += UpdateEvent.Dt
        pass
        
        self.CurrentDT = UpdateEvent.Dt
    
    def onMouseDown(self, mEvent):
        mPos = Zero.Mouse.ScreenPosition
        pos = self.Viewport.ScreenToWorldZPlane(mPos, self.ZValue)
        
        self.isGrabbing = True
        self.StartingPos = pos
        self.Owner.SphereCollider.Radius -= 1
        
        if self.Debug:
            print("[{}].MouseGrab: Mouse Down".format(self.Owner.Name))
    
    def onMouseUp(self, mEvent):
        if not self.isGrabbing:
            return
        
        mPos = Zero.Mouse.ScreenPosition
        pos = self.Viewport.ScreenToWorldZPlane(mPos, self.ZValue)
        
        self.isGrabbing = False
        self.TimeGrabbed = 0
        self.Owner.SphereCollider.Radius += 1
        
        distance = pos - self.StartingPos
        #self.Owner.RigidBody.Velocity = vec3(distance.x * self.CurrentDT, 0, 0)
        
        if self.Debug:
            print("[{}].MouseGrab: Mouse Up".format(self.Owner.Name))
    
    def onMouseUpdate(self, mEvent):
        pass
    
    def onMouseEnter(self, MouseEvent):
        if self.Debug:
            print("[{}].MouseGrab: Mouse Hover".format(self.Owner.Name))
        
    def onMouseExit(self, MouseEvent):
        if self.Debug:
            print("[{}].MouseGrab: Mouse Exit".format(self.Owner.Name))
    
    def moveToMouse(self, dt):
        mPos = Zero.Mouse.ScreenPosition
        pos = self.Viewport.ScreenToWorldZPlane(mPos, self.ZValue)
        
        #self.Owner.Transform.Translation = pos
        
        targetPosition = pos
        position = self.Owner.Transform.Translation
        distance = self.distance(position, targetPosition)
        
        self.Owner.Transform.Translation = pos
        if False and distance > self.FollowingDistance:
            delta = targetPosition - position
            delta *= dt
            
            self.Owner.Transform.Translation += delta * self.MoveSpeed
    
    def isMouseDown(self):
        if self.isDown(Zero.MouseButtons.Left):
            return True
        if self.isDown(Zero.MouseButtons.Middle):
            return True
        if self.isDown(Zero.MouseButtons.Right):
            return True
        
        return False
    
    def isDown(self, button):
        return Zero.Mouse.IsButtonDown(button)
    
    def distance(self, p1, p2):
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
    
    def sendParentEvent(self, name, e):
        self.Owner.Parent.DispatchEvent(name, e)

Zero.RegisterComponent("MouseGrab", MouseGrab)