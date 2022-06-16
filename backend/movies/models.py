from django.db import models
from model_utils.models import TimeStampedModel
from model_utils import Choices

# All movie metadata models/tables

# Metadata about the movie + the individual test results (which are in the same table because they're always accessed together)
class MovieMetaModel(TimeStampedModel):
    GENRE = Choices(  # Enumerates all the genres. We store them as ints in the DB for faster lookups and to save space in the DB.
        (0, 'Action'),
        (1, 'Horror'),
        (2, 'Comedy'),
        (3, 'Adventure'),
        (4, 'Drama'),
        (5, 'Thriller/Suspense'),
        (6, 'Musical'),
        (7, 'Romantic Comedy'),
        (8, 'Western'),
        (9, 'Black Comedy'),
        (10, 'Other')
    )

    title = models.CharField(max_length=100, db_index=True, unique=True)
    releaseDate = models.DateField(db_index=True)
    genre = models.PositiveSmallIntegerField(choices=GENRE, db_index=True)
    gross = models.PositiveBigIntegerField(db_index=True)
    image = models.ImageField(upload_to="posters/", default="posters/default.jpg")  # TODO: add a copy of this field that's an icon version for smoother searching https://stackoverflow.com/questions/63759605/django-soft-resize-uploaded-image-to-multiple-sizes-and-upload-to-respective-fol
    bechdelResult = models.BooleanField(null=True, blank=True)

# Detailed Results of the Tests for a given movie.
# Note that the actual proper result of each test is in the MovieMetaModel
# All tests are in the same table since they're always accessed together.
class TestResultsModel(TimeStampedModel):
    movieId = models.OneToOneField(MovieMetaModel, primary_key=True, on_delete=models.CASCADE)
    bRule1Result = models.BooleanField(null=True, blank=True, help_text="Has at least two named women")
    bRule2Result = models.BooleanField(null=True, blank=True, help_text="Who speak to each other")
    bRule3Result = models.BooleanField(null=True, blank=True, help_text="About something other than a man")
    notes = models.CharField(max_length=255, blank=True, null=True)
