import Zero
import Events
import Property
import VectorMath

#sproutList = ["red", "blue", "yellow", "poison", "dying", "blank"]
sproutList = ["yellow", "blue", "red", "weed", "poison", "rainbow", "blank","mystery"]
sproutTypes = Property.DeclareEnum("flowerTypes", sproutList)
sproutAmount = sproutList.index(sproutTypes.blank)

effectList = ["sunny", "rainy", "dry", "weed", "nothing"]
effectTypes = Property.DeclareEnum("effectTypes", effectList)
effectAmount = effectList.index(effectTypes.nothing)

class myCustomEnums:
    def Initialize(self):
        pass

Zero.RegisterComponent("myCustomEnums", myCustomEnums)