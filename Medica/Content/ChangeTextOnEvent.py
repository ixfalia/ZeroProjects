import Zero
import Events
import Property
import VectorMath

class ChangeTextOnEvent:
    ListenFor = Property.String()
    ChangeTextTo = Property.String()
    
    def Initialize(self, initializer):
        if self.ListenFor:
            Zero.Connect(self.Space, self.ListenFor, self.onListened)
    
    def setData(self):
        if self.ListenFor:
            Zero.Connect(self.Space, self.ListenFor, self.onListened)
    
    def onListened(self, e):
        self.Owner.SpriteText.Text = self.ChangeTextTo

Zero.RegisterComponent("ChangeTextOnEvent", ChangeTextOnEvent)