#//////////////////////////////////////////////////////////////////////////////
#// \file FieldActions.py
#// Auto-Generated State Machine file.
#//////////////////////////////////////////////////////////////////////////////
import Zero
import Events
import Property
import VectorMath
import Keys
import types
import Color
import DebugDraw
import math

# Typedefs
Vec2 = VectorMath.Vec2;
Vec3 = VectorMath.Vec3;
Vec4 = VectorMath.Vec4;
Quat = VectorMath.Quat;

class State:
    def __init__(self):
        self.StateEvents = {};
        self.EventEdges = {};
        self.Edges = [];
        self.Name = "";

class Edge:
    def __init__(self):
        self.FromState = "";
        self.ToState = "";
        self.Name = "";

class FieldActions:
    Debugging = Property.Bool(False);

    def __init__(self):
        # Default the current state to nothing
        self.CurrentState = None;
        self.States = {};
        self.ConnectMap = {};
        
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate);

        # Add States
        self.AddState("Sunny", self.SunnyState());
        self.AddState("Rainy", self.RainyState());
        self.AddState("Dry", self.DryState());

        # Add Edges
        self.AddEdge("Sunny", "Rainy", self.SunnyToRainy());
        self.AddEdge("Rainy", "Dry", self.RainyToDry());
        self.AddEdge("Dry", "Sunny", self.DryToSunny());
        self.AddEdge("Rainy", "Sunny", self.RainyToSunny());
        self.AddEdge("Dry", "Rainy", self.DryToRainy());
        self.AddEdge("Sunny", "Dry", self.SunnyToDry());

        # Set the starting state
        self.ChangeState("Sunny");
    
    ################################################################################### States
    # Sunny
    class SunnyState(State):
        # Called once when the object is created        def Initialize(self, FieldActions):            #FieldActions.ConnectState(FieldActions.Space, Events.LogicUpdate, self.OnLogicUpdate);            pass                # Called once when entering the state        def OnEnter(self, FieldActions):            FieldActions.Owner.Sprite.Color = Color.Gold            pass                # Called every frame while in this state        def OnLogicUpdate(self, FieldActions, UpdateEvent):            pass                # Called once when exiting this state        def OnExit(self, FieldActions):            pass
    # Rainy
    class RainyState(State):
        # Called once when the object is created        def Initialize(self, FieldActions):            #FieldActions.ConnectState(FieldActions.Space, Events.LogicUpdate, self.OnLogicUpdate);            pass                # Called once when entering the state        def OnEnter(self, FieldActions):            pass                # Called every frame while in this state        def OnLogicUpdate(self, FieldActions, UpdateEvent):            pass                # Called once when exiting this state        def OnExit(self, FieldActions):            pass
    # Dry
    class DryState(State):
        # Called once when the object is created        def Initialize(self, FieldActions):            #FieldActions.ConnectState(FieldActions.Space, Events.LogicUpdate, self.OnLogicUpdate);            pass                # Called once when entering the state        def OnEnter(self, FieldActions):            pass                # Called every frame while in this state        def OnLogicUpdate(self, FieldActions, UpdateEvent):            pass                # Called once when exiting this state        def OnExit(self, FieldActions):            pass


    #################################################################################### Edges
    # SunnyToRainy
    class SunnyToRainy(Edge):
        def Initialize(self, FieldActions):            FieldActions.ConnectEdge(FieldActions.Space, Events.LogicUpdate, self.OnLogicUpdate);                def OnLogicUpdate(self, FieldActions, OnLogicUpdate):            return Zero.Keyboard.KeyIsDown(Keys.Left);
    # RainyToDry
    class RainyToDry(Edge):
        def Initialize(self, FieldActions):            FieldActions.ConnectEdge(FieldActions.Space, Events.LogicUpdate, self.OnLogicUpdate);                def OnLogicUpdate(self, FieldActions, OnLogicUpdate):            return Zero.Keyboard.KeyIsDown(Keys.Left);
    # DryToSunny
    class DryToSunny(Edge):
        def Initialize(self, FieldActions):            FieldActions.ConnectEdge(FieldActions.Space, Events.LogicUpdate, self.OnLogicUpdate);                def OnLogicUpdate(self, FieldActions, OnLogicUpdate):            return Zero.Keyboard.KeyIsDown(Keys.Left);
    # RainyToSunny
    class RainyToSunny(Edge):
        def Initialize(self, FieldActions):            FieldActions.ConnectEdge(FieldActions.Space, Events.LogicUpdate, self.OnLogicUpdate);                def OnLogicUpdate(self, FieldActions, OnLogicUpdate):            return Zero.Keyboard.KeyIsDown(Keys.Left);
    # DryToRainy
    class DryToRainy(Edge):
        def Initialize(self, FieldActions):            FieldActions.ConnectEdge(FieldActions.Space, Events.LogicUpdate, self.OnLogicUpdate);                def OnLogicUpdate(self, FieldActions, OnLogicUpdate):            return Zero.Keyboard.KeyIsDown(Keys.Left);
    # SunnyToDry
    class SunnyToDry(Edge):
        def Initialize(self, FieldActions):            FieldActions.ConnectEdge(FieldActions.Space, Events.LogicUpdate, self.OnLogicUpdate);                def OnLogicUpdate(self, FieldActions, OnLogicUpdate):            return Zero.Keyboard.KeyIsDown(Keys.Left);

    
    ############################################################# State Machine Implementation
    def AddState(self, name, state):
        state.Name = name;
        # Add the state to our dictionary
        self.States[name] = state;
        state.Initialize(self);
    
    def AddEdge(self, fromState, toState, edge):
        # Set the to state
        edge.FromState = fromState;
        edge.ToState = toState;
        edge.Name = fromState + "To" + toState;
        
        # Get the state that we are adding the edge to
        state = self.States[fromState];

        # Add the edge to the state
        state.Edges.append(edge);
        edge.Initialize(self);
    
    def SetupEventConnection(self, target, eventName):
        # We only need to do this once for each event
        if (not(eventName in self.ConnectMap)):
            
            # Create the closure
            def EventResponse(self, event):
                self.RunEvents(eventName, event);
            
            # Create the method object from the closure and ourself
            methodObject = types.MethodType(EventResponse, self)
            
            # Connect the event to the method object
            Zero.Connect(target, eventName, methodObject);
            
            # Store the event in the connect map so that we don't insert again
            self.ConnectMap[eventName] = methodObject;
            
    def RunEvents(self, eventName, event):
        # Attempt to send the event to each outgoing edge of the current state
        if(eventName in self.CurrentState.EventEdges):
            # Test each edge listening to this event
            for edgeTest in self.CurrentState.EventEdges[eventName]:
                # Test the edge
                result = edgeTest(self, event);
                # Get the edge from the method object
                edge = edgeTest.__self__;
                # We need to validate the type of the return
                if(isinstance(result, bool)):
                    # If it did and it was true, we want to go to the next state
                    if(result):
                        self.ChangeState(edge.ToState);
                        return
                # If it wasn't a boolean, we need to throw an exception
                else:
                    raise Exception("The return type of edge '" + edge.Name + "' is not a Boolean (True/False)");
        
        # Attempt to send the event to the active state
        if(eventName in self.CurrentState.StateEvents):
            for stateEvent in self.CurrentState.StateEvents[eventName]:
                stateEvent(self, event);

    def ChangeState(self, stateName):
        # Call exit on the previous state
        if(self.CurrentState and self.CurrentState.OnExit):
            self.CurrentState.OnExit(self);
        
        # Change states to the new state
        self.CurrentState = self.States[stateName];
        
        # Call Enter on the new state
        if(self.CurrentState.OnEnter):
            self.CurrentState.OnEnter(self);

    def ConnectState(self, target, eventName, methodObject):
        # Set up the event connection
        self.SetupEventConnection(target, eventName);
        
        # We need to pull the state object from the method object
        state = methodObject.__self__;
        
        # If we haven't connected to this event yet, create the array entry
        if(not eventName in state.StateEvents):
            state.StateEvents[eventName] = [];
        
        # Add this method to get called when the event is sent to this state
        state.StateEvents[eventName].append(methodObject);

    def ConnectEdge(self, target, eventName, methodObject):
        # Set up the event connection
        self.SetupEventConnection(target, eventName);
        
        # We need to pull the edge object from the method object
        edge = methodObject.__self__;
        
        # Grab the state that the edge is leaving from
        state = self.States[edge.FromState];
        
        # If we haven't connected to this event yet, create the array entry
        if(not eventName in state.EventEdges):
            state.EventEdges[eventName] = [];
        
        # Add this method to get called when the event is sent to this state
        state.EventEdges[eventName].append(methodObject);
    
    def OnLogicUpdate(self, UpdateEvent):
        if(self.Debugging and self.CurrentState):
            StateMachine = Zero.GetResource("524705e5f6e79b68:FieldActions");
            StateMachine.SetDebugInfo(self.Owner.Name, self.CurrentState.Name);
            
# Register the component
Zero.RegisterComponent("FieldActions", FieldActions)