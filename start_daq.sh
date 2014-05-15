#!/bin/bash

# start_daq.sh
# Author: N. Oblath
#
# Starts a DAQ session, initially in the <off> state.
# The tmux session created is called "daq"
#
# Usage: ./start_daq.sh

SESSION="daq"

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export DAQSSN_SCRIPT_DIR=${SCRIPTDIR}

tmux has-session -t ${SESSION} &> /dev/null
RETVAL=$?

if [ ${RETVAL} -eq 0 ]; then
    echo "DAQ session already exists; use attach_daq.sh to join"
    exit
fi

tmux -2 new-session -d -s ${SESSION}

tmux new-window -t ${SESSION}:1
tmux split-window -v -p 80
tmux select-pane -t 0
tmux send-keys "python switch_mode.py off" C-m
tmux select-pane -t 0

tmux -2 attach-session -t ${SESSION}
