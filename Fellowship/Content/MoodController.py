import Zero
import Events
import Property
import VectorMath

Moods = Property.DeclareEnum("Moods", ["Neutral", "Content", "Happy", "VeryHappy", "Sad", "VerySad", "Angry", "Hungry", "Uncomfortable"])

class MoodController:
    def DefineProperties(self):
        self.Happiness = Property.Float()
        
        pass

    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        pass

    def OnLogicUpdate(self, UpdateEvent):
        pass

Zero.RegisterComponent("MoodController", MoodController)