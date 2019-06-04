import Zero
import Events
import Property
import VectorMath

import myCustomEnums
import Color
import Action

effectList = myCustomEnums.effectList
effectTypes = myCustomEnums.effectTypes
sproutTypes = myCustomEnums.sproutTypes

class EffectTracker:
    Debug = Property.Bool(default = False)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, "EffectEvent", self.onEffect)
        
        offset = VectorMath.Vec3(0,-2.85,0)
        position = self.Owner.Transform.Translation + VectorMath.Vec3(0, -2.5, 0)
        self.poison = None
        self.rainbow = None
        self.currentColor = self.Owner.Sprite.Color
        self.trackerList = []
        
        for i in range(4):
            position += offset
            obj = self.Space.CreateAtPosition("CircleSprite", position)
            self.trackerList.insert(i, obj)
        
        self.currentEffect = effectTypes.sunny
    
    def onEffect(self, eEvent):
        nuEffect = eEvent.Effect
        #raise
        
        if self.Owner.Sprite:
            #self.Owner.Sprite.Color = eEvent.Color
            self.shakeSeed(self.Owner, 0, eEvent.Color)
            #self.Owner.ColorShifting.shiftColor(eEvent.Color)
            self.Owner.ColorShifting.Active = False
            #self.Owner.ColorShifting.RandomShift = False
            self.currentColor = eEvent.Color
            if self.poison:
                self.poison.Destroy()
            if self.rainbow:
                self.rainbow.Destroy()
            
            if eEvent.Effect == sproutTypes.weed or eEvent.Effect == sproutTypes.poison:
                #self.Owner.Sprite.Color = Color.BlueViolet
                self.Owner.Sprite.SpriteSource = "Weed"
                if eEvent.Effect == sproutTypes.poison:
                    if not self.poison:
                        self.poison = self.Space.CreateAtPosition("poisonEffect", self.Owner.Transform.Translation)
                        self.poison.SphericalParticleEmitter.EmitRate = 16
                        self.poison.SphericalParticleEmitter.EmitterSize = VectorMath.Vec3(6,6,1)
            elif eEvent.Effect == sproutTypes.rainbow:
                self.Owner.ColorShifting.Active = True
                self.Owner.Sprite.SpriteSource = "DemoFlower"
                if not self.rainbow:
                    self.rainbow = self.Space.CreateAtPosition("rainbowEffect", self.Owner.Transform.Translation)
                    self.rainbow.SphericalParticleEmitter.EmitRate = 16
                    self.rainbow.SphericalParticleEmitter.EmitterSize = VectorMath.Vec3(6,6,1)
                #raise
            else:
                self.Owner.Sprite.SpriteSource = "DemoFlower"
        
        if self.Owner.SpriteText:
            self.Owner.SpriteText.Color = eEvent.Color
            self.Owner.SpriteText.Text = nuEffect
        
        if eEvent.effectQueue:
            i = 0
            first = True 
            delay = 0.081
            
            for effect in eEvent.effectQueue:
                if first:
                    first = False
                    continue
                if effect == sproutTypes.rainbow:
                    self.trackerList[i].ColorShifting.Active = True
                    pass
                else:
                    self.trackerList[i].ColorShifting.Active = False
                    pass
                
                color = eEvent.effectColors(effect)
                #print("EffectTracker.EffectQueue()", color)
                #self.trackerList[i].ColorShifting.shiftColor(color)
                #self.trackerList[i].Sprite.Color = color
                self.shakeSeed(self.trackerList[i], delay+i*0.2, color)
                i += 1
        
        self.currentEffect = nuEffect
    
    def shakeSeed(self, seed, delay, color):
        seq = Action.Sequence(seed)
        offset = VectorMath.Vec3(-0.2,0.1,0)
        position = offset + seed.Transform.Translation
        animationDelay = 0.085
        
        Action.Delay(seq, delay)
        Action.Property(seq, seed.Transform, "Translation", position, animationDelay)
        position = seed.Transform.Translation - offset
        Action.Property(seq, seed.Transform, "Translation", position, animationDelay)
        Action.Property(seq, seed.Transform, "Translation", seed.Transform.Translation)
        Action.Call(seq, self.setColor, (seed,color))
    
    def setColor(self, seed, color):
        seed.Sprite.Color = color
    
    def getCurrentEffectColor(self):
        return self.currentColor

Zero.RegisterComponent("EffectTracker", EffectTracker)