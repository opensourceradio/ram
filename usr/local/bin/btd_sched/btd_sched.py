#!/usr/bin/env python3
'''btd_sched.py: schedule music for Rivendell.

This scheduler is intimately tied to Rivendell. It uses a "Reference"
Service (Grid, Clocks, and Events) and an "Implementation" Service
(Grid, Clocks, and Events) to generate Log "merge files" (Data Import
files). The Reference Service is a "normal" Rivendell Service that one
can use with the built-in Rivendell scheduler. The Implementation
Service must include one or more Clocks containing one or more Events
that specify "IMPORT: From Music". To avoid confusion, Clocks used in
the Implementation should be enabled only for the Implementation
Service. The Implementation Service is referred to as "merge" in this
module, but may be named anything you prefer.

You must ensure that the Clocks used in your Reference Service include
no Events that "IMPORT From Music". This would result in some weird
twisting of Time and Space.

The Implementation Service must include settings for Music Data Import
(RDadmin->Manage Services->[Implementation Service]. Set the Import
Path using Rivendell wildcards representing the name of the import
file. At this time, btd_sched.py supports Rivendell wildcards that
match their equivalents in strftime(3) .

Set the "Import Template" to "[custom]" and use the following values
for the Offsets and Lengths (RDAdmin->Manage Services->[Implementation
Service]):

 - Field          Offset, Length
 - Cart Number:       10, 6
 - Title:             18, 34
 - Start Time-Hours:   0, 2
 - Start Time-Minutes: 3, 2
 - Start Time-Seconds: 6, 2
 - Length-Hours:      54, 2
 - Length-Minutes:    57, 2
 - Length-Seconds:    60, 2
Set all other Offsets and Lengths to Zero.

TODO: hour-of-day exclusion. Ensure that artists and tracks do not
play in the same our as it did in the previous N days.

TODO: "artist groups": Or "artist equivalents" (e.g., Lou Reed and
Velvet Underground, Neil Young and CSNY, Mick Jagger and the Rolling
Stones, etc.). I think, in its simplist form, this is simply a mapping
file that contains sets of "equivalent" artist names.

TODO: "exceptions": Figure out a way to account for Carts that are
scheduled outside of this scheduler (e.g., Pre- and Post-import
Carts).

'''

import sys
import re
import time
import argparse
import pprint
import schedlib
from artists import ArtistList

DEFAULT_REFERENCE_SERVICE = 'Production'
ONE_HOUR_MS = (60 * 60 * 1000)
ONE_DAY_MS = (24 * 60 * 60 * 1000)
TOMORROW_FIRST_HOUR = (int(time.strftime("%u")) % 7 * 24)
DEFAULT_ARTIST_SEPARATION = 200
__version__ = '0.1.5'

