from django_filters import FilterSet, CharFilter

from .models import MovieMetaModel

# https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html

# Filters datasets down by search criteria. Used by views.
# class MovieFilter(FilterSet):
#     title = CharFilter(lookup_expr='icontains')
#     class Meta:
#         model = MovieMetaModel
#         fields = ('id', 'title', 'releaseDate', 'genre', 'gross', 'image', 'bechdelResult','created', 'modified')