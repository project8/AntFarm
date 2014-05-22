# stop_acquire.py
# Author: N. Oblath
#                                                                                                                                                                                          
# This script is meant to be used by switch_mode.py to stop data acquisition and write the status.json file.
# It assumes that the DAQ is in the "acquire" mode.


import json
import os
import signal
import subprocess
import sys
import time

daqDir = os.environ['DAQSSNDIR']

if len(sys.argv) < 2:
    print("no pid was provided; aborting")
    sys.exit(1)

pid = int(sys.argv[1])

# disable the check_mantis_idle cron job
subprocess.Popen([daqDir + '/internal/disable_check_mantis_idle.sh'])

# stop acquisition
procDir = "/proc/" + str(pid)
if not os.path.exists(procDir):
    print("acquisition process (pid: ", pid, ") is not running", sep='')
else:
    print("stopping acquisition; killing process", pid)
    os.kill(pid, signal.SIGINT)
    time.sleep(1) # wait for mantis to shut itself down                                                                                                                                  
    if os.path.exists(procDir):
        print("process did not stop; killing more forcefully this time")
        os.kill(pid, signal.SIGKILL)
        time.sleep(0.5)
        if os.path.exists(procDir):
            print("apologies, but the acquisition can't be stopped! please help!")
            sys.exit(1)

# write the status file
statusFilename = daqDir + "/status.json"
with open(statusFilename, 'w') as statusFile:
    json.dump({"mode": 'off'}, statusFile)

