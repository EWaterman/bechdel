from rest_framework import serializers

from .models import MovieMetaModel, TestResultsModel
from .enums import GENRES, GENRES_INV

SHORT_TITLE_MAX_LEN = 30

# Handles conversion between json and python models

# A field that takes a field's value as the key and returns the associated value for serialization
class KeyValueField(serializers.Field):
    labels = {}
    inverted_labels = {}

    def __init__(self, labels, inverted_labels, *args, **kwargs):
        self.labels = labels
        self.inverted_labels = inverted_labels
        return super(KeyValueField, self).__init__(*args, **kwargs)

    def to_representation(self, obj):
        if type(obj) is list:
            return [self.labels.get(o, None) for o in obj]
        else:
            return self.labels.get(obj, None)

    def to_internal_value(self, data):
        if type(data) is list:
            return [self.inverted_labels.get(o, None) for o in data]
        else:
            return self.inverted_labels.get(data, None)


class MovieDetailsSerializer(serializers.ModelSerializer):
    genre = KeyValueField(GENRES, GENRES_INV)
    releaseDate = serializers.DateField(format="%b. %d, %Y")
    gross_clean = serializers.SerializerMethodField()
    title_short = serializers.SerializerMethodField()
    release_year = serializers.SerializerMethodField()

    class Meta:
        model = MovieMetaModel
        fields = '__all__'

    # Trim the title field down to 30 chars at the max
    def get_title_short(self, obj):
        if len(obj.title) <= SHORT_TITLE_MAX_LEN:
            return obj.title

        return obj.title[:SHORT_TITLE_MAX_LEN:] + "..."

    # Extract just the year from the release date
    def get_release_year(self, obj):
        return obj.releaseDate.year

    # Convert a number like 1000 to $1,000
    def get_gross_clean(self, obj):
        return "$" + "{:,}".format(obj.gross)


class TestResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResultsModel
        fields = '__all__'