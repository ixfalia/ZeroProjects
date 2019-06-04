import Zero
import Events
import Property
import VectorMath

import myCustomEnums

import Keys
import Color
import random

effectTypes = myCustomEnums.effectTypes#["sunny", "rainy", "dry", "nothing"]
effectList = myCustomEnums.effectList#myCustomEnums.effectList

Vec4 = VectorMath.Vec4
Vec2 = VectorMath.Vec2
Vec3 = VectorMath.Vec3

class GridManipulator:
    Debug = Property.Bool(default = False)
    row = Property.Int(default = -1)
    col = Property.Int(default = -1)
    
    currentEffect = Property.Enum(enum=effectList)
    
    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LockStepKeyDown, self.onKeyDown)
        #Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        Zero.Connect(self.Owner, "UIState_Activate", self.onActivate)
        #Zero.Connect(self.Space, "GridManipulatorEvent", self.onActivate)
        #Zero.Connect(self.Owner, "ChangeColor", self.onChangeColor)
        Zero.Connect(self.Space, "ChangeColor", self.onChangeColor)
        
        self.Grid = None
        
        self.DefaultColor = self.Owner.Sprite.Color
        self.CurrentColor = self.DefaultColor
        
        self.disabled = True#True
        self.effectAmount = effectList.index("nothing")
        self.Manager = self.Space.FindObjectByName("LevelSettings").ManipulatorManager
        
        
        iEvent = Zero.ScriptEvent()
        iEvent.Object = self
        self.Space.DispatchEvent("ManipulatorInitialization", iEvent)
        #self.setRandomEffect()
    
    def set(self, Grid):
        self.Grid = Grid
    
    def setColorstoEffects(self):
        if self.currentEffect == effectTypes.nothing:
            return Vec4(1, 1, 1, 0)
        
        if self.currentEffect == effectTypes.sunny:
            return Color.Gold
        
        if self.currentEffect == effectTypes.rainy:
            return Color.Blue
        
        if self.currentEffect == effectTypes.dry:
            return Color.Red
    
    def onKeyDown(self, kEvent):
        raise
        
        if kEvent.Key == Zero.Keys.Q:
            cEvent = Zero.ScriptEvent()
            self.Owner.DispatchEvent("ChangeColor", cEvent)
        
    
    def onChangeColor(self, cEvent):
        if cEvent.Archetype == "ManipManager" or cEvent.Archetype ==  "GridManipulator":
            self.CurrentColor = cEvent.Color
            self.currentEffect = cEvent.Effect
            #raise
    
    def onActivate(self, uEvent):
        self.currentEffect = self.Manager.useEffect()
        print("GridManipulator.onActivate():")
        print("\tUsing Effect:", self.currentEffect)
        
        if not self.row < 0:
            elements = self.Grid.getRow(self.row)
            for element in elements:
                self.setFlower(element)
            #endfore
        #endif
        elif  not self.col < 0:
            elements = self.Grid.getColumn(self.col)
            
            for element in elements:
                self.setFlower(element)
            #endfor
        #endif
        
        e = Zero.ScriptEvent()
        self.Space.DispatchEvent("ManipulatorEvent", e)
        self.Space.DispatchEvent("RemoveTurnEvent", e)
        #self.setRandomEffect()
    #enddef
    
    def onUpdate(self, uEvent):
        if self.disabled:
            return
        
        keyPressed = False
        self.CurrentColor = self.DefaultColor
        
        if Zero.Keyboard.KeyIsPressed(Keys.Q):
            keyPressed = True
            self.currentEffect = effectTypes.sunny
            self.CurrentColor = Color.Gold
        #endif
        
        if Zero.Keyboard.KeyIsPressed(Keys.W):
            keyPressed = True
            self.currentEffect = effectTypes.rainy
            self.CurrentColor = Color.Blue
        #endif
        
        if Zero.Keyboard.KeyIsPressed(Keys.E):
            keyPressed = True
            self.currentEffect = effectTypes.dry
            self.CurrentColor = Color.Red
        #endif
        
        if keyPressed:
            cEvent = Zero.ScriptEvent()
            cEvent.Color = self.CurrentColor
            cEvent.Archetype = self.Owner.ArchetypeName
            self.Owner.DispatchEvent("ChangeColor", cEvent)
            #print("GridManipulator.onUpdate(): Current State is:", self.currentEffect)
        #endif
    #enddef
    
    def setFlower(self, element):
        #element.Sprite.Color = self.CurrentColor
        #self.currentEffect = self.Manager.currentEffect
        nuColor = self.setColorstoEffects()
        
        if self.Debug:
            print("GridManipulator.setFlower():")
            print(element.Sprite.Color)
            print(nuColor)
            print(self.currentEffect)
        #raise
        #element.Sprite.Color = nuColor
        element.Sprout.applyEffect(self.currentEffect, nuColor)
    
    def setRandomEffect(self):
        #rand = random.randrange(0, self.effectAmount)
        print("setRandomEffect:", self.currentEffect)
        #self.currentEffect = effectList[rand]
        
        cEvent = Zero.ScriptEvent()
        cEvent.Color = self.setColorstoEffects()
        cEvent.Archetype = self.Owner.ArchetypeName
        #self.Space.DispatchEvent("ChangeColor", cEvent)
        #self.Owner.DispatchEvent("ChangeColor", cEvent)

Zero.RegisterComponent("GridManipulator", GridManipulator)