def get_event_sched_codes(timing):

    '''Get a count of Events and a list of Scheduler Codes used by Events
    in the Clocks for the chosen days. Returns a dict of dicts of
    lists with the outer dict indexed by Group and each containing
    dicts indexed by Scheduler Codes of (empty) lists. We use these
    per-Group Scheduler Codes to select Carts.

    :param timing: a data structure containing the first hour and last
    hour (of the week) for this session.

    :returns events_sched_codes, event_count: a list of unique
    Scheduler Codes for each Group used in Events in this session, the
    total number of Events for this session.

    '''

    group_list = re.split(r',\s*', ARGS.groups.lower())
    db = schedlib.RDDatabase(None)

    # A dict of dicts of lists.
    events_sched_codes = {g: {} for g in group_list}
    codes_re = re.compile(r'^(?P<s1>.*)\|(?P<s2>.*)$')

    query = ("SELECT COUNT(ev.sched_group) "
             "FROM SERVICE_CLOCKS sc "
             "LEFT JOIN CLOCK_LINES cl ON (sc.clock_name = cl.clock_name) "
             "LEFT JOIN EVENTS ev ON (cl.event_name = ev.name) "
             "WHERE sc.service_name = %s "
             "AND ev.sched_group IN (")
    query += ", ".join(["%s" for _ in group_list])
    query += ") AND "
    # Handle the cross-Sunday boundary.
    if timing['first_hour'] > timing['last_hour']:
        query += "(sc.hour BETWEEN %s AND 167 OR sc.hour BETWEEN 0 AND %s) "
    else:
        query += "sc.hour BETWEEN %s AND %s "
    query_args = [ARGS.reference_service]
    query_args += group_list
    query_args += [timing['first_hour'], timing['last_hour']]
    DEBUG_PRINT("get_event_sched_codes: COUNT query: {q}".format(q=query % tuple(query_args)))
    # Apparently, this fetchall() returns a list of tuples. We get the
    # integer inside by using the appropriate subscripts?
    rows = db.fetchall(query, tuple(query_args))
    event_count = rows[0][0]

    query = ("SELECT DISTINCT LCASE(ev.sched_group) AS sched_group, "
             "CONCAT(ev.have_code, '|', ev.have_code2) AS code, "
             "ev.artist_sep AS artist_sep, ev.title_sep AS title_sep "
             "FROM SERVICE_CLOCKS sc "
             "LEFT JOIN CLOCK_LINES cl ON (sc.clock_name = cl.clock_name) "
             "LEFT JOIN EVENTS ev ON (cl.event_name = ev.name) "
             "WHERE sc.service_name = %s "
             "AND ev.sched_group IN (")
    query += ", ".join(["%s" for _ in group_list])
    query += ") AND "
    # Handle the cross-Sunday boundary.
    if timing['first_hour'] > timing['last_hour']:
        query += "(sc.hour BETWEEN %s AND 167 OR sc.hour BETWEEN 0 AND %s) "
    else:
        query += "sc.hour BETWEEN %s AND %s "
    query += "ORDER BY sched_group, code"
    query_args = [ARGS.reference_service]
    query_args += group_list
    query_args += [timing['first_hour'], timing['last_hour']]
    DEBUG_PRINT("get_event_sched_codes: query: {q}".format(q=query % tuple(query_args)))
    rows = db.fetchall(query, tuple(query_args), dictionary=True)

    for row in rows:
        if row['code'] == '|':
            row['code'] = 'NoCode|'
        matches = codes_re.search(row['code'])
        if matches is None:
            # We're looking only for Events with Scheduler Code
            # constraints.
            continue

        group = row['sched_group']

        codes = matches.groupdict()
        if codes['s1'] is not None and codes['s1'] != '' and codes['s1'] not in events_sched_codes[group]:
            events_sched_codes[group][codes['s1']] = []
        if codes['s2'] is not None and codes['s2'] != '' and codes['s2'] not in events_sched_codes[group]:
            events_sched_codes[group][codes['s2']] = []

    return events_sched_codes, event_count

def calculate_pool_size(batch, event_count):
    '''Calculate the size of the "pool" (in "tracks") that we need for
    this session. The "pool" is a group of potential "tracks" (a
    simplified view of a CART) retrieved from the Rivendell Database
    with the SELECT statement found in fill_active_pool().

    The current calculation scans the Reference Service counting all
    the Events in all the Clocks containing "Must have [Scheduler]
    code" in the current "batch". It then extracts the most-used
    Scheduler Code and adding that to the same calculation for the
    "and code" Scheduler Code.

    The pool size value is stored in the global configuration data
    structure `GLOBAL_STATS['pool_size']`

    :param batch: An instance of Batch() (see schedlib.py)
    :param event_count: The total number of Events in this session
    :returns: An integer representing the the pool size

    '''
    VERBOSE_PRINT("calculate_pool_size: Most Primary Scheduler Codes: {m}, Events: {e}"
                  .format(m=max(batch.values('schedcode1').values()), e=event_count))

    return max(batch.values('schedcode1').values()) + max(batch.values('schedcode2').values())

