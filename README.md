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
|| [Context](#info_ContextClass) | Provides a transitory, globally accessible store for state information. |
|| [State](#info_StateClass) | A base FSM State class which must be inherited and have its run() method overriden with your logic. |
|| [Dispatcher](#info_DispatcherClass) | The actual engine which invokes the correct states to execute the machine. |
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

The following diagram is an example only.  Later, we will design a diagram for a basic network handshake protocol, and convert it to an FSM machine
using **fsm-gen**.
![Example FSM Diagram](https://github.com/Sultaneous/fsm/blob/master/assets/example_FSM_diagram.png "Example FSM Diagram")

#### <a id="CodingState">Part 2 -> Convert FSM Diagram to code</a>
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

#### Part 3 -> The 5 Step main()
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

### <a id="info_ContextClass">Context Class</a>

The **Context Class** is used to create context information for the FSM - contextual data for each state, which can be shared with other states.
Each state is considered independent. Persistent (global) information must be passed to it through the context object, which at its core is a dictionary
of properties.

| Method | Alias(es) | Parameters | Returns | Summary |
|:-----|:---------|:--------|:-------|:-------|
| `__init__()` | None | string contextName | Class instance | The default constructor takes one parameter, which is typically the name of the FSM being implemented. |
| `set()` | `push()`, `put()` | string key, var value| nothing | Puts a property (*Key=value*) into the context dictionary. |
| `get()` | `peek()`, `pop()` | string key | value, or *None* | Retrieves key value, if key exists; else returns *None*. |
| `delete()` | None | string key | nothing | If the key exists in dictionary, deletes it (and value). |
| `clear()` | None | None | nothing | Deletes all keys and resets context dictionary to empty. |
| `getAll()` | None | None | string JSON object | Creates a JSON representation of the context properties, if any. |
| `setNextState()` | None | string className | nothing | The name of the class to instantiate and invoke (via *run()*) for the next state. |
| `getNextState()` | None | None | string className | Returns the name of the class for the next state, if any is defined. Should be defined by *setNextState()* first. |
| `count()` | None | None | int numProperties | Returns the number of properties in the context dictionary. Executes *`len(self.__dict`)*. |
| `exists()` | None | string key | boolean doesExist | True if key exists, False otherwise. **NOTE**: Returns True if key exists and value is *None*. |

### <a id="info_StateClass">State Class</a>

The **State Class** is the base class you must:
1. Derive your state class from, and
2. Override the *run()* method, implementing your logic for that state. See [here](#CodingState) for more info.

| Method | Parameters | Returns | Summary |
|:-----|:--------|:-------|:-------|
| `__init__()` | stateName | Class instance | The constructor requires a human readable name for the state, and it must call **super()**.  See [here](#CodingState) for more info. |
| `run()` | Context object | nothing | You must override this function with your logic, and set the next state as required.  See [here](#CodingState) for more info. |

**NOTE:** The property key *`__NoCaller`* is a reserved key and **must not** be used by your program.  It is a boolean directive for the dispatcher, for when
the dispatcher is called from within fsm versus from within your module.

### <a id="info_DispatcherClass">Dispatcher Class</a>

The **Dispatcher Class** is the engine of the FSM, which invokes and switches States as required based on triggers. It has only one method, **dispatch()**,
which must be called with a valid Context object.

| Method | Parameters | Returns | Summary |
|:-----|:--------|:-------|:-------|
| `dispatch()` | Context object | nothing | When provided a valid context object, will determine the correct python pathing to the required derived State class to instantiate, and execute the finite state machine. |

In Python, a module has access to the classes in itself, and any classes it imported. You may wonder, if the fsm module doesn't import your module, how can
it invoke classes from it?  This is indeed the problem, which the dispatcher solves.  We take advantage of the interpreted nature of Python, and use reflection
to examine the module of the calling function.  From this, we can determine a proper Python path to out-of-module State Class, create a reference to it 
(a type of class pointer), and then instantiate the class from this reference:

```python
      if context.exists("__NoCaller"):
         caller_globals = globals()
      else:
         caller_globals = dict(inspect.getmembers(inspect.stack()[1][0]))["f_globals"]
      while (context.getNextState()!=None):
         klass = caller_globals[context.getNextState()]
         s=klass(context.getNextState())
         s.run(context)
      return
```

**NOTE:** As mentioned above, *`__NoCaller`* is a reserved key; if we are invoking *dispatch()* from within the fsm module (done in test cases), then
we can not look for caller class information as there is none and the class is already in scope.

### <a id="info_fsm-demo">FSM</a>

The demo code is a very simplistic FSM meant to show how to use the fsm engine.  It fulfills the following DFA diagram:

![fsm-demo Diagram](https://github.com/Sultaneous/fsm/blob/master/assets/fsm-demo_diagram.png "FSM-Demo Diagram")

#### State1: STATE_SHOWCONTEXT

State1 is as simple a state that we can make.  It overrides *run()* to report what state the machine is in, then calls the *super()* which by default, prints out the contents of the context in JSON format,
and finally, it sets the next state to invoke:

```python
   def run(self, context):
      print()
      print(f"Currently in {self.name}.")
      super().run(context)
      context.setNextState("State2")

      print (f"Next state is {context.getNextState()}.")
```

**NOTE:** When setting the next state, one **must** use the state's Class name, not it's humanly readable state name.  The class name is for the machine; 
while the state name is for your reference.

#### State2: STATE_ITERATE

According to the diagram, State2 is meant to occur three times.  It will go back to State1 each time, until a counter **x** reaches 3, at which point it will
proceed to the end instead.

State objects are scoped **locally**; this means all variables within it are lost when the state transitions to another state.  This is by **design**, as FSMs are not
meant to be **stateful** (ie, States are **stateless** by nature).  To ensure this, the dispatcher creates a **new instance** of the State class each time it is entered.
Any previous instances will be **disposed** of by Python garbage collection.  This also prevents hard to debug programming errors - all settings for a State instance are new each
time it is invoked.

But if States are stateless, how can we count how many iterations State2 has executed?  This is where the **Context** comes in.  We store whatever information
we need to persist within the context. In this case, we store a counter value; we initialize it to `0` if it doesn't already exist (first access) and increment
it by `1` if it does exist:

```python
   if not context.exists("Counter"):
      # First access, create and initialize
      x=0
      context.set("Counter", x)
   else:
      x=context.get("Counter")
      
   # ... do operation
   
   # increment and store for next time
   x+=1
   context.set("Counter", x)
```

Finally, we must clarify which state to transition to on our trigger. According to the diagram, the trigger is based on the value of x:

```python
   # Evaluate x to set next state
   if (x<3):
      context.setNextState(State1)
   else:
      context.setNextState(None)
```

Note that we use the class name, not the humanly readable state name, when setting the next state.  A value of None will cause the state machine to stop
(gracefully).

### <a id="info_fsm-rle">FSM-RLE</a>

The **fsm-rle** utility is a larger example of a slightly more complex, but useful, FSM.  This machine will take a file as input, and will 
Run-Length-Encode (*RLE*) into a *.rle* output file.  There are many different formats of RLE, so we should first look at what format we will
be using.

```C
0x05, 0x41
```

...would represent a *run* of 5 bytes, of decimal value 65, hex $41, which is equivalent to an ASCII 'A'.  This would expand to:

```C
"AAAAA"
```
so every byte in the source file is represented in a tuple of 2 bytes, the *run* and the *control* bytes.

As you can no doubt predict, RLE is a poor compression technique for most data sets such as text, emails, etc... but it has its place in raw graphics data
and even old 6502 memory compression.  However, it is simple to understand, and easy to model in an FSM.

#### Diagram of RLE FSM

The following diagram shows the FSM approach to RLE:

![fsm-rle Diagram](https://github.com/Sultaneous/fsm/blob/master/assets/fsm-rle_diagram.png "FSM-RLE Diagram")

There is also a simple utiltiy program, **urle.py**, which will decompress an RLE encoded file back to its orginal size.

### <a id="info_fsm-gen">FSM-GEN</a>

**TODO: Add documentation for FSM-GEN here**
This section will show how to use the fsm-gen tool.  We will step through an example state machine for an imaginary protocol; create the corresponding
FSM Diagram, implement the custom State logic, and build a fully functional FSM program.  This section is meant to serve as a hands-on workshop tutorial only.

** Part 1 / 3 coming Tuesday Sep 21 **

** Part 2 / 3 coming Thursday Sep 23 **

** Part 3 / 3 coming Saturday Sep 25 **
