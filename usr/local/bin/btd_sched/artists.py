'''ArtistList encapsulates a collection of artists and various aspects
about them as used in the Scheduler.

'''

import sys
import mysql.connector
from schedlib import my_print
from rivendell_lib import RDDatabase

class ArtistList():
    '''A dict indexed by artist, used to calculate "artist separation" for
    the generated log. Maintains a persistent list of artists and the
    number of units ago each was last scheduled.

    '''
    def __init__(self, separation, debug):
        '''Initializes self.artists as a dict with the existing artists
        as keys and their scheduled_ago count as values.

        :param separation: Number of "units" between scheduled events for this artist.
        :param debug: Debug mode boolean.

        '''

        self.separation = separation
        self.debug = debug

        self.query = ("SELECT * "
                      "FROM sched.artists "
                      "ORDER BY sched.artists.name")

        try:
            self.artists = dict(RDDatabase(None).fetchall(self.query, dictionary=False))
            self.storage_method = 'db'
        except mysql.connector.errors.ProgrammingError as e:
            if debug:
                print("Artist: unable to read database table sched.artists; error: '{e}"
                      .format(e=e), file=sys.stderr)
            self.initialize()

    def initialize(self):
        '''Initialize an empty data set.
        '''

    def migrate_schema(self):
        '''Gracefully handle changes to the data we store.
        '''

    def scheduled_ago(self, artist):
        '''Return the value of scheduled_ago for the artist or None if the artist
        is unknown.

        :param artist: The artist to check.

        :returns: Number of "units" ago the named artist was
        scheduled, or None if the artist is not in the list.

        '''
        if artist in self.artists:
            return int(self.artists[artist])

        return None

    def ok_to_schedule(self, artist):
        '''Let them know if the given artist is OK to schedule.

        :param artist: The artist to check for scheduling.

        :returns: Boolean indicating whether it is okay to schedule
        this artist.

        '''
        if artist == "" or artist is None:
            artist = "xx-missingartist-xx"

        if artist.lower() in self.artists and self.artists[artist.lower()] < self.separation:
            return False

        return True

    def increment(self, artist):
        '''Increment all artist "scheduled_ago" count by one. Reset the named
        artist to one.

        :param artist: The artist to reset to One.

        :returns: Nothing.

        '''

        if artist == "" or artist is None:
            artist = "xx-missingartist-xx"

        # Add this artist if it is not already on the list. We set it
        # to the actual count in the enumeration below.
        if artist.lower() not in self.artists:
            self.artists[artist.lower()] = 0

        for a in self.artists:
            self.artists[a] += 1

    def record_artists_schedule_age(self):
        '''Save all artists and their "scheduled_ago" values in the database.

        :returns: Nothing.

        '''
        for _, artist in enumerate(self.artists):
            if self.debug:
                my_print("ArtistList.record_artists_schedule_age: artist: {n}, scheduled_ago: {c}"
                         .format(n=artist.lower(), c=self.artists[artist.lower()]))

            query = ("INSERT INTO sched.artists (sched.artists.name, sched.artists.scheduled_ago) VALUES "
                     "(%s, %s) "
                     "ON DUPLICATE KEY UPDATE "
                     "scheduled_ago = %s")
            query_args = (artist.lower(), self.artists[artist.lower()], self.artists[artist.lower()])
            if self.debug:
                my_print("ArtistList.record_artists_schedule_age: query: '{q}' args: {args}, artist: '{artist}'"
                         .format(q=query, args=query_args, artist=artist.lower()))
            RDDatabase(None).execute(query, query_args)

        return True
