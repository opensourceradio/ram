#!/bin/bash

##############################################################################
##############################################################################
##
## wsrep-notify.sh Do something in response to a notification from the
## database cluster in response to a configuration update or a cluster
## status change.
##
##############################################################################
##############################################################################

##################################################################
# Global shellcheck directives:
# Shellcheck doesn't get it. We can't declare a read-only variable and
# then set it after the fact.
# shellcheck disable=SC2155

# This script complies with Semantic Versioning: http://semver.org/
declare -r vMajor=0
declare -r vMinor=1
declare -r vPatch=1
# We can do this in one step in ZSH, but Bash needs 2 statements
# shellcheck disable=SC2016
declare -r vHash='$Hash$'
declare -r vvHash="${vHash#\$Hash: }"

# Tell them how to use this command.
usage() {
  local -r myName=${1}

  ${CAT} << EOF
${myName}: Respond to a notification event from the MariaDB/MySQL Galera
cluster.

Summary: ${myName} --index <INDEX>
                         --members <MEMBERS>
                         --status <STATUS>
                         --uuid <UUID>
                         --primary <yes|no>
		         [ --help ] [ --version ]

See https://galeracluster.com/library/documentation/notification-cmd-example.html#example-notification-script
and https://galeracluster.com/library/documentation/mysql-wsrep-options.html#wsrep-notify-cmd
for details.

We expect one or more of the following parameters to be provided by the calling process.

The --status parameter includes one of status keywords: Undefined, Joiner, Donor, Joined, Synced, or Error(##) (error code if available)

The --uuid parameter provides the cluster state UUID.

The --primary parameter includes the word "yes" or "no" indicating whether the current cluster component is primary.

The --members parameter includes a comma-separated list of component member UUIDs.

The --index parameter includes the index of this node in the node list.

EOF
}

# Log STDOUT and STDERR of this script and all commands called by this
# script to separate files.
exec 1> "/var/tmp/${0##*/}.out"
exec 2> "/var/tmp/${0##*/}.err"

declare -r myName="${0##*/}"

declare -r startTime=$(date +%s)
declare -r MAILTO="${MAILTO:-dklann@broadcasttool.com}"
declare -r MAILERCONF="${MAILERCONF:=/var/lib/mysql/conf.msmtp}"
declare -r messageID="$(uuidgen)-${startTime}@$(hostname)"

# Save the output in this file which we will attach to the email
# message (see the here-doc below).
declare -r outputFile="${OUTPUT_FILE:-/var/tmp/wsrep-notify.out}"

# The timestamp on this file is the time of last email sent.
declare -r emailLastSentFile="${EMAIL_LAST_SENT_FILE:-/var/tmp/wsrep-email-sent}"

# Grab the time of last modification of the output file and the
# email-last-sent file. No worries if they do not exist.
declare -r -i outputFileLastModified=$(stat --format="%Y" "${outputFile}" || echo '0')
#declare -r -i emailLastSentTime="$(stat --format="%Y" "${emailLastSentFile}" || echo '0')"

# Append to the output file if we have accessed it in the last ten
# seconds (ie, during an "event").
if [[ -f "${outputFile}" ]] && (( (startTime - outputFileLastModified) < 10 )) ; then
    declare -r APPEND="-a"
fi

# These hold the values of the parameters passed from mysqld. We will
# use them in a subshell, so we need export them.
declare -x INDEX MEMBERS PRIMARY STATUS UUID

# Parse the command line args.
TEMP=$(getopt -o hv --long index:,members:,primary:,status:,uuid:,help,version -n "${0##*/}" -- "${@}")
# shellcheck disable=SC2181
if [[ "${?}" != 0 ]] ; then echo "Internal getopt(1) error. Terminating..." >&2 ; exit 1 ; fi
# Note the quotes around "${TEMP}": they are essential!
eval set -- "${TEMP}"
while :
do
  case "${1}" in
    --index) INDEX="${2}" ; shift 2 ;;
    --memb*) MEMBERS="${2}" ; shift 2 ;;
    --prim*) PRIMARY="${2}" ; shift 2 ;;
    --stat*) STATUS="${2}" ; shift 2 ;;
     --uuid) UUID="${2}" ; shift 2 ;;
     --help) usage "${0}" ; exit ;;
    --vers*) showVersion=1 ; shift ;;
         --) shift ; break ;;
          *) echo "Internal getopt(1) error, cannot continue!" ; exit 1 ;;
  esac
done
unset TEMP

# Now that they are set, we do not want them to change.
declare -r INDEX MEMBERS PRIMARY STATUS UUID

if ((showVersion)) ; then
  echo "${myName}: version ${vMajor}.${vMinor}.${vPatch}-${vvHash%$}"
  exit 0
fi

[[ -z "${MEMBERS}" ]] && [[ -z "${STATUS}" ]] && [[ -z "${UUID}" ]] &&
    {
	echo "Are we testing?"
	exit
    }

declare -xa members
# Because quoting MEMBERS breaks its interpretation as a series of
# space-separated array elements.
# shellcheck disable=SC2206
members=( ${MEMBERS//,/ } )

# Improve the look of the output using the length of the longest
# "member" string for horizontal spacing.
declare -i mLen=0
for member in ${members[*]} ; do
    (( ${#member} > mLen )) && mLen=${#member}
done
declare -r mLen

(
    date --iso-8601=seconds --date="@${startTime}"

    printf "%16s %${mLen}s %7s %10s %36s\n"   "INDEX"    "MEMBERS"       "PRIMARY"    "STATUS"    "UUID"
    printf "%16s %${mLen}s %7s %10s %36s\n" "${INDEX}" "${members[0]}" "${PRIMARY}" "${STATUS}" "${UUID}"
    unset "members[0]"
    for member in ${members[*]} ; do
	[[ -z "${member}" ]] && continue
	printf "+%$((mLen + 16))s\n" "${member}"
    done
) | tee "${APPEND}" "${outputFile}"

if [[ "${STATUS}" =~ [Ss]ynced ]] &&  [[ "${PRIMARY}" =~ [Yy]es ]] ; then
    # Send the contents of outputFile to the recipients listed in MAILTO
    # (above). The sed(1) expression in the "To:" line cleans up the
    # separators in MAILTO. Since we are using mail.grunch.org (see
    # ${MAILERCONF}) we need to set envelope "From:" different
    # than the msmtp "From:".
    msmtp --file "${MAILERCONF}" --read-recipients --from=dklann@grunch.org <<ENDOFMAIL
To: $(echo "${MAILTO}" | sed -r -e 's/( |[ ,][ ,])/,/')
From: mysql@$(hostname)
Reply-To: No-Reply@$(hostname)
Subject: WSREP Event
Date: $(date --rfc-822 --date="@${startTime}")
Message-ID: <${messageID}>
X-Script-Name: ${0##*/}
MIME-Version: 1.0
Content-Type: multipart/mixed;
 boundary="----------${startTime}"

This is a multi-part message in MIME format.
------------${startTime}
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: quoted-printable

$(hostname -f) experienced an event that caused a wsrep-notify-cmd. See the
attachment.

------------${startTime}
Content-Type: text/plain; charset=UTF-8;
 name="${outputFile##*/}"
Content-Transfer-Encoding: base64
Content-Disposition: attachment;
 filename="${outputFile##*/}"

$(cat < "${outputFile}" | base64)
------------${startTime}--
ENDOFMAIL

    touch "${emailLastSentFile}"
    rm "${outputFile}"
fi

exit
