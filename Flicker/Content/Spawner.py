import Zero
import Events
import Property
import VectorMath

class Spawner:
    DebugMode = Property.Bool(default = False)
    SpawnSpeed = Property.Float(default = 10)
    DelayBetweenSpawns = Property.Float(default = 3)
    SpawnLimit = Property.Int(default = -1)
    isActive = Property.Bool(default = True)
    
    SpawnCount = 0
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevelStart)
        if not self.isActive:
            return
        
        print("Spawner.Initialize()")
        
        #self.Owner.Timer.registerTimer(self.Owner.Name+"Timer", self.SpawnSpeed, self.spawn, True)
        
        
    
    def onLevelStart(self,Event):
        #test code!
        from WaveSpawner import Wave
        #wave 1
        nuWave = Wave(8)
        nuWave.addEnemy("BasicEnemy", 2)
        nuWave.addEnemy("BasicEnemy",1)
        
        self.Owner.WaveSpawner.addWave(nuWave)
        
        nuWave = Wave(8)
        nuWave.addEnemy("BasicEnemy", 1)
        nuWave.addEnemy("BasicEnemy",2)
        nuWave.addEnemy("BasicEnemy", 1)
        
        self.Owner.WaveSpawner.addWave(nuWave)
        
        #wave 2
        nuWave = Wave(15)
        nuWave.addEnemy("BasicEnemy", 2)
        nuWave.addEnemy("BasicEnemy", 3)
        
        self.Owner.WaveSpawner.addWave(nuWave)
        
        nuWave = Wave(3)
        self.Owner.WaveSpawner.addWave(nuWave)
        
        nuWave = Wave(8)
        nuWave.addEnemy("Speedy", 2)
        nuWave.addEnemy("Speedy", 1)
        nuWave.addEnemy("Speedy", 2)
        self.Owner.WaveSpawner.addWave(nuWave)
        
        nuWave = Wave(8)
        nuWave.addEnemy("Speedy", 2)
        nuWave.addEnemy("BasicEnemy", 2)
        nuWave.addEnemy("Speedy", 2)
        self.Owner.WaveSpawner.addWave(nuWave)
        
        nuWave = Wave(12)
        nuWave.addEnemy("BasicEnemy", 2)
        nuWave.addEnemy("Speedy", 2)
        nuWave.addEnemy("BasicEnemy", 2)
        nuWave.addEnemy("Speedy", 1)
        nuWave.addEnemy("BasicEnemy", 1)
        
        self.Owner.WaveSpawner.addWave(nuWave)
        
        #wave 3
        nuWave = Wave(15)
        nuWave.addEnemy("Speedy", 3)
        nuWave.addEnemy("BasicEnemy", 2)
        nuWave.addEnemy("BasicEnemy", 2)
        nuWave.addEnemy("Speedy", 4)
        nuWave.addEnemy("BasicEnemy", 2)
        nuWave.addEnemy("Speedy", 2)
        
        self.Owner.WaveSpawner.addWave(nuWave)
        
        #wave 4
        nuWave = Wave(8)
        nuWave.addEnemy("BigGuy", 2)
        
        self.Owner.WaveSpawner.addWave(nuWave)
        
        nuWave = Wave(8)
        nuWave.addEnemy("BasicEnemy", 2)
        nuWave.addEnemy("BigGuy", 2)
        nuWave.addEnemy("BasicEnemy", 1)
        
        self.Owner.WaveSpawner.addWave(nuWave)
        
        self.WaveCount = self.Owner.WaveSpawner.WaveCount
        self.TotalWaves = self.Owner.WaveSpawner.TotalWaves
        player = self.Space.FindObjectByName("MainCharacter")
        
        myEvent = Zero.ScriptEvent()
        myEvent.Type = ""
        myEvent.String = "/ " + str(int(self.TotalWaves))
        myEvent.Function = None
        
        player.UIMaker.DispatchToHUDSpace("waveTotal", myEvent)
        
        myEvent = Zero.ScriptEvent()
        myEvent.Type = ""
        myEvent.String = int(self.WaveCount)
        myEvent.Function = None
        
        player.UIMaker.DispatchToHUDSpace("waveCount", myEvent)
    #endef
    def spawn(self):
        print("Spawn")
        if not self.isActive:
            return
        if not self.SpawnLimit == -1 and self.SpawnCount >= self.SpawnLimit:
            self.isActive = False
            self.Owner.Timer.removeTimer(self.Owner.Name+"Timer")
            return
        
        self.Space.CreateAtPosition("BasicEnemy", self.Owner.Transform.Translation)
        self.SpawnCount += 1
        
        
#end class


Zero.RegisterComponent("Spawner", Spawner)