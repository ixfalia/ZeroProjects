import Zero
import Events
import Property
import VectorMath

import string
import Color

class questData:
    def __init__(self, name, EntryText, Items, KeyItems, Flags, Rewards):
        self.name = name
        self.entry = EntryText
        self.items = Items
        self.keyItems = KeyItems
        self.flags = Flags
        self.rewards = Rewards

class PromptBox:
    CheckKeyItems = Property.String()
    CheckItems = Property.String()
    CheckFlags = Property.String()
    
    Rewards = Property.String()
    SetFlags = Property.String()
    
    Text =  Property.TextBlock()
    PromptName = Property.String()
    
    #unlimitedUse = Property.Bool(False)
    #used = Property.Bool(False)
    #deactivated = Property.Bool(False)
    
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "AcceptEvent", self.onAccept)
        Zero.Connect(self.Owner, "DeclineEvent", self.onDecline)
        Zero.Connect(self.Owner, "SubmitEvent", self.onSubmit)
        Zero.Connect(self.Owner, "CancelEvent", self.onCancel)
        
        Zero.Connect(self.Owner, "PreviousEvent", self.onPrev)
        Zero.Connect(self.Owner, "NextEvent", self.onNext)
        Zero.Connect(self.Space, "CloseUI", self.onCancel)
        
        self.setData(None)
        self.Creator = None
        
        right = self.Owner.FindChildByName("NextButton")
        
        self.SliderButtonColor = right.Sprite.Color
        self.leftDisabled = False
        self.rightDisabled = False
        
        if self.Owner.SoundEmitter:
            self.Owner.SoundEmitter.PlayCue("PopUp")
        
        
    
    def setData(self, creator):
        self.KeyItems = None
        self.Items = None
        self.Flags = None
        self.ItemRewards = None
        
        self.PromptText = ""
        self.PromptDetails = ""
        
        self.TextPages = []
        self.CurrentPage = 0
        
        self.Creator = creator
        
        textParser = self.Owner.TextParser.StringToParameterLists
        
        if self.CheckKeyItems:
            #self.KeyItems = self.parseItems(self.CheckKeyItems)
            self.KeyItems = textParser(self.CheckKeyItems)
        if self.CheckItems:
            #self.Items = self.parseItems(self.CheckItems)
            self.Items = textParser(self.CheckItems)
        if self.CheckFlags:
            #self.Flags = self.parseItems(self.CheckFlags)
            self.Flags = textParser(self.CheckFlags)
        if self.Rewards:
            #self.ItemRewards = self.parseItems(self.Rewards)
            self.ItemRewards = textParser(self.Rewards)
        
        if self.Text.Name == "DefaultTextBlock":
            self.Text = None
        
        self.setText()
        self.checkPages()
        self.updateText()
        
        result = self.doYouHaveWhatIWant()
        
        if not result:
            button = self.Owner.FindChildByName("submitText")
            
            if button:
                back = button.FindChildByName("ButtonBack")
                color = back.Sprite.Color
                back.Sprite.Color = color.lerp(Color.Black, 0.8)
                button.SpriteText.Color = Color.Black
                back.Reactive.Active = False
    
    def onAccept(self, aEvent):
        ev = Zero.ScriptEvent()
        
        self.Creator.Prompter.QuestActive = True
        #self.Creator.DispatchEvent("UsedEvent", ev)
        
        #self.createPushMessage()
        self.Creator.Prompter.onQuestTaken()
        #self.Creator.Prompter.bang.Destroy()
        self.AddJournalEntry()
        self.sendQuestData()
        self.closeBox()
    
    
    def onSubmit(self, sEvent):
        if not self.Items and not self.KeyItems and not self.Flags:
            self.closeBox()
            return
        
        result = self.doYouHaveWhatIWant()
        
        #obj = Zero.Game.HUDFactory.createHUDObject("PushMessage", VectorMath.Vec3(9,0,1))
        
        backColor = Color.DarkGoldenrod.lerp(Color.Black, 0.75)
        iconColor = VectorMath.Vec4(0.71,1,0,1)
        name = self.Creator.Prompter.PromptName
        
        Zero.Game.NotificationManager.CreatePushMessage("Quest", "'{}' Completed!".format(name), "bang", iconColor, "QuestGet")
        #obj.PushMessage.setData("Quest", "Completed!", "bang", iconColor)
        
        if result:
            print("[[{0}|PromptBox]]:".format(self.Owner.Name), "Required items found in inventory")
            if self.Items:
                self.takeItems()
            
            if self.ItemRewards:
                self.GiveItems()
            
            if self.Creator.Prompter:
                e = Zero.ScriptEvent()
                self.Creator.DispatchEvent("UsedEvent", e)
                e.Quest = self.PromptName
                self.Creator.DispatchEvent("QuestComplete", e)
            
            e = Zero.ScriptEvent()
            Zero.Game.DispatchEvent("QuestCompleteEvent", e)
            Zero.Game.Journal.setFlagState(self.PromptName, True)
            
            #print(Zero.Game.Journal.DataFlags)
            self.closeBox()
    
    def onDecline(self, e):
        self.Creator.Prompter.createQuestMarker()
        self.closeBox()
    
    def onCancel(self, e):
        self.closeBox()
    
    def AddJournalEntry(self):
        Zero.Game.Journal.addEntry(self.PromptName, "Quest", False)
        Zero.Game.Journal.setFlagState(self.PromptName, False)
    
    def createPushMessage(self):
        eh = Zero.ScriptEvent()
        
        eh.Object = "PushMessage"
        eh.Offset = VectorMath.Vec3(9,0,1)
        #Zero.Game.HUDEventDispatcher.DispatchHUDEvent("CreateHUDObject", eh)
        obj = Zero.Game.HUDFactory.createHUDObject(eh.Object, eh.Offset)
        backColor = Color.DarkGoldenrod.lerp(Color.Black, 0.75)
        iconColor = VectorMath.Vec4(0.71,1,0,1)
        name = self.Creator.Prompter.PromptName
        obj.PushMessage.setData("Quest", "Added to Questbook.", "bang", iconColor)
    
    def parseString(self, parseMe):
        someString = str(parseMe)
        splitStrings = someString.split(",")
        
        list = {}
        for element in splitStrings:
            list[element.strip()] = 0
        
        return list
    
    def populateDictionary(self, list, dictionary):
        for element in list:
            dictionary[element] = None
    
    def takeItems(self):
        for item in self.Items.keys():
            e = Zero.ScriptEvent()
            e.Name = item
            e.Amount = self.Items[item]
            Zero.Game.DispatchEvent("ItemRemove", e)
        
        Zero.Game.Inventory.printInventory()
    
    def closeBox(self):
        e = Zero.ScriptEvent()
        self.Space.DispatchEvent("ReactiveExit", e)
        self.Owner.Fader.FadeDestroy()
        
        e = Zero.ScriptEvent()
        Zero.Game.GameSpaceEventDispatcher.DispatchGameSpaceEvent("UnfreezeEvent", e)
        
        if self.Owner.SoundEmitter:
            self.Owner.SoundEmitter.PlayCue("PopDown")
        
        self.enableUI()
    
    
    def doYouHaveWhatIWant(self):
        if not self.Items and not self.KeyItems and not self.Flags:
            return True #Quests with no requirements exist!
        
        if self.Items and not len(self.Items) <= 0:
            for item in self.Items:
                    #check if the item is in the inventory
                result = Zero.Game.Inventory.checkItem(item)
                #print("Doyouhavewhatiwant", item, result, self.Items)
                if not result or result < self.Items[item]:
                    return False
        
        if self.KeyItems and not len(self.KeyItems) <= 0:
            for item in self.KeyItems:
                    #check if the item is in the inventory
                result = Zero.Game.Inventory.checkItem(item)
                #print("Doyouhavewhatiwant", item, result, self.KeyItems)
                if not result or result < self.KeyItems[item]:
                    return False
        
        if self.Flags and not len(self.Flags) <= 0:
            gameFlags = Zero.Game.Journal.DataFlags
            
            for flag in self.Flags.keys():
                if not flag in gameFlags:
                    return False
                elif self.Flags[flag] == gameFlags[flag]:
                    return True
                elif self.Flags[flag] == "Complete" or self.Flags[flag] == "Obtained":
                    if gameFlags[flag] == True:
                        return True
                elif self.Flags[flag] == "Active":
                    if flag in gameFlags:
                        return True
            return False
        
        return True
    
    def GiveItems(self):
        if not self.ItemRewards:
            return
        
        for item in self.ItemRewards.keys():
            Name = item
            Amount = self.ItemRewards[item]
            #print(Name, Amount, type(Amount))
            
            if isinstance(Amount, bool):
                Zero.Game.Journal.setFlagState(Name, Amount)
            elif Amount == "Set":
                Zero.Game.Journal.setFlagState(Name, True)
            elif Amount > 0:
                e = Zero.ScriptEvent()
                e.Name = Name
                e.Amount = Amount
                
                Zero.Game.DispatchEvent("ItemGetEvent", e)
            elif Amount <= 0:
                Amount = 1
                e = Zero.ScriptEvent()
                e.Name = Name
                e.Amount = Amount
                
                Zero.Game.DispatchEvent("ItemGetEvent", e)
    
    def setText(self):
        #print("PromptBox:",self.Items, self.KeyItems, self.ItemRewards)
        
        #Change Me Later
        if self.Text:
            if self.Owner.ArchetypeName == "EntryBox":
                pass
            else:
                self.PromptText += "~{}~".format(self.PromptName) + "\n\n"
            
            splitted = self.Text.Text.split("|")
            first = False
            
            for page in splitted:
                if not first:
                    page = self.PromptText + page
                    first = True
                
                self.TextPages.append(page)
        
        self.PromptDetails += "Quest Requirements: \n"
        
        if self.Items:
            for key in self.Items.keys():
                self.PromptDetails += "    * {0}: x{1} \n".format(key, self.Items[key])
        
        if self.KeyItems:
            for key in self.KeyItems.keys():
                self.PromptDetails += "    * Obtained: {0} \n".format(key)
                #print (self.PromptDetails)
        
        if self.Flags:
            for key in self.Flags.keys():
                if self.Flags[key] == "Complete":
                    self.PromptDetails += "    * Completed Quest: {}\n".format(key)
                elif self.Flags[key] == "Obtained":
                    self.PromptDetails += "    * Obtained: {}\n".format(key)
        
        if self.Rewards:
            pushString = ""
            
            for key in self.ItemRewards.keys():
                #print("Rewards:", self.ItemRewards[key])
                reward = self.ItemRewards[key]
                
                if isinstance(reward, int) and not isinstance(reward, bool):
                    pushString += "    * {0}: x{1} \n".format(key, reward)
                elif reward == "Set":
                    pushString += "    * Gain: \"{}\"\n".format(key)
            
            if not pushString == "":
                self.PromptDetails += "\nReward: \n"
                self.PromptDetails += pushString
        
        if self.Items or self.KeyItems or self.Flags:
            self.TextPages.append(self.PromptDetails)
        
        self.Owner.SpriteText.Text = self.PromptText
        
        self.updateText()
    
    def onNext(self, e):
        TotalPages = len(self.TextPages)
        
        self.CurrentPage += 1
        
        if self.CurrentPage > TotalPages-1:
            self.CurrentPage = TotalPages-1
        
        self.updateText()
        #self.updatePageNumber(TotalPages)
    
    def onPrev(self, e):
        TotalPages = len(self.TextPages)
        
        self.CurrentPage -= 1
        
        if self.CurrentPage < 0:
            self.CurrentPage = 0
        
        self.updateText()
        #self.updatePageNumber(TotalPages)
    
    def updatePageNumber(self, total = None):
        if not total:
            total = len(self.TextPages)
        
        text = self.Owner.FindChildByName("pagenumber")
        
        if total <= 1:
            text.SpriteText.Text = ""
        else:
            text.SpriteText.Text = "{} /{}".format(self.CurrentPage+1, total)
    
    def updateText(self, text = None):
        if not text and self.TextPages:
            self.Owner.SpriteText.Text = self.TextPages[self.CurrentPage]
        elif text:
            self.Owner.SpriteText.Text = text
            self.CurrentPage = 0
            self.TextPages = []
            
            #self.disableArrows()
            
            left = self.Owner.FindChildByName("PreviousButton")
            right = self.Owner.FindChildByName("NextButton")
            
            #left.Destroy()
            #right.Destroy()
            return
        else:
            self.Owner.SpriteText.Text = "Text not specified"
        
        self.checkPages()
        self.updatePageNumber()
    
    def checkPages(self):
        left = self.Owner.FindChildByName("PreviousButton")
        right = self.Owner.FindChildByName("NextButton")
        
        if len(self.TextPages) <= 1:
            self.disableArrows()
            return
        
        if self.CurrentPage == 0:
            self.rightDisabled = True
            self.leftDisabled = True
            
            self.fadeEnable(right)
            self.fadeDisable(left)
            
        elif self.CurrentPage >= len(self.TextPages)-1:
            self.leftDisabled = False
            self.rightDisabled = True
            
            self.fadeEnable(left)
            self.fadeDisable(right)
        elif self.CurrentPage > 0 and self.CurrentPage < len(self.TextPages):
            self.enableArrows()
    
    def disableArrows(self):
        left = self.Owner.FindChildByName("NextButton")
        right = self.Owner.FindChildByName("PreviousButton")
        self.fadeDisable(left)
        self.fadeDisable(right)
    
    def enableArrows(self):
        left = self.Owner.FindChildByName("NextButton")
        right = self.Owner.FindChildByName("PreviousButton")
        
        self.rightDisabled = False
        self.leftDisabled = False
        
        self.fadeEnable(left)
        self.fadeEnable(right)
    
    def fadeEnable(self, object):
        #object.Fader.FadeIn(0.25)
        object.Sprite.Visible = True
        object.Sprite.Color = Color.Yellow #self.SliderButtonColor
        #object.ColorNexus.BaseColor = Color.Yellow
        object.Reactive.Active = True
        
    def fadeDisable(self, object):
        #object.Fader.FadeOut(0.25)
        #object.Sprite.Visible = False
        object.Sprite.Visible = False
        color = object.Sprite.Color
        #object.Sprite.Color = color.lerp(Color.DarkGray, 0.8)
        #object.ColorNexus.BaseColor = color.lerp(Color.DarkGray, 0.8)
        object.Reactive.Active = False
    
    def enableUI(self):
        e = Zero.ScriptEvent()
        self.Space.DispatchEvent("EnableEvent", e)
    
    def sendQuestData(self):
        data = questData(self.PromptName, self.Text, self.CheckItems, self.CheckKeyItems, self.CheckFlags, self.Rewards)
        Zero.Game.Journal.QuestEntries[self.PromptName] = data
    
    def split_by_length(s,block_size):
        w=[]
        n=len(s)
        for i in range(0,n,block_size):
            w.append(s[i:i+block_size])
        
        return w

Zero.RegisterComponent("PromptBox", PromptBox)