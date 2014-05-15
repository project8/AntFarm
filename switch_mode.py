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
import signal
import subprocess
import sys
import time

if len(sys.argv) <= 1:
    print("Usage: switch_mode [mode] [optional args]")
    sys.exit(0)

daqDir = os.environ['DAQSSN_SCRIPT_DIR']

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
    sys.exit(0)

# okay, so we're going to switch modes
# first switch everything off

# TODO: probably combine these if there's no difference in the action
if currentMode == acquireMode:
    pid = statusData["pid"]
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
                sys.exit(0)
elif currentMode == rsyncMode:
    pid = statusData["pid"]
    procDir = "/proc"/ + str(pid)
    if not os.path.exists(procDir):
        print("rsync process (pid: ", pid, ") is not running", sep='')
    else:
        print("stopping rsync; killing process", pid)
        os.kill(pid, signal.SIGINT)

with open(statusFilename, 'w') as statusFile:
    json.dump({"mode": offMode}, statusFile)

print("Switching DAQ to mode <", modeRequest, ">")

if modeRequest == offMode:
    sys.exit(0)

# start the new mode
if modeRequest == acquireMode:
    command = 'python ' + daqDir + '/start_acquire.py'
    if len(sys.argv) > 2:
        command += " " + " ".join(sys.argv[2:])
    args = ['tmux', 'send-keys', '-t', '1', command, 'C-m']
    proc = subprocess.Popen(args) # does not wait for return
elif modeRequest == rsyncMode:
    if len(sys.argv) < 3:
        print("Please provide an rsync configuration file")
        sys.exit(0)
    command = 'python ' + daqDir + '/start_rsync.py ' + sys.argv[2]
    args = ['tmux', 'send-keys', '-t', '1', command, 'C-m']
    proc = subprocess.Popen(args) # does not wait for return
