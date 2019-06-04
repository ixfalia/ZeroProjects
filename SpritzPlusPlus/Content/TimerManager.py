import Zero
import Events
import Property
import VectorMath

def emptyCall():
    pass
#enddef

class Timer:
    Lifetime = 0
    Lifelimit = 0
    Name = ""
    Call = emptyCall
    
    def addTime(self, time):
        self.Lifelimit += time
    #enddef()
#end class

#This class handles timer events and makes the necessary callbacks.
class TimerManager:
    DebugMode = Property.Bool( default = False )
    Timers = []
    Lifetime = 0
    
    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        pass
    #enddef()
    
    def onUpdate(self, Event):
        self.Lifetime += Event.Dt
        
        for T in self.Timers:
            T.Lifetime += Event.Dt
            
            if( T.Lifetime >= T.Lifelimit ):
                print(T.Lifetime, " is greater than", T.Lifelimit)
                if( T.Call ):
                    print("called")
                    T.Call()
                #endif
                
                self.Timers.remove(T)
            #endif
        #endfor
    #enddef()
    
    def addTimerObj(self, timer):
        self.Timers.append(timer)
    #enddef()
    
    def addTimer(self, name, Lifelimit, Call ):
        nuTimer = Timer()
        
        nuTimer.Lifelimit = Lifelimit
        nuTimer.Name = name
        nuTimer.Call = Call
        
        self.Timers.append(nuTimer)
    #enddef()
#end Class

Zero.RegisterComponent("TimerManager", TimerManager)