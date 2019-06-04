import Zero
import Events
import Property
import VectorMath

#variables
Vec3 = VectorMath.Vec3

#
class PlayerController:
    MovementFrame = Vec3()
    def Initialize(self, initializer):
        Zero.Connect( self.Space, Events.LogicUpdate, self.onUpdate )
        #Zero.Connect( self.Owner, "OnPlayerAndGround", self.onPlayerAndGround)
    #end
    
    def onUpdate( self, event ):
        #self.MovementFrame = self.Owner.GamepadController.Gamepad.LeftStick * 3
        #endif
        
            # give the movement transform data to the Dynamic Controller
        #self.MovementFrame.y = 0
        #self.Owner.DynamicController.MoveInDirection(self.MovementFrame)
        
        pass
    #end
    
    def onPlayerAndGround(self, Event):
        print("PlayerController: Player on Ground")
        self.Owner.DynamicController.OnGround = True
        self.Owner.DynamicController.EndJump()
    
    def move(self,value):
        self.MovementFrame += value
    #enddef
    
    def spray(self, value):
        pass
    #enddef
    
    def test(self):
        print("It's me PlayerController!")
    #end
#end class

Zero.RegisterComponent("PlayerController", PlayerController)