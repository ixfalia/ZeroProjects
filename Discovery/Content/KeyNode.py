import Zero
import Events
import Property
import VectorMath

import Inventory
import Color

ItemList = Inventory.ItemList

class KeyNode:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        self.Active = Property.Bool(default = True)
        self.KeyName = Property.String()
        pass

    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, "ActivateEvent", self.onActivate)
        Zero.Connect(self.Owner, "GiveEvent", self.onGive)
        Zero.Connect(self.Owner, "TakeEvent", self.onTake)
        Zero.Connect(self.Owner, "UpdateEvent", self.onUpdate)
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevelStart)
        
        #self.updateState()
        
        pass

    def OnLogicUpdate(self, UpdateEvent):
        pass
    
    def onLevelStart(self, lEvent):
        self.updateState()
    
    def onUpdate(self, updateEvent):
        self.updateState()
    
    def onActivate(self, activateEvent):
        other = activateEvent.Activator
        amount = activateEvent.Amount
        
        if not self.KeyName == "":
            id = self.KeyName
            #raise
        else:
            id = self.Owner.Name
        
        e = Zero.ScriptEvent()
        e.ID = self.Owner.Name
        
        #keyEvent = Zero.ScriptEvent()
        #keyEvent.KeyName = id
        
        if self.Active:
            self.Owner.Inventory.giveItemTo(other, self.getKeyType(), amount)
            
            self.Space.DispatchEvent("UnpowerEvent", e)
            #keyEvent.Powered = False
        else:
            itemGiven = other.Inventory.giveItemTo(self.Owner, self.getKeyType(), amount)
            type = self.getKeyType()
            
            if self.Owner.Inventory.InventoryTable[type] > 0:
                self.Space.DispatchEvent("PowerEvent", e)
            #keyEvent.Powered = True
        
        #self.Space.DispatchEvent("KeyEvent", keyEvent)
        self.updateState()
    
    def getKeyType(self):
        keytype = "KeyOrb"
        return keytype
    
    def getKeyState(self):
        keytype = self.getKeyType()
        return self.Owner.Inventory.getItem(keytype)
    
    def updateState(self):
        total = self.getKeyState()
        type = self.Owner.Inventory.getOrbType()
        
        if not self.KeyName == "":
            id = self.KeyName
        else:
            id = self.Owner.Name
        
        #red = self.Owner.Inventory.getItem("RedOrb")
        
        #print("Type of Orb:", type)
        
        if total > 0:
            self.Active = True
            self.Owner.Light.Visible = True
        else:
            self.Active = False
            self.Owner.Light.Visible = False
        
        if type == "RedOrb":
            self.Owner.Light.Color = Color.Red
        
        if id == "TutorialDoor":
            print(self.Owner.Name, "| KeyEvent:", id, self.Active, "sent.")
            #raise
            pass
        
        keyEvent = Zero.ScriptEvent()
        keyEvent.KeyName = id
        keyEvent.Powered = self.Active
        self.Space.DispatchEvent("KeyEvent", keyEvent)
    
    def onGive(self):
        pass
    
    def onTake(self):
        pass
    
    def turnOff(self):
        pass

Zero.RegisterComponent("KeyNode", KeyNode)