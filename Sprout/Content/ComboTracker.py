import Zero
import Events
import Property
import VectorMath

class ComboTracker:
    FeverForgiveness = Property.Uint(default = 2)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, "ComboEvent", self.onCombo)
        Zero.Connect(self.Space, "RemoveTurnEvent", self.onTurn)
        Zero.Connect(self.Space, "NoComboEvent", self.onComboFeverEnd)
        
        self.comboFever = 0
        self.highFever = 0
        self.comboTurn = 0
        self.comboHappend = False
        self.turnCount = 0
        self.turnsWithoutCombo = 0
    
    def onCombo(self, cEvent):
        chainLength = cEvent.ChainLength
        self.comboFever += 1
        self.turnsWithoutCombo = 0
        self.comboHappend = True
        self.comboTurn = self.turnCount
        
        print("*************** COMBO **************")
        print("\t\tFever:", self.comboFever)
        print("************************************")
        #raise
        
        if self.comboFever > self.highFever:
            self.highFever = self.comboFever
    
    def onTurn(self, tEvent):
        self.turnCount += 1
        #self.turnsWithoutCombo += 1
    
    def onComboFeverEnd(self, cEvent):
        if self.turnsWithoutCombo == self.FeverForgiveness:
            print("#################################################")
            print("#\t\tCOMBO FEVER ENDED:", self.comboFever)
            print("#\t\tHIGH FEVER:", self.highFever)
        
        if self.turnsWithoutCombo >= self.FeverForgiveness:
            self.comboFever = 0
            self.comboHappend = False
        
        self.turnsWithoutCombo += 1

Zero.RegisterComponent("ComboTracker", ComboTracker)