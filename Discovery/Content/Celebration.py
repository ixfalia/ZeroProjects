import Zero
import Events
import Property
import VectorMath

import Action

class Celebration:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        self.Active = Property.Bool(default = True)
        
        self.Duration = Property.Float(4.0)
        self.Move = Property.Bool(default = False)
        self.MoveDuration = Property.Float(2.0)
        self.MoveOffset = Property.Vector3(default = VectorMath.Vec3(0, 0, 0))
        
        self.ActivationEvent = Property.String(default = "")
        self.SendEndingEvent = Property.String(default = "")
        pass

    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevel)
        
        if not self.ActivationEvent == "":
            Zero.Connect(self.Space, self.ActivationEvent, self.onActivation)
            Zero.Connect(self.Owner, self.ActivationEvent, self.onActivation)
        
        self.LastState = self.Active
        self.StartingPosition = self.Owner.Transform.Translation
        pass
    
    def onLevel(self, lEvent):
        if self.Active:
            self.celebrate()

    def celebrate(self, duration = None, moveDuration = None):
        if not duration:
            duration = self.Duration
        if not moveDuration:
            moveDuration = self.MoveDuration
        
        print("CelebrationMessage.Celebrate(): WOO~!")
        
        if self.Owner.SpriteText:
            self.Owner.SpriteText.Visible = True
        if self.Owner.Sprite:
            self.Owner.Sprite.Visible = True
        if self.Owner.SphericalParticleEmitter:
            self.Owner.SphericalParticleEmitter.Active = True
        
        seq =  Action.Sequence(self.Owner)
        
        if self.Move:
            pos = self.Owner.Transform.Translation
            Action.Property(seq, self.Owner.Transform, "Translation", pos+self.MoveOffset, moveDuration, Action.Ease.SinInOut)
        
        Action.Delay(seq, duration)
        Action.Call(seq, self.reset)
    
    def reset(self):
        if self.Owner.SpriteText:
            self.Owner.SpriteText.Visible = False
            #self.Owner.SpriteText.Text = self.Message
        
        if self.Owner.Sprite:
            self.Owner.Sprite.Visible =  False
        if self.Owner.SphericalParticleEmitter:
            self.Owner.SphericalParticleEmitter.Active = False
        
        self.Owner.Transform.Translation = self.StartingPosition
    
    def onActivation(self, aEvent):
        self.celebrate()
    
    def onUpdate(self, uEvent):
        if self.Active and not self.LastState:
            self.celebrate()
        else:
            self.LastState = self.Active
    

Zero.RegisterComponent("Celebration", Celebration)