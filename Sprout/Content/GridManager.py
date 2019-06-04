import Zero
import Events
import Property
import VectorMath

import random

Vec2 = VectorMath.Vec2
Vec3 = VectorMath.Vec3

class GridManager:
    Debug = Property.Bool(default = True)
    rows = Property.Int(default = 5)
    cols = Property.Int(default = 5)
    
    def Initialize(self, initializer):
        #grid = []
        self.grid = [[0 for col in range(0,self.cols)] for row in range(0,self.rows)]
        
        if self.Debug:
            print("GridManager.Initialize(): Grid constructed:")
            self.printGrid()
        #endif
        #self.pushElement(0,1, 13)
        #for i in range(self.rows):
            #self.pushElement(2,i, random.randint(0,50))
        #self.getColumn(2)
        self.printGrid()
    #endef
    
    def pushElement(self, row, col, element):
        if self.Debug:
            print("GridManager.PushElement")
            print("\treplacing element:", self.grid[row][col], "at: (", row, ", ", col, ") with:", element)
        #endif
        
        #self.grid[y*GridSize.x + x] = element
        self.grid[row][col] = element
        
        if self.Debug:
            print("\tElement(", row, ", ", col, ") now has: ", self.grid[row][col])
        
        return self.grid[row][col]
    #enddef
    
    def getRow(self, rowNumber):
        return self.grid[rowNumber]
    
    def getColumn(self, colNumber):
        set = []
        
        #print("rows:", self.rows)
        #print("colNumber:", colNumber)
        
        for i in range(self.rows):
            element = self.grid[i][colNumber]
            
            set.insert(i, self.grid[i][colNumber])
        #endfor
        
        if self.Debug:
            print("GridManager.getColumn():")
            print("\t", set)
        #endif
        
        return set
    #enddef
    
    def getDiagonal(self, position):
        raise
        pass
    
    def getElement(self, row, col):
        return self.grid[row][col]
    
    def printGrid(self):
        if self.Debug:
            print("GridManager.printGrid():")
        for row in self.grid:
            print("\t", row)
            #print("\t", self.grid[0][0])
            pass
    
    def removeRow(self, row):
        pass
    
    def removeCol(self, col):
        pass

Zero.RegisterComponent("GridManager", GridManager)