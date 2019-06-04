import Zero
import Events
import Property
import VectorMath

class Wave:
    def __init__(self, timelength = 10, delayafter = 3, Type =  "Stream"):
        from collections import deque
        
        self.Enemies = deque()
        self.TimeLength = timelength
        self.DelayAfter = delayafter
        
        self.time = 0.0
        
    
    #enemies are simply strings carrying the names of the archetypes of the objects they carry
    def addEnemy(self, Enemy, count = 1):
        nuArray = []
        for i in range(count):
            nuArray.append(Enemy)
        
        self.Enemies.append(nuArray)
        #end 
    
    def addTime(self, dt, owner):
        self.time += dt
        
        if len(self.Enemies) <= 0:
            return
        
        if self.time > self.TimeLength / float(len(self.Enemies)):
            self.time = 0
            
            if owner:
                for i in self.Enemies[0]:
                    owner.Space.CreateAtPosition(i, owner.Transform.Translation)
                #end for
            self.Enemies.popleft()
            
            if len(self.Enemies) <= 0:
                self.time = self.getTotalTime()
        #endif 
    #end def
    
    def getTotalTime(self):
        return self.TimeLength + self.DelayAfter
#and class wave

class WaveSpawner:
    def Initialize(self, initializer):
        from collections import deque
        self.Queue = deque()
        self.currentWave = None
        
        self.TotalWaves = 0
        self.WaveCount = 0
        
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        pass
    
    def addWave(self, Wave):
        self.Queue.append(Wave)
        self.TotalWaves += 1
    #end def
    
    def onUpdate(self, Event):
        if len(self.Queue) > 0:
            self.Queue[0].addTime(Event.Dt, self.Owner)
        
            if self.Queue[0].time > self.Queue[0].getTotalTime():
                self.WaveCount += 1
                
                player = self.Space.FindObjectByName("MainCharacter")
                
                E = Zero.ScriptEvent()
                E.Type = ""
                E.String = self.WaveCount
                player.UIMaker.DispatchToHUDSpace("waveCount", E)
                
                self.Queue.popleft()
        #endif 
    #enddef
    
    def getWaveCount(self):
        return self.WaveCount

Zero.RegisterComponent("WaveSpawner", WaveSpawner)