def fill_active_pool(event_sched_codes_by_group):
    '''Generate a dict (aka "pool") containing up to
    "GLOBAL_STATS['pool_size']" "tracks". The "tracks" in the "pool"
    are candidates that may be used (subject to the "rules" used in
    the Rivendell Database and in this app) to populate the Music Data
    Import file.

    The data are structured as a dict of dicts of lists of dicts
    containing the data returned from the SELECT statement in this
    function.

    :param event_sched_codes_by_group: All the Scheduler Codes used by
    all the Groups in Events for this session.

    :returns: A list of candidate tracks for this session.

    '''

    group_list = list(event_sched_codes_by_group)

    # A dict of dicts of lists of tracks.
    active_pool = {g: {c: [] for c in event_sched_codes_by_group[g]} for g in group_list}

    for group in event_sched_codes_by_group:
        for schedcode in event_sched_codes_by_group[group]:
            # Some Events have no Scheduler Code constraint.
            if 'NoCode' in schedcode:
                sched_code_constraint = ""
                query_args = (group,)
            else:
                sched_code_constraint = "AND s.sched_code = %s "
                query_args = (group, schedcode)

            # TODO: How does this break for multi-Cut Carts?
            query = ("SELECT c.number AS cart_number, c.artist AS artist, c.title AS title, "
                     "u.length AS length, "
                     "s.sched_code AS cart_sched_code "
                     "FROM CART AS c "
                     "LEFT JOIN CUTS AS u ON (c.number = u.cart_number) "
                     "LEFT JOIN CART_SCHED_CODES AS s ON (c.number = s.cart_number) "
                     "WHERE c.group_name = %s "
                     "AND u.length > 0 ")
            query += sched_code_constraint
            query += ("ORDER BY u.last_play_datetime ASC "
                      "LIMIT %s")
            query_args += (GLOBAL_STATS['pool_size'],)
            DEBUG_PRINT("fill_active_pool: query: {q}".format(q=query % query_args))
            rows = schedlib.RDDatabase(None).fetchall(query, query_args, dictionary=True)

            for row in rows:
                active_pool[group][schedcode].append(row)

    return active_pool

def get_track_from_pool(active_pool, group, schedcode, used_pool, artist_list):
    '''Get a track from the active pool, putting that track in the
    used pool. The "used" pool will be consulted if we run out of
    tracks in the pool (but this should *not* happen in real life).

    :param active_pool: The pool of candidate tracks for this session.
    :param group: The Group for which to get a track from the pool.
    :param schedcode: The Scheduler Code for which to get a track from the pool.
    :param used_pool: The pool of tracks that we have scheduled for this session.
    :param artist_list: An ArtistList instance, used to keep track of
    how long ago each artist was scheduled.
    :returns: A data structure containing the details of this track
    (see the SELECT query in fill_active_pool() for details).

    '''

    if active_pool[group][schedcode]:
        for index, track in enumerate(active_pool[group][schedcode]):
            DEBUG_PRINT("get_track_from_pool: index: {i}, track: {c}"
                        .format(i=index, c=track['cart_number']))
            # Take this track out of the pool if it is OK to schedule
            # this artist and if the track length is "sane".
            if artist_list.ok_to_schedule(track['artist']):
                # Why are there even any Cuts in the Library with Zero
                # length?
                if track['length'] <= 0:
                    print("get_track_from_pool: WARNING: Invalid Length. Removing from active_pool: selected: '{s}'"
                          .format(s=track), file=sys.stderr)
                    active_pool[group][schedcode].pop(index)
                    if track['artist'] in GLOBAL_STATS['invalid_length']:
                        GLOBAL_STATS['invalid_length'][track['artist']] += 1
                    else:
                        GLOBAL_STATS['invalid_length'][track['artist']] = 1
                    continue

                # Leave the track in the pool if there is no Group
                # Scheduler Code. This *should* result in a simple
                # rotation of the tracks in this group with this
                # Scheduler Code.
                # TODO: Is this the correct condition for leaving a track in the pool?
                if 'NoCode' not in schedcode:
                    active_pool[group][schedcode].pop(index)

                VERBOSE_PRINT("get_track_from_pool:Artist: '{a}', Title: '{t}', Length: {l}"
                              .format(a=track['artist'], t=track['title'], l=track['length']))
                break

            if track['artist'] in GLOBAL_STATS['skipped']:
                GLOBAL_STATS['skipped'][track['artist']] += 1
            else:
                GLOBAL_STATS['skipped'][track['artist']] = 1
    else:
        print("get_track_from_pool: NOTICE: unable to get a track from the pool in group '{g}', schedcode '{s}'"
              .format(g=group, s=schedcode), file=sys.stderr)
        track = None

    if track is not None:
        used_pool[group][schedcode].append(track)
        artist_list.increment(track['artist'])

    return track

