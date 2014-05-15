#!/bin/bash

# stop_daq.sh
# Author: N. Oblath
#
# Turns DAQ off and kills the tmux session
#
# Usage: ./stop_daq.sh

SESSION="daq"

tmux has-session -t ${SESSION} &> /dev/null
RETVAL=$?

if [ ${RETVAL} -ne 0 ]; then
    echo "DAQ session does not exist"
    exit
fi

python switch_mode.py off

unset DAQSSN_SCRIPT_DIR

tmux kill-session -t ${SESSION}
