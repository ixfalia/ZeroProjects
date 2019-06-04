import Zero
import Events
import Property
import VectorMath

Vec4 = VectorMath.Vec4

class MouseMenuButton:
    DebugMode = Property.Bool( default = False )
    UIString = Property.String()
    
        #Mouse state properties
    isMouseDown = False
    isFocus = False
    isHovered = False
    
        #button color shift properties
    DefaultColor = Property.Vector4(default = Vec4(1, 1, 1, 1))
    HoverColor = Property.Vector4(default = Vec4(1, 1, 1, 64))
    DownColor = Property.Vector4(default = Vec4(1, 1, 1, 128))
    
    def Initialize(self, initializer):
         # Hook up the mouse events that I'll receive from the Reactive component.
        Zero.Connect(self.Owner, Events.MouseEnter, self.onMouseEnter)
        Zero.Connect(self.Owner, Events.MouseExit, self.onMouseExit)
        Zero.Connect(self.Owner, Events.MouseUp, self.onMouseUp)
        Zero.Connect(self.Owner, Events.MouseDown, self.onMouseDown)
        
        Zero.Connect(self.Space, Events.MouseDownSomewhere, self.OnMouseDownSomewhere)
        Zero.Connect(self.Space, Events.MouseUpSomewhere, self.OnMouseUpSomewhere)
    #enddef
    
    def OnMouseDownSomewhere(self, unusedEvent):
        # I know the mouse is down
        self.isMouseDown = True
        
    def OnMouseUpSomewhere(self, unusedEvent):
            # I know the mouse is up
        self.isMouseDown = False
        
            # If i am not hovered, I know I'm not the focus
        if(self.isHovered == False):
            self.isFocus = False
        #endif
    #enddef
    
    def onMouseEnter(self, Event):
        if(self.DebugMode):
            print("Mouse Enter")
        self.isHovered = True
        
        if(self.isFocus == True):
            pass
        #endif
    
    def onMouseExit(self, Event):
        if(self.DebugMode):
            print("Mouse Exit")
        
    def onMouseUp(self, Event):
        if(self.DebugMode):
            print("Mouse Up")
    
    def onMouseDown(self, Event):
        if(self.DebugMode):
            print("Mouse Down")
    

Zero.RegisterComponent("MouseMenuButton", MouseMenuButton)