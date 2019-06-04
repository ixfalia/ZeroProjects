import Zero
import Events
import Property
import VectorMath

Vec4 = VectorMath.Vec4
Vec3 = VectorMath.Vec3

class CreateOnCollide:
    onStart = Property.Bool(default = False)
    onPersist = Property.Bool(default = False)
    onEnd = Property.Bool(default = False)
    
    #DetectSpace = Property.Bool(default = False)
    #DetectGame = Property.Bool(default = False)
    #DetectBody = Property.Bool(default = True)
    
    detectSpecificObject = Property.String()
    
    Archetype = Property.Archetype()
    Offset = Property.Vector3(default = Vec3(0,0,0))
    Position = Property.Vector3(default = Vec3(0.1, 0.1, 0.1))
    
    chatText = Property.String()
    listeningfor = Property.String()
    changeTo = Property.String()
    
    def Initialize(self, initializer):
        self.addListeners(self.Owner)
        
        self.object = None
        
        if self.Position == Vec3(0.1,0.1,0.1):
            self.Position = None
    
    def addListeners(self, detect):
        if self.onStart:
            Zero.Connect(detect, Events.CollisionStarted, self.onCollision)
        if self.onPersist:
            Zero.Connect(detect, Events.CollisionPersisted, self.onCollision)
        if self.onEnd:
            Zero.Connect(detect, Events.CollisionEnded, self.onCollision)
        
        Zero.Connect(self.Owner, Events.CollisionEnded, self.onCollisionEnd)
    
    def onCollision(self, e):
        other = e.OtherObject
        
        if not self.detectSpecificObject == "":
            if other.Name == self.detectSpecificObject:
                self.createObject()
            return
        else:
            self.createObject()
    
    def createObject(self):
        if not self.Position:
            position = self.Owner.Transform.Translation + self.Offset
            self.object = self.Space.CreateAtPosition(self.Archetype, position)
        else:
            position = self.Position + self.Offset
            self.object = self.Space.CreateAtPosition(self.Archetype, position)
        
        if self.chatText:
            self.object.SpriteText.Text = self.chatText
        if self.listeningfor:
            self.object.ChangeTextOnEvent.ListenFor = self.listeningfor
            self.object.ChangeTextOnEvent.ChangeTextTo = self.changeTo
            self.object.ChangeTextOnEvent.setData()
    
    def onCollisionEnd(self, e):
        other = e.OtherObject
        
        if not self.detectSpecificObject == "":
            if other.Name == self.detectSpecificObject:
                self.destroyObject()
            return
        else:
            self.destroyObject()
    
    def destroyObject(self):
        if self.object:
            if self.object.Fader:
                self.object.Fader.FadeDestroy()

Zero.RegisterComponent("CreateOnCollide", CreateOnCollide)