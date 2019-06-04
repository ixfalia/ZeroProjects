import Zero
import Events
import Property
import VectorMath

import Action

Vec3 = VectorMath.Vec3

class Sign:
    DebugMode = Property.Bool(default = False)
    TypeTrigger = Property.Bool(default = False)
    TriggerTimeDelay = Property.Float(default = 0)
    TypeControlDown = Property.Bool(default = True)
    TypeControlA = Property.Bool(default = False)
    TypeAuto = Property.Bool(default = False)
    TypeOnGameStart = Property.Bool(default = False)
    TypeOnSpaceEvent = Property.Bool(default = False)
    TypeOnOwnerEvent = Property.Bool(default = False)
    
    EventType = Property.String(default = "")
    
    gamepad = Zero.Gamepads.GetGamePad(0) # getting first player gamepad
    MenuType = Property.Archetype()
    SpriteMenu = Property.SpriteSource()
    MenuOffset = Property.Vector3(default = Vec3(0, 2, -1) )
    
    myMenu = None
    HUDSpace = None
    playerContact = False
    isActive = False
    isUsed = False
    
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.onCollision)
        Zero.Connect(self.Owner, Events.CollisionPersisted, self.onCollisionPersist)
        Zero.Connect(self.Owner, Events.CollisionEnded, self.onCollisionEnd)
        Zero.Connect(self.Owner, "Popup", self.PopUpEvent)
        #Zero.Connect(self.Space, "HUDCreated", self.onHUD)
        Zero.Connect(self.Space, "myGamepadEvent", self.onGamepad)
        
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
        
        
    
    def onCollision(self, Event):
        other = Event.OtherObject
        
        if( other.Player ):
            self.playerContact = True
            
            self.isActive = False
            
            #if self.TypeTrigger and not self.isUsed or self.TypeAuto:
            #    self.popUpFade()
                #self.PopUp()
                #self.isUsed = True
        #endif
    
    def onGamepad(self, gEvent):
        if self.playerContact:
            if self.TypeControlA:
                if gEvent.Button == Zero.Buttons.A:
                    self.popUpFade()
            if self.TypeControlDown:
                if gEvent.Button == Zero.Buttons.DpadDown:
                    self.popUpFade()
                    #endif
                #endif
            #endif
    
    def popUpFade(self):
        seq = Action.Sequence(self.Owner)
        Action.Delay(seq, self.TriggerTimeDelay)
        Action.Call(seq, self.PopUp)
    
    def onCollisionPersist(self, cEvent):
        other = cEvent.OtherObject
        
        if other.Player:
            if(self.gamepad.IsButtonPressed(Zero.Buttons.DpadDown)):
                self.PopUp()
    
    def onCollisionEnd(self, Event):
        other = Event.OtherObject
        
        if other.Player:
            self.playerContact = False
            
            if self.TypeTrigger or self.isActive:
                self.myMenu.Fader.FadeOut()
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
    
    def onGamepad2(self, Event):
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
        if self.isActive:
            return
        
        self.isActive = True
        self.isUsed = True
        self.myMenu = self.Space.CreateAtPosition(self.MenuType, self.Owner.Transform.Translation+self.MenuOffset)
        
        if not self.SpriteMenu.Name == "DefaultSprite":
            self.myMenu.Sprite.SpriteSource = self.SpriteMenu
        
        if self.myMenu.Fader:
            self.myMenu.Fader.FadeIn()
        
        if self.myMenu.Menu:
            self.myMenu.Menu.puase()
        else:
            print("Sign.PopUp(): myMenu not found")
    
    def PopDown(self):
        self.isActive = False
        if not self.myMenu:
            return
        print(self.myMenu)
        
        seq = Action.Sequence(self.Owner)
        
        if self.myMenu.Menu:
            if self.myMenu.Fader:
                self.myMenu.Fader.FadeOut()
                Action.Delay(seq, self.myMenu.Fader.FadeOutDuration)
                Action.Call(seq, self.myMenu.Menu.unpuase)
                Action.Call(seq, self.myMenu.Menu.destroyCurrent)
                Action.Call(seq, self.myMenu.Destroy)
                return
            self.myMenu.Menu.unpuase()
            self.myMenu.Menu.destroyCurrent()
            self.myMenu.Destroy()
        else:
            if self.myMenu.Fader:
                self.myMenu.Fader.FadeOut()
                Action.Delay(seq, self.myMenu.Fader.FadeOutDuration)
                Action.Call(seq, self.myMenu.Destroy)
                return
            
            self.myMenu.Destroy()
            print("Sign.PopDown(): myMenu not found")
        #endif
    #enddef
    
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