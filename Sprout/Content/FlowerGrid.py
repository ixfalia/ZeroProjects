import Zero
import Events
import Property
import VectorMath

import random
import Color
import myCustomEnums

Vec2 = VectorMath.Vec2
Vec3 = VectorMath.Vec3
Vec4 = VectorMath.Vec4

flowerList = myCustomEnums.sproutList
flowerTypes = myCustomEnums.sproutTypes

class FlowerGrid:
    randomFlowers = Property.Bool(default = False)
    flowerTypes = Property.Enum(enum = flowerTypes)
    
    def Initialize(self, initializer):
        self.flowerAmounts = 1 + flowerList.index("blank")
        self.Grid = self.Owner.GridManager.grid
        self.elementSize = self.Owner.Sprite.Size.x*self.Owner.Transform.Scale.x
        self.rows = self.Owner.GridManager.rows
        self.cols = self.Owner.GridManager.cols
        self.groundPlots = [[0 for col in range(0,self.cols)] for row in range(0,self.rows)]
        #self.randomizeGrid()
        self.fillGroundPlots()
        self.fillBlankGrid()
        self.updateGrid()
        self.initializeManipulators()
    #enddef Initialize()
    
    def randomizeGrid(self):
        rows = self.Owner.GridManager.rows
        cols = self.Owner.GridManager.cols
        
        for i in range(rows):
            for k in range(cols):
                randomID = random.choice(flowerList)
                randomElement = self.createFlower(randomID)
                size = randomElement.Sprite.Size.x*randomElement.Transform.Scale.x
                
                randomElement.Sprout.randomSprout()
                randomElement.Transform.Translation = Vec2(k*size, -i*size)
                
                self.Owner.GridManager.pushElement(i,k, randomElement)
            #endfor
        #endfor
        
        self.updateGrid()
        return
    
    def initializeManipulators(self):
        rowNumber = self.Owner.GridManager.rows
        colNumber = self.Owner.GridManager.cols
        
        for row in range(rowNumber):
            element = self.Space.Create("GridManipulator")
            element.GridManipulator.set(self.Owner.GridManager)
            element.GridManipulator.row = row
            element.Transform.RotateAnglesWorld(Vec3(0,0,-1.57))
            self.setPositionBasedOnGrid(row, -1, element)
        #ednfor
        
        for col in range(colNumber):
            element = self.Space.Create("GridManipulator")
            element.GridManipulator.set(self.Owner.GridManager)
            element.GridManipulator.col = col
            element.Transform.RotateAnglesWorld(Vec3(0,0,3.14))
            self.setPositionBasedOnGrid(-1, col, element)
        #dnfor
    #enddef
    
    def updateGrid(self):
        rows = self.Owner.GridManager.rows
        cols = self.Owner.GridManager.cols
        
        for i in range(rows):
            for k in range(cols):
                element = self.Grid[i][k]
                
                #if isinstance(element, (int, float)):
                if not element.Sprout:
                    element = self.createFlower(self, flowerTypes.blank)
                    size = element.Sprite.Size.x * element.Transform.Scale.x
                    self.setPositionBasedOnGrid(i,k, element)
                    
                    self.Grid[i][k] = element
                elif element.Sprout:
                    element.Sprout.updateSprout()
                else:
                    element.Destroy()
                    element = self.createFlower(self, flowerTypes.blank)
                    self.setPositionBasedOnGrid(i,k, element)
                    
                    self.Grid[i][k] = element
                #endif
            #endfor
        #endfor
        
        return
    #enddef
    
    def getArchetype(self, ID):
        #return '{0}Flower'.format(ID)
        return "sproutSeed"
    
    def createFlower(self, ID = "redFlower"):
        ID = self.getArchetype(ID)
        flower = self.Space.Create(ID)
        return flower
    
    def testFunctionality(self):
        self.Grid[0][0].Sprite.Color = Color.Blue
        print(self.Grid[0][0].RuntimeId)
        self.Owner.GridManager.printGrid()
    
    def setPositionBasedOnGrid(self, row, column, element):
        if element.Sprout:
            size = element.Sprite.Size.x * element.Transform.Scale.x
        else:
            size = self.elementSize
        
        nuPosition = Vec2(column*size, -row*size)
        element.Transform.Translation = nuPosition
        #element.Sprout.gridPosition = Vec2(row, column)
        
        return nuPosition
    #enddef
    
    def fillBlankGrid(self):
        rows = self.Owner.GridManager.rows
        cols = self.Owner.GridManager.cols
        
        for i in range(rows):
            for k in range(cols):
                #randomID = random.choice(flowerList)
                randomElement = self.createFlower()
                #size = randomElement.Sprite.Size.x*randomElement.Transform.Scale.x
                size = self.Owner.Sprite.Size.x*self.Owner.Transform.Scale.x
                
                randomElement.Sprout.changeType(flowerTypes.blank)
                randomElement.Sprout.gridPosition = Vec2(i, k)
                randomElement.Transform.Translation = Vec2(k*size, -i*size)
                
                self.Owner.GridManager.pushElement(i,k, randomElement)
            #endfor
        #endfor
        #print("THIS HAPPNED")
    
    def fillGroundPlots(self):
        rows = self.Owner.GridManager.rows
        cols = self.Owner.GridManager.cols
        #size = self.Owner.Sprite.Size
        
        for i in range(rows):
            for k in range(cols):
                #randomID = random.choice(flowerList)
                randomElement = self.Space.Create("GroundPlot")
                size = self.Owner.Sprite.Size.x*self.Owner.Transform.Scale.x
                
                randomElement.Transform.Translation = Vec3(k*size, -i*size, -0.1)
                
                self.groundPlots[i][k] = randomElement
            #endfor
        #endfor
    
    def changeElement(self, row, column):
        randomID = random.choice(flowerList)
        self.Grid[row][column].changeType(randomID)
    
    def applyFunctionToSurrounding(self, row, column, fn):
        if not row-1 < 0:
            flower = self.Grid[row-1][column]
            fn(flower)
        if not column-1 < 0:
            flower = self.Grid[row][column-1]
            fn(flower)
        if not row+1 >= self.rows:
            flower = self.Grid[row+1][column]
            fn(flower)
        if not column+1 >= self.cols:
            flower = self.Grid[row][column+1]
            fn(flower)
        
        if not row-1 < 0 and not column-1 < 0:
            flower = self.Grid[row-1][column-1]
            fn(flower)
        if not row-1 < 0 and not column+1 >= self.cols:
            flower = self.Grid[row-1][column+1]
            fn(flower)
        if not row+1 >= self.rows and not column-1 < 0:
            flower = self.Grid[row+1][column-1]
            fn(flower)
        if not row+1 >= self.rows and not column+1 >= self.cols:
            flower = self.Grid[row+1][column+1]
            fn(flower)
    
    def applyFunctionToSurroundingGroundPlots(self, row, column, fn):
        if not row-1 < 0:
            flower = self.groundPlots[row-1][column]
            fn(flower)
        if not column-1 < 0:
            flower = self.groundPlots[row][column-1]
            fn(flower)
        if not row+1 >= self.rows:
            flower = self.groundPlots[row+1][column]
            fn(flower)
        if not column+1 >= self.cols:
            flower = self.groundPlots[row][column+1]
            fn(flower)
        
        if not row-1 < 0 and not column-1 < 0:
            flower = self.groundPlots[row-1][column-1]
            fn(flower)
        if not row-1 < 0 and not column+1 >= self.cols:
            flower = self.groundPlots[row-1][column+1]
            fn(flower)
        if not row+1 >= self.rows and not column-1 < 0:
            flower = self.groundPlots[row+1][column-1]
            fn(flower)
        if not row+1 >= self.rows and not column+1 >= self.cols:
            flower = self.groundPlots[row+1][column+1]
            fn(flower)
    
    def UpdatePoisonField(self):
        poisonGrid = self.Owner.ColorDataGrid.grids[flowerTypes.poison]
        
        for i in range(self.rows):
            for k in range(self.cols):
                value = poisonGrid[i][k]
                
                if value >= 4:
                    #self.groundPlots[i][k].Sprite.Color = Color.Purple.lerp(Color.White, 0.5)
                    self.groundPlots[i+1][k+1].Sprite.Color = Color.Purple.lerp(Color.White, 0.5)
                    self.groundPlots[i-1][k+1].Sprite.Color = Color.Purple.lerp(Color.White, 0.5)
                    self.groundPlots[i+1][k-1].Sprite.Color = Color.Purple.lerp(Color.White, 0.5)
                    self.groundPlots[i-1][k-1].Sprite.Color = Color.Purple.lerp(Color.White, 0.5)
                elif value > 0:
                    self.groundPlots[i][k].Sprite.Color = Color.Purple.lerp(Color.White, 0.5)
                else:
                    self.groundPlots[i][k].Sprite.Color = Color.White
    
    def placeRandomSeedAround(self, row = None, column = None):
        manip = self.Space.FindObjectByName("LevelSettings").ManipulatorManager
        #table = manip.SpawnRates.runtimeClone()
        #table[
        randomSeed = manip.randomEffect()
    
    def getRandomElement(self):
        row = random.randint(0,self.rows-1)
        col = random.randint(0, self.cols-1)
        
        #if self.Grid[row][col].Sprout.Type == sproutTypes.blank:
        return self.Grid[row][col]
    
    def placeSeed(self, row, column, type = None, overide = False):
        if not type:
            manip = self.Space.FindObjectByName("LevelSettings").ManipulatorManager
            type = manip.randomEffect()
        
        element = self.Grid[row][column]
        
        if element == 0:
            return
        
        if not element.Sprout.Type == flowerTypes.blank and not overide:
            print("[[WARNING]] Attempt to overide existing flower not intended.")
            raise
        else:
            element.Sprout.plantSeed(type)
            return element

Zero.RegisterComponent("FlowerGrid", FlowerGrid)