#!/bin/bash

# stop_daq.sh
# Author: N. Oblath
#
# Turns DAQ off and kills the tmux session
# It may be used from inside or outside of the DAQ session
#
# Usage: ./stop_daq.sh

SESSION="daq"

# Set DAQSSNDIR properly if it's not already in the environment
${DAQSSNDIR:="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"}

# Check whether the DAQ session exists
tmux has-session -t ${SESSION} &> /dev/null
RETVAL=$?

if [ ${RETVAL} -ne 0 ]; then
    echo "DAQ session does not exist"
    exit
fi

# Switch the DAQ mode to off
tmux send-keys -t ${SESSION}:1.0 "${DAQSSNDIR}/switch_mode.py off" C-m

# Close the tmux session
tmux kill-session -t ${SESSION}

# Remove status.json and setup_daq_env.sh
echo -e "${DAQSSNDIR}/setup_daq_env.sh"
if [ -e "${DAQSSNDIR}/setup_daq_env.sh" ]; then
    rm "${DAQSSNDIR}/setup_daq_env.sh"
fi

if [ -e"${DAQSSNDIR}/status.json" ]; then
    rm "${DAQSSNDIR}/status.json"
fi

echo "DAQ session terminated"
