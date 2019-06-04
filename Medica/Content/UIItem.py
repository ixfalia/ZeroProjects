import Zero
import Events
import Property
import VectorMath

class UIItem:
    def Initialize(self, initializer):
        self.Name = None
        self.Type = None
        self.Color = None
    
    def setData(self, _name, _type, _color):
        self.Name = _name
        self.Type = _type
        self.Color = _color
        
        self.setColor(_color)
        self.setType()
        
        self.Owner.HoverText.Text = self.Name
        
        #self.setName(self.Owner.FindChildByName("nameText"), _name)
        #self.setAmount(self.Owner.FindChildByName("amountText"))
        
        self.update()
    
    def resetData(self):
        self.Name = None
        self.Type = None
        self.Color = None
        
        #self.update()
        self.setType()
        self.setAmount(self.Owner.FindChildByName("amountText"))
        self.Owner.Reactive.Active = False
    
    def update(self):
        self.setColor()
        self.setType()
        self.setAmount(self.Owner.FindChildByName("amountText"))
    
    def setAmount(self, child):
        amount = Zero.Game.Inventory.checkItem(self.Name)
        
        if not amount:
            amount = 0
            child.SpriteText.Text = ""
            return
        
        formatted = "x{}".format(amount)
        child.SpriteText.Text = formatted
    
    def setColor(self, color = None):
        if not color:
            if not self.Color:
                return
            color = self.Color
        self.Owner.Sprite.Color = color
    
    def setName(self, child, name =  None):
        if not name:
            name = self.Name
        
        child.SpriteText.Text = name
    
    def setType(self):
        if self.Type:
            self.Owner.Sprite.SpriteSource = Zero.Game.Inventory.TypeSprites[self.Type]
        else:
            self.Owner.Sprite.SpriteSource = "BlankTile"

Zero.RegisterComponent("UIItem", UIItem)