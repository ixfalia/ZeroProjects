import Zero
import Events
import Property
import VectorMath
import Action

Vec4 = VectorMath.Vec4
Vec3 = VectorMath.Vec3
Vec2 = VectorMath.Vec2

class PauseMenu:
    DebugMode = Property.Bool(default = False)
    Visible = Property.Bool(default = False)
    Options = []
    
    SelectionID = 0
    menuPointerShift = Property.Vector2(default = Vec2(-4, 0))
    menuPoint = None
    isDetecting = Property.Bool(default = False) #Used to determine if the menu is detecting input
    once = False
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevelStart)
        Zero.Connect(self.Space, "InformationEvent", self.onLevelStart)
        Zero.Connect(self.Space, "myGamepadEvent", self.onGamepad)
        #self.setButtons()
        pass
        
    def onLevelStart(self, Event):
        print("PauseMenu.onLevelStart")
        #self.setButtons()
        #self.Options = []
        pass
        
    def onUpdate(self, Event):
        pass
    
    def setButtons(self):
        if self.once:
            return
        self.once = True
        if self.DebugMode:
            print("PauseMenu.setButtons(): Setting Buttons to Options")
            
        self.SelectionID = 0
        self.Options = []
        # Setting the Button Data into the List
        Button = self.Space.CreateAtPosition("MenuButton", self.Owner.Transform.Translation + Vec3( 0, 4, 2 ))
        Button.SpriteText.Text = "MainMenu"
        self.Options.append(Button)
        
        Button = self.Space.CreateAtPosition("MenuButton", self.Owner.Transform.Translation + Vec3( 0, 3, 2 ))
        Button.SpriteText.Text = "Sandbox"
        #Button.Menu.Screen0 = "Controls"
        self.Options.append(Button)
        
        #Button = self.Space.CreateAtPosition("MenuButton", self.Owner.Transform.Translation + Vec3( 0, 2, 2 ))
        #Button.SpriteText.Text = "How to Play!"
        #self.Options.append(Button)
        
        self.menuPoint = self.Space.CreateAtPosition("MenuPointer", Vec3(self.menuPointerShift) + self.Options[0].Transform.Translation)
        self.updateCursor()
    
    def onPause(self):
        print("me called")
        self.SelectionID = 0
        self.updateCursor()
        print("Visibility is currently in onPause():", self.Visible)    
        self.ToggleVisibility()
        
    def onGamepad(self, Event):
        if self.Visible == False:
            return
        if len(self.Options) <= 0:
            if(Event.Button == Zero.Buttons.B):
                self.onCancel()
            return
        
        if(Event.Button == Zero.Buttons.DpadLeft):
            self.moveLeft()
        elif(Event.Button == Zero.Buttons.DpadRight):
            self.moveRight()
        #endif
        if(Event.Button == Zero.Buttons.DpadUp):
            self.moveUp()
        if(Event.Button == Zero.Buttons.DpadDown):
            self.moveDown()
        if(Event.Button == Zero.Buttons.A):
            self.onConfirm()
        if(Event.Button == Zero.Buttons.B):
            self.onCancel()
    #enddef
    
    def moveDown(self):
        self.SelectionID += 1
        
        if(self.SelectionID > len(self.Options)-1):
            self.SelectionID = len(self.Options) -1
            
        self.updateCursor()
        
    def moveUp(self):
        self.SelectionID -= 1
        
        if(self.SelectionID < 0):
            self.SelectionID = 0
            
        self.updateCursor()
    
    def moveLeft(self):
        if self.DebugMode:
            #print("Selection Data:", self.SelectionID)
            pass
    
    def moveRight(self):
        if self.DebugMode:
            #print("Selection Data:", self.SelectionID)
            pass
    def onConfirm(self):
        #self.Options[self.SelectionID].Sprite.Visible = False
        self.Options[self.SelectionID].ButtonLogic.Do()
    
    def onCancel(self):
        #self.fadeOut(self.Options[self.SelectionID], self.Options[self.SelectionID].Sprite)
        self.onPause()
    
    def updateCursor(self):
        if self.DebugMode:
            print("Selection Data:", self.SelectionID)
            print(self.menuPointerShift)
        if len(self.Options) <= 0:
            return
        self.setCursorPosition(self.menuPointerShift + self.Options[self.SelectionID].Transform.Translation)
    
    def setCursorPosition(self, pos):
        #self.menuPoint.Transform.Translation = pos
        seq = Action.Sequence(self.menuPoint)
        me = self.menuPoint.Transform
        seq.Add( Action.Property( on=me, property="Translation",end=pos,duration=0.2,ease=Action.Ease.Linear))
    
    def ToggleVisibility(self):
        #self.Visible = not self.Visible
        #self.Owner.Sprite.Visible = self.Visible
        #self.setVisibility(not self.Visible)
        self.ToggleFade(not self.Visible)
        
    def setVisibility(self, visible):
        self.Visible = visible
        self.Owner.Sprite.Visible = visible
        self.menuPoint.Sprite.Visible = self.Visible
        if self.DebugMode:
            print(self.Options)
        
        for i in self.Options:
            i.Sprite.Visible = self.Visible 
            i.SpriteText.Visible = self.Visible
    
    def ToggleFade(self, visible):
        self.Visible = visible
        self.menuPoint.Sprite.Visible = self.Visible
        print("Visible set to: ", self.Visible)
        if not visible:
            self.fadeOut(self.Owner, self.Owner.Sprite)
            #self.fadeOut(self.menuPoint, self.menuPoint.Sprite)
            
            for i in self.Options:
                self.fadeOut(i, i.Sprite)
                self.fadeOut(i, i.SpriteText)
            #endfor
        else:
            self.fadeIn(self.Owner, self.Owner.Sprite)
            #self.fadeIn(self.menuPoint, self.menuPoint.Sprite)
            
            for i in self.Options:
                self.fadeIn(i, i.Sprite)
                self.fadeIn(i, i.SpriteText)
            #endfor
        
    def fadeOut(self, me, target):
        seq = Action.Sequence(me)
        seq.Add( Action.Property( on=target, property="Color",end=Vec4(1,1,1,0),duration=0.7))
    
    def fadeIn(self, me, target):
        seq = Action.Sequence(me)
        seq.Add( Action.Property( on=target, property="Color",end=Vec4(1,1,1,1),duration=0.7))

Zero.RegisterComponent("PauseMenu", PauseMenu)