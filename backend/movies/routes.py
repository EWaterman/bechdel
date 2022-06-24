from .views import MovieDetailsViewSet, TestResultsViewSet

routes = [
    {'regex': r'movies', 'viewset': MovieDetailsViewSet, 'basename': 'movies'},
    {'regex': r'results', 'viewset': TestResultsViewSet, 'basename': 'results'},
]
