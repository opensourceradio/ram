"""Classes related to Rivendell Artists.

Artist uses sqlalchemy to represent a single artist and various
aspects about it as used in the Scheduler.

"""

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Artist(Base):
    """An artist.

    Contains a single artist and its related scheduling information,
    such as the "age" to calculate "artist separation" for
    the generated merge file. Maintains a persistent list of artists
    and the number of units ago each was last scheduled.

    """

    __tablename__ = 'artists'
    name = Column(Unicode(34), primary_key=True)
    age = Column(Integer, default=1)

    def __repr__(self):
        """Represent ourself to the world."""
        return f"'{self.name}':{self.age}"

    def reset(self):
        """Reset age to 0. This happens when the artist gets scheduled."""
        self.age = 1

    def __add__(self, value):
        """Increment the age counter for the named artist."""
        self.age = self.age + value
        return self

    def __iadd__(self, value):
        """In-place increment (+=) of age counter for the named artist."""
        self.age += value
        return self

    def __sub__(self, value):
        """Decrement the artist's age counter."""
        self.age = self.age - value
        return self

    def __isub__(self, value):
        """In-place decrement (-=) of artist's age counter."""
        self.age -= value
        return self

class Artists():
    """The collection of all artists."""

    def __init__(self, method, location, separation):
        """Make a group of artists.

        :param method: The database backend method (sqlite, mysql,
        etc.).
        :param location: The location of the backend database.
        :param separation: The integer value representing the number
        of "units" that must transpire before an artist may be
        scheduled.

        """
        self.method = method
        self.location = location
        self.separation = separation

        self.engine = create_engine(method + '://' + location, echo=False)
        session = sessionmaker(bind=self.engine)
        self.session = session()
        Base.metadata.create_all(self.engine)

    @property
    def all(self):
        """Read the data source and return all the rows a dictionary."""
        return {a.name: a.age for a in self.session.query(Artist).all()}

    def add(self, artist):
        """Add this artist to the list."""
        try:
            new_artist = Artist(name=artist.lower(), age=1)
            self.session.add(new_artist)
            #self.session.commit()
        except:
            print("Artist: ERROR: unable to add new artist '{a}'."
                  .format(a=artist))
            return False
        return True

    def bump(self, artist):
        """Increment the age counter for all artists in the list.

        Then reset the counter for 'artist' to 1 since this is the artist
        we are scheduling.

        """
        for one_of_all_artists in self.session.query(Artist).all():
            one_of_all_artists += 1

        if artist is None:
            artist = 'xx-missing-artist-xx'

        this_artist = self.session.query(Artist).filter_by(name=artist.lower()).first()
        if this_artist is None:
            self.add(artist)
        else:
            this_artist.reset()

    def ok_to_schedule(self, artist):
        """Whether it's OK to schedule this artist.

        Has this artist been scheduled more recently than "separation"
        units?
        """
        if artist is None:
            artist = 'xx-missing-artist-xx'

        a = self.session.query(Artist).filter_by(name=artist.lower()).first()

        if a is None:
            # Apparently we have not yet seen this artist.
            if not self.add(artist):
                return False
            return True

        if a.age < self.separation:
            return False

        return True
