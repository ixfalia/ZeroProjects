import Zero
import Events
import Property
import VectorMath

import myCustomEnums
import math
import Action
import random

Vec2 = VectorMath.Vec2
Vec3 = VectorMath.Vec3
sproutTypes = myCustomEnums.sproutTypes
sproutList = myCustomEnums.sproutList

class ColorDataGrid:
    Debug = Property.Bool(default = True)
    limitGrid = Property.Bool(default = False)
    gridLimit = Property.Enum(enum = sproutTypes)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, "GridEvent", self.onGrid)
        Zero.Connect(self.Space, "PlaceFlower", self.onPlaceFlower)
        Zero.Connect(self.Space, "RemoveFlower", self.onRemoveFlower)
        
        self.rows = self.Owner.GridManager.rows
        self.cols = self.Owner.GridManager.cols
        self.currentComboRow = 0
        self.currentComboColumn = 0
        self.currentComboValue = 0
        #self.currentComboChain = []
        self.grids = {}
        self.createGrids()
    
    def createGrids(self):
        for sprout in sproutTypes:
            self.grids[sprout] = [[0 for col in range(0,self.cols)] for row in range(0,self.rows)]
            #self.printGrid(sprout)
        
        #self.grids["delete"] = [[0 for col in range(0,self.cols)] for row in range(0,self.rows)]
    
    def printGrid(self, type):
        if type == sproutTypes.blank:
            return
        if self.Debug:
            print("ColorDataGrid.printGrid():")
            print('\t===== {0} ====='.format(type))
        for row in self.grids[type]:
            print("\t\t", row)
            #print("\t", self.grids[0][0])
            pass
    
    def onGrid(self, gEvent):
        if not gEvent.Archetype == "Sprout":
            return
        #print("onGrid() Type:",gEvent.Type)
        if not gEvent.FlowerType == sproutTypes.blank:
            self.placeFlower(gEvent.Position.x, gEvent.Position.y, gEvent.FlowerType)
        else:
            self.removeFlower(gEvent.Position.x, gEvent.Position.y, gEvent.OldType)
        
        #self.printGrid(gEvent.FlowerType)
        pass
    
    def onPlaceFlower(self, fEvent):
        self.placeFlower(gEvent.Position.x, gEvent.Position.y, gEvent.FlowerType)
    
    def onRemoveFlower(self, fEvent):
        self.removeFlower(gEvent.Position.x, gEvent.Position.y, gEvent.FlowerType)
    
    def placeFlower(self, row, column, type):
        row = round(row)
        column = round(column)
        
        if self.Debug:
            print("ColorDataGrid().placeFlower()")
            print("\tPlacing", type, "flower at: Row:", row, "Column:", column)
            pass
        #endif
        isCombo = False
        self.currentComboRow = 0
        self.currentComboColumn = 0
        self.currentComboValue = 0
        
        self.grids[type][row][column] += 4
        isCombo = self.checkForAdjacentFlower(row, column, type)
        
        if not row+1 >= self.rows:
            self.grids[type][row+1][column] += 1
            isCombo = isCombo or self.checkForAdjacentFlower(row+1, column, type)
        if not column+1 >= self.cols:
            self.grids[type][row][column+1] += 1
            isCombo = isCombo or self.checkForAdjacentFlower(row, column+1, type)
        if not row-1 < 0:
            self.grids[type][row-1][column] += 1
            isCombo = isCombo or self.checkForAdjacentFlower(row-1, column, type)
        if not column-1 < 0:
            self.grids[type][row][column-1] += 1
            isCombo = isCombo or self.checkForAdjacentFlower(row, column-1, type)
        
        if self.Debug:
            #self.printGrid(type)
            pass
        
        #if type == sproutTypes.rainbow:
        #    for sprouts in sproutTypes:
        #        if sprouts == sproutTypes.rainbow:
        #            continue
        #        print(sprouts)
        #        self.placeFlower(row, column, sprouts)
        
        if isCombo:
            if self.currentComboRow == 0 or self.currentComboColumn == 0:
                #raise
                pass
            #raise
            comboChain = self.recurseSearch(self.currentComboRow, self.currentComboColumn, type)
            
            e = Zero.ScriptEvent()
            e.ChainLength = len(comboChain)
            e.Chain = comboChain
            self.Space.DispatchEvent("ComboEvent",e)
            seq = Action.Sequence(self.Owner)
            Action.Delay(seq, 0.35)
            Action.Call(seq, self.handleComboChain, (comboChain,type))
            #self.handleComboChain(comboChain,type)
        else:
            e = Zero.ScriptEvent()
            self.Owner.HUDEventDispatcher.DispatchHUDEvent("NoComboEvent", e)
            self.Space.DispatchEvent("NoComboEvent",e)
    
    def checkForAdjacentFlower(self, row, column, type):
        if not type == sproutTypes.rainbow:
            value = self.grids[type][row][column] + self.grids[sproutTypes.rainbow][row][column]
        else:
            value = self.grids[type][row][column]
            runningTotal = 0
            lastType = type
            
            for sprouts in sproutTypes:
                if sprouts == sproutTypes.rainbow:
                    continue
                compare = value + self.grids[sprouts][row][column]
                
                if compare >= 5:
                    if compare > runningTotal:
                        runningTotal = compare
                        last = sprouts
                #print("Adding to Value: (", value, " + ", self.grids[sprouts][row][column], ")")
            #endfor
            
            value = runningTotal
        #endif
        
        if value > 5:
            if value > self.currentComboValue:
                self.currentComboValue = value
                self.currentComboRow = row
                self.currentComboColumn = column
                
            return True
        #endif
        
        return value > 5
    
    def handleComboChain(self, comboChain, type):
        oneSprout = None
        
        for sproutPos in comboChain:
            sproutRow = round(sproutPos.x)
            sproutColumn = round(sproutPos.y)
            sprout = self.Owner.GridManager.getElement(sproutRow, sproutColumn)
            oneSprout = sprout
            self.handleSprout(sprout)
            #self.printGrid(type)
        
        #choice = random.choice(comboChain)
        #nrow = round(choice.x)
        #ncolumn = round(choice.y)
        #newSeed = self.Owner.GridManager.getElement(nrow, ncolumn)
        #newSeed.Sprout.resetSprout()
        #newSeed.Sprout.randomSprout()
        #newSeed.Sprout.bloomFlower()
        
        if len(comboChain) > 3:
            #oneSprout.SoundEmitter.Pitch = 1 + len(comboChain)/10
            sE = Zero.ScriptEvent()
            sE.Sound = "Combo"
            sE.Pitch = 1 + len(comboChain)/10
            self.Space.DispatchEvent("PlaySoundEvent", sE)
            #raise
            #oneSprout.SoundEmitter.PlayCue("Combo")
        else:
            sE = Zero.ScriptEvent()
            sE.Sound = "Combo"
            #sE.Pitch = 1
            self.Space.DispatchEvent("PlaySoundEvent", sE)
            #raise
        #print("handleComboChain(): Sound Dispatched")
    #endcombologic()
    
    def handleSprout(self, sprout):
        sprout.Sprout.onFullHealth(None)
    
    def removeFlower(self, row, column, type):
        row = round(row)
        column = round(column)
        
        if type == sproutTypes.blank:
            self.clearTable(type)
            return
        
        if self.Debug:
            #print("ColorDataGrid().placeFlower()")
            #print("\tRemoving", type, "flower at: Row:", row, "Column:", column)
            print
        #endif
        
        self.grids[type][row][column] -= 4
        if not row+1 >= self.rows:
            self.grids[type][row+1][column] -= 1
        if not column+1 >= self.cols:
            self.grids[type][row][column+1] -= 1
        if not row-1 < 0:
            self.grids[type][row-1][column] -= 1
        if not column-1 < 0:
            self.grids[type][row][column-1] -= 1
        
        if self.Debug:
            #self.printGrid(type)
            pass
        
        #if type == sproutTypes.rainbow:
        #    for sprouts in sproutTypes:
        #        if sprouts == sproutTypes.rainbow:
        #            continue
        #        print(sprouts)
        #        self.removeFlower(row, column, sprouts)
    
    def recurseSearch(self, row, column, type):
        table = [[False for col in range(0,self.cols)] for row in range(0,self.rows)]
        list = []
        
        self.recurseSearchHelper(row, column, type, table, list)
        return list
    
    def isAlreadyPartOfCombo(self, row, column, list):
        element = Vec2(row,column)
        if element in list:
            return True
        else:
            return False
    
    def recurseSearchHelper(self, row, column, type, table, list):
        #if table[row][column] == True:
        #    return
        
        #table[row][column] = True
        if self.isAlreadyPartOfCombo(row, column, list):
            return
        
        if not type == sproutTypes.rainbow:
            if self.grids[type][row][column] + self.grids[sproutTypes.rainbow][row][column] >= 5:
                list.append(Vec2(row,column))
            #print("ComboChain:")
            #print("\t", list)
            else:
                return
        
        else:#in the case where it is a rainbow
            value = self.grids[type][row][column]
            aType = sproutTypes.rainbow
            check = 0
            for sprouts in sproutTypes:
                if sprouts == sproutTypes.rainbow:
                    continue
                check = value + self.grids[sprouts][row][column]
                
                if check >= 5:
                    aType = sprouts
                    list.append(Vec2(row, column))
                    notherList = self.recurseSearch(row, column, sprouts)
                    
                    list.extend(notherList)
                    
                    print("```````````````````````````````````````````````````````````")
                    print("Added RainbowFlower:", row, column, "To Combo.")
                    #break
                    #raise
                #endif
            #endfor
            return
        #endif
        
        if not row-1 < 0:
            self.recurseSearchHelper(row-1, column, type, table, list)
        if not column-1 < 0:
            self.recurseSearchHelper(row, column-1, type, table, list)
        if not row+1 >= self.rows:
            self.recurseSearchHelper(row+1, column, type, table, list)
        if not column+1 >= self.cols:
            self.recurseSearchHelper(row, column+1, type, table, list)
    
    def clearTable(self, type):
        for i in range(self.rows):
            for k in range(self.cols):
                self.grids[type][i][k] = 0
    
    def printTable(self, table):
        for row in table:
            print("\t", row)

Zero.RegisterComponent("ColorDataGrid", ColorDataGrid)