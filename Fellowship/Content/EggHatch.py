import Zero
import Events
import Property
import VectorMath

import Action
import Color
import random

Stages = Property.DeclareEnum("Stages", ["Stage0","Stage1", "Stage2", "Stage3", "End"])

class EggHatch:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        self.Stage1 = Property.SpriteSource()
        self.Stage2 = Property.SpriteSource()
        self.Stage3 = Property.SpriteSource()
        self.Final = Property.SpriteSource()
        
        self.Stage0Duration = Property.Uint()
        self.Stage1Duration = Property.Uint()
        self.Stage2Duration = Property.Uint()
        self.Stage3Duration = Property.Uint()
        
        self.AnimationDelay = Property.Float()
        self.NextLevel = Property.Level()
        
        self.CurrentStage = Property.Enum(default = Stages.Stage0)
        pass

    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, Events.MouseDown, self.onMouseDown)
        Zero.Connect(self.Owner, Events.MouseUp, self.onMouseUp)
        
        #self.ChipEffect = self.Owner.FindChildByName("chipeffect")
        self.tadaaEffect = self.Owner.FindChildByName("tadaa")
        
        self.TotalClicks = 0
        self.LifetimeClicks = 0
        self.isPlayingSound = False
        pass

    def OnLogicUpdate(self, UpdateEvent):
        pass
    
    def onMouseDown(self, MouseEvent):
        self.TotalClicks += 1
        self.LifetimeClicks += 1
        
        self.evalStage()
        
        self.Space.DispatchEvent("TadaaEvent", Zero.ScriptEvent())
        
        if not self.CurrentStage == Stages.End:
            chip = self.Space.CreateAtPosition("ChipEffect", self.Owner.Transform.Translation)
            emitrate = chip.SphericalParticleEmitter.EmitRate
        else:
            chip = None
            emitrate = 8
        
        if self.CurrentStage == Stages.Stage1:
            self.Owner.Sprite.SpriteSource = self.Stage1
            pass
        elif self.CurrentStage == Stages.Stage2:
            self.Owner.Sprite.SpriteSource = self.Stage2
            emitrate *= 1.25
        elif self.CurrentStage == Stages.Stage3:
            self.Owner.Sprite.SpriteSource = self.Stage3
            emitrate *= 1.5
            self.tadaaEffect.SphericalParticleEmitter.Active = True
            self.Owner.Scalerator.Duration = 0.25
        elif self.CurrentStage == Stages.End:
            self.PlayAnimation()
            self.Owner.Collider.SendsEvents = False
            seq = Action.Sequence(self.Owner)
            Action.Delay(seq, self.AnimationDelay)
            Action.Call(seq, self.Space.LoadLevel, (self.NextLevel))
        
        if chip:
            chip.SphericalParticleEmitter.EmitRate = emitrate
        pass
    
    def onMouseUp(self, MouseEvent):
        if self.CurrentStage == Stages.Stage1:
            self.Owner.Sprite.SpriteSource = self.Stage1
            #self.Owner.SoundEmitter.Play()
            pass
        elif self.CurrentStage == Stages.Stage2:
            self.Owner.Sprite.SpriteSource = self.Stage2
            #self.Owner.SoundEmitter.Play()
        elif self.CurrentStage == Stages.Stage3:
            self.Owner.Sprite.SpriteSource = self.Stage3
            #self.Owner.SoundEmitter.Play()
        elif self.CurrentStage == Stages.End:
            self.Owner.Sprite.SpriteSource = self.Final
            #self.Owner.SoundEmitter.Play()
    
    def evalStage(self):
        print(self.TotalClicks, self.Stage1Duration)
        if self.TotalClicks >= self.Stage0Duration:
            self.CurrentStage = Stages.Stage1
            self.playSound()
        if self.TotalClicks >= self.Stage1Duration:
            self.CurrentStage = Stages.Stage2
            self.playSound()
        if self.TotalClicks >= self.Stage2Duration:
            self.CurrentStage = Stages.Stage3
            self.playSound()
        if self.TotalClicks >= self.Stage3Duration:
            self.CurrentStage = Stages.End
    
    def PlayAnimation(self):
        seq = Action.Sequence(self.Owner)
        self.Owner.Reactive.Active = False
        lSettings = self.Space.FindObjectByName("LevelSettings")
        target = lSettings.ForwardRenderer
        #color = Color.PaleGoldenrod
        #color2 = Color.Gold
        #color3 = Color.White
        
        Action.Delay(seq, 3.5)
        Action.Call(seq, self.playSound)
        Action.Delay(seq, 0.5)
        Action.Call(seq, self.changeSprite, (self.Final))
    
    def playSound(self):
        if self.isPlayingSound:
            return
        
        self.Owner.SoundEmitter.Play()
        
        seq = Action.Sequence(self.Owner)
        Action.Delay(seq, 0.75)
        Action.Call(seq, self.isNoLongerPlaying)
        
        self.isPlayingSound = True
    
    def isNoLongerPlaying(self):
        self.isPlayingSound = False
    
    def changeSprite(self, sprite):
        self.Owner.Sprite.Color = VectorMath.Vec4(108/255, 157/255, 107/255, 1)
        self.Owner.Sprite.SpriteSource = sprite

Zero.RegisterComponent("EggHatch", EggHatch)