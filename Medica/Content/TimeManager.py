import Zero
import Events
import Property
import VectorMath

import Color

class TimeManager:
    IncrementInHours = Property.Uint(default = 6)
    DaysRemaining = Property.Int(default = 4)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.LevelStarted, self.onLevel)
        Zero.Connect(self.Owner, "TimeIncrementEvent", self.onIncrement)
        
        self.Increment = self.IncrementInHours / 24.0
        self.TotalDays = self.DaysRemaining
        
        #self.updateHUDElements()
        #self.Owner.Journal.setFlagState("Whooby", True)
    
    def onLevel(self, lE):
        self.updateHUDElements()
    
    def onIncrement(self, iEvent):
        TimeTaken = e.Amount * self.Increment
        
        if not self.DaysRemaining == -1:
            self.DaysRemaining -= TimeTaken
            
            if self.DaysRemaining <= 0:
                self.DaysRemaining = 0
        
        e = Zero.ScriptEvent()
        e.TimePassed = TimeTaken
        
        Zero.Game.DispatchEvent("TimeForwardEvent", e)
    
    def updateHUDElements(self):
        HUDTimeLeft = Zero.Game.HUDFactory.HUDElements["DaysRemaining"]
        HUDCurrentTime = Zero.Game.HUDFactory.HUDElements["CurrentTime"]
        
        if self.DaysRemaining == 1:
            HUDTimeLeft.SpriteText.Text = "Final Day"
            HUDTimeLeft.SpriteText.Color = Color.Red
        else: #self.DaysRemaining == 1:
            HUDTimeLeft.SpriteText.Text = "{} Days remaining.".format(self.DaysRemaining)
        
        Day = (self.TotalDays - self.DaysRemaining) + 1
        HUDCurrentTime.SpriteText.Text = "{}:00 on Day {}".format(self.IncrementInHours, Day)

Zero.RegisterComponent("TimeManager", TimeManager)