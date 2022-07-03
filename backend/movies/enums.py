# Instead of importing any libs to do bidirectional dictionaries (https://github.com/jab/bidict), just store the inverse map as well.
def invertEnum(enum):
    inverted = {}
    for k, v in enum.items():
        if v in inverted:
            raise ValueError('Please ensure that labels map 1:1 with values')
        inverted[v] = k
    return inverted

# Enumerates user facing values keyed by internal (db) values
GENRES = {
    None: 'N/A',
    0: 'Action',
    1: 'Horror',
    2: 'Comedy',
    3: 'Adventure',
    4: 'Drama',
    5: 'Thriller/Suspense',
    6: 'Musical',
    7: 'Romantic Comedy',
    8: 'Western',
    9: 'Black Comedy',
    10: 'Other'
}
GENRES_INV = invertEnum(GENRES)

RATING = {
    None: 'N/A',
    0: 'G',
    1: 'PG',
    2: 'PG-13',
    3: 'R',
    4: 'Not Rated'
}
RATING_INV = invertEnum(RATING)

# For filtering based on test results. Stringified because it's query params.
TEST_RESULT = {
    None: 'N/A',
    '1': 'Pass',
    '0': 'Fail'
}

# For selecting the ordering of movies so maps from column name.
MOVIE_ORDERING = {
    'title': 'Movie Title',
    'releaseDate': 'Release Date',
    'gross': 'Top Grossing'
}

# Maps month to numerical value. Used when loading data to the db.
MONTH_NAMES = {
    'Jan': '01',
    'Feb': '02',
    'Mar': '03',
    'Apr': '04',
    'May': '05',
    'Jun': '06',
    'Jul': '07',
    'Aug': '08',
    'Sep': '09',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12'
}