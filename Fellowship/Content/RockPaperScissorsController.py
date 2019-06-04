import Zero
import Events
import Property
import VectorMath

class RockPaperScissorsController:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        pass

    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Space, "CardSelectEvent", self.onCardSelect)
        #Zero.Connect(self.self, "", self.onPaper)
        #Zero.Connect(self.self, "", self.onScissors)
        
        pass

    def createCards(self):
        pass
    
    def onCardSelect(self, CardEvent):
        type = CardEvent.Sender.Name
        
        if type == "rock" or type == "earth":
            #raise
            pass
        elif type == "paper" or type == "wood":
            #raise
            pass
        elif type == "scissors" or type == "metal":
            #raise
            pass
        elif type == "fire":
            #raise
            pass
        elif type == "water":
            #raise
            pass
        
        CardEvent.Sender.Destroy()

Zero.RegisterComponent("RockPaperScissorsController", RockPaperScissorsController)