import Zero
import Events
import Property
import VectorMath

class SetText:
    Text = Property.TextBlock()
    def Initialize(self, initializer):
        self.Owner.SpriteText.Text = self.Text.Text

Zero.RegisterComponent("SetText", SetText)