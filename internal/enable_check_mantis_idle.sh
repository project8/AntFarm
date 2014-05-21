#!/bin/sh

# Get the directory in which the script is being run
SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Make a filename for temporarily holding the entire crontab for the user
TEMPCRONTAB="${SCRIPTDIR}/temp_crontab_for_enabling_check_mantis_idle.crontab"
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

CRONTABLINE="* 6 * * * $SCRIPTFORCRON"
echo "$CRONTABLINE" >> $NEWCRONTAB

# Put what's left back into cron
crontab $NEWCRONTAB

# Remove the temporary files
rm $TEMPCRONTAB $NEWCRONTAB
