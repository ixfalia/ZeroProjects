import Zero
import Events
import Property
import VectorMath

import Color

TypeList = ["Water", "Wood", "Fire", "Earth", "Metal"]
Types = Property.DeclareEnum("Types", TypeList)

TypeColors = {}
TypeColors = {'Water': Color.Turquoise, 'Wood': Color.ForestGreen, 'Fire': Color.Firebrick, 'Earth': Color.Gold, 'Metal': Color.Silver}
TypeToColor = {}

for type in TypeList:
    TypeToColor[type] = TypeColors[type]

class EnumDeclarations:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        pass

    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        pass

    def OnLogicUpdate(self, UpdateEvent):
        pass

Zero.RegisterComponent("EnumDeclarations", EnumDeclarations)