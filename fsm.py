#!/usr/bin/python3

# Finite State Machine (FSM) module by Karim Sultan, August 2021.
# Provides an FSM infrastructure and code-gen utility for fast start.
# See the documentation on github/Sultaneous for details.

# States are stateless, all information for them is contained
# in the context object, which is mainly just a hash map of
# required data, as well as pointers to the current and next state.

import inspect

class Context():
   def __init__(self, contextName):
      self.name = contextName
      self.__dict = dict()
      self.__nextState = None

      # Decorators
      self.push=self.set
      self.put=self.set
      self.peek=self.get
      self.pop=self.get

   def setNextState(self, className):
      if (className==""):
         self.__nextState = None
      else:
         self.__nextState = className

   def getNextState(self):
      return(self.__nextState)

   def set(self, key, value):
      self.__dict[key]=value

   def get(self, key):
      if (key in self.__dict.keys()):
         return (self.__dict[key])
      return (None)

   def delete(self, key):
      if self.exists(key):
         del __dict[key]

   def clear(self):
      self.__dict=dict()

   def getAll(self):
      properties = []
      for key, value in self.__dict.items():
         properties.append(f"'{key}': '{value}'")
      return(properties)

   def count(self):
      return (len(self.__dict))

   def exists(self, key):
      # Returns true if key exists and is not None
      if (key in self.__dict.keys()):
         if (not self.__dict[key]==None):
            return True

      # Key does not exist or is None
      return False

# End of class Context


# THIS CLASS MUST BE DERIVED FROM (EACH FSM STATE)
# This is the "base state" class which all other states are
# derived from, and run() must be overridden.
class State():
   def __init__(self, stateName):
      self.name = stateName;

   # Must be overridend by derived class.
   def run(self, context):
      # This is base class, so simply dump contents
      # of context object.
      print (f"Currently in state {self.name}")
      print ("******************************")
      print (f"Exploring Context: {context.name}")
      print (f"Context Items: {context.count()}")
      for p in context.getAll():
         print (p)
      print ("******************************")

      # Done processing, identify next state if any
      context.setNextState(None)
      print (f"Next state is {context.getNextState()}.")
      return

# End of class State

# This class manages the states.
class Dispatcher:
   # Initiates a state object (each state is stateless and
   # therefore are created/destroyed as required) and passes
   # the context information to it so it can process it.
   def dispatch(self, context):
      # This line needs some explanation.
      # We need the global table to find the state class definitions.
      # However, those are in the calling module, which this module
      # isn't aware of.  So how do we get them?  Well we could pass
      # globals() in as a parameter, but better yet we can derive it
      # from the Python stack using Inspect.  For the stack, [1] is
      # the caller's stack, [0] is the caller's stack frame, and the
      # callers globals are stored in a dictionary called "f_globals".
      # see "inspect" @ https://docs.python.org/3/library/inspect.html
      if context.exists("__NoCaller"):
         caller_globals = globals()
      else:
         caller_globals = dict(inspect.getmembers(inspect.stack()[1][0]))["f_globals"]
      while (context.getNextState()!=None):
         klass = caller_globals[context.getNextState()]
         s=klass(context.getNextState())
         s.run(context)
      return

# End of class Dispatcher

# Demo test code
def main():
   context=Context("FSM")
   context.set("Author", "Karim Sultan")
   context.set("__NoCaller", "True")
   context.setNextState("State")
   dispatcher=Dispatcher()
   dispatcher.dispatch(context)

# End of main

if __name__=="__main__":
   main()
