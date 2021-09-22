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

You can review the explanatory API documentation, or learn how to build an FSM quickly with the code generator tool via the **[Workshop Tutorial](#Workshop)**.

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

There is also a simple utility program, **urle.py**, which will decompress an RLE encoded file back to its original size.

Armed with the above information, you are prepped to review [the code](https://github.com/Sultaneous/fsm/blob/master/fsm-rle.py) and see how easy it is to make this slightly more complicated
DFA using the **fsm engine**.


# <a id="Workshop">Step-by-Step Tutorial Workshop for Building FSMs with FSM-GEN</a>
## <a id="info_fsm-gen">FSM-GEN</a>

This section will show how to use the fsm-gen tool.  We will step through an example
state machine for an imaginary protocol; create the corresponding FSM Diagram, 
implement the custom State logic, and build a fully functional FSM program.  
*This section is meant to serve as a hands-on workshop tutorial only.*

The utility fsm-gen.py is a template code generator. It will collect parameters from
you, which it will then use to output a functional Python program.  You will then
need to edit the code template and insert your specific state logic.

This workshop will take you step-by-step through the process of building an FSM
using the Gamzia fsm module.

### STEP 1: Use Case  

For our use case, we will consider a bogus network interaction between computers.
Computers communicate using protocols. We introduce the following simple protocol
and rules, which we will call the MUD (Mislead, Useless Design) Protocol:

**START**  
*Client connects to server.*  
**Server:** HELLO *"Respond with email address"*  
**Client:** *\<email address\>*  
**Server:** DATA *"Ready to receive"  
**Client:** *\<any data\>*  
**Server:** BYE *\<client email\>*  
**END**  

### STEP 2: Describe the states 

**INIT_STATE**
- sets @email to "Unknown"
- sets @errors to 0
- sets @maxerrors to 3
- sets @data o ""
- Triggers on completion, transitions to HELLO_STATE


**HELLO_STATE**
- prints "HELLO 'Respond with email address'"
- gets input into @email
- rough validates @email value
- Trigger: bad email, transitions to INVALID_EMAIL_STATE
- Trigger: good email, transitions to DATA_STATE


**INVALID_EMAIL_STATE**
- reports invalid email, counts errors
- increments @errors 
- Trigger: if @errors >= @maxerrors, transitions to TERMINATION_STATE
- else transitions: HELLO_STATE


**DATA_STATE**
- prints "DATA 'Ready to receive'"
- prompts for a line of text data (EOL terminated) input into @data
- Trigger: if bad @data, transition to INVALID_DATA_STATE;
- else, transition to LOG_STATE


**INVALID_DATA_STATE**
- reports invalid, counts instances
- increments errors
- Trigger: if @errors >= @maxerrors, transitions to TERMINATION_STATE
- Transitions to DATA_STATE


**LOG_STATE**
- writes the data to an outfile
- reports results
- Transitions to TERMINATION_STATE


**TERMINATION_STATE**
- prints "BYE '@email'"
- ends / signals FSM to exit


### STEP 3: Create FSM Diagram

The following state diagram visualizes the logic outlined for the use case:

![fsm-mud diagram](https://github.com/Sultaneous/fsm/blob/master/assets/fsm-mud_diagram.png "FSM-MUD Diagram") 

### STEP 4: Run fsm-gen.py

NOTE: The python script fsm-gen.py does not need any command line arguments.
A future version will allow for automation; however at the time of this writing,
the utility program is interactive only.

It will prompt you for information about your FSM and will output a functional
code template.  This template will run immediately, but will not do anything
of significance until you code your own logic into each appropriate state class.

```bash
> python fsm-gen.py
```

To replicate our MUD FSM in fsm-gen, answer the prompts as follows:

```bash
Welcome to FSM Template Generator for the Python FSM module.
By Karim Sultan, September 2021.

This utility will ask a few questions about your DFA / FSM and will generate
a code template.  This is the interactive version.

1. Name of outfile: mud.py
Writing to source file: "mud.py"

2. Number of states? (1-100) 7
Generating 7 states.

3. Would you like to name the states (tag or brief description)? [y/n] <y> y
Name for State 1: INIT_STATE
Name for State 2: HELLO_STATE
Name for State 3: INVALID_EMAIL_STATE
Name for State 4: DATA_STATE
Name for State 5: INVALID_DATA_STATE
Name for State 6: LOG_STATE
Name for State 7: TERMINATION_STATE
The state names are:
INIT_STATE
HELLO_STATE
INVALID_EMAIL_STATE
DATA_STATE
INVALID_DATA_STATE
LOG_STATE
TERMINATION_STATE

4. Will you use command line parameters? [y/n] <y> y
Using command line parameters: True

5. Do you want to show syntax for usage? [y/n] <y> y
Show usage syntax on no parameters: True

6. What is the name of this app?  <Mud>
Using app name of "Mud"

7. What is the author's name? <Unknown> Sultaneous
Using author name of "Sultaneous"

Ready to produce summary.  Hit <enter> to continue... [y] <y> y

8. Summary
App name: "Mud" by "Sultaneous"
Writing to source file: "mud.py"
Generating 7 states.
  1.  State1:   INIT_STATE
  2.  State2:   HELLO_STATE
  3.  State3:   INVALID_EMAIL_STATE
  4.  State4:   DATA_STATE
  5.  State5:   INVALID_DATA_STATE
  6.  State6:   LOG_STATE
  7.  State7:   TERMINATION_STATE
Requires use of command line parameters: True
Show usage syntax when no parameters: True

I am now ready to generate a python code template.
Do you wish me to begin?  [y/n] <y> y
SUCCESS!
```

**NOTES:**  
1. Step 1 is the **file name** of the python file to generate.  If it exists you will be
prompted to allow overwrite.  
2. Step 2 is the **number of states** in our FSM.  The diagram shows 7.  
3. Step 3 allows you to **name the states**.  If you select 'n', then the states are
given unique but generic names.  We will select 'y' as we want to identify our
states as per our diagram.  
    1. We are now **prompted to name each state**; we replicate the names from the
diagram.  
4. The generator can add code to collect the **command line arguments** for us into
argc and args\[\].  We will select yes in case we want to extend this template
further (for example, provide the log file name on the command line).
5. The show syntax option is only available if we choose to use command line
arguments.  It will provide a **blurb on syntax** when the program is executed
without parameters.
6. The **name of the app** is the name of the FSM, set in the context, used by the
engine.
7. Enter **your name**.
8. This is a **summary** step which **reports** what will be built.  **NOTE: the
report will be saved to a file named <outfile.py.report> for later reference.
Answer 'y' to generate the template, or enter 'n' to abort (**all entries will be lost**).
If you enter 'n' you will be asked to confirm.

You can now validate everything worked properly by executing the template:

```bash
> python mud.py

Mud by Sultaneous, September 21, 2021
<Explain purpose>
Syntax: mud.py <mandatory params> ... [optional params] ...
```

Ok, we requested the use of command line arguments, even though we don't really
need them.  So since we didn't provide any, mud just shows the syntax and exits.
We can get around this by giving it a dummy argument.

```bash
> python mud.py dummy_parameter

Currently in INIT_STATE
Currently in HELLO_STATE
Currently in INVALID_EMAIL_STATE
Currently in DATA_STATE
Currently in INVALID_DATA_STATE
Currently in LOG_STATE
Currently in TERMINATION_STATE
SUCCESS!
```

That's better.  This time, the state machine was executed, and the default
behaviour of each generated template is to just report its state name, and then
proceed to the next state.  This has the effect of enumerating our states,
but it doesn't do anything useful yet.

### STEP 5: Add Your Logic

The last step is for us to edit the code template and fill in our logic.  We
will do this in a state-by-state basis. Our first state's humanly readable label
is "*INIT_STATE*", but its class name is **State1**.  The remaining states are classes
**State2** through **State7**.  The code for each class contains their name so we don't
get confused.  We can also refer to the report generated by fsm-gen.  

Finally, the generator will create a useful table called **states** which is a 
dictionary that maps the humanly readable name to its class name.  This way one
can refer to states using the human labels:

```python
   states={}
   states['INIT_STATE'] = "State1"
   
   # Setting State by Class name
   context.setNextState("State1")
   
   # Setting State by Human Label
   context.setNextState(states["INIT_STATE"])
```
 #### State1: INIT_STATE
 
 The INIT_STATE sets up some variables in the context.  These will be shared
 between multiple states.
 
 ```python
 class State1(State):
   def __init__(self, stateName):
      super().__init__("INIT_STATE")

   def run(self, context):
      # Initialize context properties
      context.set("email", "Unknown")
      context.set("errors", 0)
      context.set("maxErrors", 3)
      context.set("data", "")
      context.set("outfile", "mud.tmp")

      # Set the next state based on triggers/transitions
      context.setNextState(states["HELLO_STATE"])

# End of class State1
 ```
 
 - "email" is given a temporary value in case FSM terminates early
 - once our required shared variables are initialized, we transition automatically
 to **HELLO_STATE** (as per the diagram).
 
 #### State2: HELLO_STATE
 
 The **HELLO_STATE** issues the HELLO protocol command, and reads input. It also
 performs a poor-man's "validation" of the email.
 
 ```python
 class State2(State):
   def __init__(self, stateName):
      super().__init__("HELLO_STATE")

   def run(self, context):
      # Issue HELLO <msg>
      print("HELLO \"Respond with email\"")
      email=input("> ")

      # Set the next state based on triggers/transitions
      # Poor man's validation / for demo purpose only
      if (not '@' in email) or (not '.' in email):
         context.setNextState(states["INVALID_EMAIL_STATE"])
      else:
         # Ensure we reset error counter
         context.set("errors", 0)
         context.set("email", email)
         context.setNextState(states["DATA_STATE"])

# End of class State2
```

- if email doesn't pass test, then we transition to **INVALID_EMAIL_STATE**
- if email is ok, reset error counter, store email, and transition to **DATA_STATE**

#### State3: INVALID_EMAIL_STATE

This state increments the error count and reports it.  If maxErrors is exceeded,
it will terminate (via TERMINATION_STATE).

```python
class State3(State):
   def __init__(self, stateName):
      super().__init__("INVALID_EMAIL_STATE")

   def run(self, context):
      # Count and report
      context.set("errors", context.get('errors')+1)
      print(f"Invalid email, error number {context.get('errors')} of {context.get('maxErrors')}.")

      # Set the next state based on triggers/transitions
      if (context.get('errors')>=context.get('maxErrors')):
         context.setNextState(states["TERMINATION_STATE"])
      else:
         context.setNextState(states["HELLO_STATE"])

# End of class State3

```
- if less than max errors, transitions back to **HELLO_STATE** and repeats.
- if maxErrors (3) exceeded, it transitions to **TERMINATION_STATE**.

#### State 4: DATA_STATE

This state is responsible for collecting, and validating, data from the client.
Data is considered invalid if it is blank or empty.

```python
class State4(State):
   def __init__(self, stateName):
      super().__init__("DATA_STATE")

   def run(self, context):
      # Issue DATA <msg>
      print("DATA \"Respond with text data\"")
      context.set("data", input("> "))
      
      # Set the next state based on triggers/transitions
      if (context.get("data")=="") or (context.get("data").strip()==""):
         context.setNextState(states["INVALID_DATA_STATE"])
      else:
         context.setNextState(states["LOG_STATE"])

# End of class State4
```
- recall the error counter was reset prior to entering this state, so the client
can make up to three mistakes here
- data is empty if it is "" and is blank if it contains only whitespace (we use
str.strip() to test for this)

#### State5: INVALID_DATA_STATE

This state is very similar to **INVALID_EMAIL_STATE**.  For this workshop, we are 
being explicit, but perhaps you can envision how both these states could be
generalized into a single **INVALID_INPUT_STATE**.  There are always multiple ways
to design a DFA.

```python
class State5(State):
   def __init__(self, stateName):
      super().__init__("INVALID_DATA_STATE")

   def run(self, context):
      # Count and report
      context.set("errors", context.get('errors')+1)
      print(f"Invalid data, error number {context.get('errors')} of {context.get('maxErrors')}.")

      # Set the next state based on triggers/transitions
      if (context.get('errors')>=context.get('maxErrors')):
         context.setNextState(states["TERMINATION_STATE"])
      else:
         context.setNextState(states["DATA_STATE"])

# End of class State5
```

- The logic we added here is almost identical to State3 (**INVALID_EMAIL_STATE**)
- If within permitted errors, just loop back to **DATA_STATE** and repeats

#### State6: LOG_STATE

This state writes the data to the file.  We will prefix the data with the email
address so that we know who sent what.  The file name is stored in the context;
it is done this way so that theoretically one could extend this utility to read
the file name from a command line argument.

```python
class State6(State):
   def __init__(self, stateName):
      super().__init__("LOG_STATE")

   def run(self, context):
      # Append data to temp file
      file=open(context.get("outfile"), "a+")
      fmt="[{}] {}\n"
      file.write(str.format(fmt, context.get('email'),
                                 context.get('data')))
      file.close()
      
      # Set the next state based on triggers/transitions
      context.setNextState(states["TERMINATION_STATE"])

# End of class State6
```

- file is opened in 'a' *APPEND* mode, to ensure we collect logs, not overwrite
them
- file is opened with '+' modifier to create it if it doesn't exist
- once we have written out the file, we are done.  Transition automatically
to **TERMINATION_STATE**

#### State7: TERMINATION_STATE

This is the final state - it simply issues a BYE <email> message and then sets
the next state to None.  A None value indicates to the dispatcher to stop processing
and to end the FSM.

```python
class State7(State):
   def __init__(self, stateName):
      super().__init__("TERMINATION_STATE")

   def run(self, context):
      # Issue BYE <email>
      print(f"BYE {context.get('email')}")

      # Set the next state based on triggers/transitions
      context.setNextState(None)

# End of class State7
```

- **That's it!**  We've mapped the entire FSM MUD Diagram into coded states with
transitions.  We should now have a functional state machine.
- run the **mud.py** program to test our logic

#### Execution

Here's some example output (with intentional errors):

```text
> python mud.py

HELLO "Respond with email"
> Sultaneous
Invalid email, error number 1 of 3.
HELLO "Respond with email"
> Sultaneous.com
Invalid email, error number 2 of 3.
HELLO "Respond with email"
> Sultaneous@pythoncoding.ca
DATA "Respond with text data"
> 
Invalid data, error number 1 of 3.
DATA "Respond with text data"
> 		 
Invalid data, error number 2 of 3.
DATA "Respond with text data"
> This is the first data sent under the MUD Protocol FSM!
BYE Sultaneous@pythoncoding.ca
SUCCESS!
```

our log file:

```bash
> cat mud.tmp
[Sultaneous@pythoncoding.ca] This is the first data sent under the MUD Protocol FSM!
>
```

## Conclusion

Some notes:
- State machines are powerful methods of design and implementation
- State machines are not useful for all computer science applications
- State machines can be used in a vast number of scenarios
- The fsm module is a fast and painless way to make state machines of varying 
complexity
- An FSM diagram is an essential design tool for laying out your machine
- From the diagram, you need only code relevant logic for each state.
- The Context class provides a transport layer for stateful, cross-state information
- The Dispatcher class provides a Context driven automation which runs your
machine for you
- The *fsm-gen* utility script will autogenerate a code template for you,
preparing scaffolding for your logic
- The workshop tutorial takes you through the proposal, design, diagramming, and
implementation of an FSM example, showing how easy using the fsm module can be!

- FSM's are fun, powerful, and automated.

