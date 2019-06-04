import Zero
import Events
import Property
import VectorMath

import PetLogic
import Action

import random

Moods = PetLogic.Moods
PetActions = PetLogic.PetActions

class AnimationController:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        pass

    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
        #References
        self.CryEffect = self.Owner.FindChildByName("drop")
        self.EatEffect = self.Owner.FindChildByName("bit")
        self.HappyEffect = self.Owner.FindChildByName("aura")
        #self.LoveEffect = self.Owner.Parent.FindChildByName("
        #Frame Data
        self.AnimationCrying = "Dragon_Munch"
        self.AnimationEating = "Dragon_Munch"
        self.AnimationIdle = "Dragon_Idle"
        self.AnimationOpen = "Dragon_Open"
        self.AnimationDepressed = "Dragon_Sad"
        
        #
        self.isAnimating = False
        self.isSoundPlaying = False
        pass

    def OnLogicUpdate(self, UpdateEvent):
        currentAction = self.Owner.PetLogic.CurrentAction
        
        if currentAction == PetActions.Eating:
            self.playSound()
            if not self.isAnimating:
                self.playEat()
        elif currentAction == PetActions.OpenMouth:
            self.playOpen()
            self.animationOff()
        elif currentAction == PetActions.Expression:
            self.playExpression()
        elif currentAction == PetActions.Idle:
            self.playIdle()
        pass
    
    def changeSprite(self, name):
        self.Owner.Sprite.SpriteSource = name
    
    def playSound(self):
        if self.isSoundPlaying:
            return
        
        seq = Action.Sequence(self.Owner)
        Action.Delay(seq, 0.35 * random.random())
        Action.Call(seq, self.resetSound)
        self.Owner.SoundEmitter.Play()
        
        self.isSoundPlaying = True
    
    def resetSound(self):
        self.isSoundPlaying = False
    
    def getMood(self):
        return self.Owner.PetLogic.CurrentMood
    
    def playIdle(self):
        mood = self.getMood()
        
        if mood == Moods.Crying:
            if not self.isAnimating:
                #self.animationPlaying()
                #self.changeSprite(self.AnimationDepressed)
                #self.cryEffect()
                pass
        if mood == Moods.Neutral:
            self.changeSprite(self.AnimationIdle)
            self.wipeEffects()
        else:
            self.wipeEffects()
        pass
    
    def playExpression(self):
        mood = self.getMood()
        
        if mood == Moods.Crying:
            if not self.isAnimating:
                self.animationPlaying()
                self.changeSprite(self.AnimationCrying)
                self.cryEffect()
        if mood == Moods.Happy:
            self.happyEffect()
        else:
            self.wipeEffects()
    
    def playWalk(self):
        #this will need to account for moods
        pass
    
    def playOpen(self):
        self.changeSprite(self.AnimationOpen)
        pass
    
    def playEat(self):
        self.animationPlaying()
        self.changeSprite(self.AnimationEating)
        pass
    
    def playHurt(self):
        pass
    
    def playSleep(self):
        pass
    
    def cryEffect(self, duration = 1):
        seq = Action.Sequence(self.Owner)
        Action.Delay(seq, duration)
        
        self.CryEffect.SphericalParticleEmitter.Active = True
    
    def happyEffect(self, duration = 1):
        self.HappyEffect.SphericalParticleEmitter.Active = True
    
    def wipeEffects(self):
        self.CryEffect.SphericalParticleEmitter.Active = False
        self.EatEffect.SphericalParticleEmitter.Active = False
        self.HappyEffect.SphericalParticleEmitter.Active = False
        #self.StunEffect.SphericalParticleEmitter.Active = False
        
        self.animationOff()
        
        self.changeSprite(self.AnimationIdle)
    
    def animationPlaying(self):
        self.isAnimating = True
    
    def animationOff(self):
        self.isAnimating = False

Zero.RegisterComponent("AnimationController", AnimationController)