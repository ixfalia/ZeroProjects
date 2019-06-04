import Zero
import Events
import Property
import VectorMath

class TextParser:
    def Initialize(self, initializer):
        pass
    
    def StringToParameterLists(self, parseMe, setDelimiter = ",", paramDelimiter = ":"):
        someString = str(parseMe)
        splitStrings = someString.split(",")
        
        parameters = {}
        setValue = None
        
        for element in splitStrings:
            splited = element.split(":")
            
            name = splited[0]
            value = None
            
            if len(splited) > 1:
                value = splited[1]
            
            setValue = self.setIndexValue(value)
            
            parameters[name.strip()] = setValue
        #endfor
        
        return parameters
    
    def parseString(self, parseMe, delim = None):
        if not delim:
            delim = ","
        
        someString = str(parseMe)
        splitStrings = someString.split(delim)
        
        parameters = {}
        
        for element in splitStrings:
            parameters[element.strip()] = 0
        
        return parameters
    
    def setIndexValue(self, value):
        if value:
            value = value.strip()
            
            if value == "Complete":
                #value = "Complete"
                return "Complete"
            elif value.isdigit():
                myValue = int(value.strip())
                
                #if myValue < 0:
                    #myValue = 1
                
                #value = myValue
                
                return myValue
            else:
                compare = value.capitalize()
                if compare == "False" or compare == "True":
                    #value = bool(compare)
                    return bool(compare)
                else:
                    #value = compare
                    return compare
        else:
            #amount = 1
            return 1
        
    def stringToBool(self, _string):
        return _string.capitalize() in ["True", "T", "Y"]

Zero.RegisterComponent("TextParser", TextParser)