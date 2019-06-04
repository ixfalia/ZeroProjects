import Zero
import Events
import Property
import VectorMath

import Color

import Keys
import Action
import math

Vec3 = VectorMath.Vec3

class MovementController:
    speed = Property.Float(default = 10)
    
    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.RightMouseDown, self.onRightMouseDown)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.onCollision)
        Zero.Connect(self.Owner, Events.CollisionEnded, self.onCollisionEnd)
        
        settings = self.Space.FindObjectByName("LevelSettings")
        self.Viewport = settings.CameraViewport
        self.depth = -1
        self.colliding = False
        #self.speed = 1
        self.seq = Action.Sequence(self.Owner)
    
    def onRightMouseDown(self, mEvent):
        mousePosition = mEvent.Position
        
        worldposition = self.Viewport.ScreenToWorldZPlane(mousePosition, self.depth)
        
        direction = worldposition - self.Owner.Transform.Translation
        direction.normalize()
        
        angle = worldposition.angleZ()
        
        zAxis = Vec3(0,0,1)
        angleVec = VectorMath.Vec3(0, 0, angle)
        #Rotation = VectorMath.Vec3.RotateTowards(self.Owner.Transform.Rotation, angleVec, 1);
        self.Space.PhysicsSpace.CastRayFirst
        
        self.Owner.Transform.Rotation = VectorMath.Quat.AxisAngle(zAxis, angle);
        #self.Owner.Transform.Rotation = Rotation
        
        #print(direction)
        circle = self.Space.CreateAtPosition("targetCircle", worldposition)
        collisionCheck = self.castRay(worldposition)
        
        if self.castRay(worldposition):
            #circle.Sprite.Color = Color.Red
            self.moveToPosition(worldposition)
        else:
            self.moveToPosition(worldposition)
    
    def moveToPosition(self, position):
        #if not Zero.Keyboard.KeyIsDown(Keys.Shift):
        self.seq.Cancel()
        
        self.seq = Action.Sequence(self.Owner)
        
        mypos = self.Owner.Transform.Translation
        distance = math.sqrt((position.x - mypos.x)**2 + (position.y - mypos.y)**2)
        duration = distance / self.speed
        
        position = VectorMath.Vec3(position.x, position.y, 0)
        
        #print(mypos, position, distance, duration)
        
        Action.Property(self.seq, self.Owner.Transform, "Translation", position, duration)
    
    def onCollision(self, e):
        other = e.OtherObject
        
        if other.Collider.Ghost:
            return
        
        print("**PlayerCollided with Object**")
        self.colliding = True
        self.seq.Cancel()
        self.seq = Action.Sequence(self.Owner)
    
    def onCollisionEnd(self, e):
        #print("Pong")
        self.colliding = False
    
    def castRay(self, end):
        ray = VectorMath.Ray()
        ray.Start =  self.Owner.Transform.Translation
        direction = end - self.Owner.Transform.Translation
        direction.normalize()
        ray.Direction = direction
        #ray.Distance = 20.0
        color = Color.LawnGreen
        
        return self.Space.PhysicsSpace.CastRayFirst(ray)
    
    def moveLeft(self):
        pass
    
    def moveRight(self):
        pass
    
    def moveUp(self):
        pass
    
    def moveDown(self):
        pass

Zero.RegisterComponent("MovementController", MovementController)