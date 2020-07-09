'''A set of classes and functions for btd_sched.py (and others?).
'''

import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
import re
from iteration_utilities import deepflatten
from rivendell_lib import RDDatabase

def my_print(*p_args, **p_kwargs):
    '''My print function that always goes to STDERR.

    '''
    print(*p_args, **p_kwargs, file=sys.stderr)

class Event():
    '''An Event is an atomic element containing rules for scheduling Carts.
    '''
    def __init__(self, service_name, event_name):
        '''Instantiate an Event with the associated fields.

        :param service_name: The name of (typically) the Rivendell
        Reference Service.
        :param event_name: The name of a Rivendell Event to retrieve.

        '''
        self.attributes = {}
        self.service_name = service_name
        self.event_name = event_name
        self.query = ("SELECT DISTINCT LCASE(ev.sched_group) AS sched_group, "
                      "ev.have_code AS schedcode1, ev.have_code2 AS schedcode2, "
                      "ev.artist_sep AS artist_sep, ev.title_sep AS title_sep "
                      "FROM SERVICE_CLOCKS sc "
                      "LEFT JOIN CLOCK_LINES cl ON (sc.clock_name = cl.clock_name) "
                      "LEFT JOIN EVENTS ev ON (cl.event_name = ev.name) "
                      "WHERE sc.service_name = %s AND "
                      "ev.name = %s")
        self.query_args = (service_name, event_name,)
        db = RDDatabase(None)
        event = db.fetchone(self.query, self.query_args, dictionary=True)
        self.attributes['sched_group'] = event['sched_group']
        self.attributes['schedcode1'] = event['schedcode1']
        self.attributes['schedcode2'] = event['schedcode2']
        self.attributes['artist_sep'] = event['artist_sep']
        self.attributes['title_sep'] = event['title_sep']
        self.attributes['codes'] = event['schedcode1'] + '|' + event['schedcode2']
        db.close()

    def list_attributes(self):
        '''Return the list of Event attributes.
        '''
        return list(dict.fromkeys(self.attributes))

    def get_query(self):
        '''Return a string containing the formatted query for an Event.

        '''
        return self.query % self.query_args

class Hour():
    '''An Hour is a list of Events each with a start time and a duration
    (length).

    '''
    def __init__(self, service_name, hour):
        '''Instantiate an Hour, getting all the hour's Events.

        :param service_name: The name of (typically) the Rivendell
        Reference Service.
        :param hour: A "Rivendell hour of the week" to retrieve (from
        0 [Midnight Monday] to 167 [11pm Sunday]).

        '''
        self.service_name = service_name
        self.hour = hour
        self.events = []
        self.query = ("SELECT cl.start_time AS start_time, "
                      "cl.length AS length, cl.event_name AS event_name "
                      "FROM CLOCK_LINES AS cl "
                      "LEFT JOIN SERVICE_CLOCKS AS sc ON (sc.clock_name = cl.clock_name) "
                      "WHERE sc.service_name = %s AND hour = %s")
        self.query_args = (self.service_name, self.hour,)
        db = RDDatabase(None)
        rows = db.fetchall(self.query, self.query_args, dictionary=True)
        for row in rows:
            self.events.append({
                'start_time': row['start_time'],
                'length': row['length'],
                'event': Event(service_name, row['event_name'])
            })

    def values(self, attribute):
        '''Return a list of unique values and their counts for the given
        Events attribute in this Hour. See the constructor for the
        list of attributes for each Event.

        :param attribute: An Event attribute (see Event()) for which
        to retrieve values.

        '''
        values = {}
        # If the first one has this attribute, they will all have it.
        if not attribute in self.events[0]['event'].attributes:
            print("Hour::attributes(): ERROR: no such attribute: {attr}. Try one of '{l}'."
                  .format(attr=attribute, l=self.events[0]['event'].list_attributes()), file=sys.stderr)
            return None

        values_for_hour = [self.events[x]['event'].attributes[attribute]
                           for x, _ in enumerate(self.events)]

        # Get the counts of values for each instance of the specified
        # Event attribute for this Hour.
        for v in list(dict.fromkeys(values_for_hour)):
            values[v] = values_for_hour.count(v)

        return values

    def get_query(self):
        '''Return a string containing the formatted query with query_args for
        an Hour.

        '''
        return self.query % self.query_args

