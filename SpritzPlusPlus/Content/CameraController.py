import Zero
import Events
import Property
import VectorMath
import Action

Vec3 = VectorMath.Vec3

class CameraController:
    DebugMode = Property.Bool(default = False)
    Freeze = Property.Bool(default = False)
    targetObject = Property.Cog()
    startingTarget = Property.Cog()
    #stringTarget = Property.String(default="MainCharacter")
    ZValue =Property.Float(default = 40)
    
    goalViewing = Property.Bool(default = True)
    viewtime = Property.Float(default = 1)
    traveltime = Property.Float(default = 5)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.onLogicUpdate)
        Zero.Connect(self.Space, "myGamepadEvent", self.onGamepad)
        
        self.seq = Action.Sequence(self.Owner)
        self.travelling = False
        
        player = self.Space.FindObjectByName("MainCharacter")
        player.GamepadController.disable()
        
        if not self.startingTarget:
            self.currentTarget = self.targetObject
        else:
            self.currentTarget = self.startingTarget
            
            Action.Delay(self.seq, self.viewtime)
            Action.Call(self.seq, self.changeTarget)
        
        if self.DebugMode:
            print("CameraController: Initialized")
            print("\tTarget:",self.targetObject)
        
    #end Initialize()
    
    def changeTarget(self, newTarget = None):
        if newTarget == None and self.targetObject:
            self.currentTarget = self.targetObject
        else:
            self.currentTarget = newTarget
        
        target = self.Owner.Transform
        tTransl = self.currentTarget.Transform.Translation
        end = VectorMath.Vec3(tTransl.x, tTransl.y, self.ZValue)
        self.travelling = True
        
        Action.Property(self.seq, target, "Translation", end*0.25, self.traveltime*0.25)
        Action.Property(self.seq, target, "Translation", end, self.traveltime/4)
        Action.Call(self.seq, self.notTravelling)
        Action.Call(self.seq, self.unfreezeplayer)
    
    def onLogicUpdate(self, UpdateEvent):
        if not self.Freeze and not self.travelling:
            currentTranslation = self.Owner.Transform.Translation
            targetTranslation = self.currentTarget.Transform.WorldTranslation
            
            if self.DebugMode:
                print("CameraController.onLogicUpdate():")
                print("\t Target:", self.currentTarget)
                print("\t Target WTranslation:",self.currentTarget.Transform.WorldTranslation)
                print("\t Target Translation:", self.currentTarget.Transform.Translation)
                print("\t CurrentTranslation:", self.Owner.Transform.Translation)
            
                #New Camera Keeps it's y and z values, if i care about y movement then i can change to targetTranslation.y
            newTranslation = VectorMath.Vec3(targetTranslation.x, targetTranslation.y, self.ZValue)
            
            self.Owner.Transform.Translation = newTranslation
    #end onLogicUpdate()
    
    def FreezeCamera(self, isFrozen = None):
        if isFrozen == None:
            self.Freeze = not self.Freeze
        else:
            self.Freeze = isFrozen
        
    
    def notTravelling(self):
        self.travelling = False
    
    def unfreezeplayer(self):
        player = self.Space.FindObjectByName("MainCharacter")
        
        player.GamepadController.enable()
        
        lEvent = Zero.ScriptEvent()
        player.HUDEventDispatcher.DispatchHUDEvent("LevelBegin", lEvent)
    
    def onGamepad(self, gEvent):
        if(gEvent.Button == Zero.Buttons.DpadUp or gEvent.Button == Zero.Buttons.DpadDown
        or gEvent.Button == Zero.Buttons.DpadLeft or gEvent.Button == Zero.Buttons.DpadRight):
            return
        
        self.currentTarget = self.targetObject
        
        self.notTravelling()
        self.unfreezeplayer()
        
        self.seq.Cancel()
        
        Zero.Disconnect(self.Space, "myGamepadEvent", self.onGamepad)
#end class CameraController

Zero.RegisterComponent("CameraController", CameraController)