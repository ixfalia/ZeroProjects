import Zero
import Events
import Property
import VectorMath
import Action

import math

Vec3 = VectorMath.Vec3

class CameraController:
    DebugMode = Property.Bool(default = False)
    Freeze = Property.Bool(default = False)
    targetObject = Property.Cog()
    startingTarget = Property.Cog()
    #stringTarget = Property.String(default="MainCharacter")
    Offset = Property.Vector3(default = Vec3())
    ZValue =Property.Float(default = 40)
    
    goalViewing = Property.Bool(default = True)
    viewtime = Property.Float(default = 1)
    traveltime = Property.Float(default = 5)
    
    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LevelStarted, self.onLevelStart)
        Zero.Connect(self.Space, Events.LogicUpdate, self.onLogicUpdate)
        Zero.Connect(self.Space, "myGamepadEvent", self.onGamepad)
        Zero.Connect(self.Space, Events.KeyDown, self.onKeyboard)
        #Zero.Connect(self.Space, "OnGround", self.onOnGround)
        
        self.seq = Action.Sequence(self.Owner)
        self.travelling = False
        self.tweenTime = 1.0
        self.tweenTimer = 0.0
        self.tweening = False
        
        player = self.Space.FindObjectByName("MainCharacter")
        #player.GamepadController.disable()
        
        if not self.targetObject:
            self.targetObject = player
        if not self.startingTarget:
            if self.goalViewing:
                self.currentTarget = self.Space.FindObjectByName("EndGoal")
            else:
                self.currentTarget = self.targetObject
        else:
            self.currentTarget = self.startingTarget
            
            Action.Delay(self.seq, self.viewtime)
            Action.Call(self.seq, self.changeTarget)
        
        if self.DebugMode:
            print("CameraController: Initialized")
            print("\tTarget:",self.targetObject)
        
    #end Initialize()
    
    def onLevelStart(self, lEvent):
        pass
    
    def changeTarget(self, newTarget = None):
        if newTarget == None and self.targetObject:
            self.currentTarget = self.targetObject
        else:
            self.currentTarget = newTarget
        
        target = self.Owner.Transform
        tTransl = self.currentTarget.Transform.Translation + self.Offset
        end = VectorMath.Vec3(tTransl.x, tTransl.y, self.ZValue)
        self.travelling = True
        
        Action.Property(self.seq, target, "Translation", end*0.25, self.traveltime*0.25)
        Action.Property(self.seq, target, "Translation", end, self.traveltime/4)
        Action.Call(self.seq, self.notTravelling)
        Action.Call(self.seq, self.unfreezeplayer)
    
    def onLogicUpdate(self, UpdateEvent):
        if not self.Freeze and not self.travelling:
            currentTranslation = self.Owner.Transform.Translation
            targetTranslation = self.currentTarget.Transform.WorldTranslation + self.Offset
            
            if self.DebugMode:
                print("CameraController.onLogicUpdate():")
                print("\t Target:", self.currentTarget)
                print("\t Target WTranslation:",self.currentTarget.Transform.WorldTranslation)
                print("\t Target Translation:", self.currentTarget.Transform.Translation)
                print("\t CurrentTranslation:", self.Owner.Transform.Translation)
            
            distanceToTarget = math.fabs(targetTranslation.x - currentTranslation.x)
            tweenDistance = 10.0
            
            if False:#self.tweening:
                self.tweenTimer += UpdateEvent.Dt
                step = self.tweenTimer / self.tweenTime
                
                newTranslation = self.Owner.Transform.Translation.lerp(targetTranslation, step)
                
                if self.tweenTimer >= self.tweenTime or tweenDistance <= 2:
                    self.tweening = False
            if False:#distanceToTarget >= tweenDistance:
                self.tweenTimer = 0
                self.tweening = True
                newTranslation = VectorMath.Vec3(targetTranslation.x, currentTranslation.y, self.ZValue)
            else:
                #New Camera Keeps it's y and z values, if i care about y movement then i can change to targetTranslation.y
                newTranslation = VectorMath.Vec3(targetTranslation.x, targetTranslation.y, self.ZValue)
            
            self.Owner.Transform.Translation = newTranslation
            #print("CameraPos:",self.Owner.Transform.Translation)
    #end onLogicUpdate()
    
    def updateY(self):
        #if self.tweening:
        #    return
        
        currentTranslation = self.Owner.Transform.Translation
        targetTranslation = self.currentTarget.Transform.WorldTranslation# + self.Offset
        newTranslation = VectorMath.Vec3(currentTranslation.x, targetTranslation.y, self.ZValue)
        time = math.fabs(currentTranslation.y - targetTranslation.y)/50
        
        #self.Owner.Transform.Translation = VectorMath.Vec3(currentTranslation.x, targetTranslation.y, self.ZValue)
        
        #self.tweening = True
        
        #seq = Action.Group(self.Owner)
        #Action.Property(seq, self.Owner.Transform, "Translation", targetTranslation, time, Action.Ease.Linear)
        #Action.Call(seq, self.tweenDone)
    
    def tweenDone(self):
        self.tweening = False
    
    def FreezeCamera(self, isFrozen = None):
        if isFrozen == None:
            self.Freeze = not self.Freeze
        else:
            self.Freeze = isFrozen
        
    
    def notTravelling(self):
        self.travelling = False
    
    def unfreezeplayer(self):
        player = self.Space.FindObjectByName("MainCharacter")
        
        #player.GamepadController.enable()
        
        if player.HUDEventDispatcher:
            lEvent = Zero.ScriptEvent()
            player.HUDEventDispatcher.DispatchHUDEvent("LevelBegin", lEvent)
        #endif
    #enddef
    
    def onGamepad(self, gEvent):
        if(gEvent.Button == Zero.Buttons.DpadUp or gEvent.Button == Zero.Buttons.DpadDown
        or gEvent.Button == Zero.Buttons.DpadLeft or gEvent.Button == Zero.Buttons.DpadRight):
            return
        
        self.currentTarget = self.targetObject
        
        self.notTravelling()
        self.unfreezeplayer()
        
        self.seq.Cancel()
        
        Zero.Disconnect(self.Space, "myGamepadEvent", self.onGamepad)
    
    def onKeyboard(self, gEvent):
        self.currentTarget = self.targetObject
        
        self.notTravelling()
        self.unfreezeplayer()
        
        self.seq.Cancel()
        Zero.Disconnect(self.Space, Events.KeyDown, self.onKeyboard)
    
#end class CameraController

Zero.RegisterComponent("CameraController", CameraController)