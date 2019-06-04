import Zero
import Events
import Property
import VectorMath

import Action
import Color

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
        Zero.Connect(Zero.Game, "DataFlagEvent", self.onFlag)
        #Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        #Zero.Connect(self.Space, "FlagUpdateEvent", self.onFlagUpdate) #for quests that require certain flags.
        
        self.Created = None
        self.QuestActive = False
        
        self.QuestMark = None
        self.bang = None
        #self.bangCreated = False
        self.otherbang = None
        self.Requirements = None
        
        self.BroadcastQuestAvailability()
        
        self.setData()
        
        if self.checkRequirements() and (not self.used or self.unlimitedUse):
            self.createQuestMarker()
            self.onReactivate(None)
            pass
    
    def setData(self):
        self.Requirements = None
        
        if self.RequireFlags:
            #self.Requirements = self.parseItems(self.RequireFlags)
            self.Requirements = Zero.Game.TextParser.StringToParameterLists(self.RequireFlags)
        
        if not self.checkRequirements():
            self.Owner.Reactive.Active = False
    
    def checkRequirements(self):
        if self.RequireFlags and not len(self.RequireFlags) <= 0:
            gameFlags = Zero.Game.Journal.DataFlags
            
            for flag in self.Requirements.keys():
                if not flag in gameFlags:
                    return False
                elif self.Requirements[flag] == gameFlags[flag]:
                    raise
                    return True
                elif self.Requirements[flag] == "Complete":
                    raise
                    if gameFlags[flag] == True:
                        return True
                elif self.Requirements[flag] == "Active":
                    return flag in gameFlags
            raise
            return False
        return True
    
    def onFlag(self, fEvent):
        name = fEvent.FlagName
        set = fEvent.Set
        gameFlags = Zero.Game.Journal.DataFlags
        
        
        if not self.Requirements or not name in self.Requirements:
            return
        
        #print(self.Owner.Name, self.Requirements, gameFlags)
        
        check = self.Requirements[name]
        
        if check == "Complete":
            check = True
        
        #if name in gameFlags:
        #if gameFlags[name] == check:
        if self.checkRequirements():
            self.activateQuest()
    
    def onActivate(self, e):
        if self.deactivated:
            return
        
        self.destroyBang()
        
        if not self.used or self.unlimitedUse or self.QuestActive:
            self.popUpPrompt()
        self.Freeze()
    
    def onUsed(self, e):
        self.destroyBang()
        
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
            self.Created = HUDFactory.createHUDObject("QuestBox", VectorMath.Vec3(), True)
        else:
            self.Created = HUDFactory.createHUDObject("PromptBox", VectorMath.Vec3(), True)
        
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
        print("WHoody",self.bang)
        self.destroyBang()
        
        if self.QuestMark:
            self.QuestMark.Destroy()
        
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
    
    def activateQuest(self):
        self.Owner.Reactive.Active = True
        
        if self.checkRequirements() and (not self.used or self.unlimitedUse):
            self.onReactivate(None)
            self.createQuestMarker()
            
            print("activateQuest():", self.bang)
            self.otherbang = self.bang
            
    
    def destroyBang(self):
        e = Zero.ScriptEvent()
        if self.bang:
            self.bang.Destroy()
            #self.bang.DispatchEvent("QuestMarkBangDestroy", e)
            #self.bang.Sprite.Visible = False
        if self.otherbang:
            print("DestroyBang", self.bang, self.otherbang)
            self.otherbang.Destroy()
            #self.otherbang.DispatchEvent("QuestMarkBangDestroy", e)
            #self.otherbang.Sprite.Color = Color.Red
        
        mark = self.Owner.FindChildByName("questmark")
        if mark:
            mark.Destroy()
    

Zero.RegisterComponent("Prompter", Prompter)