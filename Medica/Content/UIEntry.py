import Zero
import Events
import Property
import VectorMath

class UIEntry:
    EntryName = Property.String()
    Entry = Property.String()
    
    Offset = Property.Vector3()
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "MouseActivateEvent", self.onActivate)
        
        self.questData = None
        self.Active = False
    
    def setData(self, name, sprite, color, textBody, creator):
        text = self.Owner.FindChildByName("entryText")
        icon = self.Owner.FindChildByName("entryIcon")
        
        text.SpriteText.Text = name
        icon.Sprite.SpriteSource = sprite
        icon.Sprite.Color = color
        
        self.EntryName =  name
        self.Entry = textBody
        self.Active = True
        self.Creator = creator
        
        if self.EntryName in Zero.Game.Journal.QuestEntries:
            self.questData = Zero.Game.Journal.QuestEntries[self.EntryName]
    
    def onActivate(self, e):
        #ui = self.Space.FindObjectByName("journalButton")
        ui = self.Creator
        
        eBox = self.Space.CreateAtPosition("EntryBox", self.Offset)
        eBox.PromptBox.Creator = ui
        text = "~{}~\n\n\t {}".format(self.EntryName, self.Entry)
        
        if self.questData:
            eBox.PromptBox.CheckKeyItems = self.questData.keyItems
            eBox.PromptBox.CheckItems = self.questData.items
            eBox.PromptBox.CheckFlags = self.questData.flags
            eBox.PromptBox.Rewards = self.questData.rewards
            eBox.PromptBox.Text = self.questData.entry
            eBox.PromptBox.PromptName = self.questData.name
            
            eBox.PromptBox.setData(self.Owner)
        else:
            eBox.PromptBox.updateText(text)
        
        e = Zero.ScriptEvent()
        self.Space.DispatchEvent("DisableEvent", e)
    
    def resetData(self):
        text = self.Owner.FindChildByName("entryText")
        icon = self.Owner.FindChildByName("entryIcon")
        
        text.SpriteText.Text = ""
        icon.Sprite.SpriteSource = "BlankTile"
        
        self.Owner.Reactive.Active = False
        self.Active = False

Zero.RegisterComponent("UIEntry", UIEntry)