import Zero
import Events
import Property
import VectorMath

class timer:
    track = 0
    def __init__(self, name, count, function, isRepeat):
        #print( "timer.constructor", name, count, function, isRepeat)
        self.name = name
        self.count = count
        self.fnc = function
        self.isRepeat = isRepeat
        self.Active = True
    
    def updateTime(self, dt):
        self.track += dt
    
    def Broadcast(self,other):
        print("timer.Broadcast: My Time is UP!")
        timerEvent = Zero.ScriptEvent()
        other.Owner.DispatchEvent(self.name, timerEvent)
    #end def Broadcast
#end class timer

class Timer:
    DebugMode = Property.Bool(default = True)
    
    
    def Initialize(self, initializer):
        self.Registry = {}
        self.RemoveRegistry = {}
        self.Time = 0
        
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        #Zero.Connect(self.Space, Events.LevelStarted, self.onLevelStart)
        
    
    def onLevelStart(self, Event):
        pass
    
    def onUpdate(self, Event):
        if not self.Owner:
            self.Registry.clear()
        
        #if len(self.RemoveTRegistry)
        self.Time += Event.Dt
        removeList = {}
        if self.DebugMode:
            print(self.Owner.Name, self.Registry)
            pass
        if len(self.RemoveRegistry) > 0:
            for i in self.RemoveRegistry:
                self.Registry.pop(i)
            self.RemoveRegistry.clear()
        
        for i in self.Registry:
            if not self.Registry[i].Active:
                continue
            
            self.Registry[i].updateTime(Event.Dt*1.4)
            
            e = self.Registry[i]
            if self.DebugMode:
                print(self.Owner.Name, "Timer.onUpdate()", Event.Dt, "timer current track", e.track, "count:", e.count)
                pass
            if e.track >= e.count:
                if self.DebugMode:
                    #print(self.Owner.Name, "Timer: ", e.name, "Called")
                    pass
                if not e.fnc:
                    e.Broadcast(self)
                else:
                    e.fnc()
                #endif
                
                if e.isRepeat:
                    e.track = 0
                    pass
                else:
                    removeList[e.name] = True
                #endif
            #endif
        #end for
        
        for i in removeList:
            self.removeTimer(i)
    #end def
    
    def registerTimer(self, name, count, function, isRepeat):
        if name in self.Registry:
            print("Name,", name, "already exists in registry! Original Being overwritten!")
            #raise
        
        nuTimer = timer(name, count, function, isRepeat)
        self.Registry[name] = None
        self.Registry[name] = nuTimer
        
        if self.DebugMode:
            print(self.Owner.Name, "timer.registerTimer()", name, "timer registered.")
            print("timer data:", count, function, isRepeat)
            print("registry@:", self.Registry)
    
    def removeTimer(self, name):
        if name in self.Registry:
            if self.DebugMode:
                print("timer.RemoveTimer() Removing Timer: ", name)
            #del self.Registry[name]
            timer = self.Registry[name]
            timer.Active = False
            self.RemoveRegistry[name] = name
    #enddef
    
    def removeTimerDelayed(self, name):
        if name in self.Registry:
            if self.DebugMode:
                print("timer.RemoveTimer() Removing Timer: ", name)
            #del self.Registry[name]
            self.RemoveList[name]
    #enddef
    
    def EventBase(self, name):
        myEvent = Zero.ScriptEvent()
        self.Owner.DispatchEvent(name+"Timer", myEvent)

Zero.RegisterComponent("Timer", Timer)