#!/usr/bin/python3

# A shallow FSM demo which just defines two states,
# and ping-pongs back and forth until State2 has executed
# 3 times. State information to determine when State2 has
# been executed thrice is managed in the context object.
# This is free software, use as you wish.
# August 2021, Karim Sultan
from fsm import *

# This class just reports it's name, calls the parent class
# super function to dump conext, and then sets the next state.
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

# This state uses a key in the context object to manage its
# own state and determine when it has executed three times.
# This may be somewhat contrary to the stateless concept,
# but it's just a demo and shows use of the context object.
class State2(State):
   # We need to call the parent __init__()
   def __init__(self, stateName):
      super().__init__(stateName)

   # We need to override this function from State()
   def run(self, context):
      print()
      print(f"Currently in {self.name}")
      if (context.exists("S2I")):
         x=context.get("S2I")
      else:
         x=1
         context.set("S2I", x)

      # trigger
      if (x<=3):
         context.setNextState("State1")
         print (f"{self.name} run() iteration {x} of 3")
         x+=1
      else:
         context.setNextState(None)
         context.isDone = True

      # update state in context
      context.set("S2I", x)

      print (f"Next state is {context.getNextState()}.")
# End of class State2

# Only five steps are needed to run the FSM.
def main():
   # 1. Create our context
   context=Context("FSM")
   # (Populate it with some dummy values for this test)
   context.set("Author", "Karim Sultan")
   context.set("Dummy", "Value")
   context.set("Example", "Demo")

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
   
