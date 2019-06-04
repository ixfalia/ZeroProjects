import Zero
import Events
import Property
import VectorMath

import Action

Stats = Property.DeclareEnum("Stats", ["Health", "Stamina", "MaxHealth", "MaxStamina", "Physical", "Special", "Defense", "Resistance", "Speed", "Fullness", "Hunger", "Happiness", "Energy"])

class Statistics:
    def DefineProperties(self):
        defaultValue = 0.1 #stats go from 0-1, 1 being max
        
        self.Level = Property.Uint(default = 1)
        self.Health = Property.Float(default = 1.0)
        self.Stamina = Property.Float(default = 1.0)
        
        self.MaxHealth = Property.Uint(default = 100)
        self.MaxStamina = Property.Uint(default = 50)
        
        self.Physical = Property.Float(defaultValue)
        self.Special = Property.Float(defaultValue)
        self.Defense = Property.Float(defaultValue)
        self.Resistance = Property.Float(defaultValue)
        self.Speed = Property.Float(defaultValue) 
        
        self.MaxStat = Property.Uint(default = 255)
        
        self.Age = Property.Uint(default = 0)
        #self.LifeSpan = Property.Uint(default = 10)
        
        self.Fullness = Property.Float(default = 0.25)
        self.Hunger = Property.Float(default = 0.25)
        
        self.Happiness = Property.Float(0.0) #should go from
        self.Energy = Property.Float(1)
        
        self.isSick = Property.Bool()

    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, Events.LevelStarted, self.onLevel)
        Zero.Connect(self.Owner, "PetRegisterEvent", self.onPetRegister)
        Zero.Connect(self.Owner, "MoodUpdateEvent", self.onMoodUpdate)
        
        self.Pet = None
        self.StatChangeList = {}
        
        self.CurrentMood = None
        
        self.sendUpdate()
        pass
    
    def onLevel(self, LevelEvent):
        self.sendUpdate()

    def OnLogicUpdate(self, UpdateEvent):
        pass
    
    def addStat(self, stat, value):
        nuValue = self.__dict__[stat] + value
        
        if stat == Stats.Happiness:
            if nuValue < -1.0:
                nuValue = -1.0
        elif nuValue < 0:
            nuValue = 0.0
        
        if nuValue > 1:
            nuValue = 1.0
        
        self.updateStat(stat, nuValue)
    
    def updateStat(self, stat, value):
        old = self.__dict__[stat]
        self.__dict__[stat] = value
        
        if not old == value:
            print("[{}.Statistics]: {} stat updated from {} to {}".format(self.Owner.Name, stat, old, value))
            delta = value - old
            
            if stat == "Speed" or stat == "Fullness" or stat == "Happiness":
                pass
            elif delta < 0:
                self.StatChangeList[stat] = "{} {}".format( int(self.MaxStat * delta), stat)
            else:
                if stat == "Hunger":
                    name = "Stomach"
                else:
                    name = stat
                self.StatChangeList[stat] = "+{} {}".format( int(self.MaxStat * (value - old)), name)
        
        e = Zero.ScriptEvent()
        e.Type = stat
        e.Value = value
        e.Data = self.Owner
        
        self.Owner.DispatchEvent("StatUpdateEvent", e)
    
    def finishedAdding(self):
        timeoffset = 0.25
        distanceoffset = 3
        seq = Action.Sequence(self.Pet)
        Clock = self.Pet.Space.FindObjectByName("ClockBack")
        
        for stat in self.StatChangeList:
            pos = self.Pet.Transform.Translation
            nuPos = VectorMath.Vec3(pos.x, pos.y + distanceoffset, pos.z + 4)
            
            Action.Delay(seq, timeoffset)
            Action.Call(seq, self.Pet.PetLogic.createPopText, (self.StatChangeList[stat], nuPos))
            
            distanceoffset += 1.5
        
        Clock.SoundEmitter.Play()
    
    def createPopText(self, text, position):
        obj = self.Space.CreateAtPosition("PopText", position)
        obj.SpriteText.Text = text
    
    def sendUpdate(self):
        e = Zero.ScriptEvent()
        e.Data = self.Owner
        
        self.GameSession.DispatchEvent("StatUpdateEvent", e)
    
    def getStat(self, stat):
        value = None
        #value = eval("self.{}".format(stat))
        
        value = self.__dict__[stat]
        
        return value
    
    def setStat(self, stat, set):
        self.__dict__[stat] = set
    
    def onPetRegister(self, PetEvent):
        self.Pet = PetEvent.Sender
    
    def onMoodUpdate(self, MoodEvent):
        self.CurrentMood = MoodEvent.Mood
        
        print("Statstics knows that the mood is:", self.CurrentMood)

Zero.RegisterComponent("Statistics", Statistics)