import Zero
import Events
import Property
import VectorMath

import random
import Action

Moods = Property.DeclareEnum("Moods", ["Neutral", "Content", "Happy", "VeryHappy", "Depressed", "Crying", "Angry", "Hungry", "Full", "Uncomfortable"])
PetActions = Property.DeclareEnum("PetActions", ["Idle", "Walking", "OpenMouth", "Eating", "Expression", "Sleeping", "Colapsing"])

class PetLogic:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        self.CurrentMood = Property.Enum(default = Moods.Neutral)
        self.CurrentAction = Property.Enum(default = PetActions.Idle)
        
        self.TauntLimit = Property.Uint(default = 2)
        
        self.TickTime = Property.Float(default = 90)
        pass

    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevel)
        Zero.Connect(self.Owner, "PetEvent", self.onPet)
        Zero.Connect(self.Owner, "TauntEvent", self.onTaunt)
        Zero.Connect(self.Owner, "FoodDetectEvent", self.onFood)
        Zero.Connect(self.Space, "MakeHappyEvent", self.onAddHappy)
        Zero.Connect(self.GameSession, "TimeProgression", self.onTimeProgression)
        
        self.ExpressionDuration = 4.0
        self.TauntCount = 0
        self.MoodLevels = {}
        
        for mood in Moods:
            self.MoodLevels[mood] = 0
        
        self.resetExpressionCounter()
        pass
    
    def onLevel(self, LevelEvent):
        e = Zero.ScriptEvent()
        e.Pet = self.Owner
        e.Sender = self.Owner
        self.Space.DispatchEvent("PetRegisterEvent", e)
        self.GameSession.DispatchEvent("PetRegisterEvent", e)
        
        self.registerTick()
    
    def changeMood(self, mood):
        self.CurrentMood = mood
        
        MoodEvent = Zero.ScriptEvent()
        MoodEvent.Mood = self.CurrentMood
        self.GameSession.DispatchEvent("MoodUpdateEvent", MoodEvent)
        print("[PetLogic] Mood Changed to:", self.CurrentMood)
    
    def addMood(self, mood, amount):
        self.MoodLevels[mood] += amount
        
        self.evaluateMood()
    
    def checkExpression(self):
        if self.CurrentAction == PetActions.Idle:
            expressionActionCheck = random.random()
            
            print("self.CheckingExpression")
            if expressionActionCheck < 0.65:
                self.changeAction(PetActions.Expression)
    
    def resetExpressionCounter(self):
        seq = Action.Sequence(self.Owner)
        Action.Delay(seq, 4)
        Action.Call(seq, self.checkExpression)
        Action.Call(seq, self.resetExpressionCounter)
    
    def changeAction(self, action):
        if action == PetActions.Eating:
            self.TauntCount = 0
            self.changeMood(Moods.Neutral)
        if action == PetActions.Expression:
            seq = Action.Sequence(self.Owner)
            Action.Delay(seq, self.ExpressionDuration)
            Action.Call(seq, self.changeAction, (PetActions.Idle))
        
        self.CurrentAction = action
        print("[PetLogic] Action Changed to:", self.CurrentAction)
    
    def evaluateMood(self):
        #this function takes the information in the mood levels and evaluates if they impact the pets emotions yet
         
         crying = self.MoodLevels[Moods.Crying]
         happy = self.MoodLevels[Moods.Happy] + self.MoodLevels[Moods.VeryHappy] * 2 + self.GameSession.Statistics.Happiness
         mad = self.MoodLevels[Moods.Angry]
         
         if crying - happy > 4:
             self.changeMood(Moods.Crying)
         elif happy - crying > 4:
             self.changeMood(Moods.Happy)
         else:
             self.changeMood(Moods.Neutral)

    def OnLogicUpdate(self, UpdateEvent):
        pass
    
    def evaluateTicks(self, ticks):
        for timeslice in range(ticks):
            #do shit
            pass
    
    def Tick(self):
        Statistics = self.GameSession.Statistics
        
        Statistics.addStat("Energy", -0.25)
        Statistics.addStat("Hunger", -0.25)
        
        happiness = Statistics.getStat("Happiness")
        happyMod =  0
        
        if happiness > 0:
            happyMod = -0.1
        elif happiness < 0:
            happyMod = 0.1
        
        Statistics.addStat("Happiness", happyMod)
        
        self.registerTick()
    
    def registerTick(self):
        seq = Action.Sequence(self.Owner)
        Action.Delay(seq, self.TickTime)
        Action.Call(seq, self.Tick)
    
    def onPet(self, e):
        type = e.Type
        
        if type == "ChangeMood":
            self.changeMood(e.Mood)
            #self.changeAction(e.Expression
    
    def onTaunt(self, e):
        self.TauntCount += 1
        self.addMood(Moods.Crying, 1)
        
        #if self.MoodLevels[Moods.Crying] > self.TauntLimit:
        #    self.changeMood(Moods.Crying)
    
    def onFood(self, e):
        type = e.Type
        
        if type == "FoodEnter":
            self.changeAction(PetActions.OpenMouth)
        elif type == "FoodExit":
            self.changeAction(PetActions.Idle)
            #self.onTaunt(e)
    
    def onAddHappy(self, e):
        self.addMood(Moods.Happy, 4)
    
    def onTimeProgression(self, TimeEvent):
        timePassed = TimeEvent.TimePassed
        
        self.evaluateTicks()
    
    def createPopText(self, text, position):
        obj = self.Space.CreateAtPosition("PopText", position)
        obj.SpriteText.Text = text

Zero.RegisterComponent("PetLogic", PetLogic)