def generate_import_lines(active_pool, used_pool, artist_list, timing, batch):
    '''Generate a list of "Import Lines" to be saved in a Music Data Import
    file.

    :param active_pool: the list of candidate tracks for this session
    :param used_pool: the list of tracks used in this session
    :param artist_list: the list of artists and how long ago each was last scheduled for play
    :param timing: the first hour and the last hour for this session
    :param batch: an instance of Batch()
    :returns: a list of tracks with timing suitable for saving to a Music Data Import file.

    '''

    group_list = list(active_pool)
    date_list = [batch.days[i].clock_date for i in range(len(batch.days))]
    import_list = {d: [] for d in date_list}

    # This gawdawful set of queries retrieves all the events (in time
    # order) for the requested Groups and the requested day(s) from
    # the Reference Service. Split into separate queries to properly
    # handle the Sunday-Monday boundary.
    query_base = ("SELECT sc.hour AS hour, cl.start_time AS starttime, "
                  "cl.length AS length, LCASE(ev.sched_group) AS sched_group, "
                  "ev.have_code AS schedcode1, ev.have_code2 as schedcode2 "
                  "FROM SERVICE_CLOCKS AS sc "
                  "LEFT JOIN CLOCK_LINES AS cl ON (sc.clock_name = cl.clock_name) "
                  "LEFT JOIN EVENTS AS ev ON (cl.event_name = ev.name) "
                  "WHERE sc.service_name = %s AND ")
    if timing['first_hour'] > timing['last_hour']:
        query = query_base + ("sc.hour BETWEEN %s AND 167 "
                              "AND ev.sched_group IN (")
        query += ", ".join(["%s" for _ in group_list])
        query += ") ORDER BY sc.hour, cl.start_time; "
        query += query_base + ("sc.hour BETWEEN 0 AND %s "
                               "AND ev.sched_group IN (")
        query += ", ".join(["%s" for _ in group_list])
        query += ") ORDER BY sc.hour, cl.start_time;"
        query_args = (ARGS.reference_service, timing['first_hour'],)
        query_args += tuple(group_list)
        query_args += (ARGS.reference_service, timing['last_hour'],)
        query_args += tuple(group_list)
    else:
        query = query_base + ("sc.hour BETWEEN %s AND %s "
                              "AND ev.sched_group IN (")
        query += ", ".join(["%s" for _ in group_list])
        query += ") ORDER BY sc.hour, cl.start_time;"
        query_args = (ARGS.reference_service, timing['first_hour'], timing['last_hour'],)
        query_args += tuple(group_list)

    DEBUG_PRINT("generate_import_lines: query: {q}".format(q=query % query_args))

    # mysql.connector.cursor.execute() returns an iterable when multi
    # is True. This happens because I broke the request into 2 SELECT
    # statements for the case of generating data import files for
    # Sunday *and* Monday ; see
    # https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html
    # (or equivalent) for details.
    for result in schedlib.RDDatabase(None).execute(query, query_args, multi=True, dictionary=True):
        VERY_VERBOSE_PRINT("generate_import_lines: NEW BATCH")
        previous = {
            'hour': -1,
            'start_time': 0,
            'length': 0,
        }
        rows = result.fetchall()

        for row in rows:
            # Rivendell "hours" are 0-167, so we need to coerce them
            # into 0-23 for each day. And we need to do the
            # calculations in milliseconds.
            this_hour_ms = (int(row['hour']) % 24) * ONE_HOUR_MS
            # Modulo 25 so we catch the last hour of the day.
            next_hour_ms = (this_hour_ms + ONE_HOUR_MS) % (ONE_HOUR_MS * 25)

            VERBOSE_PRINT("generate_import_lines: hour: {hr} ({ah}), next_hour_ms: {n}"
                          .format(hr=row['hour'], ah=int(row['hour']) % 24, n=next_hour_ms))

            # Use the Clock's Start Time if this is a new hour,
            # otherwise use the length of previous track for the
            # calulation.
            if int(row['hour']) > previous['hour']:
                start_time = this_hour_ms + int(row['starttime'])
                previous['start_time'] = 0

                # Similar for days.
                if this_hour_ms == 0:
                    batch_date = date_list.pop(0)

                VERY_VERBOSE_PRINT("generate_import_lines: NEW HOUR: {h}, start_time: {sthms} ({st})"
                                   .format(h=row['hour'], sthms=ms2HMS(start_time), st=start_time))
            else:
                start_time = previous['start_time'] + previous['length']
                VERY_VERBOSE_PRINT("generate_import_lines: OLD HOUR: {h}, start_time: {sthms} ({st})"
                                   .format(h=row['hour'], sthms=ms2HMS(start_time), st=start_time))

            if int(previous['start_time']) + int(previous['length']) >= next_hour_ms:
                VERBOSE_PRINT("generate_import_lines: NOTICE: at {t}, hour {h} overfilled due to len: {l}"
                              .format(t=ms2HMS(start_time), h=ms2HMS(this_hour_ms), l=previous['length']))
                continue

            if row['schedcode1'] == '':
                DEBUG_PRINT("generate_import_lines: No have_code for Event at {hr}, {st}"
                            .format(hr=row['hour'], st=row['starttime']))
                row['schedcode1'] = 'NoCode'

            track = get_track_from_pool(active_pool,
                                        row['sched_group'],
                                        row['schedcode1'],
                                        used_pool,
                                        artist_list)

            if track is None:
                VERBOSE_PRINT("generate_import_lines: NOTICE: track is 'None', using 'filler'")
                GLOBAL_STATS['dry_pool'] += 1
                track = {'cart_number': 0, 'title': 'MISSING', 'length': 0}

            import_list[batch_date].append({
                'day': int(row['hour'] / 24),
                'hour': int(row['hour']),
                'start_time': int(start_time),
                'cart_number': track['cart_number'],
                'title': track['title'],
                'length': int(track['length']),
            })

            previous['hour'] = row['hour']
            previous['start_time'] = start_time
            previous['length'] = track['length']

    return import_list

