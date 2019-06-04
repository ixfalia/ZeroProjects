import Zero
import Events
import Property
import VectorMath

import Color
import Action

Vec3 = VectorMath.Vec3

class QuestUI:
    BackColor = Property.Color()
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "MouseActivateEvent", self.onActivate)
        Zero.Connect(self.Space, "CloseUI", self.onClose)
        Zero.Connect(Zero.Game, "NewQuestEvent", self.onQuest)
        Zero.Connect(Zero.Game, "QuestCompleteEvent", self.onQuestComplete)
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevel)
        
        self.Label = "Quests"
        self.Back = None
        self.QuestOpen = True
        
        self.StartingPosition = Vec3(-5,3.5,0)
        
        self.Pages = []
        self.slots = []
        
        self.VecticalSpace = 1.5
        self.HorizonalSpace = 10
        self.QuestCompletion = None
        
        self.DisableUI = False
        
        self.Rows = 7
        self.Columns = 2
        
        self.PageSize = self.Rows * self.Columns
    
    def onLevel(self, e):
        #self.updateQuestCompletion()
        pass
    
    def checkAvailableQuests(self):
        AvailableQuests = Zero.Game.Journal.AvailableQuests
        count = 0
        
        for quest in AvailableQuests:
            if AvailableQuests[quest]:
                count += 1
        return count
    
    def updateQuestCompletion(self):
        AvailableQuests = Zero.Game.Journal.AvailableQuests
        complete = self.checkAvailableQuests()
        
        #print(AvailableQuests)
        #print("\t[[ QuestUI Available Quests: {} / {} ]]".format(complete, len(AvailableQuests)))
        
        if not self.QuestCompletion:
            self.createQuest()
            self.fadeOut()
            self.QuestCompletion = self.Back.FindChildByName("usefulTextR")
        
        self.QuestCompletion.SpriteText.Text = "Quest Completion: {} / {}".format(complete, len(AvailableQuests))
        
        if complete >= len(AvailableQuests):
            color = Color.Green
        else:
            color = Color.Gold
        
        self.QuestCompletion.ColorNexus.BaseColor = color
        self.QuestCompletion.SpriteText.Color = color
    
    def onActivate(self, e):
        Zero.Disconnect(self.Space, "CloseUI", self.onClose)
        dEvent = Zero.ScriptEvent()
        self.Space.DispatchEvent("CloseUI", dEvent)
        Zero.Connect(self.Space, "CloseUI", self.onClose)
        
        if not self.Back:
            self.QuestOpen = True
            self.createQuest()
            self.updateQuestCompletion()
        elif not self.QuestOpen:
            self.updateSlots()
            self.updateQuestCompletion()
            self.fadeIn()
            self.disableSlots()
            self.enableSlots()
        else:
            self.fadeOut()
    
    def createQuest(self):
        self.Back = self.Space.CreateAtPosition("MenuBack", Vec3(0, 0, -1))
        b = self.Back.FindChildByName("Title")
        self.QuestCompletion = self.Back.FindChildByName("usefulTextR")
        b.SpriteText.Text = self.Label
        self.Back.ColorNexus.BaseColor = self.BackColor
        self.updateQuestCompletion()
        self.Back.Fader.FadeIn()
        
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
        
        #items = Zero.Game.Inventory.items
        #itemEntries = Zero.Game.Journal.ItemEntries
        
        #dataFlags = Zero.Game.Journal.DataFlags
        Quests = Zero.Game.Journal.QuestFlags
        Completed = Zero.Game.Journal.AvailableQuests
        iconColor = VectorMath.Vec4(0.71,1,0,1)
        
        i = 0 
        self.wipeSlots()
        
        for name in Quests.keys():
            if name in Zero.Game.Journal.QuestEntries:
                data = Zero.Game.Journal.QuestEntries[name]
                slot = self.slots[i]
                
                if Completed[name]:
                    slot.UIEntry.setData(data.name, "check", Color.ForestGreen, data.entry.Text)
                else:
                    slot.UIEntry.setData(data.name, "bang", iconColor, data.entry.Text)
                
                slot.Reactive.Active = True
                i += 1
        #self.disableSlots()
        #self.enableSlots()
    
    def fadeOut(self):
        self.Back.Fader.FadeOut()
        self.QuestOpen = False
        
        for item in self.slots:
            item.Fader.FadeOut()
    
    def fadeIn(self):
        self.Back.Fader.FadeIn()
        self.QuestOpen = True
        
        for item in self.slots:
            item.Fader.FadeIn()
    
    def onClose(self, e):
        if self.QuestOpen and self.Back:
            self.Back.Fader.FadeOut()
            self.fadeOut()
            self.QuestOpen = False
    
    def wipeSlots(self):
        for obj in self.slots:
            obj.UIEntry.resetData()
            obj.Reactive.Active = False
    
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
    
    def onQuest(self, e):
        pass
    
    def checkforQuestCompletion(self):
        AvailableQuests = Zero.Game.Journal.AvailableQuests
        complete = self.checkAvailableQuests()
        
        #print(AvailableQuests)
        #print("\t[[ QuestUI Available Quests: {} / {} ]]".format(complete, len(AvailableQuests)))
        
        if not self.QuestCompletion:
            self.createQuest()
            self.fadeOut()
            self.QuestCompletion = self.Back.FindChildByName("usefulTextR")
        
        if complete >= len(AvailableQuests):
            self.Celebrate()
    
    def onQuestComplete(self, e):
        self.checkforQuestCompletion()
        pass
    
    def Celebrate(self):
        self.Space.CreateAtPosition("CelebrationMessage", Vec3(0, 7, 5))
        seq = Action.Sequence(self.Owner)
        Action.Delay(seq, 3.5)
        Action.Call(seq, self.LevelDone)
    
    def LevelDone(self):
        e = Zero.ScriptEvent()
        Zero.Game.DispatchEvent("LevelComplete", e)

Zero.RegisterComponent("QuestUI", QuestUI)