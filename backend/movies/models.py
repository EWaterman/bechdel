from django.db import models
from model_utils.models import TimeStampedModel
from model_utils import Choices

# All movie metadata models/tables

# Metadata about the movie + the individual test results (which are in the same table because they're always accessed together)
class MovieMetaModel(TimeStampedModel):
    class Genre(models.IntegerChoices):
        ACTION = 0
        HORROR = 1
        COMEDY = 2
        ADVENTURE = 3
        DRAMA = 4
        THRILLER = 5
        MUSICAL = 6
        ROMCOM = 7
        WESTERN = 8
        BCOMEDY = 9
        OTHER = 10

    # TODO: add rating field
    class Rating(models.IntegerChoices):
        G = 0
        PG = 1
        PG13 = 2
        R = 3
        NR = 4
    
    title = models.CharField(max_length=100, db_index=True, unique=True)
    releaseDate = models.DateField(db_index=True)
    genre = models.PositiveSmallIntegerField(choices=Genre.choices, db_index=True)
    gross = models.PositiveBigIntegerField(db_index=True)
    # TODO: add a copy of this field that's an icon version for smoother searching
    # https://stackoverflow.com/questions/63759605/django-soft-resize-uploaded-image-to-multiple-sizes-and-upload-to-respective-fol
    # https://stackoverflow.com/questions/32125053/how-to-resize-image-and-save-it-django
    image = models.ImageField(upload_to="posters/", default="posters/default.jpg")
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
