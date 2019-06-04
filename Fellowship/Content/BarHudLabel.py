import Zero
import Events
import Property
import VectorMath

import Color

Vec4 = VectorMath.Vec4

class BarHudLabel:
    def DefineProperties(self):
        UndefinedColor = Vec4(-1,-1,-1,-1)
        
        self.LabelName = Property.String()
        self.BarLevel = Property.Float(default = 0.1)
        self.StatName = Property.String()
        
        self.LowColor = Property.Color(default = UndefinedColor)
        self.HighColor = Property.Color(default = UndefinedColor)
        pass

    def Initialize(self, initializer):
        Zero.Connect(self.Space, "PetRegisterEvent", self.onPetRegister)
        
        if not self.StatName == "":
            Zero.Connect(self.Space, "StatUpdateEvent", self.onStat)
            Zero.Connect(self.GameSession, "StatUpdateEvent", self.onStat)
        
        if not self.LabelName:
            self.LabelName = self.StatName
        if not self.BarLevel:
            self.BarLevel = 0.01
        
        self.Label = self.Owner.FindChildByName("label")
        self.Label.SpriteText.Text = self.LabelName
        
        self.Bar = self.Owner.FindChildByName("bar")
        self.Bar.BarController.setValue(self.BarLevel)
        
        self.Pet = None
        self.CurrentValue = self.BarLevel
        self.UndefinedColor = Vec4(-1,-1,-1,-1)
        
        #Hot pink is (1, 0.411765, 0.705882, 1) Vec4(1, 0.411765, 0.705882, 1)
        if not self.LowColor == self.UndefinedColor:
            self.Bar.BarController.LowColor = self.LowColor
        if not self.HighColor == self.UndefinedColor:
            self.Bar.BarController.HighColor = self.HighColor

    def OnLogicUpdate(self, UpdateEvent):
        pass
    
    def setBar(self, value = None):
        if not value:
            value = self.CurrentValue
        
        #print("{}.BarHudLabel.setBar: Setting Bar to {}".format(self.Owner.Name, value))
        
        if self.StatName == "Happiness":
            value = (value + 1) / 2
        
        self.Bar.BarController.setValue(value)
        
        if self.LabelName == "":
            self.Label.SpriteText.Text = "{}:".format(self.StatName, int(value * 255))
        else:
            self.Label.SpriteText.Text = "{}:".format(self.LabelName, int(value * 255))
    
    
    def onStat(self, sEvent):
        type = sEvent.Type
        
        if type and type == self.StatName:
            value = sEvent.Value
        elif sEvent.Data:
            value = sEvent.Data.Statistics.getStat(self.StatName)
        else:
            return
        
        self.CurrentValue = value
        self.setBar(value)
    
    def onPetRegister(self, petEvent):
        if petEvent.Pet:
            self.Pet = petEvent.Pet
        
        self.CurrentValue = self.GameSession.Statistics.getStat(self.StatName)
        self.setBar()

Zero.RegisterComponent("BarHudLabel", BarHudLabel)