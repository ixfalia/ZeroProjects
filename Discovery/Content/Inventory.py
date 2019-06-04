import Zero
import Events
import Property
import VectorMath

ItemList = Property.DeclareEnum("ItemList", ["KeyOrb","EmptyOrb","VoidOrb","RedOrb"])

class Inventory:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        self.StartingInventory = Property.String()
        self.ItemMax = Property.Int(default = 1)
        self.MaxCapacity = Property.Int(default = 1)
        self.Accepts = Property.String() #If restricted, what kind of orb does this node take
        pass

    def Initialize(self, initializer):
        self.InventoryTable = {}
        self.currentCapacity = 0
        #self.ItemMax = 1
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, "GiveInventoryEvent", self.onGiveInventory)
        Zero.Connect(self.Owner, "TakeInventoryEvent", self.onTakeInventory)
        
        for item in ItemList:
            self.setItem(item, 0)
        
        if not self.StartingInventory == "":
            self.StartingInventory = self.Owner.TextParser.ParseParameterText(self.StartingInventory)
            
            for key, value in self.StartingInventory.items():
                self.setItem(key, 0)
                self.addItem(key, value)
        pass

    def OnLogicUpdate(self, UpdateEvent):
        pass
    
    def setItem(self, itemName, value = False):
        self.InventoryTable[itemName] = value
    
    def addItem(self, itemName, amount = 1):
        if not itemName in self.InventoryTable:
            self.InventoryTable[itemName] = 0
        
        #self.InventoryTable[itemName] += int(amount)
        
        self.changeItem(itemName, amount)
        
        e = Zero.ScriptEvent()
        e.Type = itemName
        
        for i in range(int(amount)):
            self.Owner.DispatchEvent("AddItemEvent", e)
        #perhaps add a limit
        
        #print("{}(Inventory): \n\tAdded {} to Inventory. Total: {}".format(self.Owner.Name, itemName, self.InventoryTable[itemName]))
    
    def removeItem(self, itemName, amount = 1):
        if not itemName in self.InventoryTable:
            self.InventoryTable[itemName] = 0
        
        #self.InventoryTable[itemName] -= amount
        self.changeItem(itemName, -amount)
        
        e = Zero.ScriptEvent()
        e.Type = itemName
        
        self.Owner.DispatchEvent("RemoveItemEvent", e)
    
    def getItem(self, itemName):
        return self.InventoryTable[itemName]
    
    def changeItem(self, itemName, amount):
        amount = int(amount)
        
        total = self.InventoryTable[itemName] + int(amount)
        
        if total < 0:
            self.InventoryTable[itemName] = 0
        elif total > self.ItemMax:
            self.InventoryTable[itemName] = self.ItemMax
        else:
            self.InventoryTable[itemName] = total
            
            self.currentCapacity += amount
        
        e = Zero.ScriptEvent()
        self.Owner.DispatchEvent("UpdateEvent", e)
    
    def onGiveInventory(self, InventoryEvent):
        item = InventoryEvent.ItemName
        amount = InventoryEvent.ItemAmount
        
        self.giveItem(item, amount)
        pass
    
    def onTakeInventory(self, InventoryEvent):
        item = InventoryEvent.ItemName
        amount = InventoryEvent.ItemAmount
    
    def giveItemTo(self, recipient, itemName, amount = 1): 
        if not recipient.Inventory:
            raise
        if not amount:
            amount = 1
        currentItem = self.InventoryTable[itemName]
        
        if not currentItem - amount < 0:
            self.removeItem(itemName, amount)
            recipient.Inventory.addItem(itemName, amount)
        else:
            return None
    
    def getOrbType(self):
        #print(self.InventoryTable)
        if not bool(self.InventoryTable):
            for item in self.InventoryTable:
                if item > 0:
                    raise
                    return item
            
            return None
        else:
            return None

Zero.RegisterComponent("Inventory", Inventory)