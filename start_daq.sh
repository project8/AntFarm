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
export DAQSSNDIR=${SCRIPTDIR}

# Check whether the session is already started
tmux has-session -t ${SESSION} &> /dev/null
RETVAL=$?

if [ ${RETVAL} -eq 0 ]; then
    echo "DAQ session already exists; use attach_daq.sh to join"
    exit
fi

# Annoyingly, while the DAQSSNDIR variable will be visible from the session panes, 
# I can't add it to the path from here in a way that is still there in the panes.
# Instead, we'll create a temporary script and source it from the panes
ADDTOPATH="${SCRIPTDIR}/add_to_path.sh"
echo "#!/bin/bash" > $ADDTOPATH
echo "export PATH=${DAQSSNDIR}:${PATH}" >> $ADDTOPATH

# Start the new session
tmux -2 new-session -d -s ${SESSION}

tmux new-window -t ${SESSION}:1
tmux split-window -v -p 80
tmux select-pane -t ${SESSION}:1.0
tmux send-keys "source ${ADDTOPATH}" C-m
tmux send-keys "${SCRIPTDIR}/switch_mode.py off" C-m
tmux select-pane -t $SESSION}:1.0

tmux -2 attach-session -t ${SESSION}
