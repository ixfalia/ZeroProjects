import Zero
import Events
import Property
import VectorMath
import Action
import random

Vec3 = VectorMath.Vec3
Vec2 = VectorMath.Vec2

class MainMenu:
    DebugMode = Property.Bool(default=False)
    TestButton = None
    StartGame = None
    Options = None
    Credits = None
    
    selection = []
    selectID = 0
    menuPoint = None
    menuPointerShift = Vec2(-3.5, 0)
    Timer = 0
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevelStart)
        Zero.Connect(self.Space, "myGamepadEvent", self.onButtonDown)
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        
        #self.selection = []
        #self.menuPoint = self.Space.CreateAtPosition("MenuPointer", self.menuPointerShift + self.selection[0].Transform.Translation)
        
    def onButtonDown(self, Event):
        if(Event.Button == Zero.Buttons.DpadLeft):
            self.selectID -= 1
            
            if self.selectID < 0:
                self.selectID = 0
            else:
                self.Owner.SoundEmitter.Play()
            
            self.updateCursor()
        #endif
        if(Event.Button == Zero.Buttons.DpadRight):
            self.selectID += 1
            
            if self.selectID > len(self.selection)-1:
                self.selectID = len(self.selection)-1
            else:
                self.Owner.SoundEmitter.Play()
            
            self.updateCursor()
        #endif
        if(Event.Button == Zero.Buttons.A or Event.Button == Zero.Buttons.Start):
            #self.selection[self.selectID].SpriteText.Text = "DURR"
            self.selection[self.selectID].ButtonLogic.Do()
        if(Event.Button == Zero.Buttons.B):
            #self.selection[self.selectID].SpriteText.Text = "NURR"
            pass
    
    def onLevelStart(self, Event):
        print("onlevelstart")
        self.selection = []
        self.selectID = 0
        
        self.selection.append(self.Space.FindObjectByName("TestButton"))
        self.selection.append(self.Space.FindObjectByName("TestButton2"))
        #self.selection.append(self.Space.FindObjectByName("TestButton3"))
        #self.selection.append(self.Space.FindObjectByName("TestButton4"))
        
        self.menuPoint = self.Space.CreateAtPosition("MenuPointer", self.menuPointerShift + self.selection[0].Transform.Translation)
        #self.menuPoint = self.Space.Create("MenuPointer")
        self.menuPoint.Sprite.Visible = True
    
    def setCursorPosition(self, pos):
        seq = Action.Sequence(self.menuPoint)
        me = self.menuPoint.Transform
        Action.Property(seq, me, property="Translation",end=pos,duration=0.5,ease=Action.Ease.Linear)
        #self.menuPoint.Transform.Translation = pos
    
    def updateCursor(self):
        if self.DebugMode:
            print(self.selectID)
        self.setCursorPosition(self.menuPointerShift + self.selection[self.selectID].Transform.Translation)
    
    def onUpdate(self, Event):
        self.Timer += Event.Dt
        
        if self.Timer > 0.1:
            self.Timer = 0
            return
        
        if(self.Owner.Sprinkler):
            #watervel = Vec3( 2*random.uniform(-0.5, 0.5), 0.8, 0 )
            random.seed(self.Space.TimeSpace.RealTimePassed)
            
            watervel = self.menuPoint.Transform.Translation - self.Owner.Transform.Translation
            watervel *= 0.5
            self.Owner.Sprinkler.ShootStick(watervel.normalized())
            
            watervel = Vec3(random.uniform(-1.0, 2.0), 1.5, 0 )
            self.Owner.Sprinkler.shootUnlimited(watervel)

Zero.RegisterComponent("MainMenu", MainMenu)