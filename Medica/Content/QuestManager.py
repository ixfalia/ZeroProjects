import Zero
import Events
import Property
import VectorMath

class QuestData:
    Name = ""
    CheckItems = {}
    CheckKeyItems = {}
    CheckFlags = {}
    Requirements = {}
    Rewards = {}
    
    def __init__(self, name, requires, flags, items, keyitems, rewards, questdescription):
        self.Name = name
        self.FlagsRequired = flags
        self.CheckItems = items
        self.CheckKeyItems = keyitems
        self.CheckFlags = flags
        self.Rewards = rewards
        self.Requirements = requires
        self.description = questdescription

class QuestManager:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "NewQuestEvent", self.onNewQuest)
        
        self.QuestEntries = {}
        self.ActiveQuests = {}
        self.CompletedQuests = {}
        
        self.NPCRelations = {}
        
        self.setQuests()
    
    def onNewQuest(self, e):
        self.addQuest(e.Name, e.Entry)
    
    def addQuest(self, name, entry):
        self.QuestEntries[name] = entry
    
    def setQuests(self):
        requirements = {}
        checkItems = {}
        checkFlags = {}
        checkKeys = {}
        rewards = {}
        
        #**********************************************
        ## TestQuest
        requirements = {"Demo":"Active"}
        checkItems = {"Demo Item":1}
        rewards = {"Demo State":True, "Demo Quest Complete":True}
        quest = QuestData("TestQuest", requirements, checkFlags, checkItems, checkKeys, rewards, "Quest_Test")
        
        #**********************************************
        ## Dirty Water
        requirements = {"Help The Town":"Active"}
        rewards = {"Renown Up":1}
        quest = QuestData("Dirty Water", requirements, None, None, None, rewards, "Quest_DirtyWater")
        
        #**********************************************
        ## Help The Town
        checkFlags = {"Artist's Masterpiece":"Complete", "Dirty Water":"Complete"}
        rewards = {"Town Stage 1":True}
        quest = QuestData("Help The Town", None, checkFlags, None, None, rewards, "Quest_HelpTheTown")
        
        #**********************************************
        ## Filling Up The Journal
        checkKeys = {"Serenian Water":0, "Saiga Flax":0, "Linjee Mushroom":0, "Whoober Tuber":0, "Purgidine Ore":0}
        checkFlags = {"Serenian Water":"Obtained", "Saiga Flax":"Obtained", "Linjee Mushroom":"Obtained", "Whoober Tuber":"Obtained", "Purgidine Ore":"Obtained"}
        rewards = {"Riverside Seal":1}
        quest = QuestData("Filling Up The Journal", None, checkFlags, None, None, rewards, "Tutorial_FirstQuest")
        
        pass

Zero.RegisterComponent("QuestManager", QuestManager)