def save_import_list(import_list):
    '''Save the import list to one or more Music Data Import files. Files
    are created using the specified path template in the Music Data
    Import "Import Path" setting for the Implementation Service.

    File name "templates" are retrieved from the Rivendell Database
    using the statement "SELECT mus_path FROM SERVICES WHERE name =
    %s", and the name of the Implementation Service is substituted for
    "%s" (see the class definition in schedlib.OutputFile).

    :param import_list: A list of tracks and timing values.
    :returns: Nothing

    '''
    DEBUG_PRINT("save_import_list: NEW BATCH")

    for import_date in import_list:
        import_file = schedlib.OutputFile(ARGS.implementation_service, import_date, ARGS.verbose > 0)
        import_file.make_pathname()
        VERBOSE_PRINT("save_import_list: Date: '{d}' File: '{f}'."
                      .format(d=import_date, f=import_file.fullpath))

        with open(import_file.fullpath, 'w') as output_file:

            for track in import_list[import_date]:

                VERBOSE_PRINT("save_import_list: Date: {d}, Hour: {h}."
                              .format(d=import_date, h=track['hour']))

                # The spacing in this print statement must match the values
                # set in RDAdmin->Manage Services->[IMPLEMENTATION SERVICE]
                # See module docstring for details.
                #              |         |       | 2         3         4         5 |       6         7         8
                #              012345678901234567890123456789012345678901234567890123456789012345678901234567890
                output_line = "{start:8}  {track:6}  {title:<34}  {length:8}\n".format(start=ms2HMS(track['start_time']),
                                                                                       track=track['cart_number'],
                                                                                       title=track['title'][:34],
                                                                                       length=ms2HMS(track['length']))
                VERBOSE_PRINT(output_line)
                output_file.write(output_line)

