import Zero
import Events
import Property
import VectorMath
import random

Vec3 = VectorMath.Vec3

class ButtonLogic:
    def Initialize(self, initializer):
        pass
    def Do(self):
        if self.Owner.LevelChangeButton:
            self.Owner.LevelChangeButton.activate()
        elif self.Owner.MenuButton:
            self.Owner.MenuButton.do()
        else:
            random.seed(self.Space.TimeSpace.CurrentTime)
        
            for i in range(3):
                collectible = self.Space.Create("twinkle")
                collectible.Transform.Translation = self.Owner.Transform.Translation
                collectible.RigidBody.Velocity = Vec3( 2*random.uniform(-1.0, 1.0), 10, 1 )

Zero.RegisterComponent("ButtonLogic", ButtonLogic)