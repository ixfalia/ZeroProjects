import Zero
import Events
import Property
import VectorMath

class MenuMaker:
    def DefineProperties(self):
        self.MenuSubElements = Property.String()
        self.Levels = Property.Level()
        self.StartingOffset = Property.Vector3()
        self.OffestAmount = Property.Float()
        
        self.ResourceTable = Property.ResourceTable()
        
        #HardCodes
        self.Option1 = Property.Level()
        self.Option2 = Property.Level()
        self.Option3 = Property.Level()
        self.Option4 = Property.Level()
        pass

    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, Events.MouseDown, self.onMouseDown)
        Zero.Connect(self.Owner, Events.MouseUp, self.onMouseUp)
        self.SubMenuList = []
        self.CreatedElements = []
        
        for key in self.__dict__.keys():
            for i in range(5):
                checkstring = "Option{}".format(i)
                element = self.__dict__[key]
                
                if key == checkstring and not element.Name == "DefaultLevel":
                    self.SubMenuList.append(element)
        
        print(self.SubMenuList)
        pass

    def OnLogicUpdate(self, UpdateEvent):
        pass
    
    def onMouseDown(self, MouseEvent):
        if self.CreatedElements:
            self.destroyElements()
        
        offset = 0
        
        for menuitem in self.SubMenuList:
            label = self.ResourceTable.FindValue(menuitem.Name)
            #label = self.ResourceTable.GetNameAt(id)
            
            offsetV = VectorMath.Vec3(0, offset, 0)
            owner = self.Owner.Transform.Translation
            position = VectorMath.Vec3(owner.x, owner.y, 0) + self.StartingOffset + offsetV
            
            self.createElement(position, label, menuitem)
            
            offset += self.OffestAmount
    
    def destroyElements(self):
        if self.CreatedElements:
            for e in self.CreatedElements:
                obj = self.CreatedElements.pop()
                #obj.DestructionTimer.Active = True
                obj.Destroy()
    
    def onMouseUp(self, MouseEvent):
        if self.CreatedElements:
            for e in self.CreatedElements:
                obj = self.CreatedElements.pop()
                #obj.DestructionTimer.Active = True
                obj.Destroy()
        pass
    
    def createElement(self, position, name, level):
        #position = VectorMath.Vec3(0, -3, 6)
        #print(position)
        nuObj = self.Owner.Parent.Space.CreateAtPosition("SubOption", position)
        
        nuObj.LevelTransitionButton.Level = level
        #print(nuObj)
        label = nuObj.FindChildByName("label")
        print(label, name)
        label.SpriteText.Text = name
        
        self.CreatedElements.append(nuObj)

Zero.RegisterComponent("MenuMaker", MenuMaker)