def get_first_hour_from_date(start_date):
    '''Get the first hour of a day of the week for a scheduling session.

    :param start_date: the start date for this session as 'YYYY-MM-DD'
    :returns: The first week-hour (Zero-based) for the given starting date.

    Daily first hours of the week (see also Rivendell.SERVICE_CLOCKS):
    Mon: 0
    Tue: 24
    Wed: 48
    Thu: 72
    Fri: 96
    Sat: 120
    Sun: 144

    '''

    if not start_date:
        return TOMORROW_FIRST_HOUR

    # Allow some flexibility in the date they give us.
    date_regexp = re.compile(r'(?P<year>\d{4}).?(?P<month>\d{2}).?(?P<day>\d{2})')
    match = date_regexp.search(start_date)
    if match is None:
        print("btd-sched.py: ERROR: unknown date format, please use 'YYYY-MM-DD'", file=sys.stderr)
        sys.exit(2)

    d_parts = match.groupdict()
    normalized_start_time = "{yyyy}-{mm}-{dd}".format(yyyy=d_parts['year'], mm=d_parts['month'], dd=d_parts['day'])
    start_time = time.strptime(normalized_start_time, '%Y-%m-%d')

    return (int(time.strftime("%u", start_time)) - 1) * 24

def get_last_hour_from_date(start_date, days=1):
    '''Get the last hour in a scheduling session.

    :param start_date: The start date for this session as 'YYYY-MM-DD'
    :param days: The number of days to pick tracks for this session.
    :returns: The last week-hour (Zero-based) for the given starting
    date and number of days.

    Daily last hours of the week (see also Rivendell.SERVICE_CLOCKS):
    Mon: 23
    Tue: 47
    Wed: 71
    Thu: 95
    Fri: 119
    Sat: 143
    Sun: 167

    '''

    if start_date:
        first_hour = get_first_hour_from_date(start_date)
    else:
        first_hour = TOMORROW_FIRST_HOUR

    return (first_hour + ((days - 1) * 24) + 23) % 168

def ms2HMS(ms):
    '''Convert "ms" milliseconds into a string containing the two-digit
    hour, minutes, and seconds.

    :param ms: milliseconds
    :returns: A string formatted as 'HH:MM:SS' (zero-filled)

    '''

    hours = int(ms / 1000 / 60 / 60 % 24)
    minutes = int(ms / 1000 / 60 % 60)
    seconds = int(ms / 1000 % 60)

    hms = "{hh:02d}:{mm:02d}:{ss:02d}".format(hh=hours, mm=minutes, ss=seconds)
    return hms

