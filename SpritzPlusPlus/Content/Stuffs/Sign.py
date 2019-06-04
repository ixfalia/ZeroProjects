import Zero
import Events
import Property
import VectorMath

Vec3 = VectorMath.Vec3

class Sign:
    DebugMode = Property.Bool(default = False)
    TypeTrigger = Property.Bool(default = False)
    TypeControlDown = Property.Bool(default = True)
    TypeControlA = Property.Bool(default = False)
    TypeAuto = Property.Bool(default = False)
    TypeOnGameStart = Property.Bool(default = False)
    TypeOnSpaceEvent = Property.Bool(default = False)
    TypeOnOwnerEvent = Property.Bool(default = False)
    
    EventType = Property.String(default = "")
    
    gamepad = Zero.Gamepads.GetGamePad(0) # getting first player gamepad
    MenuType = Property.String(default = "twinkle")
    MenuOffset = Property.Vector3(default = Vec3(0, 2, -1) )
    
    myMenu = None
    HUDSpace = None
    playerContact = False
    isActive = False
    isUsed = False
    
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.onCollision)
        Zero.Connect(self.Owner, Events.CollisionEnded, self.onCollisionEnd)
        Zero.Connect(self.Owner, "Popup", self.PopUpEvent)
        Zero.Connect(self.Space, "HUDCreated", self.onHUD)
        
        if self.TypeOnSpaceEvent:
            if self.EventType == "":
                print("Sign.EventType is not defined")
            else:
                if self.DebugMode:
                    print("Sign Event Connected")
                Zero.Connect(self.Space, self.EventType, self.onEvent)
        
        if self.TypeOnOwnerEvent:
            if self.EventType == "":
                print("Sign.EventType is not defined")
            else:
                if self.DebugMode:
                    print("Sign", self.EventType, "Event Connected to sign.")
                Zero.Connect(self.Owner, self.EventType, self.onEvent)
        
        
    
    def onEvent(self, Event):
        print("Sign.onEvent(): Event Detected.")
        if not self.isUsed:
                self.PopUp()
                self.isUsed = True
    
    def onCollision(self, Event):
        other = Event.GetOtherObject(self.Owner)
        
        if( other.PlayerController ):
            self.playerContact = True
            
            if self.TypeTrigger and not self.isUsed:
                self.PopUp()
                self.isUsed = True
        #endif
    
    def onCollisionEnd(self, Event):
        other = Event.GetOtherObject(self.Owner)
        
        if other.PlayerController:
            self.playerContact = False
            
            if self.TypeTrigger:
                self.PopDown()
        #endif
    
    def onHUD(self, Event):
        print("Sign.onHUD()")
        self.isHUDMade = True
        self.HUDSpace = Event.HUDSpace
        
        Zero.Connect(self.HUDSpace, "myGamepadEvent", self.onGamepad)
        
        if self.TypeOnGameStart:
            print("GLNBFEIU:{PJHGGUHPOSIRUHGI:PURhis")
            self.PopUp()
    #enddef
    
    def onGamepad(self, Event):
        if self.isActive:
            if Event.Button == Zero.Buttons.B or Event.Button == Zero.Buttons.Back:
                if self.DebugMode:
                    print("Sign.onGamepad(): Canceling Menu")
                self.PopDown()
            if Event.Button == Zero.Buttons.A or Event.Button == Zero.Buttons.Start:
                self.PopDown()
                pass
            #endif
        #endif
        
        if not self.playerContact:
            return
        
        if not self.isActive:
            if self.TypeControlA:
                if Event.Button == Zero.Buttons.A:
                    pass
            if self.TypeControlDown:
                if Event.Button == Zero.Buttons.DpadDown:
                    pause = self.HUDSpace.FindObjectByName("HUDController")
                    if not pause.HUDManager.isPaused:
                        self.PopUp()
                    #endif
                #endif
            #endif
    #enddef
    
    def PopUp(self):
        self.isActive = True
        self.myMenu = self.HUDSpace.CreateAtPosition(self.MenuType, self.MenuOffset)
        
        if self.myMenu.Menu:
            self.myMenu.Menu.puase()
        else:
            print("Sign.PopUp(): myMenu not found")
    
    def PopDown(self):
        self.isActive = False
        if not self.myMenu:
            return
        print(self.myMenu)
        if self.myMenu.Menu:
            self.myMenu.Menu.unpuase()
            self.myMenu.Menu.destroyCurrent()
            self.myMenu.Destroy()
        else:
            print("Sign.PopDown(): myMenu not found")
            
    def PopUpEvent(self, Event):
        self.isActive = True
        self.myMenu = self.HUDSpace.CreateAtPosition(self.MenuType, self.MenuOffset)
        
        if self.myMenu.Menu:
            self.myMenu.Menu.puase()
        else:
            print("Sign.PopUp(): myMenu not found")
        
    def PopUpDynamic(self, type):
        self.isActive = True
        self.myMenu = self.HUDSpace.CreateAtPosition(type, self.MenuOffset)
        
        if self.myMenu.Menu:
            self.myMenu.Menu.puase()
        else:
            print("Sign.PopUp(): myMenu not found")

Zero.RegisterComponent("Sign", Sign)