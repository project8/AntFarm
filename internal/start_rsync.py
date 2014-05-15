# start_acquire.py
# Author: N. Oblath
#
# This script is meant to be used by switch_mode.py to start data transfer and write the status.json file.
# It assumes that the DAQ is in the "off" mode.

import json
import os
import subprocess
import sys

daqDir = os.environ['DAQSSN_SCRIPT_DIR']

if len(sys.argv) == 1:
    print("Please supply a configuration file for the rsync mode")
    sys.exit(1)

if not os.path.isfile(sys.argv[1]):
    print("Configuration file is not valid:", sys.argv[1])
    sys.exit(1)

configData = {}
with open(sys.argv[1], 'r') as configFile:
    configData = json.load(configFile)

# source
sourceArgs = []

for dir in configData["source"]["dirs"]:
    sourceArgs.append(dir)

destHost = configData["destination"]["host"]
destUser = configData["destination"]["user"]
destTopDir = configData["destination"]["top-dir"]

args = ['rsync', '-avPz']

destStr = destUser + '@' + destHost + ':' + destTopDir

args.extend(sourceArgs)
args.append(destStr)


proc = subprocess.Popen(args)

statusFilename = daqDir + "/status.json"

with open(statusFilename, 'w') as statusFile:
    json.dump({"mode": "acquire", "pid": proc.pid}, statusFile)

print("start_acquire.py is finished ( pid =", proc.pid, ")")
