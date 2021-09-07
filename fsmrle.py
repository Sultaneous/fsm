#!/usr/bin/python3

# This is a Run Length Encoded (RLE) FSM which accepts a file as input,
# and outputs a run-length encoded file:
#
# BYTE   BYTE
# <run>  <byte>
#
# So, 06 65 01 DE would represent 65 65 65 65 65 65 DE
#
# RLE is not very efficient.  It can be optimized better and works best
# on files with repetitive data (such as raw graphics files).  But this
# isn't about making an RLE tool.  This is about demonstrating the
# FSM engine with a functional FSM tool.
# NOTE: See FSM diagram in the source code directory

from fsm import Context, State, Dispatcher
import io
import os
import struct
import sys
argv=sys.argv
argc=(len(argv))

class State0(State):
   # Call super in base class for constructor
   def __init__(self, stateName):
      super().__init__("State0 - Intiatilize Context")

   # Must override this to provide logic for state
   def run(self, context):

      # Initialize
      context.push("run", 0)
      context.push("controlByte", -1)

      # Next State:
      context.setNextState("State1")
# End of class State0

class State1(State):
   # Call super in base class for constructor
   def __init__(self, stateName):
      super().__init__("State1 - Read Char")

   # Override
   def run(self, context):
      # Algorithm: Normally I would use a chunked read pattern,
      # with an interim buffer, but this is just a demo and
      # not meant for production so I will just it into memory
      # and using a memory stream, read it byte by byte.

      # If no memory stream then load file data into memory.
      if (not context.exists("memStream")):
         file=open(context.get("infile"), "rb")
         data=file.read()
         ms=io.BytesIO(data)
         context.push("memStream", ms)
      else:
         # memory stream exists, so load it
         ms=context.get("memStream")

      if not eof(ms):
         b=ms.read(1)
         context.push("byte", b)

         # Set the next state
         context.setNextState("State2")
      else:
         # TODO: Set this to the EOF State. For now, exit
         print("EOF.")
         context.setNextState("State4")

# End of class State1

class State2(State):
   # Call super in base class for constructor
   def __init__(self, stateName):
      super().__init__("State2 - Count Char")

   # Override
   def run(self, context):
      b=context.get("byte")

      #if (context.get("run")==0):
      if (context.get("outfileSize") <= 0 and context.get("run")==0):
         # First byte.  Count it.
         context.push("run", 1)

         # Stash it
         context.push("controlByte", b)
      else:
         # Is this a repeat byte?
         if (context.get("controlByte")==b):
            context.push("run", context.get("run")+1)

            # Next state is read char again
            context.setNextState("State1")
         else:
            # New byte. Terminate current run.
            x = context.get("run").to_bytes(1, "big")
            c = context.get("controlByte")
            rle = x + c
            context.push("rle", rle)

            # Reset counters
            context.push("controlByte", b)
            context.push("run", 1)

            # Set next state -> Write Run to file
            context.setNextState("State3")


      # TODO: Check if we have 255 in counter and flush it

# End of class State2

class State3(State):
   # Call super in base class for constructor
   def __init__(self, stateName):
      super().__init__("State3 - Write Run")

   # Override
   def run(self, context):
      # Ensure we have data to write
      # Redundant / shouldn't happen / but this caught a nasty bug
      # so I'm leaving it in.
      if not context.exists("rle"):
         context.setNextState("State1")

      file=open(context.get("outfile"), "ab+")
      rle=context.get("rle")
      c=file.write(rle)
      context.push("outfileSize", context.get("outfileSize")+c)
      file.close()

      # Next state
      # Get next char
      context.setNextState("State1")

# End of class State3

class State4(State):
   # Call super in base class for constructor
   def __init__(self, stateName):
      super().__init__("State4 - EOF / Terminate")

   # Override
   def run(self, context):
      # Do any clean up and exit
      # Nothing to do - yet.

      # TODO: Show statistics
      ofs=context.get("outfileSize")
      ifs=context.get("infileSize")
      pct=ofs/ifs*100

      print(f"Initial size: {ifs:,} bytes.")
      print(f"Outfile size: {ofs:,} bytes.")
      print(f"Reduction: {100.0 - pct:.02f}%")

      # Next state -> exit
      context.setNextState(None)

# End of class State4

# Detects EOF.  Python should have this built in.
def eof(f):
   cur = f.tell()    # save current position
   f.seek(0, os.SEEK_END)
   end = f.tell()    # find the size of file
   f.seek(cur, os.SEEK_SET)
   return cur == end

def showSyntax():
   print("Run Length Encoder Finite State Machine")
   print("This is a demo example of how to use the fsm module.")
   print("Syntax: fsmrle <input file>")
   print("Will output to <file.rle> and overwrite any existing output.")
   return()

def doHouseKeeping(context):
   if not os.path.isfile(argv[1]):
      print (f"Invalid input file: {argv[1]}")
      exit()
   infile=argv[1]
   context.push("infile", infile)
   context.push("infileSize", os.path.getsize(infile))

   # We keep the file name.  This way we know what the source file is.
   outfile=infile+".rle"
   context.push("outfile", outfile)
   context.push("outfileSize", 0)
   # overwrite it if it already exists
   if os.path.isfile(outfile):
      os.remove(outfile)

def main():
   if (argc<2):
      showSyntax()
      return

   # 1. Create context
   context=Context("RLE FSM")
   doHouseKeeping(context)

   # 2. Define initial state
   context.setNextState("State0")

   # 3. Create dispatcher
   print("Working... please wait.")
   dispatcher=Dispatcher()

   # 4. Dispatch!  This executes the FSM
   dispatcher.dispatch(context)

   # 5. Done
   print("Finished.")


if __name__=="__main__":
   main()
   
      
