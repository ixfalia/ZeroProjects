import Zero
import Events
import Property
import VectorMath

import Color
import myCustomEnums
import random
import Action

Vec4 = VectorMath.Vec4
Vec3 = VectorMath.Vec3
Vec2 = VectorMath.Vec2

sproutList = myCustomEnums.sproutList
sproutTypes = myCustomEnums.sproutTypes

effectTypes = myCustomEnums.effectTypes

def totalSprouts():
    #return -1 + sproutTypes.index("blank")
    pass

class Sprout:
    DebugPrint = Property.Bool(False)
    Type = Property.Enum(enum = sproutTypes)
    Effect = Property.Enum(enum = effectTypes)
    gridPosition = Property.Vector2(default=VectorMath.Vec2())
    bloomed = Property.Bool(default = False)
    GrowthTime = Property.Int(default = 3)
    #Component = Property.PyScript()
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "UIState_Default", self.onDefault)
        Zero.Connect(self.Owner, "FullHealth", self.onFullHealth)
        Zero.Connect(self.Owner, "DeathEvent", self.onDeath)
        #Zero.Connect(self.Owner, "UIState_Activate", self.onActivate)  #disabling the activate functions cuz they broke and I am working around them
        #Zero.Connect(self.Owner, Events.MouseDown, self.onActivate)
        #Zero.Connect(Zero.Mouse, Events.MouseDown, self.onActivate)
        Zero.Connect(self.Space, "EffectEvent", self.onEffect)
        Zero.Connect(self.Space, "ReactivateEvent", self.onReactivate)
        Zero.Connect(self.Owner, "BloomEvent", self.onBloom)
        Zero.Connect(self.Space, "OutOfTurns", self.onGameOver)
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevel)
        
        #HACKS! Getting 'Round Limitations
        #Zero.Connect(Zero.Keyboard, Events.KeyDown, self.onKeyDown)
        Zero.Connect(self.Owner, "UIState_Hover", self.onMouseEnter)
        Zero.Connect(self.Owner, Events.MouseExit, self.onMouseExit)
        Zero.Connect(self.Space, "SproutClickEvent", self.onActivate)
        
        self.wiltColor = Vec4(0.384,0.412,0.153, 1)
        self.delayOffset = 0
        self.bloomed = False
        self.currentColor = Vec4(0,0,0,0)
        self.startingTextColor = self.Owner.SpriteText.Color
        self.currentEffect = None
        self.startingGrowthTime = self.GrowthTime
        self.rainbow = None
        self.poison = None
        self.isPoisoned = False
        self.TurnCount = self.GrowthTime
        self.GameOver = False
        
        #self.StartingScale = self.Owner.Transform.Scale
        
        self.isMouseHover = False; #MORE HACKS
        
        if self.Type == sproutTypes.blank:
            self.Owner.SpriteText.Visible = False
        elif self.bloomed:
            self.Owner.SpriteText.Visible = False
        else:
            self.Owner.SpriteText.Visible = True
        #self.gridPosition = None
        
        self.Manager = self.Space.FindObjectByName("LevelSettings").ManipulatorManager
        self.FlowerGrid = self.Space.FindObjectByName("MasterGrid").FlowerGrid
        
        self.totalTypes = sproutList.index("mystery")
        self.updateSprout()
        #self.wilt()
        pass
    
    def changeType(self, type):
        oldType = self.Type
        
        self.Type = type
        #print("Sprout.changeType:", self.Type)
        self.updateSprout()
        
        #self.sendGridEvent()
    
    def resetSprout(self):
        self.wiltColor = Vec4(0.384,0.412,0.153, 1)
        self.delayOffset = 0
        self.bloomed = False
        self.currentColor = Vec4(0,0,0,0)
        self.currentEffect = None
        self.rainbow = None
        #self.TurnCount = self.GrowthTime
        self.Owner.Sprite.SpriteSource = "mysteryseed"
        self.isPoisoned = False
        if self.Type == sproutTypes.blank:
            self.Owner.SpriteText.Visible = True
        elif self.bloomed:
            self.Owner.SpriteText.Visible = True
        else:
            self.Owner.SpriteText.Visible = True
        
        #self.Owner.SpriteText.Color = Vec4(1,1,1,1)
        
        self.updateSprout()
    
    def sendGridEvent(self):
        e = Zero.ScriptEvent()
        e.Position = self.gridPosition
        e.FlowerType = self.Type
        #e.OldType = oldType
        e.Archetype = "Sprout"
        self.Space.DispatchEvent("GridEvent", e)
    
    def updateSprout(self):
        if self.GameOver:
            if(self.GameOver):
                self.Owner.SpriteText.Visible = False;
            return
        
        self.Owner.Sprite.Color = self.Manager.effectColors(self.Type)
        
        self.Owner.Scalarator.Active = False
        self.Owner.ColorShifting.Active = False
        
        #if self.TurnCount <= 0:
        #    self.changeType(sproutTypes.blank)
        
        self.updateText()
        
        if self.Type == sproutTypes.blank:
            self.Owner.SpriteText.Visible = False
        elif self.bloomed:
            self.Owner.SpriteText.Visible = False
        else:
            self.Owner.SpriteText.Visible = True
        #endif block
        
        if self.bloomed:
            self.Owner.Sprite.SpriteSource = "DemoFlower"
            self.updateText()
            self.Owner.Transform.Scale = self.Owner.Scalarator.startingScale
            
            #new 2019
            #self.Owner.Rotator.Active = False;
            #self.Owner.SmoothRotator.Active = True;
            
            if self.rainbow:
                self.rainbow.SphericalParticleEmitter.EmitRate = 16
            if self.poison:
                self.poison.SphericalParticleEmitter.EmitRate = 8
                self.poison.SphericalParticleEmitter.EmitterSize = Vec3(4,4,1)
        else:
            self.Owner.Scalarator.Active = True
            #self.Owner.Rotator.Active = True;
            #self.Owner.SmoothRotator.Active = False;
        #endif block
        
        if self.Type == sproutTypes.blank:
            self.Owner.Sprite.Color = Vec4(0,0,0,0)
            if self.rainbow:
                self.rainbow.Destroy()
            if self.poison:
                self.poison.Destroy()
            pass
        elif self.Type == sproutTypes.rainbow:
            self.Owner.ColorShifting.Active = True
            if not self.rainbow:
                self.rainbow = self.Space.CreateAtPosition("rainbowEffect", self.Owner.Transform.Translation)
            pass
        elif self.Type == sproutTypes.poison:
            if not self.poison:
                self.poison = self.Space.CreateAtPosition("poisonEffect", self.Owner.Transform.Translation)
        else:
            self.Owner.Scalarator.Active = False
        #endif block
    #endef updateSprout()
    
    def onActivate(self, aEvent):
        #print("Sprout.onActivate()")
        if self.GameOver:
            print("self.Gameover")
            return
        
        if(not self.isMouseHover):
            return; 
        #endif
        
        if not self.Type == sproutTypes.blank:
            #self.changeType(sproutTypes.blank)
            return
        
        self.currentEffect = self.Manager.useEffect()
        self.Owner.SoundEmitter.PlayCue("Dig")
        Zero.Connect(self.Space, "TurnIncrementEvent", self.onTurn)
        self.TurnCount = self.GrowthTime
        
        #print("Sprout.onActivate",self.currentEffect)
        self.changeType(self.currentEffect)
        row, column = self.getGridPosition()
        print("********************************************************************")
        print("== Sprout.onActivate() ==")
        print("Placed", self.Type, "sprout at (", row, ",",column,")") 
        print("\tTurns set to:", self.TurnCount, "current GrowthTime is", self.GrowthTime)
        print("********************************************************************")
        e = Zero.ScriptEvent()
        self.Space.DispatchEvent("RemoveTurnEvent", e)
        #self.randomSprout()
        pass
    
    def plantSeed(self, type = None):
        if not self.Type == sproutTypes.blank:
            #self.changeType(sproutTypes.blank)
            return
        
        if not type:
            type = self.Manager.getRandomEffect()
        
        self.TurnCount = self.GrowthTime
        self.currentEffect = type
        self.changeType(type)
        self.updateText()
        self.updateSprout()
        self.Owner.Sprite.Color = self.Manager.effectColors(type)
        
        row, column = self.getGridPosition()
        
        print("********************************************************************")
        print("== Sprout.plantSeed() ==")
        print("Placed", self.Type, "sprout at (", row, ",",column,")") 
        print("\tTurns set to:", self.TurnCount, "current GrowthTime is", self.GrowthTime)
        print("********************************************************************")
        
        if not type == sproutTypes.blank:
            Zero.Connect(self.Space, "TurnIncrementEvent", self.onTurn)
            
        #else:
            #self.resetSprout()
    
    def effectToType(self, type):
        if not type:
            type = self.currentEffect
        
        if type == effectTypes.dry:
            return sproutTypes.red
        
        if type == effectTypes.rainy:
            return sproutTypes.blue
        
        if type == effectTypes.sunny:
            return sproutTypes.yellow
        
        return sproutTypes.dead
    
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
        
        if type == sproutTypes.poison:
            color = Color.Purple
        
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
    
    def onDefault(self, uiEvent):
        #self.updateSprout()
        pass
    
    def onEffect(self, Event):
        self.currentColor =  Event.Color
        #self.effectQueue = Event.Queue
        #print("Sprout.onEffect", Event.Color)
        #raise
    
    def applyEffect(self, effect, color = None):
        #print("Sprout.applyEffect():")
        #print("\t Applying Effect:", effect)
        
        if not color:
            color = Color.AliceBlue
            #raise
        
        if self.Type == sproutTypes.blank:
            return
        
        if self.Type == sproutTypes.yellow:
            if effect == effectTypes.sunny:
                self.bloom()
            elif effect == effectTypes.rainy:
                self.wilt()
            elif effect == effectTypes.dry:
                self.wilt()
                pass
        
        if self.Type == sproutTypes.blue:
            if effect == effectTypes.sunny:
                self.wilt()
            elif effect == effectTypes.rainy:
                self.bloom()
            elif effect == effectTypes.dry:
                self.wilt()
        
        if self.Type == sproutTypes.red:
            if effect == effectTypes.sunny:
                self.wilt()
                pass
            elif effect == effectTypes.rainy:
                self.wilt()
            elif effect == effectTypes.dry:
                self.bloom()
        
        return self.bloomed
        #self.Owner.Sprite.Color = color
    
    def onFullHealth(self, hEvent):
        WaitTime = 1.0
        
        if self.Type == sproutTypes.rainbow:
            effect = self.Owner.Space.CreateAtPosition("rainbowBloomEffect", self.Owner.Transform.Translation)
            self.Owner.ColorShifting.Active = False
        else:
            effect = self.Owner.Space.CreateAtPosition("bloomEffect", self.Owner.Transform.Translation)
            effect.SpriteParticleSystem.Tint = self.Manager.effectColors(self.Type)
        
        if self.Type == "red":
            e = Zero.ScriptEvent()
            e.Turns = 1
            self.Space.DispatchEvent("AddTurnEvent", e)
        #endif
        if self.Type == sproutTypes.poison:
            row, column = self.getGridPosition()
            self.FlowerGrid.applyFunctionToSurrounding(row, column, self.unPoisonSeeds)
            self.FlowerGrid.applyFunctionToSurroundingGroundPlots(row, column, self.unPoisonGround)
            #self.FlowerGrid.UpdatePoisonField()
        
        oldType = self.Type
        self.changeType(sproutTypes.blank)
        
        seq = Action.Sequence(self.Owner)
        Action.Delay(seq, WaitTime)
        #self.bloomed = True
        self.resetSprout()
        
        e = Zero.ScriptEvent()
        e.Position = self.gridPosition
        e.FlowerType = self.Type
        e.OldType = oldType
        e.Archetype = "Sprout"
        self.Space.DispatchEvent("GridEvent", e)
    #enddef
    
    def onDeath(self, hEvent):
        #randomID = random.choice(sproutList)
        #self.changeType(randomID)
        ded = self.Space.CreateAtPosition("DeathEffect", self.Owner.Transform.Translation)
        ded.Transform.Scale =  Vec3(0.5,0.5,1)
        ded.Transform.Translation += Vec3(0,1,1)
        self.Owner.Rotator.Disable()
        self.changeType("death")
    
    def randomSprout(self):
        #randomID = random.choice(sproutList)
        randomID = random.randrange(0, self.totalTypes)
        self.changeType(sproutList[randomID])
        #self.changeType(sproutTypes.mystery)
    
    def onBloom(self, bEvent):
        self.Owner.Sprite.SpriteSource = "DemoFlower"
        self.bloomed = True
        #self.changeType()
        
        if self.Type == sproutTypes.poison:
            row, column = self.getGridPosition()
            self.FlowerGrid.applyFunctionToSurrounding(row, column, self.poisonSeeds)
            self.FlowerGrid.applyFunctionToSurroundingGroundPlots(row, column, self.poisonGround)
        #endif
        
        self.updateSprout()
        self.sendGridEvent()
        self.updateText()
    
    def bloomFlower(self):
        self.Owner.Sprite.SpriteSource = "DemoFlower"
        self.bloomed = True
        
        self.Owner.Scalarator.Active = False
        self.Owner.ColorShifting.Active = False
        
        self.updateText()
        self.Owner.Sprite.SpriteSource = "DemoFlower"
        
        if self.rainbow:
            self.rainbow.SphericalParticleEmitter.EmitRate = 16
        if self.poison:
            self.poison.SphericalParticleEmitter.EmitRate = 8
            self.poison.SphericalParticleEmitter.EmitterSize = Vec3(4,4,1)
        
        self.sendGridEvent()
        
        if self.Type == sproutTypes.rainbow:
            self.Owner.ColorShifting.Active = True
            if not self.rainbow:
                self.rainbow = self.Space.CreateAtPosition("rainbowEffect", self.Owner.Transform.Translation)
            pass
        elif self.Type == sproutTypes.poison:
            if not self.poison:
                self.poison = self.Space.CreateAtPosition("poisonEffect", self.Owner.Transform.Translation)
        else:
            self.Owner.Scalarator.Active = False
    
    def getGridPosition(self):
        return round(self.gridPosition.x), round(self.gridPosition.y)
    
    def onTurn(self, tEvent):
        self.TurnCount -= 1
        #print("\t", self.Type, "Sprout's turn decreased to", self.TurnCount, "out of", self.GrowthTime)
        if self.Owner.SpriteText:
            self.Owner.SpriteText.Text = '{0}'.format(self.TurnCount, self.GrowthTime)
        if self.Type == sproutTypes.poison and self.bloomed:
            row, column = self.getGridPosition()
            self.FlowerGrid.applyFunctionToSurroundingGroundPlots(row, column, self.poisonGround)
        
        if self.TurnCount <= 0:
            e = Zero.ScriptEvent()
            self.Owner.DispatchEvent("BloomEvent", e)
            Zero.Disconnect(self.Space, "TurnIncrementEvent", self.onTurn)
    
    def mysterySeed(self):
        self.changeType(sproutTypes.mystery)
        self.Owner.SpriteText.Text = '?'
    
    def onGameOver(self, gEvent):
        self.updateSprout()
        self.GameOver = True#not self.GameOver
        #print("Sprout.GameOver is:", self.GameOver)
    
    def onReactivate(self,EVent):
        self.GameOver = False
    
    def onLevel(self, lEvent):
        #self.GameOver = True
        pass
    
    def playCue(self, sound, pitch = None):
        if not pitch:
            pitch = 1
        
        self.Owner.SoundEmitter.Pitch = pitch
        self.Owner.SoundEmitter.PlayCue(sound)
    
    def placeRandomSeed(self, sprout):
        if not sprout.Sprout.Type == sproutTypes.blank:
            return
        
    def setTurnCount(self, count):
        self.TurnCount = count
        self.updateText()
    
    def updateText(self):
        if self.Type == sproutTypes.blank:
            self.Owner.SpriteText.Visible = False
        elif self.bloomed:
            self.Owner.SpriteText.Visible = False
        else:
            self.Owner.SpriteText.Visible = True
        
        if self.Owner.SpriteText:
            self.Owner.SpriteText.Text = '{0}'.format(self.TurnCount, self.GrowthTime)
    
    ###########################################################################
    #### Poison Functions
    ##
    def poisonSeeds(self, sprout):
        if sprout.Sprout.Type == sproutTypes.poison:
            sprout.SpriteText.Color = self.startingTextColor
            return
        if not sprout.Sprout.Type == sproutTypes.blank:
            sprout.Sprout.TurnCount += 1
        
        sprout.Sprout.GrowthTime += 1
        color = Color.Purple.lerp(Color.Black, .75)#Vec4(224/255,204/255,224/255,1)
        sprout.SpriteText.Color = color
        print("PoisonSeeds: GrowthTime inhibited to", sprout.Sprout.GrowthTime)
    
    def unPoisonSeeds(self, sprout):
        sprout.Sprout.GrowthTime -= 1
        
        if sprout.Sprout.TurnCount > sprout.Sprout.GrowthTime:
            sprout.Sprout.TurnCount = sprout.Sprout.GrowthTime
        if sprout.Sprout.GrowthTime < sprout.Sprout.startingGrowthTime:
            sprout.Sprout.GrowthTime = sprout.Sprout.startingGrowthTime
        
        sprout.SpriteText.Color = self.startingTextColor
    
    def poisonGround(self, ground):
        if ground.Sprite:
            ground.Sprite.Color = Color.Purple.lerp(Color.White, 0.5)
            #self.FlowerGrid.UpdatePoisonField()
    
    def unPoisonGround(self, ground):
        if ground.Sprite:
            ground.Sprite.Color = Color.White
            #self.FlowerGrid.UpdatePoisonField()
    
    def onMouseEnter(self, mouseEvent):
        self.isMouseHover = True;
        
        if(self.DebugPrint):
            print("Sprout.onMouseEnter() isMouseHover = {}".format(self.isMouseHover));
    #endef onMouseEnter()
    
    def onMouseExit(self, mouseEvent):
        self.isMouseHover = False;
        
        if(self.DebugPrint):
            print("Sprout.onMouseExit() isMouseHover = {}".format(self.isMouseHover));
    #endef onMouseExit()
    
    
    # This was added in JUN 2019 to test if we can use an event to bypass the HUD. The the message binding should commented out.
    def onKeyDown(self, keyboardEvent):
        #print("= Sprout.onKeyDown() = ");
        if(not self.isMouseHover):
            return;
        #endif
        
        if(Zero.Keyboard.KeyIsPressed(Zero.Keys.Space)):
            self.onActivate(keyboardEvent);
        #endif
    #endef onKeyDown()

Zero.RegisterComponent("Sprout", Sprout)