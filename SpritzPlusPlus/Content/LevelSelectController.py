import Zero
import Events
import Property
import VectorMath

import Action
import Color

Vec3 = VectorMath.Vec3

class LevelSelectController:
    defaultSelectionID = Property.Uint(default = 0)
    TravelTime = Property.Float(default = 1.2)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, "myGamepadEvent", self.onGamepad)
        Zero.Connect(self.Space, "GamepadButtonInit", self.onButtonInit)
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevel)
        
        print("LevelSelectController.Initialize()")
        
        self.ButtonList = []
        self.currentSelection = self.defaultSelectionID
        #self.currentSelection = 0
        self.Traveling = False
        #self.first = False
        #raise
    
    def reset(self):
        Zero.Connect(self.Space, "myGamepadEvent", self.onGamepad)
        Zero.Connect(self.Space, "GamepadButtonInit", self.onButtonInit)
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevel)
        
        self.ButtonList = []
        self.currentSelection = self.defaultSelectionID
        #self.currentSelection = 0
        self.Traveling = False
        
        print("LevelSelectController.rest()")
    
    def onLevel(self, lEvent):
        #print("LevelSelectController.onLevel():")
        #print("\t", self.ButtonList)
        
        lastLevel = Zero.Game.LevelManager.getLastLevel()
        print("onLevel(). Last Level:", lastLevel.Name)
        button, self.currentSelection = self.findButtonWithLevel(lastLevel)
        print("onLevel(). button", button, "currentselection", self.currentSelection)
        
        #self.SendUpdateEvent()
        self.checkButtonColors()
        self.Owner.Transform.Translation = self.ButtonList[self.currentSelection].Transform.Translation
        self.ButtonList[self.currentSelection].GamepadButton.Active = True
        self.ButtonList[self.currentSelection].Sprite.Color = Color.Yellow
        
        if not self.currentSelection == 0:
            self.SendUpdateEvent()
        #self.changeSelection(self.currentSelection)
    
    def onButtonInit(self, gEvent):
        #self.checkButtonColors()
        self.ButtonList.insert(gEvent.ID, gEvent.Object)
    
    def onGamepad(self, gEvent):
        if gEvent.Button == Zero.Buttons.DpadLeft:
            self.Owner.Sprite.FlipX = False
            self.changeSelection(self.currentSelection-1)
        elif gEvent.Button == Zero.Buttons.DpadRight:
            self.Owner.Sprite.FlipX = True
            self.changeSelection(self.currentSelection+1)
    
    def changeSelection(self, ID):
        if ID < 0:
            return
        if ID >= len(self.ButtonList):
            return
        if self.Traveling:
            return
        
        #print("LevelSelectController.changeSelection()")
        #print("\tChanging Selection To:", ID)
        
        old = self.ButtonList[self.currentSelection]
        self.checkButtonColors()
        old.GamepadButton.Active = False
        
        self.currentSelection = ID
        
        e = Zero.ScriptEvent()
        self.Space.DispatchEvent("FadeEvent", e)
        
        seq = Action.Sequence(self.Owner)
        end = self.ButtonList[ID].Transform.Translation
        Action.Property(seq, self.Owner.Transform, "Translation", end, self.TravelTime, Action.Ease.Linear)
        Action.Call(seq, self.ActivateButton)
        Action.Call(seq, self.EndTravel)
        
        self.Traveling = True
    
    def updateSelection(self, newID):
        pass
    
    def findButtonWithLevel(self, level):
        i = 0
        
        for button in self.ButtonList:
            if button.LevelChangeButton.LevelChange.Name == level.Name:
                return button,i
            
            i += 1
    
    def EndTravel(self):
        self.Traveling = False
        if self.ButtonList[self.currentSelection].LevelChangeButton.LevelChange.Name == "MainMenu":
            e = Zero.ScriptEvent()
            self.Space.DispatchEvent("FadeEvent", e)
            return
        
        self.ButtonList[self.currentSelection].Sprite.Color = Color.Yellow
        
        seq = Action.Sequence(self.Owner)
        Action.Call(seq, self.SendUpdateEvent)
    
    def SendUpdateEvent(self):
        selectionID = Zero.Game.LevelManager.levelTable.FindIndexOfResource(self.ButtonList[self.currentSelection].LevelChangeButton.LevelChange)
        e = Zero.ScriptEvent()
        e.CurrentSelection = selectionID
        e.Position = self.Owner.Transform.Translation
        e.LevelData = Zero.Game.AccomplishmentDataManager.getLevelData(selectionID)
        
        #print(e.LevelData.LevelName)
        #print(e.LevelData.TotalFlowers)
        
        self.Space.DispatchEvent("LevelDataEvent", e)
    
    def ActivateButton(self):
        self.ButtonList[self.currentSelection].GamepadButton.Active = True
        #self.ButtonList[self.currentSelection].Sprite.Color = Ye
        pass
    
    def checkButtonColors(self):
        for button in self.ButtonList:
            level = button.LevelChangeButton.LevelChange
            index = Zero.Game.LevelManager.levelTable.FindIndexOfResource(level)
            data = Zero.Game.AccomplishmentDataManager.getLevelData(index)
            
            if data.Played:
                button.Sprite.Color = Color.CadetBlue
            else:
                button.Sprite.Color = Color.Firebrick
        #endfor
        
        #select = self.ButtonList[self.currentSelection]
        #select.Sprite.Color = Color.Yellow

Zero.RegisterComponent("LevelSelectController", LevelSelectController)