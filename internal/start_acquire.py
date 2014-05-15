# start_acquire.py
# Author: N. Oblath
#
# This script is meant to be used by switch_mode.py to start data acquisition and write the status.json file.
# It assumes that the DAQ is in the "off" mode.

import json
import os
import subprocess
import sys

daqDir = os.environ['DAQSSNDIR']

args = ['/usr/local/bin/mantis_server']
if len(sys.argv) > 1:
    args.extend(sys.argv[1:])

proc = subprocess.Popen(args)

statusFilename = daqDir + "/status.json"

with open(statusFilename, 'w') as statusFile:
    json.dump({"mode": "acquire", "pid": proc.pid}, statusFile)

print("start_acquire.py is finished ( pid =", proc.pid, ")")
