from .views import MovieDetailsViewSet

routes = [
    {'regex': r'movies', 'viewset': MovieDetailsViewSet, 'basename': 'movies'},
]
