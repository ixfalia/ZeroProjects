import Zero
import Events
import Property
import VectorMath

Vec3 = VectorMath.Vec3
Vec2 = VectorMath.Vec2

class UIManager:
    DebugMode = Property.Bool(default = True)
    
    MainSpace = None
    Menu = None
    Timer = 0
    
    deadzone = Property.Float(default = 0.2) #used to define deadzones for menu interaction.
    
    otherPause = False
    isPaused = False
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevel)
        Zero.Connect(self.Space, "GamePause", self.onPause)
        Zero.Connect(self.Space, "myGamepadEvent", self.onGamepad)
        Zero.Connect(self.Space, "InformationEvent", self.onInfo)
        
        self.moveright = self.Space.FindObjectByName("moveright")
        self.moveleft = self.Space.FindObjectByName("moveleft")
        self.Pause = self.Space.FindObjectByName("Pause")
        self.Spectrum = self.Space.FindObjectByName("Spectrum")
        
        self.moveright.Sprite.Visible = False
        self.moveleft.Sprite.Visible = False
    #enddef
    
    def onLevel(self, Event):
        #self.Owner.SoundEmitter.Play()
        pass
    
    def onGamepad(self, Event):
        if Event.Button == Zero.Buttons.Start:
            self.handleStart()
        if self.isPaused == True and Event.Button == Zero.Buttons.B or Event.Buttons == Zero.Buttons.Back:
            self.handleStart()
        
    #enddef
    
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
                self.isPaused = not self.isPaused
                print("HUDManager.MainSpace Cannot be found. Game is not paused.")
            
            self.Pause.Sprite.Visible = self.isPaused
            self.Spectrum.Model.Visible = self.isPaused
            #if self.Menu.PauseMenu:
            #    self.Menu.PauseMenu.onPause()
            #else:
            #    self.Menu.Sprite.Visible = self.isPaused
    #enddef
    
    def onPause(self, Event):
        pass
    
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
    #enddef
    
    def changeLevel(self, level):
        self.Space.LoadLevel( level )
        
    def playSoundCue(self, cue):
        self.Owner.SoundEmitter.PlayCue(cue)
#endclass

Zero.RegisterComponent("UIManager", UIManager)