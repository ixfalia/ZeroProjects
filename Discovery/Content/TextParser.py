import Zero
import Events
import Property
import VectorMath

class TextParser:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        self.Debug = Property.Bool(default = False)
        pass

    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        pass

    def OnLogicUpdate(self, UpdateEvent):
        pass
    
    def ParseParameterText(self, text):
        ReturnValue = {}
        ParameterList = text.split(',')
        
        for parameter in ParameterList:
            name, amount = parameter.split(":")
            ReturnValue[name] = amount
        
        if self.Debug:
            print("{}(TextParser): \n\t".format(self.Owner.Name), ReturnValue)
        return ReturnValue
    
    def ParseText(self, text, delim):
        splitted = text.split(delim)
        returnList = []
        for item in splitted:
            returnList.append(item.strip())
        return returnList

def ParseParameterText(text, OwnerName = None):
    ReturnValue = {}
    ParameterList = text.split(',')
    
    for parameter in ParameterList:
        name, amount = parameter.split(":")
        name = name.strip()
        ReturnValue[name] = eval(amount)
    
    if OwnerName:
        #print("{}(TextParser): \n\t".format(OwnerName, ReturnValue))
        pass
    return ReturnValue
    
def ParseText(text, delim):
    splitted = text.split(delim)
    returnList = []
    for item in splitted:
        returnList.append(item.strip())
    return returnList

Zero.RegisterComponent("TextParser", TextParser)