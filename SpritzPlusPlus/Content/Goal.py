import Zero
import Events
import Property
import VectorMath
import Action

Vec3 =  VectorMath.Vec3
Vec4 =  VectorMath.Vec4

class Goal:
    Timer = 0
    ActiveTimer = False
    Time = 3
    isUsed = False
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "OnPlayerAndGoal", self.onPlayerAndGoal)
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
    
    def onUpdate(self, Event):
        if self.ActiveTimer:
            self.Timer += Event.Dt
            
        if self.Timer >= self.Time and not self.isUsed:
            #self.doLogic()
            self.Timer = 0
        if self.Timer >= self.Time and self.isUsed:
            me = Zero.ScriptEvent()
            self.Space.DispatchEvent("LevelComplete", me)
            
    
    def onPlayerAndGoal(self, Event):
        print("on player and goal")
        player = self.Space.FindObjectByName("MainCharacter")
        
        #hud = player.HUDMaker.getHUD()
        #manager = hud.FindObjectByName("HUDController")
        #manager.HUDManager.PauseMainSpace()
        spaceEvent = Zero.ScriptEvent()
        self.Space.DispatchEvent("DisableControl", spaceEvent)
        player.RigidBody.Static = True
        
        self.ActiveTimer = True
        self.doLogic()
        
    def doLogic(self):
        player = self.Space.FindObjectByName("MainCharacter")
        
        hud = player.HUDMaker.getHUD()
        flowerCount = hud.FindObjectByName("Flowers")
        count = int(flowerCount.SpriteText.Text)
        
        for i in range(count+1):
            FlowerEvent = Zero.ScriptEvent()
            self.Space.DispatchEvent( "goalflower"+str(i), FlowerEvent)
        
        if count >= 7:
            FlowerEvent = Zero.ScriptEvent()
            self.Space.DispatchEvent("SuperGoal", FlowerEvent)
            
        self.isUsed =  True

Zero.RegisterComponent("Goal", Goal)