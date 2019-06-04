import Zero
import Events
import Property
import VectorMath
import Action

Vec3 = VectorMath.Vec3

class FollowTarget:
    DebugMode = Property.Bool(default = False)
    
    TargetName = Property.String(default = "MainCharacter")
    isMovingTarget = Property.Bool(default = True)
    isActive = Property.Bool(default = True)
    isSmoothStep = Property.Bool(default = False)
    Speed = Property.Float(default = 0.7)
    ResponseTime = Property.Float(default = 0.5)
    
    currentDestination = None
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        self.Target = self.Space.FindObjectByName(self.TargetName)
        
        self.currentDestination = self.Space.FindObjectByName(self.TargetName).Transform.Translation
            #self.Owner.Timer.registerTimer("Follower", self.ResponseTime, self.stepTowardsTarget, True)
    #enddef
    
    def onUpdate(self, Event):
        #print(self.Owner.Name, "FollowTarget.onUpdate() Current Target is:", self.TargetName)
        self.stepTowardsTarget()
    #enddef
    
    def createNewStepTimer(self, duration):
        self.Owner.Timer.registerTimer("FollowTarget", duration, self.stepTowardsTarget(), True)
    
    def stepTowardsTarget(self):
        target = self.Space.FindObjectByName(self.TargetName)
        
        if not target or not self.Owner:
            print("FollowTarget.stepTowardsTarget() Target Not Found. Target", target, "or", self.Owner, "is nil")
            #raise
            return
        
        travel = target.Transform.Translation - self.Owner.Transform.Translation
        
        travel.normalize()
        
        trans = self.Owner.Transform
        trans.Translation  += travel * (self.Speed/10)
        
        #self.Owner.Transform.Translation += travel
    
    def ChangeTarget(self, name):
        if self.DebugMode:
            print(self.Owner.Name, "FollowTarget.ChangeTarget() Target Changed to: ", name)
        self.TargetName = name
    
    def getVector(self, target = None, normalized = True):
        if not target:
            target = self.Space.FindAllObjectsByName(name)
            
            if not target:
                raise
                return None
        #endif
        
        travel = target.Transform.Translation - self.Owner.Transform.Translation
        
        if normalized:
            travel.normalize()
        
        return travel
#end class 

Zero.RegisterComponent("FollowTarget", FollowTarget)