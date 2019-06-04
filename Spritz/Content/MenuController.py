import Zero
import Events
import Property
import VectorMath
#-------------------------------------------------\
# Applicable States
class BaseState:
    Name = "BaseState"
    
    def OnEnter(self, Owner):
        print(self.Name, "OnEnter()")
    def OnUpdate(self, Owner):
        pass
    def OnExit(self, Owner):
        print(self.Name, "OnExit()")
    
#end class

class MainState(BaseState):
    def OnEnter(self, Owner):
        pass
#endclass

class MenuController:
    Statemachine = None
    def Initialize(self, initializer):
        self.Statemachine = self.Owner.StateMachine
        
        self.Statemachine.AddState("PauseMain", MainState())

Zero.RegisterComponent("MenuController", MenuController)