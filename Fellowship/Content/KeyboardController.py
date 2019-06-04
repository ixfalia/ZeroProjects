import Zero
import Events
import Property
import VectorMath

import Action

import random

Keys = Zero.Keys
Keyboard = Zero.Keyboard

InputActions = Property.DeclareEnum("InputActions", ["MoveUp", "MoveDown", "MoveLeft", "MoveRight", "ActivateKey", "GiveKey", "TakeKey", "FireKey", "CheatGhost", "CheatSkipForwards", "CheatSkipBackwards"])

class KeyboardController:
    KeyStatus = {}
    def DefineProperties(self):
        self.Active = Property.Bool(default = True)
        self.Debug = Property.Bool(default = True)
        pass

    def Initialize(self, initializer):
        self.setupKeyStatus()
        
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        pass

    def OnLogicUpdate(self, UpdateEvent):
        self.checkKeyboard()
        self.evaluateKeyboard()
    
    def checkKeyboard(self):
        self.setKeyStatus(InputActions.MoveUp, Keyboard.KeyIsDown(Keys.W))
        self.setKeyStatus(InputActions.MoveDown, Keyboard.KeyIsDown(Keys.S))
        self.setKeyStatus(InputActions.MoveLeft, Keyboard.KeyIsDown(Keys.A))
        self.setKeyStatus(InputActions.MoveRight, Keyboard.KeyIsDown(Keys.D))
        
        self.setKeyStatus(InputActions.ActivateKey, Keyboard.KeyIsPressed(Keys.Space))
        #self.setKeyStatus(InputActions.TakeKey, Keyboard.KeyIsPressed(Keys.E))
        #self.setKeyStatus(InputActions.GiveKey, Keyboard.KeyIsPressed(Keys.R))
        
        #self.setKeyStatus(InputActions.CheatGhost, Keyboard.KeyIsPressed(Keys.Zero))
        #self.setKeyStatus(InputActions.CheatSkipBackwards, Keyboard.KeyIsPressed(Keys.Minus))
        #self.setKeyStatus(InputActions.CheatSkipForwards, Keyboard.KeyIsPressed(Keys.Equal))
    
    def evaluateKeyboard(self):
        if self.getKeyStatus(InputActions.MoveUp):
            #self.Owner.MovementController.moveUp()
            pass
            
        if self.getKeyStatus(InputActions.MoveDown):
            #self.Owner.MovementController.moveDown()
            pass
            
        if self.getKeyStatus(InputActions.MoveLeft):
            #self.Owner.MovementController.moveLeft()
            pass
            
        if self.getKeyStatus(InputActions.MoveRight):
            #self.Owner.MovementController.moveRight()
            pass
        
        if self.getKeyStatus(InputActions.ActivateKey):
            e = Zero.ScriptEvent()
            e.Key = InputActions.ActivateKey
            
            #self.Space.CreateAtPosition("TestBerry", VectorMath.Vec3(-9, 9, 0))
            pass
        
        if self.getKeyStatus(InputActions.CheatSkipForwards):
            children = self.GameSession.PlayerTracker.Camera.Children
            
            for child in children:
                if child.Name == "SoundNode_Rising":
                    #child.SoundEmitter.Volume = 0
                    seq = Action.Sequence(child)
                    Action.Property(seq, child.SoundEmitter, "Volume", 0, 0.5)
                if child.Name == "SoundNode_Critical":
                    #child.SoundEmitter.Volume = 0.3
                    seq = Action.Sequence(child)
                    Action.Property(seq, child.SoundEmitter, "Volume", 0.3, 0.5)
        
        if self.getKeyStatus(InputActions.CheatSkipBackwards):
            children = self.GameSession.PlayerTracker.Camera.Children
            
            for child in children:
                if child.Name == "SoundNode_Rising":
                    #child.SoundEmitter.Volume = 0.3
                    seq = Action.Sequence(child)
                    Action.Property(seq, child.SoundEmitter, "Volume", 0.3, 0.5)
                    
                if child.Name == "SoundNode_Critical":
                    #child.SoundEmitter.Volume = 0
                    
                    seq = Action.Sequence(child)
                    Action.Property(seq, child.SoundEmitter, "Volume", 0, 0.5)
    
    def setupKeyStatus(self):
        for action in InputActions:
            self.KeyStatus[action] = False
        
        #print(self.KeyStatus)
        pass
    
    def setKeyStatus(self, keyAction, state):
        oldStatus = self.KeyStatus[keyAction]
        
        self.KeyStatus[keyAction] = state
        
        if self.Debug and not oldStatus == state:
            print("KeyState Changed: {}: {}".format(keyAction, self.KeyStatus[keyAction]))
    
    def getKeyStatus(self, keyAction):
        return self.KeyStatus[keyAction]

Zero.RegisterComponent("KeyboardController", KeyboardController)