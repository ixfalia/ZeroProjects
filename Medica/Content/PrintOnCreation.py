import Zero
import Events
import Property
import VectorMath

class PrintOnCreation:
    Message = Property.String()
    
    def Initialize(self, initializer):
        #print("\t[{}]: {}".format(self.Owner.Name, self.Message))
        print("\t[{}]: {}".format(self.Owner.Name, self.Message))

Zero.RegisterComponent("PrintOnCreation", PrintOnCreation)