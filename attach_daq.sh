#! /bin/bash

# attach_daq.sh
# Author: N. Oblath
#
# Attaches the DAQ session
#
# Usage: ./attach_daq.sh

SESSION="daq"

tmux has-session -t ${SESSION} &> /dev/null
RETVAL=$?

if [ ${RETVAL} -ne 0 ]; then
    echo "DAQ session does not exist; use start_daq.sh to start it"
    exit
fi

tmux attach-session -t ${SESSION}
