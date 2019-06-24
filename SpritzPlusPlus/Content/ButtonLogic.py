import Zero
import Events
import Property
import VectorMath
import random
import Action

Vec3 = VectorMath.Vec3

class ButtonLogic:
    playSound = Property.SoundCue()
    
    def Initialize(self, initializer):
        pass
    def Do(self):
        if self.Owner.SoundEmitter and not self.playSound.Name == "DefaultCue":
            playingSound = True
            seq = Action.Sequence(self.Owner)
            self.Owner.SoundEmitter.PlayCue(self.playSound)
        
        if self.Owner.LevelChangeButton:
            if playingSound:
                Action.Delay(seq, 1.5)
                Action.Call(seq,self.Owner.LevelChangeButton.activate)
            else:
                self.Owner.LevelChangeButton.activate()
        elif self.Owner.MenuButton:
            self.Owner.MenuButton.do()
        else:
            random.seed(self.Space.TimeSpace.RealTimePassed)
        
            for i in range(3):
                collectible = self.Space.Create("twinkle")
                collectible.Transform.Translation = self.Owner.Transform.Translation
                collectible.RigidBody.Velocity = Vec3( 2*random.uniform(-1.0, 1.0), 10, 1 )

Zero.RegisterComponent("ButtonLogic", ButtonLogic)