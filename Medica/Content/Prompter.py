import Zero
import Events
import Property
import VectorMath

import Action

boxTypes = ["PromptBox", "QuestBox", "EntryBox"]
BoxTypes = Property.DeclareEnum("BoxTypes", boxTypes)

class Prompter:
    CheckKeyItems = Property.String()
    CheckItems = Property.String()
    CheckFlags = Property.String()
    
    RequireFlags = Property.String()
    RequireKeyItems = Property.String()
    RequireItems = Property.String()
    
    Rewards = Property.String()
    SetFlags = Property.String()
    
    PopUpType = Property.Enum(default = BoxTypes.PromptBox, enum = BoxTypes)
    
    PromptName = Property.String(default = "UndefinedPrompterName")
    
    PromptText = Property.TextBlock()
    
    FreezeGame = Property.Bool(default = True)
    onEvent = Property.Bool(default = False)
    DetectedEvent = Property.String(default = "MouseActivateEvent")
    
    sendEventOnCompletion = Property.String()
    
    unlimitedUse = Property.Bool(False)
    used = Property.Bool(False)
    deactivated = Property.Bool(False)
    
    offset = Property.Vector3()
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "MouseActivateEvent", self.onActivate)
        Zero.Connect(self.Owner, "UsedEvent", self.onUsed)
        Zero.Connect(self.Owner, "DeactivateEvent", self.onDeactivate)
        Zero.Connect(self.Owner, "ReactivateEvent", self.onReactivate)
        Zero.Connect(self.Owner, "QuestComplete", self.onQuestComplete)
        #Zero.Connect(self.Space, "FlagUpdateEvent", self.onFlagUpdate) #for quests that require certain flags.
        
        self.Created = None
        self.QuestActive = False
        
        self.QuestMark = None
        self.bang = None
        
        self.BroadcastQuestAvailability()
        
        if not self.used or self.unlimitedUse:
            self.createQuestMarker()
            self.onReactivate(None)
            pass
    
    def onActivate(self, e):
        if self.deactivated:
            return
        
        if self.bang:
            self.bang.Destroy()
        
        if not self.used or self.unlimitedUse or self.QuestActive:
            self.popUpPrompt()
        self.Freeze()
    
    def onUsed(self, e):
        if self.bang:
            self.bang.Destroy()
        
        if self.unlimitedUse:
            self.deactivated = True
            
            seq = Action.Sequence(self.Owner)
            Action.Delay(seq, 2)
            Action.Call(seq, self.createQuestMarker)
            Action.Call(seq, self.onReactivate, (None))
        
        self.used = True
        self.BroadcastQuestAvailability()
    
    def onDeactivate(self, e):
        self.deactivated = True
    
    def onReactivate(self, e):
        self.deactivated = False
    
    def popUpPrompt(self):
        if not self.PopUpType == BoxTypes.PromptBox:
            self.createOtherBox()
            return
        
        myTransl = self.Owner.Transform.Translation
        position = VectorMath.Vec3(myTransl.x, myTransl.y, 3)
        HUD = Zero.Game.FindSpaceByName("HUDSpace")
        HUDFactory = HUD.FindObjectByName("HUDManager").HUDFactory
        
        if self.Created:
            self.Created.Destroy()
        
        #self.Created = HUD.CreateAtPosition("PromptBox", VectorMath.Vec3())
        if self.QuestActive:
            self.Created = HUDFactory.createHUDObject("QuestBox", VectorMath.Vec3())
        else:
            self.Created = HUDFactory.createHUDObject("PromptBox", VectorMath.Vec3())
        
        newGuy = self.Created
        
        newGuy.PromptBox.CheckKeyItems = self.CheckKeyItems
        newGuy.PromptBox.CheckItems = self.CheckItems
        newGuy.PromptBox.CheckFlags = self.CheckFlags
        newGuy.PromptBox.Rewards = self.Rewards
        newGuy.PromptBox.Text = self.PromptText
        newGuy.PromptBox.PromptName = self.PromptName
        
        newGuy.PromptBox.setData(self.Owner)
    
    def Freeze(self):
        pass
    
    def createQuestMarker(self):
        if self.QuestActive:
            return
        pos = self.Owner.Transform.Translation + VectorMath.Vec3(0, 3, 2)
        self.bang = self.Space.CreateAtPosition("QuestMarker", pos)
        
        self.bang.AttachToRelative(self.Owner)
    
    def onQuestComplete(self, e):
        if e.Quest == self.PromptName:
            self.QuestActive = False
            if self.QuestMark:
                self.QuestMark.Destroy()
            
            if self.sendEventOnCompletion:
                cE = Zero.ScriptEvent()
                self.Space.DispatchEvent(self.sendEventOnCompletion, cE)
    
    def popActiveMarker(self):
        iconColor = VectorMath.Vec4(0.71,1,0,1)
        pos = self.Owner.Transform.Translation + VectorMath.Vec3(0, 3, 2)
        self.QuestMark = self.Space.CreateAtPosition("QuestMarker", pos)
        self.QuestMark.Sprite.SpriteSource = "icon_mystery"
        self.QuestMark.AttachToRelative(self.Owner)
    
    def onQuestTaken(self):
        if self.bang:
            self.bang.Destroy()
        self.popActiveMarker()
        self.QuestActive = True
    
    def BroadcastQuestAvailability(self):
        if not self.PopUpType == BoxTypes.PromptBox:
            return
        
        e = Zero.ScriptEvent()
        
        e.Name = self.PromptName
        e.isComplete = self.used
        
        Zero.Game.DispatchEvent("QuestAvailableEvent", e)
    
    def createOtherBox(self):
        myTransl = self.Owner.Transform.Translation
        position = VectorMath.Vec3(myTransl.x, myTransl.y, 3)
        HUD = Zero.Game.FindSpaceByName("HUDSpace")
        HUDFactory = HUD.FindObjectByName("HUDManager").HUDFactory
        
        self.Created = HUDFactory.createHUDObject(self.PopUpType, VectorMath.Vec3())
        
        newGuy = self.Created
        
        newGuy.PromptBox.CheckKeyItems = self.CheckKeyItems
        newGuy.PromptBox.CheckItems = self.CheckItems
        newGuy.PromptBox.CheckFlags = self.CheckFlags
        newGuy.PromptBox.Rewards = self.Rewards
        newGuy.PromptBox.Text = self.PromptText
        newGuy.PromptBox.PromptName = self.PromptName
        
        newGuy.PromptBox.setData(self.Owner)

Zero.RegisterComponent("Prompter", Prompter)