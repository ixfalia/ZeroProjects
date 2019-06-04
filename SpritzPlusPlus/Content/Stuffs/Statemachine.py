import Zero

# Used to determine when to switch between states
class Edge:
    def __init__(self, toState, condition):
        self.ToState = toState;
        self.Condition = condition;

class StateMachine:
    def __init__(self):
        # Default the current state to nothing
        self.CurrentState = None;
        
    def Initialize(self, initializer):
        # We want to get an update every frame
        Zero.Connect(self.Space, "LogicUpdate", self.OnUpdate);
        
    def OnUpdate(self, UpdateEvent):
        # Do nothing if the starting state was not set
        if(self.CurrentState == None):
            return;
           
        # Check all edges to see if we need to change state
        self.CheckEdgeConditions();
        
        # Update the current state
        self.CurrentState.OnUpdate(self.Owner, UpdateEvent.Dt);
        
    def CheckEdgeConditions(self):
        # Walk each edge on the current state
        for edge in self.GetEdges(self.CurrentState):
            # If the edge condition passes
            if(edge.Condition(self.Owner)):
                # Call the on exit of the current state
                self.CurrentState.OnExit(self.Owner);
                # Set the current state to the state that the edge is pointing to
                self.CurrentState = self.GetState(edge.ToState);
                # Call the on enter of the new state
                self.CurrentState.OnEnter(self.Owner);
                # No need to continue iterating
                break;
        
    def AddState(self, stateName, state):
        # Add the state to our dictionary
        self.__dict__["S_" + stateName] = state;
        # Add edges to the dictionary of the state
        state.__dict__["E_Edges"] = [];
    
    def AddEdge(self, fromState, toState, condition):
        # Get the state that we are adding the edge to
        state = self.GetState(fromState);
        # Create the edge
        newEdge = Edge(toState, condition);
        # Add the edge to the state
        self.GetEdges(state).append(newEdge);
        
    def SetStartingState(self, stateName):
        # Get the state and set it as the current state
        self.CurrentState = self.GetState(stateName);
        # Call OnEnter on the starting state
        self.CurrentState.OnEnter(self.Owner);
    
    def GetEdges(self, state):
        # The edges are stored in the dictionary of the state
        return state.__dict__["E_Edges"];
    
    def GetState(self, stateName):
        # The state is stored on our dictionary
        return self.__dict__["S_" + stateName];

# Register the component so that it can be added to objects in the engine
Zero.RegisterComponent("myStateMachine", StateMachine)