import Zero
import Events
import Property
import VectorMath

Vec3 = VectorMath.Vec3

class LevelDataUpdater:
    Offset = Property.Vector3(default = Vec3())
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, "LevelDataEvent", self.onLevelData)
        Zero.Connect(self.Space, "FadeEvent", self.onFade)
        
        self.chubby = None
    
    def onLevelData(self, lEvent):
        print("onLevelData startingpos:", self.Owner.Transform.Translation)
        newposition = lEvent.Position + self.Offset
        self.Owner.Transform.Translation = Vec3(newposition.x, newposition.y, -1)
        print("onLevelData nexpos: ", self.Owner.Transform.Translation)
        self.updateData(lEvent.LevelData)
    
    def updateData(self, data):
        #current = data.CurrentLevel
        lData = data
        
        self.Owner.FindChildByName("FlowerFaceIcon").FindChildByName("FlowerPetal").ChangeColor.ChangeColor()
        
        name = self.Owner.FindChildByName("NameText")
        name.SpriteText.Text = lData.LevelName
        
        print("updateData():", lData.LevelName)
        
        fTrack = self.Owner.FindChildByName("FlowerTrack")
        fTrack.SpriteText.Text = "{0} / {1}".format(lData.Flowers, lData.TotalFlowers)
        
        if lData.Flowers >= lData.TotalFlowers:
            myTrans = self.Owner.Transform.Translation
            end = VectorMath.Vec3(myTrans.x, myTrans.y+2, 1)
            print(myTrans, "petal", end)
            self.chubby = self.Space.CreateAtPosition("ChubbyIcon", end)
        #stuff = self.Owner.FindChildByName("TimeTrack")
        #minutes = lData.BestTime 
        #stuff.SpriteText.Text = "{0}".format(lData.BestTime)
        
        stuff = self.Owner.FindChildByName("ScoreTrack")
        stuff.SpriteText.Text = str(int(lData.HighScore)).zfill(5)
        
        self.Owner.Fader.FadeIn()
    
    def onFade(self, fEvent):
        if self.chubby:
            self.chubby.Destroy()
        self.Owner.Fader.FadeOut()

Zero.RegisterComponent("LevelDataUpdater", LevelDataUpdater)