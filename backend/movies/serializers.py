from rest_framework import serializers
from .models import MovieMetaModel, TestResultsModel
from .enums import GENRES, GENRES_INV

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

    class Meta:
        model = MovieMetaModel
        fields = '__all__'

class TestResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResultsModel
        fields = '__all__'