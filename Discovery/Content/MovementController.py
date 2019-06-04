import Zero
import Events
import Property
import VectorMath

import Action

Vec3 = VectorMath.Vec3

class MovementController:
    def DefineProperties(self):
        self.Active = Property.Bool(default = True)
        self.UseDelta = Property.Bool(default = True)
        
        self.MovementScalar = Property.Float(10)
        pass

    def Initialize(self, initializer):
        self.delta = 0
        
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        pass

    def onUpdate(self, UpdateEvent):
        self.delta = UpdateEvent.Dt
    
    def moveLeft(self):
        move = Vec3(-1, 0, 0)
        
        self.positionalMove(move)
        pass
    
    def moveRight(self):
        move = Vec3(1, 0, 0)
        
        self.positionalMove(move)
        pass
    
    def moveUp(self):
        move = Vec3(0, 1, 0)
        
        self.positionalMove(move)
        pass
    
    def moveDown(self):
        move = Vec3(0, -1, 0)
        
        self.positionalMove(move)
        pass
    
    def positionalMove(self, direction):
        if not self.UseDelta:
            dt = 0
        else:
            dt = self.delta
        
        self.Owner.Transform.Translation += direction * self.MovementScalar * dt
    
    def physicsMove(self, direction):
        pass

Zero.RegisterComponent("MovementController", MovementController)