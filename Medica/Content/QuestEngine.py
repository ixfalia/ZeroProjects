import Zero
import Events
import Property
import VectorMath

class QuestEngine:
    def Initialize(self, initializer):
        self.ActiveQuests = []
        self.CompletedQuests = []

Zero.RegisterComponent("QuestEngine", QuestEngine)