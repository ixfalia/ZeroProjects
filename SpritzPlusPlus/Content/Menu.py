import Zero
import Events
import Property
import VectorMath

Vec3 = VectorMath.Vec3
class Menu:
    StateMachine = None
    DebugMode = Property.Bool(default = False)
    ScreenAmount = Property.Uint(default = 0)
    Screen0 = Property.String(default = "blank")
    Screen1 = Property.String(default = "blank")
    Screen2 = Property.String(default = "blank")
    Screen3 = Property.String(default = "blank")
    Screen4 = Property.String(default = "blank")
    
    currentScreen = None
    screenIndex = 0
    screens = []
    HUD = None
    once = False
    empty = True
    
    moveleft = None
    moveright = None
    nextpage = None
    
    Offset = Property.Vector3(default = Vec3(0, -3, 0))
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, "myGamepadEvent", self.onGamepad)
        self.HUD = self.Space.FindObjectByName("HUDController")
        
        self.setup()
        #self.setupStatemachine()
        
    
    def setupStatemachine(self):
        pass
    
    def setup(self):
        if self.once:
            return
        
        self.screens = []
        self.currentScreen = None
        self.screenIndex = 0
        self.currentIndex = 0
        
        self.moveright = self.Space.FindObjectByName("moveright")
        self.moveleft = self.Space.FindObjectByName("moveleft")
        self.pressB = self.Space.FindObjectByName("pressB")
        
        print("BLABKJASFBKSDJGFB", self.pressB)
        if self.moveright:
            self.moveright.Sprite.Visible = False
            self.moveleft.Sprite.Visible = False
            self.pressB.Sprite.Visible = False
        
        print("Menu.setup():")
        
        if not self.Screen0 == "blank":
            print("Menu.setup() Screen0 set")
            self.screens.append( self.Screen0 )
            self.empty = False
        if not self.Screen1 == "blank":
            print("Menu.setup() Screen1 set")
            self.screens.append( self.Screen1 )
            self.empty = False
        if not self.Screen2 == "blank":
            print("Menu.setup() Screen2 set")
            self.screens.append( self.Screen2 )
            self.empty = False
        if not self.Screen3 == "blank":
            print("Menu.setup() Screen3 set")
            self.screens.append( self.Screen3 )
            self.empty = False
        
        if not self.empty:
            self.currentScreen = self.Space.CreateAtPosition("TestMenu", self.Offset + self.Owner.Transform.Translation)
            self.currentScreen.Sprite.Visible = True 
            self.currentScreen.Sprite.Color = VectorMath.Vec4(1,1,1,1)
            self.currentScreen.MenuSprite.changeSprite(self.screens[self.screenIndex])
            #self.currentScreen.Sprite.Color = VectorMath.Vec4(1,1,1,0)#for fading later
            self.currentIndex = self.screenIndex
            
            self.pressB.Sprite.Visible = True
            
            if len(self.screens) > 1:
                if self.moveleft:
                    self.moveleft.Sprite.Visible = False
                    self.moveright.Sprite.Visible = True
                
            
        self.once = True
    
    def onGamepad(self, Event):
        changed = False
        
        if(Event.Button == Zero.Buttons.DpadLeft):
            self.screenIndex -= 1
            changed = True
            if self.screenIndex < 0:
                self.screenIndex = 0
                changed = False
        if(Event.Button == Zero.Buttons.DpadRight):
            self.screenIndex += 1
            changed = True
            if self.screenIndex > len(self.screens)-1:
                self.screenIndex = len(self.screens)-1
                changed = False
            
        if Event.Button == Zero.Buttons.B or Event.Button == Zero.Buttons.Back:
            self.pressB.Sprite.Visible = False
        if Event.Button == Zero.Buttons.A or Event.Button == Zero.Buttons.Start:
            self.pressB.Sprite.Visible = False
        
        if(Event.Button == Zero.Buttons.DpadUp):
            pass
        if(Event.Button == Zero.Buttons.DpadDown):
            pass
            
        if changed:
            self.UpdateScreen()
    #enddef
    
    def unpuase(self):
        #HUD = self.Space.FindObjectByName("HUDController")
        self.HUD.HUDManager.UnpauseMainSpace()
        
    def puase(self):
        #HUD = self.Space.FindObjectByName("HUDController")
        self.HUD.HUDManager.PauseMainSpace()
        
    def UpdateScreen(self):
        print("index changed")
        self.currentScreen.Destroy()
        self.currentScreen = self.Space.CreateAtPosition("TestMenu", self.Offset + self.Owner.Transform.Translation)
        self.currentScreen.MenuSprite.changeSprite(self.screens[self.screenIndex])
        self.currentIndex = self.screenIndex
        
        if self.screenIndex == 0 and len(self.screens) > 1:
            self.moveright.Sprite.Visible = True
            self.moveleft.Sprite.Visible = False
            
        elif self.screenIndex == len(self.screens)-1 and len(self.screens) > 1:
            self.moveleft.Sprite.Visible = True
            self.moveright.Sprite.Visible = False
        elif not self.screenIndex == 0 or self.screenIndex == len(self.screens)-1:
            self.moveleft.Sprite.Visible = True
            self.moveright.Sprite.Visible = True
        pass
    
    def createCurrent(self, name):
        pass
    
    def destroyCurrent(self):
        if not self.empty:
            self.currentScreen.Destroy()
            self.moveright = self.Space.FindObjectByName("moveright")
            self.moveleft = self.Space.FindObjectByName("moveleft")
            
            self.moveright.Sprite.Visible = False
            self.moveleft.Sprite.Visible = False
            
    

Zero.RegisterComponent("Menu", Menu)