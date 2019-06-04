import Zero
import Events
import Property
import VectorMath

class TimeWaitManager:
    class Timer:
        def __init__(self, duration, name, callback):
            self.Duration_ = duration
            self.Name_ = name
            self.Callback_ = callback
            
            self.TotalTime_ = 0
    #end class Timer
    
    def DefineProperties(self):
        self.Debug = Property.Bool(default = True)
        self.DebugExtreme = Property.Bool(default = True)
        #self.Lives = Property.Int(9)
        self.TotalTime = Property.Float()
        #self.CurrentTimer = Property.Bool()
        pass

    def Initialize(self, initializer):
        #self.MainSpace = self.Owner.FindSpaceByName("Main")
        Zero.Connect(self.GameSession, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.GameSession, "DebugUpdate", self.onDebug)
        
        self.CurrentTimer = None
        self.TotalTime = 0
        
        self.WaitList = []
        self.addTimer(10, "foo")
        pass

    def OnLogicUpdate(self, UpdateEvent):
        self.TotalTime += UpdateEvent.Dt
        
        self.updateTime(UpdateEvent.Dt)
        
        if self.DebugExtreme and self.CurrentTimer:
            print("\t[TimerManager] ({}) {:.2f}/{:.2f}".format(self.CurrentTimer.Name_, self.CurrentTimer.TotalTime_, self.CurrentTimer.Duration_))
        pass
    
    def updateTime(self, dt):
        if not self.WaitList:
            return
        
        if self.CurrentTimer:
            self.CurrentTimer.TotalTime_ += dt
            
            totalTime = self.CurrentTimer.TotalTime_
            duration = self.CurrentTimer.Duration_
            
            if totalTime >= duration:
                self.timerDone()
            #endif
        else:
            print(self.WaitList)
            raise
            self.CurrentTimer = self.WaitList[0]
            
            self.CurrentTimer.TotalTime_ += dt
    
    def createTimer(self, duration, name, callback = None):
        timer = self.Timer(duration, name, callback)
        
        return timer
    
    def addTimerObject(self, timer):
        self.WaitList.append(timer)
        
        if not self.CurrentTimer:
            self.CurrentTimer = self.WaitList[0]
    
    def addTimer(self, duration, name, callback = None):
        timer = self.createTimer(duration, name, callback)
        
        self.addTimerObject(timer)
    
    def timerDone(self):
        if self.CurrentTimer.Callback_:
            self.CurrentTimer.Callback_()
        
        self.WaitList.pop(0)
        
        if self.WaitList:
            self.CurrentTimer = self.WaitList[0]
        else:
            self.CurrentTimer = None
    
    def onDebug(self, DebugEvent):
        self.Debug = DebugEvent.DebugMode
        self.DebugExtreme = DebugEvent.DebugExtreme

Zero.RegisterComponent("TimeWaitManager", TimeWaitManager)