def main():
    '''Prepare a data import file for merging with a Log using Rivendell's
    RDLogManager.

    '''
    # Seed the "scheduled_ago" list from storage.
    artist_list = ArtistList(ARGS.artist_separation, ARGS.verbose > 2)

    # Use the counter in Batch() to get the number of each Scheduler
    # Code for this session.
    batch = schedlib.Batch(ARGS.reference_service, ARGS.start_date, ARGS.days)

    timing = {
        'first_hour': get_first_hour_from_date(ARGS.start_date),
        'last_hour' : get_last_hour_from_date(ARGS.start_date, ARGS.days),
    }

    event_sched_codes_by_group, event_count = get_event_sched_codes(timing)
    GLOBAL_STATS['pool_size'] = calculate_pool_size(batch, event_count)
    active_pool = fill_active_pool(event_sched_codes_by_group)

    # A dict of dicts of lists matching the dict in active_pool.
    used_pool = {g: {c: [] for c in event_sched_codes_by_group[g]} for g in list(active_pool)}

    import_list = generate_import_lines(active_pool, used_pool, artist_list, timing, batch)
    artist_list.record_artists_schedule_age()

    save_import_list(import_list)

    if ARGS.verbose > 3:
        pprint.pprint(used_pool, stream=sys.stderr)

    if ARGS.stats:
        pprint.pprint(GLOBAL_STATS, stream=sys.stderr)

if __name__ == '__main__':

    PARSER = argparse.ArgumentParser(prog='btd_sched',
                                     description='Pick and schedule tracks to merge using RDLogManager.')
    PARSER.add_argument('implementation_service',
                        help="The name of the Rivendell Service containing one or more Clocks containing one or more Events that specify 'IMPORT: From Music'",
                        action='store')
    PARSER.add_argument('-V', '--version',
                        help='Display this app version string.',
                        action='version',
                        version='%(prog)s: ' + __version__)
    PARSER.add_argument('-v', '--verbose',
                        help='Be chatty about progress. Use up to 3 times for more chattiness.',
                        default=0,
                        action='count')
    PARSER.add_argument('-a', '--artist-separation',
                        type=int,
                        help='Specify the number of tracks before and artist can be scheduled again.',
                        default=DEFAULT_ARTIST_SEPARATION,
                        action='store')
    PARSER.add_argument('-d', '--days',
                        type=int,
                        help='Specify the number of days to schedule tracks (default is one day).',
                        default=1,
                        action='store')
    PARSER.add_argument('-o', '--output-dir',
                        help='Name the output directory for the import data file. This overrides the Music Data Import Path set in RDAdmin.',
                        action='store')
    PARSER.add_argument('-g', '--groups',
                        help='Specify a comma-separated list of Rivendell Groups to schedule.',
                        default='music',
                        action='store')
    PARSER.add_argument('-r', '--reference-service',
                        help='Specify a Rivendell Service name to use as "reference" for Clocks and Events.',
                        default=DEFAULT_REFERENCE_SERVICE,
                        action='store')
    PARSER.add_argument('-s', '--start-date',
                        help='Specify the starting date (as YYYY-MM-DD) for scheduling tracks (default is "tomorrow").',
                        default=time.strftime("%F", time.localtime(time.time() + (3600 * 24))),
                        action='store')
    PARSER.add_argument('-S', '--stats',
                        help='Output global statistics at the end of the scheduling session.',
                        default=False,
                        action='store_true')

    ARGS = PARSER.parse_args()

    VERBOSE_PRINT = schedlib.my_print if ARGS.verbose > 0 else lambda *a, **k: None
    VERY_VERBOSE_PRINT = schedlib.my_print if ARGS.verbose > 1 else lambda *a, **k: None
    DEBUG_PRINT = schedlib.my_print if ARGS.verbose > 2 else lambda *a, **k: None

    GLOBAL_STATS = {
        'pool_size': 0,
        'invalid_length': {},
        'skipped': {},
        'dry_pool': 0,
    }

    if ARGS.groups:
        VERY_VERBOSE_PRINT("btd_sched.py: Filling pool with Carts from Group '{group}'."
                           .format(group=ARGS.groups))

    main()

    sys.exit()
