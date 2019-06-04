import Zero
import Events
import Property
import VectorMath

import ItemsEnumerations
import Color
import string

KeyItems = ItemsEnumerations.KeyItems

class Item:
    def __init__(self, name, limit = 8):
        self.name = name
        self.amount = 0
        self.type = None
        self.color = None
        self.sprite = None
        
        if not limit:
            limit = 8
        else:
            self.limit = limit
    
    def __str__(self):
        formatted = "Name:{} \n\tType:{} \n\tColor:{} \n\tLimit:{}".format(self.name, self.type, self.color.__str__(), self.limit)
        return formatted
    
    def __repr__(self):
        return self.__str__()
    
    def typeToSprite(self):
        pass
#end Class Item

class Inventory:
    Debug = Property.Bool(default = True)
    #ItemList = Property.ResourceTable()
    ParameterText = Property.TextBlock()
    
    def Initialize(self, initializer):
        #Zero.Connect(self.Space, "ItemGetEvent", self.onItemGet)
        #Zero.Connect(self.Space, "ItemRemove", self.onItemRemove)
        #Zero.Connect(self.Space, "GetInventory", self.onGetInventory)
        
        Zero.Connect(self.Owner, "ItemGetEvent", self.onItemGet)
        Zero.Connect(self.Owner, "ItemRemove", self.onItemRemove)
        Zero.Connect(self.Owner, "GetInventory", self.onGetInventory)
        
        self.itemData = {}
        self.items = {}
        
        self.setTypeSprites()
        self.populateItems()
    
    def onItemGet(self, e):
        self.addItem(e.Name, e.Amount)
        self.addItemNotification(e.Name, e.Amount)
    
    def addItem(self, itemName, amount = 1):
        print("\t[[{0}|Inventory]]".format(self.Owner.Name), itemName, "added to inventory.")
        if not itemName in self.items:
            self.items[itemName] = 0
            self.sendJournalEvent(itemName)
        
        self.items[itemName] += amount
        print("\t\t", itemName, "at", self.items[itemName])
    
    def removeItem(self, itemName, amount = 1):
        if not amount:
            amount = 1
        
        itemCount = self.items[itemName]
        remaining = itemCount - amount
        
        if remaining < 0:
            raise Warning("NotEnough")
        
        self.items[itemName] -= amount
    
    def checkItem(self, itemName):
        if self.Debug:
            print("==========================")
            print("// Inventory.CheckItem()")
            print("\tCurrent Inventory:", self.items)
        
        if not itemName in self.items and not itemName in KeyItems:
            self.items[itemName] = False
        elif not itemName in self.items:
            self.items[itemName] = 0
        
        if self.Debug:
            print("\tcheck inventory result:", self.items[itemName])
            print("==========================")
        return self.items[itemName]
    
    def onItemRemove(self, e):
        self.removeItem(e.Name, e.Amount)
    
    def onGetInventory(self, e):
        pass
    
    def printInventory(self):
        print("=============================")
        print("[[{0}|Inventory]]".format(self.Owner.Name), self.items)
        print("=============================")
    
    def populateItems(self):
        myString = self.ParameterText.Text
        splitLines = myString.split("\n")
        
        for line in splitLines:
            name, parameters = line.split(":")
            
            splitComma = parameters.split(",")
            
            name = name.strip()
            type = splitComma[0].strip()
            color = splitComma[1].strip()
            limit = None
            
            if len(splitComma) > 2:
                limit = splitComma[2]
            
            nuItem = Item(name)
            nuItem.type = type
            nuItem.color = eval("Color." + color)
            nuItem.sprite = self.TypeSprites[type]
            
            self.itemData[name] = nuItem
    
    def setDefaultItemData(self, name):
        nuItem = Item(name)
        nuItem.type = ItemsEnumerations.Categories.Mystery
        nuItem.color = Color.Red
        
        self.itemData[name] = nuItem
    
    def setTypeSprites(self):
        self.TypeSprites = {}
        
        for name in ItemsEnumerations.Categories:
            self.TypeSprites[name] = "icon_{}".format(name.lower())
        
    
    def sendJournalEvent(self, name):
        e = Zero.ScriptEvent()
        
        e.Name = name 
        e.Type = "Item"
        
        Zero.Game.DispatchEvent("AddJournalEntryEvent", e)
    
    def addItemNotification(self, name, amount):
        label = "Inventory"
        message = "Obtained {} x{}.".format(name, amount)
        
        data = self.itemData[name]
        noti = Zero.Game.NotificationManager.CreatePushMessage(label, message, data.sprite, data.color, "ItemGet", amount)
        noti.PushMessage.Item = name

Zero.RegisterComponent("Inventory", Inventory)