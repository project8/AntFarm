#! /bin/bash

# detach_daq.sh
# Author: N. Oblath
#
# Detaches the current client from the DAQ session.
# Should be used from within the DAQ session.
# If used outside of a tmux session, it will have no effect.
# If used from within a different tmux session, will detatch the client from that session.
#
# Usage: ./detach_daq.sh

#SESSION="daq"

tmux detach-client
