# Instead of importing any libs to do bidirectional dictionaries (https://github.com/jab/bidict), just store the inverse map as well.
def invertEnum(enum):
    inverted = {}
    for k, v in enum.items():
        if v in inverted:
            raise ValueError('Please ensure that labels map 1:1 with values')
        inverted[v] = k
    return inverted

GENRES = {
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

RATINGS = {
    0: 'G',
    1: 'PG',
    2: 'PG-13',
    3: 'R',
    4: 'Not Rated'
}
RATINGS_INV = invertEnum(RATINGS)

# A copy of this is hardcoded into any forms that filter by test result
TEST_RESULT = {
    'Pass': True,
    'Fail': False,
}