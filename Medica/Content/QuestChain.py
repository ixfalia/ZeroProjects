import Zero
import Events
import Property
import VectorMath

class QuestChain:
    Quests = Property.String()
    
    def Initialize(self, initializer):
        self.ActiveQuest = None
        
        self.parseQuests()
    
    def parseQuests(self):
        if self.Quests:
            chain = self.Quests.split("|")
            
            for pair in chain:
                splitted = pair.split(":")
                
                questName = splitted[0]
                
                if len(splitted) > 1:
                    flag = splitted[1]
            
            

Zero.RegisterComponent("QuestChain", QuestChain)