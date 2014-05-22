#!/usr/bin/python

# Changes the DAQ operating mode
#
# Usage: switch_mode [mode] [args]
#
# Modes and optional arguments:
# - off
#   - (none)
# - acquire
#   - all arguments are optional and will be passed to mantis_server
# - rsync
#   - rsync config file (required)

import io
import json
import os
import subprocess
import sys

if len(sys.argv) <= 1:
    print("Usage: switch_mode [mode] [optional args]")
    sys.exit(0)

daqDir = os.environ['DAQSSNDIR']

lockFilename = daqDir + '/daq.lock'
if os.path.exists(lockFilename):
    print("DAQ session lock exists; someone else must be doing something. Please try again later.")
    sys.exit(0)
open(lockFilename, 'a').close()

offMode = "off"
acquireMode = "acquire"
rsyncMode = "rsync"

# get requested mode
modeRequest = sys.argv[1]

# open/create the status file
statusFilename = daqDir + "/status.json"

if not os.path.isfile(statusFilename):
    # file does not exist
    # create it and make the mode "off"
    with open(statusFilename, 'w') as statusFile:
        json.dump({"mode": offMode}, statusFile)

# read the status file and parse json
statusData = {}
with open(statusFilename, 'r') as statusFile:
    statusData = json.load(statusFile)

# get the current mode
currentMode = statusData["mode"]

# if we're already in the requested mode, exit
if modeRequest == currentMode:
    print("DAQ system is already in mode <", currentMode, ">")
    os.remove(lockFilename)
    sys.exit(0)

# okay, so we're going to switch modes
# first switch everything off

if currentMode == acquireMode:
    subprocess.call(['python', daqDir + '/internal/stop_acquire.py', str(statusData['pid'])])
elif currentMode == rsyncMode:
    subprocess.call(['python', daqDir + '/internal/stop_rsync.py'])

with open(statusFilename, 'w') as statusFile:
    json.dump({"mode": offMode}, statusFile)

print("Switching DAQ to mode <", modeRequest, ">")

if modeRequest == offMode:
    os.remove(lockFilename)
    sys.exit(0)

# start the new mode
if modeRequest == acquireMode:
    command = 'python ' + daqDir + '/internal/start_acquire.py'
    if len(sys.argv) > 2:
        command += " " + " ".join(sys.argv[2:])
    args = ['tmux', 'send-keys', '-t', 'daq:1.1', command, 'C-m']
    proc = subprocess.Popen(args) # does not wait for return
elif modeRequest == rsyncMode:
    if len(sys.argv) < 3:
        print("Please provide an rsync configuration file")
        os.remove(lockFilename)
        sys.exit(0)
    command = 'python ' + daqDir + '/internal/start_rsync.py ' + sys.argv[2]
    args = ['tmux', 'send-keys', '-t', 'daq:1.1', command, 'C-m']
    proc = subprocess.Popen(args) # does not wait for return

os.remove(lockFilename)