class Day():
    '''A Day is a list of 24 Hours.
    '''
    def __init__(self, service_name, clock_date):
        '''Instantiate a Day, getting all 24 Hours.

        :param service_name: The name of (typically) the Rivendell
        Reference Service.
        :param clock_date: A date (in the form YYYY-MM-DD,
        Zero-filled) representing the day for which to generate a
        Rivendell Log. This date is simply used to calculate the
        starting hour of the week (from 0 [Midnight Monday] to 167
        [11pm Sunday]).

        '''
        self.hours = []
        self.service_name = service_name
        self.clock_date = clock_date
        # These "hours" are Rivendell hours of the week (0 - 167).
        self.first_hour = (int(time.strftime("%u", time.strptime(clock_date, "%Y-%m-%d"))) - 1) * 24
        self.last_hour = self.first_hour + 23
        self.query = ("SELECT hour, clock_name FROM SERVICE_CLOCKS "
                      "WHERE service_name = %s AND "
                      "hour BETWEEN %s AND %s")
        self.query_args = (service_name, self.first_hour, self.last_hour)
        db = RDDatabase(None)
        rows = db.fetchall(self.query, self.query_args, dictionary=True)
        for row in rows:
            self.hours.append({
                'hour': row['hour'],
                'clock_name': row['clock_name'],
                'clock': Hour(service_name, row['hour'])
            })

    def values(self, attribute):
        '''Return a sorted list of unique values for the given Event attribute
        for the Day. Technique from
        https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists

        '''
        values = {}
        values_by_hour = [[self.hours[h]['clock'].events[e]['event'].attributes[attribute]
                           for e, _ in enumerate(self.hours[h]['clock'].events)]
                          for h, _ in enumerate(self.hours)]
        # Get the counts of values for each instance of the specified
        # Event attribute for this Day.
        for v in list(dict.fromkeys([item for sublist in values_by_hour for item in sublist])):
            values[v] = [item for sublist in values_by_hour for item in sublist].count(v)

        return values

    def get_query(self):
        '''Return a string containing the formatted query with query_args for
        a Day.

        '''
        return self.query % self.query_args

class Batch():
    '''A Batch is a collection of Days in a scheduling session.
    '''
    def __init__(self, service_name, start_date, day_count=1):
        '''Instantiate a Batch getting all the Days, Hours and Events.

        :param service_name: The name of (typically) the Rivendell
        Reference Service.
        :param start_date: The batch start date (in the form
        YYYY-MM-DD, Zero-filled).
        :param day_count: The number of days in this batch.

        A specific Event in a Batch is referenced with, e.g.,
        Batch('service-name',
        'yyyy-mm-dd').days[daynum].hours[hournum]['clock'].events[eventnum]['event'].event_name

        '''
        self.days = []
        self.service_name = service_name
        self.start_date = start_date
        self.day_count = day_count
        self.days = [Day(service_name,
                         (datetime.strptime(start_date, '%Y-%m-%d') +
                          timedelta(days=count)).strftime("%F"))
                     for count in range(day_count)]

    def values(self, attribute):
        '''Return a dict of occurances indexed by "attribute" for the given Event attribute
        for the entire Batch. See above for the details.

        :param attribute: An Event attribute to summarize.

        :returns: A dict indexed by attribute values, the dict values
        being the number of occurances of that attribute value.

        '''
        values = {}
        values_by_day_by_hour = [[[self.days[d].hours[h]['clock'].events[e]['event'].attributes[attribute]
                                   for e, _ in enumerate(self.days[d].hours[h]['clock'].events)]
                                  for h, _ in enumerate(self.days[d].hours)]
                                 for d, _ in enumerate(self.days)]
        # Get the counts of values for each instance of the specified
        # Event attribute for this whole Batch.
        for v in list(dict.fromkeys(list(deepflatten(values_by_day_by_hour, depth=2)))):
            values[v] = list(deepflatten(values_by_day_by_hour, depth=2)).count(v)

        return values

    def refresh(self):
        '''Reload the entire configuration using the original instantiation
        values. This might be used in a long-running process during
        which the database may have changed.

        '''
        self.days = [Day(self.service_name,
                         (datetime.strptime(self.start_date, '%Y-%m-%d') +
                          timedelta(days=count)).strftime("%F"))
                     for count in range(self.day_count)]

