import Zero
import Events
import Property
import VectorMath

import ItemsEnumerations
import Color

Vec3 = VectorMath.Vec3
TabTypes = ItemsEnumerations.EntryTypes

class JournalUI:
    BackColor = Property.Color()
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "MouseActivateEvent", self.onActivate)
        Zero.Connect(self.Space, "CloseUI", self.onClose)
        #Zero.Connect(self.Space, "AddEntry", self.onEntry)
        Zero.Connect(self.Space, "EnableEvent", self.onEnable)
        Zero.Connect(self.Space, "DisableEvent", self.onDisable)
        
        self.StartingPosition = Vec3(-5,3.5,0)
        
        self.Label = "Journal"
        self.Back = None
        self.JournalOpen = True
        
        self.Pages = []
        self.slots = []
        
        self.VecticalSpace = 1.5
        self.HorizonalSpace = 10
        
        self.DisableUI = False
        
        self.Rows = 7
        self.Columns = 2
        
        self.entryData = {}
        self.currentTab = "Mystery"
        
        self.PageSize = self.Rows * self.Columns
    
    def onActivate(self, e):
        #Zero.Game.Journal.printJournal()
        
        Zero.Disconnect(self.Space, "CloseUI", self.onClose)
        dEvent = Zero.ScriptEvent()
        self.Space.DispatchEvent("CloseUI", dEvent)
        Zero.Connect(self.Space, "CloseUI", self.onClose)
        self.updateSlots()
        
        if not self.Back:
            self.JournalOpen = True
            self.createJournal()
            self.disableSlots()
            self.enableSlots()
        elif not self.JournalOpen:
            self.updateSlots()
            self.fadeIn()
            self.disableSlots()
            self.enableSlots()
        else:
            self.fadeOut()
            self.disableSlots()
    
    def createJournal(self):
        self.slots = []
        self.createBack()
        
        position = self.StartingPosition
        x = 0
        i, k = 0, 0
        
        for i in range(self.Rows):
            x = 0
            y = position.y + (i*self.VecticalSpace) * -1
            
            for k in range(self.Columns):
                x = position.x + (k*self.HorizonalSpace)
                
                object = self.Space.CreateAtPosition("UIEntry", Vec3(x, y))
                object.Reactive.Active = False
                self.slots.append(object)
                self.Back.AttachToRelative(object)
                
                #print("({},{})".format(x, y))
        
        self.updateSlots()
    
    def updateSlots(self):
        if not self.slots:
            return
        
        items = Zero.Game.Inventory.items
        itemEntries = Zero.Game.Journal.ItemEntries
        locEntries = Zero.Game.Journal.LocationEntries
        
        itemFlags = Zero.Game.Journal.ItemFlags
        locFlags = Zero.Game.Journal.LocationFlags
        
        i = 0 
        self.wipeSlots()
        
        #make this stuff a function, or at least the checking a function, 
        #then you can easily check if i is out of bounds and needs to go to a new page
        for name in itemFlags.keys():
            if name in itemEntries:
                data = Zero.Game.Inventory.itemData[name]
                
                sprite = Zero.Game.Inventory.TypeSprites[data.type]
                slot = self.slots[i]
                slot.UIEntry.setData(name, data.sprite, data.color, itemEntries[name], self.Owner)
                
                #slot.Reactive.Active = True
                i += 1
        
        for name in locFlags.keys():
            print(name, locEntries)
            if name in locEntries:
                sprite = "icon_location"
                color = Color.ForestGreen
                slot = self.slots[i]
                slot.UIEntry.setData(name, sprite, color, locEntries[name], self.Owner)
                
                i+=1
        
        self.disableSlots()
        #self.enableSlots()
    
    def updateSlots2(self):
        if not self.slots:
            return
        i = 0
        
        for type in TabTypes:
            if i >= self.PageSize:
                break
            
            if len(self.entryData[type]) > 0:
                for data in self.entryData:
                    #data = entryData[type]
                    
                    slot = self.slots[i]
                    slot.UIEntry.setData(name, data.sprite, data.color, itemEntries[name])
                    slot.Reactive.Active = True
                    i += 1
        raise #implement this here
        #implement tab system. and page system.
    
    def createBack(self):
        self.Back = self.Space.CreateAtPosition("MenuBack", Vec3(0, 0, -1))
        b = self.Back.FindChildByName("Title")
        b.SpriteText.Text = self.Label
        self.Back.ColorNexus.BaseColor = self.BackColor
        self.Back.Fader.FadeIn()
    
    def onClose(self, e):
        if self.Back:
            self.fadeOut()
    
    def fadeOut(self):
        self.Back.Fader.FadeOut()
        self.JournalOpen = False
        
        for item in self.slots:
            item.Fader.FadeOut()
        
        self.disableSlots()
    
    def fadeIn(self):
        self.Back.Fader.FadeIn()
        self.JournalOpen = True
        
        for item in self.slots:
            item.Fader.FadeIn()
    
    def wipeSlots(self):
        for obj in self.slots:
            obj.UIEntry.resetData()
            obj.Reactive.Active = False
        self.disableSlots()
    
    def onEnable(self, e):
        self.enableSlots()
    
    def onDisable(self, e):
        self.disableSlots()
    
    def disableSlots(self):
        self.DisableUI = False
        
        for obj in self.slots:
            obj.Reactive.Active = False
    
    def enableSlots(self):
        self.DisableUI = True
        
        for obj in self.slots:
            if obj:
                if obj.UIEntry:
                    if obj.UIEntry.Active:
                        obj.Reactive.Active = True
    
    def setData(self):
        categories = ItemsEnumerations.categories
        
        for type in categories:
            self.entryData[type] = {}
    
    def onEntry(self, e):
        self.entryData[e.Type][e.Name] = e.Data
        self.disableSlots()
        #self.updateSlots2()

Zero.RegisterComponent("JournalUI", JournalUI)