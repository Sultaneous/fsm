#!/usr/bin/python3

# Code template generator for FSM library.
# September 2021, Karim Sultan
from fsm import *
import os
from datetime import datetime

# Generator Data
# Most generator data must be declared in place, not in advance.
# This is due to how Python handles format strings; it resolves
# them at declaration, not at run-time usage, so the multi-line
# strings that use formatting must be declared only after the
# required variables used in them have been defined.  For shame,
# Python.
clparameters='''import sys
argv=sys.argv
argc=(len(argv))
'''

### Code generator logic ###

# Prompt function which displays a prompt and a list of one 
# character options, and returns true if the option is equal
# to the match parameter.  The default parameter is chosen
# if user inputs a blank line (<enter>).
def prompt(prompt, options, default, match):
   # Validate
   if (not default in options):
      return(False)
   # Convert options list to prompt string
   s="["
   s+="/".join(str(p) for p in options)
   s+=f"] <{default}> "
   r=""
   while not (r in options):
      r=input(prompt+" "+s)
      if r=="": r=default
   return(r==match)


def main():
   s='''
Welcome to FSM Template Generator for the Python FSM module.
By Karim Sultan, September 2021.

This utility will ask a few questions about your DFA / FSM and will generate
a code template.  This is the interactive version.
'''
   print (s)
   responses = dict()

   # Get the outfile to write to, prompt for overwrite if exists
   valid=False;
   while not valid:
      responses["outfile"]=input("1. Name of outfile: ")
      if os.path.isfile(responses["outfile"]):
         if prompt("File exists. Overwrite?", ['y','n'], 'y', 'y'):
            valid=True
      else:
         if responses["outfile"]!="":
            valid=True
   print(f"Writing to source file: \"{responses['outfile']}\"")
      
   # Get the number of states
   print()
   valid=False
   maxStates=100
   while not valid:
      xs=input(f"2. Number of states? (1-{maxStates}) ")
      try:
         x=int(xs)
      except ValueError:
         print(f"You entered '{xs}' but a positive integer value is required. ")
      else:
         if not (x<=0 or x>maxStates):
            responses["numStates"]=x
            valid=True
   print(f"Generating {responses['numStates']} states.")

   # Optional, allow user to name states
   print()
   responses['stateNames']=[]
   if (prompt("3. Would you like to name the states (give a tag or brief description)?",['y','n'], 'y', 'y')):
      for i in range(responses['numStates']):
         responses['stateNames'].append(input(f"Name for State {i+1}: "))
   else:
      for i in range(responses['numStates']):
         responses['stateNames'].append(f"Unnamed FSM State #{i+1}")
   print("The state names are:")
   print('\n'.join(str(p) for p in responses['stateNames']))

   # Optional, use command line parameters
   print()
   responses["hasCLParameters"]=prompt("4. Will you use command line parameters?", ['y','n'], 'y', 'y')
   print(f"Using command line parameters: {responses['hasCLParameters']}")

   # Optional, show a usage syntax if no parameters
   responses["hasSyntax"]=False
   if responses["hasCLParameters"]:
      print()
      responses["hasSyntax"]=prompt("5. Do you want to show syntax for usage?", ['y','n'], 'y', 'y')
   print(f"Show usage syntax on no parameters: {responses['hasSyntax']}")

   # Get app name
   print()
   aname,_=os.path.splitext(responses['outfile'])
   ins=input(f"6. What is the name of this app?  <{aname}> ")
   if ins=="":
      responses["appName"]=aname
   else:
      responses["appName"]=ins
   print(f"Using app name of \"{responses['appName']}\"")

   # Get author name
   print()
   responses["author"]=input(f"7. What is the author's name? <Unknown> ")
   if responses["author"]=="": 
      responses["author"]="Unknown"
   print(f"Using author name of \"{responses['author']}\"")

   # Pause
   print()
   prompt("Ready to produce summary.  Hit <enter> to continue...", ['y'], 'y', 'y')

   # Summary and confirm step
   print()
   print("8. Summary")
   print(f"App name: \"{responses['appName']}\" by \"{responses['author']}\"")
   print(f"Writing to source file: \"{responses['outfile']}\"")
   print(f"Generating {responses['numStates']} states.")
   if not responses["stateNames"]==None:
      for i in range(len(responses['stateNames'])):
         print(f" {i+1:2}.  State{i+1}:   {responses['stateNames'][i]}")
   print(f"Requires use of command line parameters: {responses['hasCLParameters']}")
   print(f"Show usage syntax when no parameters: {responses['hasSyntax']}")
   print()

   print("I am now ready to generate a python code template.")
   if not prompt("Do you wish me to begin? ", ['y','n'], 'y', 'y'):
      if not prompt("Are you sure?  All entries will be lost! ", ['y','n'], 'n', 'n'):
         print("OK. Goodbye.")
         exit()
   
   # Time to write
   outfile=open(responses["outfile"], "w+")

   header=f'''#!/usr/bin/python3

# This is a code template.  You must add your logic to each
# of the state classes in the run() function, as shown below.
#
# TODO: REPLACE THIS HEADER WITH YOUR HEADER

# Generated by FSMGen Utility {datetime.today().strftime('%B %d, %Y')} for {responses['author']}.
from fsm import *
'''
   outfile.write(header)

   if (responses["hasCLParameters"]):
      outfile.write(clparameters)

   syntax=f'''
def showSyntax():
   print("{responses['appName']} by {responses['author']}, {datetime.today().strftime('%B %d, %Y')}")
   print("<Explain purpose>")
   print("Syntax: {responses['outfile']} <mandatoy params> ... [optional params] ...")
   print()
   return()

'''
   if (responses["hasSyntax"]):
      outfile.write(syntax)

   for i in range(responses["numStates"]):
      outfile.write(f"class State{i+1}(State):")
      outfile.write("\n")

      s="   def __init__(self, stateName):"
      outfile.write(s)
      outfile.write("\n")
  
      s=f"      super().__init__(\"{responses['stateNames'][i]}\")"
      outfile.write(s)
      outfile.write("\n")
      outfile.write("\n")

      s="   def run(self, context):"
      outfile.write(s)
      outfile.write("\n")

      s="      # TODO Replace with your logic"
      outfile.write(s)
      outfile.write("\n")

      s="      print(f\"Currently in {self.name}\")"
      outfile.write(s)
      outfile.write("\n")
      outfile.write("\n")

      s="      # Set the next state based on triggers/transitions"
      outfile.write(s)
      outfile.write("\n")

      if (i==responses["numStates"]-1):
         ns="None"
      else:
         ns=f"\"State{i+2}\""
      s=f"      context.setNextState({ns})"
      outfile.write(s)
      outfile.write("\n")
      outfile.write("\n")
   
      s=f"# End of class State{i+1}"
      outfile.write(s)
      outfile.write("\n")
      outfile.write("\n")

   # Main
   s="def main():"
   outfile.write(s)
   outfile.write("\n")

   if (responses['hasSyntax']):
      s="   if (argc<2):\n      showSyntax()\n      return"
      outfile.write(s)
      outfile.write("\n")

   smain=f'''
   # Only five steps are needed to run the FSM.

   # 1. Create our context
   context=Context("{responses['appName']}")

   # 2. Identify the first state to instantiate
   context.setNextState("State1")

   # 3. Create our dispatcher
   dispatcher=Dispatcher()

   # 4. Dispatch! This executes the FSM
   dispatcher.dispatch(context)

   # 5. Done
   print("SUCCESS!")

# End of main

# If module executed, run main
if __name__=="__main__":
   main()



'''
   outfile.write(smain)

   outfile.close()

   print("SUCCESS!")
   

# If Module is run directly...
if __name__=="__main__":
   main()
   
