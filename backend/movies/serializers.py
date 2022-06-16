from rest_framework import serializers
from .models import MovieMetaModel, TestResultsModel

# Handles conversion between json and python models
class MovieDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieMetaModel
        fields = ('id', 'title', 'releaseDate', 'genre', 'gross', 'image', 'bechdelResult','created', 'modified')

class TestResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResultsModel
        fields = ('id', 'movieId', 'bRule1Result', 'bRule2Result', 'bRule3Result', 'notes', 'created', 'modified')