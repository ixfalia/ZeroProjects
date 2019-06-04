import Zero
import Events
import Property
import VectorMath

class Marvel:
    def __init__(self, name, text, discovered = False, color = None):
        self.Name = name
        self.Text = text
        self.Discovered = discovered
#endclass

class Collectable:
    def __init__(self, name, amount, text = None):
        self.Name = name
        self.Amount = amount
        self.Text = text

class CollectionBook:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        self.CollectionResource = Property.ResourceTable()
        pass

    def Initialize(self, initializer):
        self.CollectionTable = {}
        self.MarvelTable = {}
        self.Marvels = {}
        
        Zero.Connect(self.Owner, "CollectionEvent", self.onCollection)
        Zero.Connect(self.Owner, "MarvelEvent", self.onMarvel)
        pass
    
    def addMarvel(self, name, text, discovered = False):
        if not discovered:
            discovered = False
        
        self.MarvelTable[name] = Marvel(name, text, discovered)
        m = self.getMarvel(name)
        print(m.Name, m.Discovered, m.Text)
        print(self.MarvelTable)
    
    def discoverMarvel(self, name, discoverState = True):
        last = self.MarvelTable[name].Discovered
        
        self.Marvels[name] = discoverState
        self.MarvelTable[name].Discovered = discoverState
        
        if not last and discoverState:
            self.makeMarvelMessage("marvel")
        else:
            self.makeMarvelMessage("gotit")
    
    def makeMarvelMessage(self, name):
        children = self.Owner.PlayerTracker.Camera.Children
        
        for child in children:
            if child.Name == name:
                child.Celebration.onActivation(None)
    
    def getMarvel(self, name):
        if name in self.MarvelTable:
            return self.MarvelTable[name]
        else:
            return None
    
    def getMarvelCount(self):
        count = 0
        for m in self.MarvelTable:
            if m.Discovered:
                count += 1
        
        return count
    
    def getTotalMarvels(self):
        return len(self.MarvelTable)
    
    def addCollection(self, name, amount = 1, description = None):
        print(amount)
        raise
        if not name in self.CollectionTable:
            self.CollectionTable[name] = 0
        
        self.CollectionTable[name] += amount #to just add entry put amount = 0, to subtract just put amount = -#
    
    def getCollection(self, name):
        if name in self.CollectionTable:
            return self.CollectionTable[name]
        else:
            return None
    
    def onCollection(self, CollectionEvent):
        name = CollectionEvent.Name
        
        if CollectionEvent.Amount:
            amount = CollectionEvent.Amount
        else:
            amount = 1
        
        if self.CollectionEvent.TextBlock:
            description = CollectionEvent.TextBlock
        
        self.addCollection(name, CollectionEvent.Amount, CollectionEvent.TextBlock)
    
    def onMarvel(self, MarvelEvent):
        name = MarvelEvent.Name
        discovered = MarvelEvent.Discovered
        
        print("onMarvel:", name in self.MarvelTable, self.MarvelTable)
        
        if not name in self.MarvelTable:
            self.addMarvel(name, MarvelEvent.Text)
            print("onMarvel after Add:", self.MarvelTable)
        else:
            self.discoverMarvel(name, discovered)

Zero.RegisterComponent("CollectionBook", CollectionBook)