#!/bin/sh

# Set DAQSSNDIR properly if it's not already in the environment
${DAQSSNDIR:="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.."} &> /dev/null

# Get the directory in which the script is being run
SCRIPTDIR="$DAQSSNDIR/internal"

# Make a filename for temporarily holding the entire crontab for the user
TEMPCRONTAB="${SCRIPTDIR}/temp_enable_cmi.crontab"
NEWCRONTAB="${TEMPCRONTAB}.new"

SCRIPTFORCRON="check_mantis_idle.py"

# List the crontab contents into the temporary file
crontab -l > $TEMPCRONTAB

# Check if the crontab already has check_mantis_idle.py
if grep -q $SCRIPTFORCRON "$TEMPCRONTAB"; then
    exit
fi

# Remove previous commented lines about added crontab files
sed '/^#/d' <$TEMPCRONTAB >$NEWCRONTAB

CRONTABLINE="*/5 * * * * ${SCRIPTDIR}/$SCRIPTFORCRON ${DAQSSNDIR}"
echo "$CRONTABLINE" >> $NEWCRONTAB

# Put what's left back into cron
crontab $NEWCRONTAB

# Remove the temporary files
rm $TEMPCRONTAB $NEWCRONTAB
