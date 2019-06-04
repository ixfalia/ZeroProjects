import Zero
import Events
import Property
import VectorMath

import KeyboardController

InputActions = KeyboardController.InputActions

class PlayerLogic:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        pass

    def Initialize(self, initializer):
        self.DefaultLight = self.Owner.Light.Intensity
        self.OrbList = []
        
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevel)
        Zero.Connect(self.Owner, Events.CollisionPersisted, self.onCollisionPersist)
        Zero.Connect(self.Owner, "AddItemEvent", self.onAddItem)
        Zero.Connect(self.Owner, "RemoveItemEvent", self.onRemoveItem)
        Zero.Connect(self.GameSession, "PlayerPollEvent", self.onGetPlayer)
        
        PlayerEvent = Zero.ScriptEvent()
        
        PlayerEvent.Player = self.Owner
        PlayerEvent.Name = self.Owner.Name
        
        self.Space.DispatchEvent("PlayerCreationEvent", PlayerEvent)
        self.GameSession.DispatchEvent("PlayerCreationEvent", PlayerEvent)

    def onLevel(self, LevelEvent):
        self.Owner.Inventory.addItem("KeyOrb", 2)
    
    def OnLogicUpdate(self, UpdateEvent):
        self.GameSession.TimeWaitManager.OnLogicUpdate(UpdateEvent)
        self.updateLight()
        pass
    
    def onCollisionPersist(self, CollisionEvent):
        other = CollisionEvent.OtherObject
        
        if other.Collider.CollisionGroup.Name == "KeyNode":
            e = Zero.ScriptEvent()
            #e.ItemName = "KeyOrb"
            #other.DispatchEvent("TakeInventoryEvent", e)
            if self.Owner.KeyboardController.getKeyStatus(InputActions.ActivateKey):
                #other.Light.Active = False
                
                #other.Inventory.giveItemTo(self.Owner, "KeyOrb", 1)
                e = Zero.ScriptEvent()
                e.Activator = self.Owner
                e.Amount = 1 
                other.DispatchEvent("ActivateEvent", e)
        if other.Collider.CollisionGroup.Name == "Trigger":
            e = Zero.ScriptEvent()
            
            if not other.WarpLogic:
                return
            if not other.WarpLogic.Active:
                return
            
            if self.Owner.KeyboardController.getKeyStatus(InputActions.ActivateKey):
                self.playWarpAnimation()
                other.Warp.WarpMe(self.Owner)
    
    def updateLight(self):
        lights = self.Owner.Inventory.getItem("KeyOrb")
        
        self.Owner.Light.Intensity = lights+self.DefaultLight/5
    
    def onAddItem(self, iEvent):
        itemName = iEvent.Type
        
        if not itemName == "KeyOrb":
            return
        
        orb = self.Space.CreateAtPosition("KeyOrb", self.Owner.Transform.Translation + VectorMath.Vec3(-1, -1, 0))
        
        if self.OrbList:
            last = self.OrbList.pop()
            orb.FollowTarget.changeTarget(last)
            self.OrbList.append(last)
        else:
            PlayerEvent = Zero.ScriptEvent()
            
            PlayerEvent.Player = self.Owner
            PlayerEvent.Name = self.Owner.Name
            orb.FollowTarget.onPlayer(PlayerEvent)
        
        
        self.OrbList.append(orb)
        pass
    
    def onRemoveItem(self, iEvent):
        orb = self.OrbList.pop()
        orb.Destroy()
        pass
    
    def onGetPlayer(self, pEvent):
        PlayerEvent = Zero.ScriptEvent()
        
        PlayerEvent.Player = self.Owner
        PlayerEvent.Name = self.Owner.Name
        
        self.GameSession.DispatchEvent("PlayerCreationEvent", PlayerEvent)
        pEvent.Target.DispatchEvent("PlayerCreationEvent", PlayerEvent)
    
    def playWarpAnimation(self):
        pass

Zero.RegisterComponent("PlayerLogic", PlayerLogic)