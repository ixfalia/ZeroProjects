import Zero
import Events
import Property
import VectorMath

#Listens for specific messages and updates text
class TextUpdateListener:
    DebugMode = Property.Bool(default = False)
    
    EventType = Property.String(default = "")
    
    def Initialize(self, initializer):
        if not self.EventType == "":
            Zero.Connect(self.Space, self.EventType, self.onEvent)
            
    def onEvent(self, Event):
        if self.DebugMode:
            print("TextUpdateListener.onEvent(): Updating text")
        
        if Event.Type == "Add":
            self.Owner.SpriteText.Text = str(int(Event.String) + int(self.Owner.SpriteText.Text))
        elif Event.Type == "Subtract":
            self.Owner.SpriteText.Text = str(int(Event.String) - int(self.Owner.SpriteText.Text))
        else:
            self.Owner.SpriteText.Text = str(Event.String)
        
        #later should probably do this instead
        #Event.Function(self.Owner) the function should accept this object's self to perform maniuplations

Zero.RegisterComponent("TextUpdateListener", TextUpdateListener)