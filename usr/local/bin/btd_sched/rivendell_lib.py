"""A collection of convenience classes.

Aand functions for interacting with a Rivendell database and web API.

"""

import sys
import re
import configparser
import mysql.connector

class RDDBConfig():
    """A Rivendell database configuration.

    We look the credentials up in the standard location if they are not
    passed to the constructor.

    """

    def __init__(self, db_credentials=None):
        """Construct an instance.

        Make a (possibly empty) database access configuration. Uses the
        credentials in db_credentials if supplied, otherwise uses the
        credentials in /etc/rd.conf.

        :param db_credentials: A string containing colon-separated (:)
        database credentials.

        """
        self.db_credentials = db_credentials
        self.__config = None

        self.db_credential_pattern = '^(?P<user>.*?):(?P<password>.*?):(?P<host>.*?):(?P<database>.*)$'
        self.db_credential_re = re.compile(self.db_credential_pattern)
        self.credentials = {}

        if self.db_credentials is not None:
            matches = self.db_credential_re.search(self.db_credentials)
            self.credentials = matches.groupdict()
            return

        self.__config = configparser.ConfigParser()

        try:
            self.__config.read_file(open('/etc/rd.conf'))
        except FileNotFoundError as e:
            print("What? No config? I quit ({e}).".format(e=e))
            sys.exit()

        self.credentials = {
            'user': self.__config.get('mySQL', 'Loginname'),
            'password': self.__config.get('mySQL', 'Password'),
            'host': self.__config.get('mySQL', 'Hostname'),
            'database': self.__config.get('mySQL', 'Database'),
        }
        return

    def get_config_pattern(self):
        """Get the config RE pattern.

        Return the regular expression pattern that we use to split the
        credential into its constituent parts.
        """
        return self.db_credential_pattern

    def get_credentials(self):
        """Return the credentials for this instance of the object."""
        return self.credentials

    def get_config(self):
        """Return the configuration from /etc/rd.conf as a configparser object."""
        return self.__config

class RDDatabase():
    """An authenticated database connection."""

    def __init__(self, config):
        """Instantiate an RDDatabase.

        Connect to the database specified in config (or in
        /etc/rd.conf), and remember that connection.

        :param config: A string containing colon-separated (:)
        database credentials.

        """
        self.config = RDDBConfig(config)
        self.saved_cursor = None
        self.cnx = mysql.connector.connect(
            user=self.config.credentials['user'],
            password=self.config.credentials['password'],
            host=self.config.credentials['host'],
            database=self.config.credentials['database'])

    def close(self):
        """Close a previously opened cursor."""
        self.saved_cursor.close()

    def cursor(self, dictionary=False):
        """Set a cursor on the database.

        :param dictionary: A boolean indicating whether to return the
        query results as a dict. Default: False

        :returns: The cursor.

        """
        self.saved_cursor = self.cnx.cursor(dictionary=dictionary)
        return self.saved_cursor

    def execute(self, query, query_args=None, dictionary=False, multi=False):
        """Set a cursor on the database and execute the given query.

        :param query: A string containing a valid MariaDB statement,
        possibly containing wildcards to be substituted with
        query_args.
        :param query_args: A tuple containing values to substitute
        wildcards in the query.
        :param dictionary: A boolean indicating whether to return the
        query results as a dict. Default: False
        :param multi: A boolean indicating whether to accept multiple
        statements in a single query. Default False.

        :returns: The result of the statement (see
        https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html
        for details).

        """
        if not query:
            return None

        self.cursor(dictionary=dictionary)
        return self.saved_cursor.execute(query, query_args, multi=multi)

    def fetchone(self, query, query_args=None, dictionary=False, multi=False):
        """Set a cursor on the database, execute the query and return the first result.

        :param query: A string containing a valid MariaDB statement,
        possibly containing wildcards to be substituted with
        query_args.
        :param query_args: A tuple containing values to substitute
        wildcards in the query.
        :param dictionary: A boolean indicating whether to return the
        query results as a dict. Default: False
        :param multi: A boolean indicating whether to accept multiple
        statements in a single query. Default False.

        :returns: The result of the statement (see
        https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-fetchone.html
        for details).

        """
        if not query:
            return None

        self.cursor(dictionary=dictionary)
        self.saved_cursor.execute(query, query_args, multi=multi)
        return self.saved_cursor.fetchone()

    def fetchnext(self):
        """Fetch the next result of a query.

        :returns: The result of the statement (see
        https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-fetchone.html
        for details).

        """
        if not self.saved_cursor:
            return None

        return self.saved_cursor.fetchone()

    def fini(self):
        """Fetch "all the rest" of the rows.

        Ostensibly from a previous query, but also from a previously
        execute()'d query. Then close() the database cursor.

        :returns: Any remaining rows from a previously requested
        execute(). Also close()s the database. See
        https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-close.html
        for details.

        """
        if not self.saved_cursor:
            return None

        try:
            rows = self.saved_cursor.fetchall()
        except mysql.connector.errors.InterfaceError as e:
            print("RDDatabase.fini(): ERROR: in completing fetch: '{e}'. Likely already fecthed all the rows."
                  .format(e=e), file=sys.stderr)
            return None

        self.close()

        return rows

    def fetchall(self, query, query_args=None, dictionary=False, multi=False):
        """Set a cursor on the database, execute the query and return all results.

        :param query: A string containing a valid MariaDB statement,
        possibly containing wildcards to be substituted with
        query_args.
        :param query_args: A tuple containing values to substitute
        wildcards in the query.
        :param dictionary: A boolean indicating whether to return the
        query results as a dict. Default: False
        :param multi: A boolean indicating whether to accept multiple
        statements in a single query. Default False.

        :returns: All the rows that satisfy the statement in
        query. Also close()s the database. See
        https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-close.html
        for details.

        """
        if not query:
            return None

        cursor = self.cursor(dictionary=dictionary)
        cursor.execute(query, query_args, multi=multi)
        rows = cursor.fetchall()
        self.close()

        return rows
