#!/usr/bin/python



import json
import os
import subprocess
import sys

lastTimeKey = "last-time"
sameTimeCountKey = "same-time-count"

# assuming we check every 5 minutes, after 6 checks we'll definitely be over 30 minutes
sameTimeCountMax = 5

daqDir = os.environ['DAQSSNDIR']

# open/create the status file
statusFilename = daqDir + "/status.json"

# read the status file and parse json
statusData = {}
with open(statusFilename, 'r') as statusFile:
    statusData = json.load(statusFile)

if not statusData["mode"] == "acquire":
    print("DAQ is not in < acquire > mode; aborting")
    sys.exit(1)

mantisPID = statusData["pid"]

proc = subprocess.Popen(["ps", "-p", str(mantisPID), "-h", "-o", "time"], stdout=subprocess.PIPE)
psOut, psErr = proc.communicate()

currentTime = psOut.decode("utf-8")

timeCheckCount = 0;
if "last-time" in statusData:
    lastTime = statusData[lastTimeKey]
    timeCheckCount = statusData[sameTimeCountKey]
    print("have last time:", lastTime, " and timeCheckCount:", timeCheckCount)
    if currentTime == lastTime:
        timeCheckCount += 1
        print("timeCheckCount is now", timeCheckCount)
        if timeCheckCount > sameTimeCountMax:
            proc = subprocess.Popen([daqDir + "/switch_mode.py", "rsync"])
            sys.exit(0)
    else:
        timeCheckCount = 0

statusData[lastTimeKey] = currentTime
statusData[sameTimeCountKey] = timeCheckCount
with open(statusFilename, 'w') as statusFile:
    json.dump(statusData, statusFile)

