import Zero
import Events
import Property
import VectorMath

import Color
import ItemsEnumerations

class Journal:
    Debug = Property.Bool(default = True)
    ItemDescriptions = Property.TextBlock()
    LocationDescriptions = Property.TextBlock()
    
    #Row = Property.Uint()
    #Column = Property.Uint()
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "AddJournalEntryEvent", self.onAddEntry)
        Zero.Connect(self.Owner, "QuestEvent", self.onQuest)
        Zero.Connect(self.Owner, "QuestAvailableEvent", self.onQuestAvailable)
        
            #Text Data for all the entries
        self.ItemEntries = {}
        self.MedicineEntries = {}
        self.CraftingEntries = {}
        self.QuestEntries = {}
        self.LocationEntries = {}
        
            #All the flags
        self.ItemFlags = {}
        self.LocationFlags = {}
        self.MedicineFlags = {}
        self.CraftingFlags = {}
        self.QuestFlags = {}
        self.CompletedQuestFlags = {}
        self.CharacterFlags = {}
        
            #Quests
        self.AvailableQuests = {}
        
        self.pushColors = {}
        
        self.DataFlags = {} #use this to store all the bool data, just index with name
        
        self.populateData()
        
        if self.Debug:
            #self.printJournalData()
            pass
    
    def onAddEntry(self, e):
        self.addEntry(e.Name, e.Type)
    
    def addEntry(self, name, type, state = None):
        if not name in self.DataFlags:
            self.DataFlags[name] = True
            print(name, "Added to Journal.")
        
        if not state == None:
            self.setFlagState(name, state)
        
        if type:
            if type == "Item":
                self.InsertInto(name, self.ItemFlags)
                #self.updateInventory()
                self.sendPushMessage(name, "Item")
            elif type == "Medicine":
                self.InsertInto(name, self.MedicineFlags)
            elif type == "Crafting":
                self.InsertInto(name, self.CraftingFlags)
            elif type == "Quest":
                self.InsertInto(name, self.QuestFlags)
                self.sendPushMessage(name, "Quest")
            elif type == "Character":
                self.InsertInto(name, self.CharacterFlags)
            elif type == "Location":
                self.InsertInto(name, self.LocationFlags)
                self.sendPushMessage(name, "Location")
    
    def InsertInto(self, name, data):
        if not name in data:
            data[name] = True
    
    def onQuest(self, e):
        pass
    
    def populateData(self):
        self.ItemEntries = self.parseItems(self.ItemDescriptions.Text)
        self.LocationEntries = self.parseItems(self.LocationDescriptions.Text)
        #self.MedicineEntries = self.parseItems(self.MedicineDescriptions.Text)
        #self.CharacterEntries = self.parseItems(self.CharacterDescriptions.Text)
        #self.CraftingEntries = self.parseItems(self.CraftingDescriptions.Text)
        
        #self.printJournal()
    
    def parseItems(self, parseMe):
        someString = str(parseMe)
        splitStrings = someString.split(";")
        
        list = {}
        
        for element in splitStrings:
            splited = element.split(":")
            
            name = splited[0]
            amount = None
            
            if len(splited) > 1:
                amount = splited[1]
            else:
                amount = ""
        #endfor
            
            list[name.strip()] = amount
        
        return list
    
    def printJournal(self):
        items = self.Owner.Inventory.items
        
        print("++++++++++++++++++++++++++++")
        print("Journal Entries:")
        print(self.DataFlags)
        
        for name in self.DataFlags.keys():
            if name in self.ItemEntries:
                print("\t__", name, "__")
                print("\t\t", self.ItemEntries[name])
        
        print("++++++++++++++++++++++++++++")
    
    def sendPushMessage(self, name, type, sound = None):
        iconColor = Color.Wheat
        message = ""
        sprite = "bang"
        backColor = None
        amount = None
        
        if type == "Quest":
            iconColor = VectorMath.Vec4(0.71,1,0,1)
            message = "added to Questbook."
            sound = "QuestGet"
        elif type == "Item":
            #data = Zero.Game.Inventory.itemData[name]
            data = Zero.Game.Inventory.getData(name)
            iconColor = data.color
            sprite = "icon_entry"#data.sprite
            message = "Entry added to Journal."
        elif type == "Location":
            iconColor = Color.DeepGreen
            sprite = "icon_location"
            message = "Location added to Journal."
            sound = "QuestComplete"
        
        message = Zero.Game.NotificationManager.CreatePushMessage(name, message, sprite, iconColor, sound, amount)
    
    def setPushColors(self):
        self.pushColors["Quest"] = Color.DarkGoldenrod.lerp(Color.Black, 0.75)
        self.pushColors["Item"] = Color.CadetBlue.lerp(Color.Black, 0.7)
    
    def updateInventory(self):
        hud = self.Owner.LevelManager.getHUDSpace()
        inv = hud.FindObjectByName("inventorybutton")
        inv.InventoryUI.updateInventory()
    
    def onQuestAvailable(self, e):
        print("\t[[Journal Received QuestAvailable:", e.Name, e.isComplete, "]]")
        self.AvailableQuests[e.Name] = e.isComplete
    
    def setFlagState(self, Name, Set):
        print("\tJournal Setting Data Flag:", Name, Set)
        #if Name in self.DataFlags and self.DataFlags[Name] == Set:
        #    return
        
        self.DataFlags[Name] = Set
        
        e = Zero.ScriptEvent()
        
        e.FlagName = Name
        e.State = Set
        
        self.Owner.DispatchEvent("DataFlagEvent", e)


Zero.RegisterComponent("Journal", Journal)