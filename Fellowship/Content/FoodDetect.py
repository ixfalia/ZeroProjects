import Zero
import Events
import Property
import VectorMath

class FoodDetect:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        pass

    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.onCollision)
        Zero.Connect(self.Owner, Events.CollisionEnded, self.onCollisionEnd)
        
        self.FoodWatched = None
        pass

    def OnLogicUpdate(self, UpdateEvent):
        pass
    
    def onCollision(self, CollisionEvent):
        other = CollisionEvent.OtherObject
        
        if other.Collider.CollisionGroup.Name == "Food":
            #self.Owner.Parent.Sprite.SpriteSource = "Dragon_Open"
            self.dispatchToParent("FoodEnter")
            
            self.FoodWatched = other.RuntimeId
        pass
    
    def onCollisionEnd(self, CollisionEvent):
        other = CollisionEvent.OtherObject
        
        if other.Collider.CollisionGroup.Name == "Food" and other.RuntimeId == self.FoodWatched:
            #self.Owner.Parent.Sprite.SpriteSource = "Dragon_Idle"
            self.Owner.DispatchUp("TauntEvent", Zero.ScriptEvent())
            self.dispatchToParent("FoodExit")
            pass
        pass
    
    def dispatchToParent(self, type):
        e = Zero.ScriptEvent()
        e.Type = type
        
        self.Owner.Parent.DispatchEvent("FoodDetectEvent", e)

Zero.RegisterComponent("FoodDetect", FoodDetect)