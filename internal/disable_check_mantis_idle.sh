#!/bin/sh

# Set DAQSSNDIR properly if it's not already in the environment
${DAQSSNDIR:="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.."} &> /dev/null

# Get the directory in which the script is being run
SCRIPTDIR="${DAQSSNDIR}/internal"

# Make a filename for temporarily holding the entire crontab for the user
TEMPCRONTAB="${SCRIPTDIR}/temp_disable_cmi.crontab"
NEWCRONTAB="$TEMPCRONTAB.new"

# List the crontab contents into the temporary file
crontab -l > $TEMPCRONTAB

SCRIPTFORCRON="check_mantis_idle.py"

# Check whether the relevant line actually exists in the crontab
if ! grep -q $SCRIPTFORCRON "$TEMPCRONTAB"; then
    exit
fi

# Use sed to remove the line mentioning the script check_mantis_idle.py
# Also remove previous commented information about loaded crontab files
sed -e "/$SCRIPTFORCRON/d" -e '/^#/d' <$TEMPCRONTAB >$NEWCRONTAB


# Put what's left back into cron
crontab $NEWCRONTAB

# Remove the temporary files
rm $TEMPCRONTAB $NEWCRONTAB
