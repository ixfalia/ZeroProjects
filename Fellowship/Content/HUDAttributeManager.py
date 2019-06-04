import Zero
import Events
import Property
import VectorMath

class HUDAttributeManager:
    def DefineProperties(self):
        self.isActivated = Property.Bool(default = False)
        pass

    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Space, "HUDAttributesButton", self.onHUDAttributes)
        
        self.Update()
        pass
    
    def ToggleActivation(self):
        self.isActivated = not self.isActivated
        
        self.Update()
    
    def Update(self):
        #if self.isActivated:
        #    self.Activate()
        #else:
        #    self.Deactivate()
        self.Owner.Sprite.Visible = self.isActivated
        
        for child in self.Owner.Children:
            if child.BarHudLabel:
                for subchild in child.Children:
                    self.updateSpriteVisibility(subchild)
                continue
                #endfor
            #endif
            
            self.updateSpriteVisibility(child)
        #endfor
    
    def updateSpriteVisibility(self, child):
        if child.Sprite:
                child.Sprite.Visible = self.isActivated
        if child.SpriteText:
            child.SpriteText.Visible = self.isActivated

    def OnLogicUpdate(self, UpdateEvent):
        old = self.isActivated
        
        if not old == self.isActivated:
            self.Update()
        pass
    
    def onHUDAttributes(self, hEvent):
        self.ToggleActivation()

Zero.RegisterComponent("HUDAttributeManager", HUDAttributeManager)