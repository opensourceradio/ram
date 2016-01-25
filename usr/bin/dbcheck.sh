#!/bin/zsh

##############################################################################
##############################################################################
##
## dbcheck.sh: ensure that the Rivendell database is accessible before
## exiting this script. This is used by the various systemd service
## scripts in rivendell.target.
##
############################################################
### DO NOT USE THIS SCRIPT WITHOUT MAKING MODIFICATIONS! ###
############################################################
##
## NOTE:
## This script is COMPLETELY installation-specific! See the "BUG ALERT" below.
##
##############################################################################
##############################################################################

# log STDOUT and STDERR of this script and all commands called by this script to separate files
exec 1> /var/tmp/${0##*/}.out
exec 2> /var/tmp/${0##*/}.err

RM=$(whence rm) ; RM=${RM:-${ROOT:-/}bin/rm}
LN=$(whence ln) ; LN=${LN:-${ROOT:-/}bin/ln}
LOGGER=$(whence logger) ; LOGGER=${LOGGER:-${ROOT:-/}usr/bin/logger}

if [[ -f ${ROOT:-/}usr/local/bin/zsh-functions ]] ; then
    if [[ -r ${ROOT:-/}usr/local/bin/zsh-functions ]] ; then
	source ${ROOT:-/}usr/local/bin/zsh-functions
    else
	${LOGGER} --stderr -t ${0##*/} -p local7.err -i "ERROR: Cannot read '/usr/local/bin/zsh-functions' (${?}). Check permissions."
    fi
else
    ${LOGGER} --stderr -t ${0##*/} -p local7.err -i "ERROR: Cannot find '/usr/local/bin/zsh-functions' (${?})."
fi

##
## Theory of Operation
##
## - virtual machine 'rd-service' gets autostarted by libvirt on boot
##
## - AFTER jackd is running, AND AFTER the database is accessible we
## need to start rivendell daemons on the host.
##
## - AFTER the database is accessible AND rivendell HOST daemons are
## running we start AIRPLAY VM(s)
##
## - AFTER the database is accessible we start MANAGEMENT VM(s)
##
## See also the systemd service files and their associated
## dependencies in /etc/systemd/system/rivendell.target.wants
##

##
## rbRunning()
## Return true (Zero) if we can make a valid connection to the remote
## database and retrieve a count of carts in the CART table.
##
dbRunning() {
    local cartCount=0 returnValue=1

    cartCount=$(doSQL "SELECT COUNT(*) FROM CART")
    ${LOGGER} -t ${0##*/} -p local7.info -i "Found ${cartCount} CARTs in the ${db} database."

    (( cartCount )) && returnValue=0

    return ${returnValue}
}

maxAttempts=${MAX_ATTEMPTS:-100}
sleepTime=${SLEEP_TIME:-1}
exitValue=1

loopCount=1
while :
do
    # wait for the database to be started before proceeding further
    dbRunning && { exitValue=0 ; break ; }

    (( loopCount++ > maxAttempts )) && break

    sleep ${sleepTime}
done

if (( loopCount > maxAttempts ))
then
    ${LOGGER} --stderr -t ${0##*/} -p local7.error -i "ERROR: Tried ${loopCount} times to start the RAM systems."
    exitValue=9
fi

exit ${exitValue}
