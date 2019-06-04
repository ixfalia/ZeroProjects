import Zero
import Events
import Property
import VectorMath
import Color

import ItemsEnumerations

Vec3 = VectorMath.Vec3
ItemTypes = ItemsEnumerations.Categories

class InventoryUI:
    #Rows = Property.Uint(default = 4)
    #Columns = Property.Uint(default = 12)
    BackColor = Property.Color()
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "MouseActivateEvent", self.onActivate)
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevel)
        Zero.Connect(self.Space, "CloseUI", self.onClose)
        
        self.StartingPosition = Vec3(-7.5,3,0)
        self.Rows = 4
        self.Columns = 7
        self.Spacing = 2.45
        self.slots = None
        self.Back = None
        self.Label = "Inventory"
        
        self.InventoryOpen = False
    
    def onActivate(self, e):
        #Zero.Game.Inventory.printInventory()
        Zero.Disconnect(self.Space, "CloseUI", self.onClose)
        dEvent = Zero.ScriptEvent()
        self.Space.DispatchEvent("CloseUI", dEvent)
        Zero.Connect(self.Space, "CloseUI", self.onClose)
        
        if not self.slots:
            self.InventoryOpen = True
            self.createInventory()
            self.updateInventory()
        elif not self.InventoryOpen:
            self.InventoryOpen =  True
            self.updateInventory()
            self.fadeIn()
            #self.updateInventory()
        else:
            self.fadeOut()
            self.InventoryOpen = False
        
        self.updatePauseState()
    
    def onLevel(self, e):
        #self.createInventory()
        #self.TestCreate()
        #self.fadeOut()
        pass
    
    def TestCreate(self):
        e = Zero.ScriptEvent()
        e.Name = "Whoober Tuber"
        e.Amount = 2
        Zero.Game.DispatchEvent("ItemGetEvent", e)
        e.Name = "Glacia Berry"
        Zero.Game.DispatchEvent("ItemGetEvent", e)
        e.Name = "Glacia Leaf"
        Zero.Game.DispatchEvent("ItemGetEvent", e)
        e.Name = "Salvia Leaf"
        Zero.Game.DispatchEvent("ItemGetEvent", e)
        e.Name = "Saiga Flax"
        Zero.Game.DispatchEvent("ItemGetEvent", e)
        e.Name = "Gooey Concoction"
        Zero.Game.DispatchEvent("ItemGetEvent", e)
        #HUD = Zero.Game.FindSpaceByName("HUDSpace")
        #HUDFactory = HUD.FindObjectByName("HUDManager").HUDFactory
        #item = HUDFactory.createHUDObject("UIItem", VectorMath.Vec3())
        #berry = Zero.Game.Inventory.itemData["Whoober Tuber"]
        
        #item.UIItem.setData(berry.name, berry.type, berry.color)
    
    def onClose(self, e):
        if self.InventoryOpen:
            self.Back.Fader.FadeOut()
            self.fadeOut()
            self.InventoryOpen = False
    
    def createInventory(self):
        self.slots = []
        position = self.StartingPosition
        x = 0
        i, k = 0, 0
        
        self.Back = self.Space.CreateAtPosition("MenuBack", Vec3(0, 0, -1))
        self.Back.ColorNexus.BaseColor = self.BackColor
        self.Back.Fader.FadeIn()
        
        b = self.Back.FindChildByName("Title")
        b.SpriteText.Text = self.Label
        
        for i in range(self.Rows):
            x = 0
            y = position.y + (i*self.Spacing) * -1
            
            for k in range(self.Columns):
                x = position.x + (k*self.Spacing)
                
                object = self.Space.CreateAtPosition("UIItem", Vec3(x, y))
                object.Reactive.Active = False
                self.slots.append(object)
                self.Back.AttachToRelative(object)
                
                #print("({},{})".format(x, y))
        
        self.updateInventory()
        #self.fadeIn()
    
    def destroyInventory(self):
        for item in self.slots:
            item.Fader.FadeDestroy()
        
        self.Back.Fader.FadeDestroy()
        
    
    def fadeIn(self):
        if not self.Back:
            return
        self.Back.Fader.FadeIn()
        
        for item in self.slots:
            item.Fader.FadeIn()
        
    
    def fadeOut(self):
        if not self.Back:
            return
        self.Back.Fader.FadeOut()
        
        for item in self.slots:
            item.Fader.FadeOut()
    
    def updateInventory(self):
        inventory = Zero.Game.Inventory.items
        
        print("currentInventory", inventory)
        i = 0
        
        self.wipeSlots()
        
        for name in inventory.keys():
            #print("updateInventory:", name, inventory[name])
            
            if inventory[name] > 0:
                #print("\t", name, inventory[name]>0)
                if not name in Zero.Game.Inventory.itemData:
                    Zero.Game.Inventory.setDefaultItemData(name)
                
                #print("\t {} Added to Inventory Slot {}".format(name, i))
                data = Zero.Game.Inventory.itemData[name]
                
                sprite = Zero.Game.Inventory.TypeSprites[data.type]
                slot = self.slots[i]
                slot.UIItem.setData(name, data.type, data.color)
                slot.Reactive.Active = True
                slot.Fader.FadeIn()
                
                i += 1
    
    def wipeSlots(self):
        for obj in self.slots:
            obj.UIItem.resetData()
    
    def updatePauseState(self):
        if self.InventoryOpen:
            pass

Zero.RegisterComponent("InventoryUI", InventoryUI)