class OutputFile():
    '''A class encapsulating an output file, including name generation,
    path manipulation, and reading and writing the output file.

    '''
    def __init__(self, service_name, import_date, debug):
        '''Construct the object and set the directory name for the file.

        :param service_name: The (case-insensitive) Implementation Service name.
        :param import_date: the date (in YYYY-MM-DD format) for the output file.
        :param debug: Debug mode (boolean)

        '''

        self.service_name = service_name
        self.import_date = import_date
        self.debug = debug
        self.fullpath = None

        self.query = "SELECT mus_path FROM SERVICES WHERE name = %s"
        self.query_args = (self.service_name,)
        rows = RDDatabase(None).fetchall(self.query, self.query_args, dictionary=True)

        self.mus_path = Path(rows[0]['mus_path'])

    def get_query(self):
        '''Return a string containing the formatted query with query_args for
        a Day.

        :returns: The query with the '%s' directive(s) expanded.

        '''
        return self.query % self.query_args

    def make_directory(self):
        '''Create the directory hierarchy if it does not exist.

        :returns: True or False depending on the success or failure of
        creating the directory

        '''

        if not self.mus_path.parent.is_dir():
            try:
                if self.debug:
                    my_print("make_directory: '{dir}' is missing, attempting to create it."
                             .format(dir=str(self.mus_path.parent.name)))
                self.mus_path.parent.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                print("schedlib.OutputFile: ERROR: Unable to create directory '{d}' ('{e}')."
                      .format(d=self.mus_path.parent.name, e=e), file=sys.stderr)
                return False

        return True

    def make_name(self):
        '''Normalize the import date specified in the constructor.

        :returns: A string representing the import date. Also resets self.import_date.

        '''

        date1_regexp = re.compile(r'(?P<year>\d{4}).?(?P<month>\d{1,2}).?(?P<day>\d{1,2})')
        match = date1_regexp.search(self.import_date)
        if match is None:
            date2_regexp = re.compile(r'(?P<day_or_month>\d{1,2}).?(?P<month_or_day>\d{1,2}).?(?P<year>\d{4})')
            match = date2_regexp.search(self.import_date)
            if match is None:
                print("btd-sched.py: ERROR: '{date}': unknown date format, please use 'YYYY-MM-DD' or similar."
                      .format(date=self.import_date), file=sys.stderr)
                sys.exit(1)
            d_parts = match.groupdict()

            # We cannot be assured this will work as they intend, but
            # give it a shot.
            if int(d_parts['day_or_month']) > 12:
                d_parts['day'] = d_parts['day_or_month']
                d_parts['month'] = d_parts['month_or_day']
            elif int(d_parts['month_or_day']) > 12:
                d_parts['day'] = d_parts['month_or_day']
                d_parts['month'] = d_parts['day_or_month']
            else:
                print("make_name: ERROR: '{date}': ambiguous date, please use 'YYYY-MM-DD' or similar."
                      .format(date=self.import_date), file=sys.stderr)
                return None
        else:
            d_parts = match.groupdict()

        self.import_date = "{yyyy}-{mm}-{dd}.txt".format(yyyy=d_parts['year'],
                                                         mm=d_parts['month'],
                                                         dd=d_parts['day'])
        if self.debug:
            print("make_name: set self.filename to '{f}'."
                  .format(f=self.import_date), file=sys.stderr)

        return self.import_date

    def make_pathname(self):
        '''Create a Path object pointing to the full path of the output file.

        :returns: a Path object containing the full path of the
        file. Also saved with the object as self.fullpath.

        '''

        # Try to avoid breakage if they use Rivendell-specific
        # ("non-strftime(3)") placeholders in the Import Path setting
        # in Rivendell.SERVICES.mus_path.
        try:
            import_date = Path(time.strftime(self.mus_path.name,
                                             time.strptime(self.import_date,
                                                           '%Y-%m-%d')))
        except ValueError as e:
            if self.debug:
                print("schedlib.OutputFile: unknown directive in Music Data Import Path: {e}"
                      .format(e=e), file=sys.stderr)
            import_date = self.make_name()

        self.fullpath = self.mus_path.parent / import_date
        return self.fullpath
