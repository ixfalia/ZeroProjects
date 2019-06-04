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
    locked = Property.Bool(default = False)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevelStart)
        Zero.Connect(self.Space, "myGamepadEvent", self.onButtonDown)
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        
    def onButtonDown(self, Event):
        if(Event.Button == Zero.Buttons.B or Event.Button == Zero.Buttons.Start):
            self.locked = not self.locked
        
        if self.locked:
            return
        
        if(Event.Button == Zero.Buttons.DpadLeft or Event.Button == Zero.Buttons.DpadUp):
            self.selectID -= 1
            
            if self.selectID < 0:
                self.selectID = self.selectID = len(self.selection)-1
            
            self.updateCursor()
        #endif
        if(Event.Button == Zero.Buttons.DpadRight or Event.Button == Zero.Buttons.DpadDown):
            self.selectID += 1
            
            if self.selectID > len(self.selection)-1:
                self.selectID = 0
            
            self.updateCursor()
        #endif
        if(Event.Button == Zero.Buttons.A or Event.Button == Zero.Buttons.Start):
            #self.selection[self.selectID].SpriteText.Text = "DURR"
            if self.DebugMode:
                print("Activate Button:", self.selection[self.selectID].Name)
            self.selection[self.selectID].ButtonLogic.Do()
        if(Event.Button == Zero.Buttons.B):
            #self.selection[self.selectID].SpriteText.Text = "NURR"
            pass
    
    def onLevelStart(self, Event):
        print("onlevelstart")
        self.selection = []
        self.selectID = 0
        
        self.selection.append(self.Space.FindObjectByName("testbutton1"))
        self.selection.append(self.Space.FindObjectByName("testbutton2"))
        self.selection.append(self.Space.FindObjectByName("testbutton3"))
        
        self.menuPoint = self.Space.CreateAtPosition("MenuPointer", self.menuPointerShift + self.selection[0].Transform.Translation)
        self.menuPoint.Transform.Translation *= Vec3(1,1,3)
        self.menuPoint.Sprite.Visible = True
    
    def setCursorPosition(self, pos):
        seq = Action.Sequence(self.menuPoint)
        me = self.menuPoint.Transform
        seq.Add( Action.Property( on=me, property="Translation",end=pos,duration=0.5,ease=Action.Ease.Linear))
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
        

Zero.RegisterComponent("MainMenu", MainMenu)