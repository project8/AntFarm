#!/bin/bash
#
# reset_all.sh
# Author: N. Oblath
#
# Resets the DAQ session to its pristine state.
# Should be able to handle non-standard states, such as missing status files, etc.
#
# Usage: > ./reset_all.sh

# Set DAQSSNDIR properly if it's not already in the environment
${DAQSSNDIR:="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"}

# Call stop_daq.sh to shutdown the DAQ session
${DAQSSNDIR}/stop_daq.sh

# It may be that mantis is still running, if the status.json file did not match the state of mantis_server
# So shutdown mantis_server, if it's running
# TODO
# ps | grep mantis_server

# It also may be that the check_mantis_idle cron job wasn't removed from the crontab
${DAQSSNDIR}/internal/disable_check_mantis_idle.sh

# TODO: Should something be done about rsync, if it hapens to still be running?

# If they're present, remove the files that are created by the DAQ session
if [ -e "${DAQSSNDIR}/setup_daq_env.sh" ]; then
    rm "${DAQSSNDIR}/setup_daq_env.sh"
fi

if [ -e "${DAQSSNDIR}/status.json" ]; then
    rm "${DAQSSNDIR}/status.json"
fi

# Remove any temporary files that have been left accidentally
rm "${DAQSSNDIR}/internal/temp*.crontab"
