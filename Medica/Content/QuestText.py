import Zero
import Events
import Property
import VectorMath

class QuestText:
    Text = Property.TextBlock()
    
    def Initialize(self, initializer):
        self.Owner.SpriteText.Text = self.Text.Text
        
        #for child in self.Owner.Hierarchy.Children:
            #child.Transform.Scale = self.GetSize()
    
    def GetSize(self, text = None):
        if not text:
            text = self.Text
        
        return self.Owner.SpriteText.MeasureGivenText(text)

Zero.RegisterComponent("QuestText", QuestText)