import Zero
import Events
import Property
import VectorMath

class TextBoxController:
    def Initialize(self, initializer):
        #Zero.Connect(self.Owner, "AcceptEvent", self.onAccept)
        #Zero.Connect(self.Owner, "PreviousEvent", self.onPrev)
        #Zero.Connect(self.Owner, "NextEvent", self.onNext)
        #Zero.Connect(self.Space, "CloseUI", self.onCancel)
        #Zero.Connect(self.Owner, "CloseUI", self.onCancel)
        
        self.currentPage = 0
    
    def addPage(self, pageText):
        pass

Zero.RegisterComponent("TextBoxController", TextBoxController)