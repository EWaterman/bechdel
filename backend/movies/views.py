from operator import ge
from django.db.models import Count, Case, When
from django.db.models.functions import ExtractYear
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView
from django.template.loader import render_to_string
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.pagination import PageNumberPagination

from .models import MovieMetaModel, TestResultsModel
from .serializers import MovieDetailsSerializer, TestResultsSerializer
from .enums import GENRES_INV, TEST_RESULT

NAVBAR_SEARCH_LIMIT = 5
HOMEPAGE_SEARCH_LIMIT = 20
SEARCH_NUM_MOVIES_PER_PAGE = 10
SUPPORTED_ORDERING_FIELDS = {"title", "releaseDate", "gross"}
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
# TODO: Serialize genre correctly. https://micropyramid.com/blog/customizing-django-rest-api-serializers/
# RN this isn't even acting as a ListView (hence the commented out fields). We just call get_queryset directly.
# Need to find a way to call this ListView from the AdvancedSearchView TemplateView directly so it invokes stuff like pagination
# and serialization and filling out the template (rn it's backwards where we pass the data to a context that calls movie_list_wrapper
# which is actually fine I guess, just would likely be easier if this was automatic but likely we'll need to do it manually....).
# 
# https://stackoverflow.com/questions/57166495/include-class-based-listview-as-a-template-snippet-in-a-templateview
# https://www.agiliq.com/blog/2017/12/when-and-how-use-django-listview/
class MovieDetailsByComplexView(ListView):
    # serializer_class = MovieDetailsSerializer
    # paginate_by = SEARCH_NUM_MOVIES_PER_PAGE
    # context_object_name = 'movies'
    # template_name = 'view_wrappers/movie_list_wrapper.html'

    def get_queryset(self):
        # All the search criteria is query params so we can avoid caching the result (because it's highly variable)
        titleQ = self.request.GET.get('title')
        genreQ = self.request.GET.get('genre')
        yearQ = self.request.GET.get('year')
        bechdelResultQ = self.request.GET.get('bResult')
        orderByQ = self.request.GET.get('order', "releaseDate")
        ascendingQ = self.request.GET.get('ascending')

        # Sanitize the inputs
        title = titleQ if titleQ is not None and len(titleQ) > 0 else None
        genre = GENRES_INV.get(genreQ)
        year = yearQ if yearQ is not None and len(yearQ) > 0 else None
        bechdelResult = TEST_RESULT.get(bechdelResultQ)
        orderBy = orderByQ if orderByQ in SUPPORTED_ORDERING_FIELDS else "releaseDate"

        # Filter the results
        movies = MovieMetaModel.objects.all()
        if title is not None:
            movies = movies.filter(title__icontains=title)
        if genre is not None:
            movies = movies.filter(genre=genre)
        if year is not None:
            movies = movies.filter(releaseDate__year=year)
        if bechdelResult is not None:
            movies = movies.filter(bechdelResult=bechdelResult)

        # Order the results
        ascending = "" if ascendingQ is not None else "-"  # Checkbox params are only provided (to "on") if checked.
        return movies.order_by(ascending + orderBy)


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
# TODO: make this take in a count and page number so we can fetch more dynamically.
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


# For graphing data. Fetches all results, grouped by year released.
# TODO: Support limiting (ie fetch top 10, 100, all movies of each year...).
# To do this it'd be better to fetch all the data ordered by gross, then loop through, grouping it manually after. That way we only have 1 trip to the db.
def results_by_year(count=DEFAULT_GRAPH_DATA_COUNT):
    results = (MovieMetaModel.objects
        .annotate(year=ExtractYear('releaseDate'))  # Wrap each row with a new 'year' field
        .values('year')  # Group by the new year field
        .annotate(
            total=Count('id'),  # Id is unique so will count the total rows matching the grouping
            bechPass=Count(Case(When(bechdelResult=True, then=1)))))  # Will count all the rows that pass

    return render_to_string(
        template_name="view_wrappers/movie_results_by_year_wrapper.html",
        context={"results": results}
    )


# For graphing data. Fetches all results, grouped by genre released.
# TODO: Support limiting (ie fetch top 10, 100, all movies of each year...).
# To do this it'd be better to fetch all the data ordered by gross, then loop through, grouping it manually after. That way we only have 1 trip to the db.
# TODO: also group this by year so we can see how it trends over time. Can stack each year's % passing for each genre on top of each other to get total % passing for all genres.
def results_by_genre(count=DEFAULT_GRAPH_DATA_COUNT):
    results =  (MovieMetaModel.objects
        .values('genre')  # Group by genre
        .annotate(
            total=Count('id'),  # Id is unique so will count the total rows matching the grouping
            bechPass=Count(Case(When(bechdelResult=True, then=1)))))  # Will count all the rows that pass
    
    return render_to_string(
        template_name="view_wrappers/movie_results_by_genre_wrapper.html",
        context={"results": results}
    )