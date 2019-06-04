import Zero
import Events
import Property
import VectorMath

Vec4 = VectorMath.Vec4
Vec3 = VectorMath.Vec3

ItemTypes = Property.DeclareEnum("ItemTypes", ["Food", "Medicine", "Treasure"])

class InventoryManager:
    class Item:
        Name = ""
        Amount = 0
        Icon = ""
        Color = VectorMath.Vec4()
        Use = None
        
        def __init__(self, name, amount, icon, color, type):
            self.Name = name
            self.Amount = 0
            self.Icon = icon
            self.Color = color
            self.Type = type
        
        def Use(self, user, function = None):
            if not function:
                function = self.defaultUse
            
            function(user)
        
        def defaultUse(self, user):
            ItemEvent = Zero.ScriptEvent()
            ItemEvent.ItemData = self
            ItemEvent.ItemName = self.Name
            ItemEvent.ItemType = self.Type
            
            user.Owner.DispatchEvent("ItemUseEvent", ItemEvent)
    #end class item

    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        pass

    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "ItemUseEvent", self.onItemUse)
        self.Inventory = {}
        pass

    def UseItem(self, itemName):
        self.Inventory[itemName].Use(self.Owner)
    
    def AddItemParameters(self, Name, Amount, Icon, Color, Type):
        item = self.Item(Name, Amount, Icon, Color)
        
        self.AddItem(item)
    
    def AddItem(self, item):
        self.Inventory[item.Name] = item
    
    def onItemUse(self, ItemEvent):
        name = ItemEvent.ItemName
        type = ItemEvent.ItemType
        item = ItemEvent.ItemData
        raise
        
        if type == "Food":
            self.CreateFood(name, item)

Zero.RegisterComponent("InventoryManager", InventoryManager)