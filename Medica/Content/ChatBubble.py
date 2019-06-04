import Zero
import Events
import Property
import VectorMath

import Color

import collections

Vec2 = VectorMath.Vec2
Vec3 = VectorMath.Vec3
Vec4 = VectorMath.Vec4

class textAttributes:
    def __init__(self, font, size, color):
        self.font = font
        self.size = size
        self.color = color

class chatLine:
    def __init__(self, line, duration, textAtt = None):
        self.line = line
        self.duration = duration
        self.textStyle = textAtt

class ChatBubble:
    Messages = Property.String()
    useTextBlock = Property.Bool(default = False)
    Block = Property.TextBlock()
    
    BubbleColor = Property.Color(default = Color.White)
    TextColor  = Property.Color()
    
    Offset = Property.Vector3(default = Vec3(1, 2, 1))
    WaitForEvent = Property.String(default = Events.LevelStarted)
    
    def Initialize(self, initializer):
        if not self.WaitForEvent == "":
            Zero.Connect(self.Space, self.WaitForEvent, self.onEvent)
        Messages = []
        
        #Type the lines in with the strings and delineate with commas and colons
        #the colons will determine numbers the specify duration
        
        #duration of 0 will wait indefinitely until the player clicks on the bubble
        #it will display a blinking icon that specifies if there's more text
        #If the player clicks on the bubble the text should skip regardless of duration
        #but there should be a minor wait time before this can happen again.
    
    def parseChatText(self):
        line = None
        duration = None
        nuLine = chatLine(line, duration)
    
    def onEvent(self, e):
        pass

Zero.RegisterComponent("ChatBubble", ChatBubble)