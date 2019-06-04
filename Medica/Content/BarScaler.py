import Zero
import Events
import Property
import VectorMath

class BarScaler:
    Percentage = Property.Float(default = 100)
    def Initialize(self, initializer):
        self.Percentage = self.Percentage/100
        self.StartingPercentage = self.Percentage

Zero.RegisterComponent("BarScaler", BarScaler)