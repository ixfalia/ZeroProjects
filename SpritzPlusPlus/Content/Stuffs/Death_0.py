import Zero
import Events
import Property
import VectorMath
import Action

class Death:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "PlayerDeath", self.onPlayerDeath)
    
    def onPlayerDeath(self, Event):
        seq = Action.Sequence(self.Owner)
        target = self.Owner
        group = Action.Group(None)
        
        if self.Owner.SoundEmitter:
            self.Owner.SoundEmitter.PlayCue("Death")
        if self.Owner.Teleport:
            self.Owner.Teleport.GoToCheckpoint()
        if self.Owner.WaterTank:
            self.Owner.WaterTank.replenish(0.5)
            
    def makePlayerVisible(self):
        if self.Owner.Sprite:
            self.Owner.Sprite.Visible = True
        else:
            print("Player.Death.makePlayerVisible(): player sprit not found.")

Zero.RegisterComponent("Death", Death)