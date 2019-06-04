import Zero
import Events
import Property
import VectorMath

import myCustomEnums
import Color
import Keys
import random
from collections import deque

effectList = myCustomEnums.effectList
effectTypes = myCustomEnums.effectTypes
sproutList = myCustomEnums.sproutList
sproutTypes = myCustomEnums.sproutTypes

class ManipulatorManager:
    Debug = Property.Bool(default = True)
    disabled = Property.Bool(default = False)
    currentEffect = Property.Enum(enum = sproutTypes)
    maxQueueSize = Property.Uint(default = 5)
    SpawnRates = Property.ResourceTable()
    
    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevelStart)
        Zero.Connect(self.Space, "ManipulatorInitialization", self.onManipInit)
        Zero.Connect(self.Space, "ManipulatorEvent", self.onManip)
        
        self.manipulatorList = []
        self.effectQueue = []#deque(maxlen = self.maxQueueSize)
        self.DefaultColor = self.effectColors()
        self.CurrentColor = self.effectColors()
        #self.currentEffect = effectTypes.sunny
        
        self.effectAmount = sproutList.index("blank")
        
        self.populateEffectQueue()
        self.updateInfo()
        
    
    def onManipInit(self, iEvent):
        self.manipulatorList.append(iEvent.Object)
        #print("onManipInit:")
        #print("\t", self.manipulatorList)
    
    def onLevelStart(self, lEvent):
        self.updateInfo()
    
    def onUpdate(self, uEvent):
        #self.updateInfo()
        return
        if self.disabled:
            return
    #enddef
    
    def clearEffects(self):
        self.effectQueue = []
        #self.updateInfo()
    
    def changeSpawnTable(self, table):
        if isinstance(table, str):
            table = Zero.ResourceSystem.GetResourceByTypeAndName("ResourceTable", table)
        
        self.SpawnRates = table
        self.clearEffects()
        self.populateEffectQueue()
    
    def onManip(self, mEvent):
        pass
        #self.currentEffect = self.useEffect()
    
    def populateEffectQueue(self):
        #if not self.effectQueue:
            #self.effectQueue.append(self.currentEffect)
        
        while not len(self.effectQueue) == self.maxQueueSize:
            self.effectQueue.append(self.randomEffect())
        
        self.updateInfo()
    
    def updateInfo(self):
        if self.Debug:
            print("effectQueue:\n\t", self.effectQueue)
            if self.effectQueue:
                print("currentEffect:", self.effectQueue[0])
        if not self.effectQueue:
            return
        self.currentEffect = self.effectQueue[0]
        weed = False
        
        if self.currentEffect == effectTypes.weed:
            weed = True
            
        if self.Owner.Sprite:
            self.Owner.Sprite.Color = self.effectColors()
        e = Zero.ScriptEvent()
        e.Effect = self.currentEffect
        e.Color = self.effectColors()
        e.effectColors = self.effectColors
        e.weed = True
        e.effectQueue = self.effectQueue
        e.Archetype =  self.Owner.ArchetypeName
        
        self.Owner.HUDEventDispatcher.DispatchHUDEvent("EffectEvent", e)
        self.Space.DispatchEvent("EffectEvent", e)
        self.Space.DispatchEvent("ChangeColor", e)
        #print("Event Sent")
    #end def updateInfo()
    
    def effectColors(self, effect = None):
        if not effect:
            effect = self.currentEffect
        
        if self.Owner.Sprite:
            self.Owner.ColorShifting.Active = False
        #print("ManipulatorManager.effectColors() Effect:", effect)
        
        if effect == effectTypes.nothing:
            return Vec4(1, 1, 1, 0)
        
        elif effect == effectTypes.sunny:
            return Color.Gold
        
        elif effect == effectTypes.rainy:
            return Color.Blue
        
        elif effect == effectTypes.dry:
            return Color.Red
        
        elif effect == effectTypes.weed:
            return Color.SaddleBrown
        
        elif effect == sproutTypes.red:
            return Color.Red
        elif effect == sproutTypes.yellow:
            return Color.Yellow
        elif effect == sproutTypes.blue:
            return Color.Blue
        
        elif effect == sproutTypes.weed:
            return Color.SaddleBrown
        
        elif effect == sproutTypes.poison:
            return Color.Purple
        elif effect == sproutTypes.rainbow:
            return Color.Azure
        elif effect == sproutTypes.blank:
            return VectorMath.Vec4(1,1,1,0)
        else:
            return Color.WhiteSmoke
    #enddef
    
    def enumToColor(self, type = None):
        if not type:
            type = self.Type
        
        color = VectorMath.Vec4(1,1,1,0)
        
        if type == sproutTypes.red:
            color = Color.Red
        
        if type == sproutTypes.blue:
            color = Color.Blue
        
        if type == sproutTypes.yellow:
            color = Color.Yellow
        
        if effect == effectTypes.weed:
            color =  Color.SaddleBrown
        #if type == sproutTypes.poison:
        #    color = Color.Purple
        
        if type == sproutTypes.blank:
            color = Vec4(1,1,1,0)
        
        #if type == sproutTypes.dying:
        #    color = Color.SaddleBrown
        if type == "death":
            self.Owner.Sprite.SpriteSource = "DeathFlower"
            color = Color.SaddleBrown#.lerp(Color.DimGray, 0.5)
        
        if not type == sproutTypes.blank:
            color = Vec4(color.r, color.g, color.b, 1)
        
        return color
    #enddef
    
    def useEffect(self):
        #print("Manip.useEffect()")
        effect = self.effectQueue.pop(0)
        self.currentEffect = effect
        #self.populateEffectQueue()
        self.effectQueue.append(self.randomEffect())
        self.updateInfo()
        
        return effect
    
    
    def randomEffect(self):
        #rand = random.randrange(0, self.effectAmount)
        rand = self.SpawnRates.SampleValue(random.random(), random.random())
        rand = sproutList.index(rand)
        if self.Debug:
            pass
            #print("ManipulatorManager.randomEffect:", self.currentEffect)
        #self.currentEffect = effectList[rand]
        return sproutList[rand]
    

Zero.RegisterComponent("ManipulatorManager", ManipulatorManager)