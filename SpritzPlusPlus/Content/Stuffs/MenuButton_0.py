import Zero
import Events
import Property
import VectorMath

class MenuButton:
    isPop = Property.Bool(default = True)
    PopUp = Property.String(default = "IntroductionMenu")
    isLevelChange = Property.Bool(default = False)
    LevelChange = Property.String(default = "MainMenu")
    Position = Property.Vector3()
    popVisible = Property.Bool(default = False)
    
    isHUDMade = False
    HUDSpace = None
    
    menu = None
    
    def Initialize(self, initializer):
        self.menu = self.Space.CreateAtPosition(self.PopUp, self.Owner.Transform.Translation)
        print("MenuButton: ", self.menu)
        if self.menu:
            print(self.PopUp, "created.")
            #self.menu.Sprite.Visible = self.popVisible
        
    
    def do(self):
        self.menu = self.Space.CreateAtPosition("TestMenu", self.Owner.Transform.Translation)
        if self.isPop:
            self.menu.Sprite.Visible =  True
        elif self.isLevelChange:
            manager = self.Space.FindObjectByName("HudManager")
            manager.MainSpace.DestroyAll()
            manager.MainSpace.LoadLevel(self.LevelChange)
        pass

Zero.RegisterComponent("MenuButton", MenuButton)