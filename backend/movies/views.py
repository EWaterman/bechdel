from django.db.models import Count, Case, When
from django.db.models.functions import ExtractYear
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView
from django.template.loader import render_to_string
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from .models import MovieMetaModel, TestResultsModel
from .serializers import MovieDetailsSerializer, TestResultsSerializer
from .enums import GENRES, TEST_RESULT, MOVIE_ORDERING

NAVBAR_SEARCH_LIMIT = 5
HOMEPAGE_SEARCH_LIMIT = 20
SEARCH_NUM_MOVIES_PER_PAGE = 12
DEFAULT_GRAPH_DATA_COUNT = 100

# Operations on movie metadata. Non-reads require admin access.
class MovieDetailsViewSet(viewsets.ModelViewSet):
    queryset = MovieMetaModel.objects.all()
    serializer_class = MovieDetailsSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


# Operations on test results. Non-reads require admin access.
class TestResultsViewSet(viewsets.ModelViewSet):
    queryset = TestResultsModel.objects.all()
    serializer_class = TestResultsSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


# Fetch a list of movie metadata filtered by multiple fields.
# Used in the advanced search page.
class MovieDetailsByComplexView(ListView):
    model = MovieMetaModel
    paginate_by = SEARCH_NUM_MOVIES_PER_PAGE
    context_object_name = 'movies'
    template_name = 'view_wrappers/movie_list_wrapper.html'

    def get_queryset(self, *args, **kwargs):
        # All the search criteria is query params so we can avoid caching the result (because it's highly variable)
        titleQ = self.request.GET.get('title')
        genreQ = self.request.GET.get('genre')
        yearQ = self.request.GET.get('year')
        bechdelResultQ = self.request.GET.get('bResult')
        orderByQ = self.request.GET.get('order', "title")
        ascendingQ = self.request.GET.get('ascending')

        # Sanitize the inputs
        title = titleQ if titleQ is not None and len(titleQ) > 0 else None
        genre = genreQ if genreQ in GENRES.keys() else None
        year = yearQ if yearQ is not None and len(yearQ) > 0 else None
        bechdelResult = bechdelResultQ if bechdelResultQ in TEST_RESULT.keys() else None
        orderBy = orderByQ if orderByQ in orderByQ in MOVIE_ORDERING.keys() else "title"

        movies = super(MovieDetailsByComplexView, self).get_queryset(*args, **kwargs)

        # Filter the results
        if title is not None:
            movies = movies.filter(title__icontains=title)
        if genre is not None:
            movies = movies.filter(genre=genre)
        if year is not None:
            movies = movies.filter(releaseDate__year=year)
        if bechdelResult is not None:
            movies = movies.filter(bechdelResult=bechdelResult)

        # Order the results and return (don't bother serializing cause there's no real field translation)
        ascending = "" if ascendingQ is not None else "-"  # Checkbox params are only provided (to "on") if checked.
        return (movies
            .annotate(releaseYear=ExtractYear('releaseDate'))  # Wrap each row with a new 'releaseYear' field
            .order_by(ascending + orderBy))


# Fetch a list of movie metadata by movie title. Used in the navbar search.
# Only returns partial data and uses AJAX to speed up the query.
def movies_min_by_title_view(request):
    # Title is a query param so we can avoid caching the result (because it's highly variable)
    title = request.GET.get('title', "")

    # Only select the top 5 matching entries since we don't want to overflow the display
    movies = (MovieMetaModel.objects
        .filter(title__icontains=title)[:NAVBAR_SEARCH_LIMIT]
        .annotate(releaseYear=ExtractYear('releaseDate'))  # Wrap each row with a new 'releaseYear' field
        .values('id', 'title', 'releaseYear', 'image'))

    html = render_to_string(
        template_name="view_wrappers/movie_list_min_wrapper.html",
        context={
            "movies_min_by_title": movies,
            "title": title
        }
    )
    return JsonResponse(data={"html_from_view": html}, safe=False)


# Fetches the metadata of the 20 most recently released movies.
# Used on the homepage. Only returns partial data.
def movies_card_by_date_view():
    movies = (MovieMetaModel.objects.all()
        .order_by('releaseDate')[:HOMEPAGE_SEARCH_LIMIT]
        .values('id', 'title', 'image', 'bechdelResult'))

    return render_to_string(
        template_name="view_wrappers/movie_list_card_wrapper.html",
        context={"movie_cards": movies}
    )


# Fetch all the metadata and test data for a given movie id.
def movie_details(movieIdParam):
    # This is a get by PK (so we expect an entry) but handle the error case gracefully.
    try:
        movie = MovieDetailsSerializer(MovieMetaModel.objects.get(id=movieIdParam)).data
    except ObjectDoesNotExist:
        movie = None
        
    try:
        testResult = TestResultsSerializer(TestResultsModel.objects.get(movieId=movieIdParam)).data
    except ObjectDoesNotExist:
        testResult = None

    return render_to_string(
        template_name="view_wrappers/movie_details_wrapper.html",
        context={
            "movie_meta": movie,
            "test_results": testResult,
        }
    )

def getGraphData(results, xLabel):
    # To build the graphs, we need two lists: year on the X axis and % passed on the Y axis.
    xData = []
    percPassData = []
    for result in results:
        xData.append(result.get(xLabel))

        # Make sure a year actually has movies to avoid divide by zero errors.
        numMovies = result.get('total')
        if numMovies is None or numMovies == 0:
            percPassData.append(0)
        else:
            percPassData.append(round(100 * result.get('bechPass') / result.get('total')))
    
    return xData, percPassData

# For graphing data. Fetches all results, grouped by year released.
def results_by_year(count=DEFAULT_GRAPH_DATA_COUNT):
    resultsByYear = (MovieMetaModel.objects
        .filter(bechdelResult__isnull=False)  # Ignore rows that don't have any test result data as they'll skew the results
        .annotate(year=ExtractYear('releaseDate'))  # Wrap each row with a new 'year' field
        .values('year')  # Group by the new year field
        .annotate(
            total=Count('id'),  # Id is unique so will count the total rows matching the grouping
            bechPass=Count(Case(When(bechdelResult=True, then=1))))  # Will count all the rows that pass
        .order_by('year'))

    yearsData, percPassData = getGraphData(resultsByYear, 'year')

    return render_to_string(
        template_name="view_wrappers/movie_results_by_year_wrapper.html",
        context={
            "results": {
                'x': yearsData,
                'y': percPassData
            }
        }
    )


# For graphing data. Fetches all results, grouped by genre.
def results_by_genre(count=DEFAULT_GRAPH_DATA_COUNT):
    resultsByGenre = (MovieMetaModel.objects
        .filter(bechdelResult__isnull=False)  # Ignore rows that don't have any test result data as they'll skew the results
        .values('genre')  # Group by genre
        .annotate(
            total=Count('id'),  # Id is unique so will count the total rows matching the grouping
            bechPass=Count(Case(When(bechdelResult=True, then=1))))  # Will count all the rows that pass
        .order_by('genre'))
    
    genreData, percPassData = getGraphData(resultsByGenre, 'genre')

    # Convert the genre ints to their Strigified names. There's prob a better way to do this using serializers but this works for now.
    genreData = [GENRES.get(genre) for genre in genreData]

    return render_to_string(
        template_name="view_wrappers/movie_results_by_genre_wrapper.html",
        context={
            "results": {
                'x': genreData,
                'y': percPassData
            }
        }
    )