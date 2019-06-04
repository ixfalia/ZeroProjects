import Zero
import Events
import Property
import VectorMath

class Ability:
    def __init__(self, _name, _something):
        pass
#endclass

class EquippedAbility:
    def __init__(self, Ability):
        self.Name = ""

class ActiveAbilityManager:
    def Initialize(self, initializer):
        
        self.EquipedAbilities = ["Staff", "Sword"]
        
        it = iter(self.EquipedAbilities)
        rit = reversed(self.EquipedAbilities)
        print("============================")
        
        #NOTE: Python iterators when returned begin with their __next__() returning first element
        name = it.__next__()
        print(name)
        
        name = it.__next__()
        print(name)
        
        print("Now Reverse")
        #NOTE: Reverse Python iterators __next()__ returns last element.
        name = rit.__next__()
        print(name)
        
        name = rit.__next__()
        print(name)
        
        #name = rit.__next__()
        #print(name)
        print("============================")

Zero.RegisterComponent("ActiveAbilityManager", ActiveAbilityManager)