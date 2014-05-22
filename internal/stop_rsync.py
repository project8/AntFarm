# stop_acquire.py
# Author: N. Oblath
#                                                                                                                                                                                          
# This script is meant to be used by switch_mode.py to stop data acquisition and write the status.json file.
# It assumes that the DAQ is in the "acquire" mode.


import json
import os
import submodule
import sys
import time

daqDir = os.environ['DAQSSNDIR']

if len(sys.argv) < 2:
    print("no pid was provided; aborting")
    sys.exit(1)

pid = int(sys.argv[1])

# stop rsync
procDir = "/proc"/ + str(pid)
if not os.path.exists(procDir):
    print("rsync process (pid: ", pid, ") is not running", sep='')
else:
    print("stopping rsync; killing process", pid)
    os.kill(pid, signal.SIGINT)

# write the status file
statusFilename = daqDir + "/status.json"
with open(statusFilename, 'w') as statusFile:
    json.dump({"mode": 'off'}, statusFile)

