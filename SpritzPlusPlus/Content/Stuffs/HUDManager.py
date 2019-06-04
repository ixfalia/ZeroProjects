import Zero
import Events
import Property
import VectorMath

Vec3 = VectorMath.Vec3
Vec2 = VectorMath.Vec2

class HUDManager:
    DebugMode = Property.Bool(default = False)
    DefaultTankSize = 9
    Gamepad = Zero.Gamepads.GetGamePad(0) # getting first player gamepad
    deadzone = Property.Float(default = 0.2) #used to define deadzones for menu interaction.
    FlowerTrack = 0
    
    MainSpace = None
    Menu = None
    Timer = 0
    
    otherPause = False
    isPaused = False
    
    moveleft = None
    moveright = None
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        Zero.Connect(self.Space, "WaterTankEvent", self.onWaterTank)
        Zero.Connect(self.Space, "PointsEvent", self.onPoints)
        Zero.Connect(self.Space, "InformationEvent", self.onInfo)
        Zero.Connect(self.Space, "myGamepadEvent", self.onGamepad)
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevelStart)
        Zero.Connect(self.Space, "FlowerGet", self.onFlower)
        
        self.Menu = self.Space.Create("HUDMenu")
        self.Menu.Sprite.Visible = False
        
        self.moveright = self.Space.FindObjectByName("moveright")
        self.moveleft = self.Space.FindObjectByName("moveleft")
        
        self.moveright.Sprite.Visible = False
        self.moveleft.Sprite.Visible = False
        
        if self.DebugMode:
            print("Hudmanager made in space: ", self.Space)
    
    def onLevelStart(self, Event):
        #self.Menu = self.Space.Create("HUDMenu")
        self.Space.SoundSpace.PlayMusic("BGM_MagicHat")
        pass
    #enddef
    
    def onUpdate(self, Event):
        #if(self.Gamepad.IsButtonPressed(Zero.Buttons.Start)):
            #self.handleStart()
        
        if(self.MainSpace):
            if(self.MainSpace.TimeSpace.Paused):
                #self.MenuPadUpdate(Event.Dt)
                pass
            else:
                pass
            #endif
        #endif
    #enddef
    
    def onGamepad(self, Event):
        if Event.Button == Zero.Buttons.Start:
            self.handleStart()
        if self.isPaused == True and Event.Button == Zero.Buttons.B or Event.Buttons == Zero.Buttons.Back:
            self.handleStart()
        
    
    def handleStart(self):
        if self.DebugMode:
            print("HUDManager.handleStart()")
        
        self.SelectionID = Vec2()
        
        if not self.otherPause:
            if self.DebugMode:
                print("Start Button Pressed, Game Paused.")
            if self.MainSpace:
                    self.MainSpace.TimeSpace.TogglePause()
                    self.isPaused = self.MainSpace.TimeSpace.Paused
            else:
                print("HUDManager.MainSpace Cannot be found. Game is not paused.")
            
            if self.Menu.PauseMenu:
                self.Menu.PauseMenu.onPause()
            else:
                self.Menu.Sprite.Visible = self.isPaused
        #endif
        
        #menu = self.Space.FindObjectByName("Menu")
        #menu.Sprite.Visible =  not menu.Sprite.Visible
        
        
    #enddef
    
    def PauseMainSpace(self):
        self.otherPause = True
        
        if self.MainSpace:
            self.MainSpace.TimeSpace.Pause()
    
    def UnpauseMainSpace(self):
        self.otherPause = False
        
        if self.MainSpace:
            self.MainSpace.TimeSpace.Paused = False
    
    def onInfo(self, Event):
        print("HUDManager.OnInfo: Got Message!")
        self.MainSpace = Event.Space
        self.UIPause = self.MainSpace.TimeSpace.Pause
        
        #Zero.Connect(self.MainSpace, "FlowerEvent", self.onFlower)
    
    def onWaterTank(self, TankEvent):
        TankHUD = self.Space.FindObjectByName("UITank")
        
        #if TankHUD and self.DebugMode:
            #print("HUD: TankFound")
        
        current = TankHUD.Transform.Scale
        
        TankHUD.Transform.Scale = Vec3(current.x, self.DefaultTankSize * TankEvent.Tank, current.z)
        
        if TankEvent.isReplenishing:
            TankHUD.Model.Material = "TankWater"
        else:
            TankHUD.Model.Material = "Water"
        
        if self.DebugMode:
            #print("TankScale: ", TankHUD.Transform.Scale.y)
            #print("Tank: ", TankEvent.Tank)
            pass
    #enddef
    
    def onPoints(self, PointEvent):
        if self.DebugMode:
            print("HUDManager.onPoints()")
            print(PointEvent.Points)
        PointHUD = self.Space.FindObjectByName("Points")
        
        PointHUD.SpriteText.Text = str(int(PointEvent.Points))
        print(PointHUD)
        print(PointHUD.SpriteText.Text)
    
    def onFlower(self, Event):
        print("onFlower")
        PointHUD = self.Space.FindObjectByName("Flowers")
        self.FlowerTrack += 1
        PointHUD.SpriteText.Text = str(int(self.FlowerTrack))
    #enddef
    
    def Do(self, command, param = None):
        if command == "LevelChange":
            self.changeLevel(param)
        elif command == "Quit":
            Zero.Game.Quit()
        elif command == "Reset":
            Zero.Game.Reset()
        elif command == "Pause":
            Zero.Game.Pause()
        else:
            print("UIManager Do: " + command + " is not a UI command.")
        #endif
    #enddef
    
    def changeLevel(self, level):
        self.Space.LoadLevel( level )
        
    def playSoundCue(self, cue):
        self.Owner.SoundEmitter.PlayCue(cue)
#end Class

Zero.RegisterComponent("HUDManager", HUDManager)