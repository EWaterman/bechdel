from enum import Enum

# Maps strings to ints to save space in the DB and to
# avoid spelling mistakes when inserting/searching

class Genre(Enum):
    ACTION = 0
    ADVENTURE = 1
    HORROR = 2
    DRAMA = 3
    COMEDY = 4
    MUSICAL = 5
    THRILLER = 6
    ROMANTIC_COMEDY = 7
    BLACK_COMEDY = 8

class Rating(Enum):
    G = 0
    PG = 1
    PG_13 = 2
    R = 3
    NOT_RATED = 4