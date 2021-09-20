# Gamzia Finite State Machine module for Deterministic Finite Automatons

Finite State Machine engine in Python 3+ with examples. No if/else statements! Class driven.

## Import

To use this module in your Python program, simply import it:

```python
from fsm import *
```

or, if you prefer to be explicit

```python
from fsm import Context, State, Dispatcher
```

## Contents of this project

| Module | Classes | Summary |
| :------ | :------- | :-------|
|[fsm](#info_fsm) | Context, State, Dispatcher | Contains the a DFA engine for Finit State Machines. |
|| Context | Provides a transitory, globally accessible store for state information. |
|| State | A base FSM State class which must be inherited and have its run() method overriden with your logic. |
|| Dispatcher | The actual engine which invokes the correct states to execute the machine. |
|[fsm-demo](#info_fsm-demo) | | A simple code example for using the FSM module. |
|[fsm-rle](#info_fsm-rle) | | A more complex, purposeful example of using the FSM module, which acts as a utility for Run-Length Encoding. |
|[fsm-gen](#info_fsm-gen) | | A powerful command line utility for automatic code template generation for your DFA as an FSM.  |
| urle | | A simple command line utility to expand RLE archives. |

## API Documentation

### <a id="info_fsm">FSM</a>

A Finite State Machine (**FSM**), in Computer Science terms, is a "directed graph".  It is **finite**, as there is a complete path from start to termination.
It is **Stateful** as it consists of a number of states that execute independently until a trigger condition occurs to force a transition to another state.
It is a machine, because a well designed FSM can be given input and run independently.

An FSM is also known as a Deterministic Finite Automaton (**DFA**). It is deterministic, because when given the same input it will always produce the same
output (randomness aside).  It is finite as per above.  And it is an automaton, which is another name for automatic machine.

#### FSM Module

The FSM module is a complete engine for creating and executing FSMs.  It restricts state scope to local, with the exception of a **Context** object,
which is responsible for making shared information accessible.  It uses a base **State** Class, which provides a method (**run()**) to be overridden, 
to contain your specific state logic. And it is an automated machine, providing a **Dispatcher** class, which controls State transitions, instantiates
desired states, and monitors progress until completion.

Using the FSM module is simple.

#### Part 1 -> Create an FSM Diagram
Before starting to code, you should create a diagram containing each state, their triggers and which states they transition to.

![Example FSM Diagram](https://github.com/Sultaneous/fsm/blob/master/assets/example_FSM_diagram.png "Example FSM Diagram")

#### Part 2 -> Convert FSM Diagram to code
1. You create a class based on **State** base class:
```python
class MyState(State):
```

2. You call the base constructor with your State's  **plain-language label** (meant for ease of reference):
```python
   def __init__(self, stateName):
      super().__init__(stateName)
```

2. You **override the run() function** and provide your logic for this specific state:
```python
   def run(context):
      # TODO: Replace this with your logic
      print()
      print(f"Currently in {self.name}")
```

3. Still in **run()**, you add your triggers and the appropriate state to transition to:
```python
      # Example only
      if (input=""):
         context.setNextState("STATE_END_OF_FILE")
      else:
         context.setNextState("STATE_PARSE_LABEL")
```

**Example State Class**
```python
class State1(State):
   def __init__(self, stateName):
      super().__init__(stateName)

   def run(self, context):
      print()
      print(f"Currently in {self.name}")
      super().run(context)
      context.setNextState("State2")

      print (f"Next state is {context.getNextState()}.")
# End of class State1
```

#### Part 3 -> 5 Step Main()
Starting the FSM is simple.  There are 5 required steps:
1. Create the context object.  Populate it with any required initial values.
```python
def main():
   # 1. Create our context 
   context = Context("MyApp")
   # Populate it with any initial values
   context.set("infile", "data.txt")
   context.set("outfile", "temp.out")
   context.set("property", "value")
```

2. Name the initial (starting) state:
```python
   # 2. Identify the first state to instantiate
   context.setNextState("MyStartState")
```

3. Create a dispatcher object.
```python
   # 3. Create our dispatcher
   dispatcher = Dispatcher(context)
```

4. Execute our dispatcher, starting and running the state machine to completion; note we must pass it our current context.
```python
   # 4. dispatcher.dispatch(context)
```

5. We're done, report any exit message
```python
   # 5. Done
   print ("SUCCESS!")
```

**Example main() function**
```python
# Only five steps are needed to run the FSM.
def main():
   # 1. Create our context
   context=Context("FSM")
   # (Populate it with some dummy values for this test)
   context.set("Module", "FSM")
   context.set("Counter", 0)

   # 2. Identify the first state to instantiate
   context.setNextState("State1")

   # 3. Create our dispatcher
   dispatcher=Dispatcher()

   # 4. Dispatch! This executes the FSM
   dispatcher.dispatch(context)

   # 5. Done
   print("SUCCESS!")
# End of main

if __name__=="__main__":
   main()
```

#### Code Template Generation
If you are creating FSMs, it is highly recommended you use the [fsm-gen](#info_fsm-gen) utility. It will build the scaffolding and you will need only to
enter your state logic in each appropriate derived State class. It is recommended to use the fsm-gen tool once you have completed your FSM diagram.

### <a id="info_fsm-demo">FSM</a>

**TODO: Add documentation for FSM here**

### <a id="info_fsm-rle">FSM</a>

**TODO: Add documentation for FSM here**

### <a id="info_fsm-gen">FSM</a>

**TODO: Add documentation for FSM here**


