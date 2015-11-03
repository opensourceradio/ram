#!/bin/bash

# What we need the script to do...
#
# -virtual machine 'rd-service' gets autostarted by libvirt on boot
#
# -AFTER jackd AND AFTER the DB is accessible we need to start rivendell
# daemons on the host.
#
# -AFTER the DB is accessible AND rivendell HOST daemons are running we
# start AIRPLAY VMs
#
# -AFTER the DB is accessible we start MANAGEMENT VMs
#
# hope that makes sense ;)
#
# I think there should be a good way to use systemd service files to do
# this along with a script that sets an environment var as a flag, or the
# above service files are dependent on the service file that launches the
# script to exit first.

# Read a .ini-style configuration file and return the value for the
# parameter passed. It's a hack, but it works.
getConfValue() {
    local confFile=${1:?"Please name a config file to read."} && shift
    local section=${1:?"Please name a config file section to read."} && shift
    local parm=${1:?"What parameter from the config file ${confFile}?"} && shift
    local returnValue=1

    while read line
    do
	# see if the line is a "section" specifier
	expr match "${line}" "\[${section}\]" > /dev/null && { inSection=1 ; continue ; }

	if (( inSection ))
	then
	    # rivendell uses parm=value (spaces not permitted, I think, but I'll check for them anyway)
	    if expr match "${line}" "${parm}[[:space:]]*=.*" > /dev/null
	    then
		# this eval() strips leading and trailing whitespace
		# from the variable too.
		value="$(eval echo ${line#*=})"
		returnValue=0
		break
	    fi
	fi
    done < ${confFile}

    echo "${value}"

    return ${returnValue}
}

# Return true (Zero) if we can make a valid connection to the remote
# database and retrieve a count of carts in the CART table.
dbRunning() {
    local cartCount=0 returnValue=1

    local dbHost=${DB_HOST:-$(getConfValue ${rdConf} mySQL Hostname)}
    local dbUser=${DB_USER:-$(getConfValue ${rdConf} mySQL Loginname)}
    local dbPass=${DB_PASS:-$(getConfValue ${rdConf} mySQL Password)}
    local db=${DB:-$(getConfValue ${rdConf} mySQL Database)}

    cartCount=$(mysql -s -N -h "${dbHost}" -u "${dbUser}" -p"${dbPass}" ${db} -e "SELECT COUNT(*) FROM CART")
    logger -i -t ${0##*/} -p local7.info "Found ${cartCount} CARTs in the ${db} database."

    (( cartCount )) && returnValue=0

    return ${returnValue}
}

rdConf=${RD_CONF:-${ROOT:-/}etc/rd.conf}
dbHost=${DB_HOST}
maxAttempts=${MAX_ATTEMPTS:-100}
sleepTime=${SLEEP_TIME:-1}
exitValue=1

if [[ -f ${rdConf} ]]
then

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
	logger -i -s -t ${0##*/} -p local7.error "ERROR: Tried ${loopCount} times to start the RAM systems."
	exitValue=9
    fi
else
    logger -i -s -t ${0##*/} -p local7.error "ERROR: Could not find ${rdConf} configuration. Is Rivendell installed?"
    exitValue=3
fi

exit ${exitValue}
