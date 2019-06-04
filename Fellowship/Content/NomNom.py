import Zero
import Events
import Property
import VectorMath

import Action

import PetLogic

PetActions = PetLogic.PetActions

class NomNom:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        pass

    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.onCollision)
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
        if not self.Owner.Statistics:
            self.Stomach = self.Owner.Parent
            self.isChild = True
            
            self.Bit = self.Stomach.FindChildByName("bit")
        else:
            self.Stomach = self.Owner
            self.isChild = False
            
            self.Bit = self.Stomach.Parent.FindChildByName("bit")

    def OnLogicUpdate(self, UpdateEvent):
        pass
    
    def onCollision(self, cEvent): 
        other = cEvent.OtherObject
        
        if other.Collider.CollisionGroup.Name == "Food":
            self.munch(other)
    
    def munch(self, food):
        if food.Food.Eaten:
            return
        
        food.Food.ApplyFood(self.Stomach)
        
        self.eatEffect(food.Food.Color)
        
        seq = Action.Sequence(food)
        
        Action.Delay(seq, food.Food.TimeToEat)
        Action.Call(seq, food.Destroy)
        Action.Call(seq, self.doneEat)
        pass
    
    def eatEffect(self, color = None):
        self.Bit.SphericalParticleEmitter.Active = True
        
        #if self.isChild:
        #    self.Owner.Parent.Sprite.SpriteSource = "Dragon_Munch"
        #else:
        #    self.Owner.Sprite.SpriteSource = "Dragon_Munch"
        self.Owner.Parent.PetLogic.changeAction(PetActions.Eating)
        if color:
            self.Bit.SpriteParticleSystem.Tint = color
    
    def doneEat(self):
        self.Bit.SphericalParticleEmitter.Active = False
        
        pos = self.Owner.Parent.Transform.WorldTranslation
        love = self.Space.CreateAtPosition("LoveEffectTimed", VectorMath.Vec3(pos.x, pos.y + 3, 4))
        
        love.AttachToRelative(self.Owner.Parent)
        
        #if self.isChild:
        #    self.Owner.Parent.Sprite.SpriteSource = "Dragon_Idle"
        #else:
        #    self.Owner.Sprite.SpriteSource = "Dragon_Idle"
        self.Owner.Parent.PetLogic.changeAction(PetActions.Idle)

Zero.RegisterComponent("NomNom", NomNom)