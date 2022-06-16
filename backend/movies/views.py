from django.views.generic import ListView
from django.template.loader import render_to_string
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.pagination import PageNumberPagination

from .models import MovieMetaModel
from .serializers import MovieDetailsSerializer
# from .filters import MovieFilter

DEFAULT_PAGE_SIZE = 50
FIRST_PAGE = 1

# Operations on movie metadata. Non-reads require admin access.
class MovieDetailsViewSet(viewsets.ModelViewSet):
    queryset = MovieMetaModel.objects.all()
    serializer_class = MovieDetailsSerializer
    # pagination_class = PageNumberPagination
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    # Paginates querysets
    # https://www.django-rest-framework.org/api-guide/pagination/
    # https://www.cdrf.co/3.12/rest_framework.pagination/PageNumberPagination.html
    def getPaginatedQuerySet(self, queryset):
        # Try to paginate. Will use the 'page' query param automatically.
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        # And if pagination is disabled or page isn't provided just return everything.
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    # Fetch paginated movie details by year, ordered by top grossing.
    @action(detail=False)
    def get_by_year(self, request, year=None):
        page = request.query_params.get('page')

        # If year is provided, filter by year.
        if year is not None:
            queryset = MovieMetaModel.objects.filter(releaseDate__year=year)
        else:
            queryset = MovieMetaModel.objects.all()

        #return self.getPaginatedQuery(queryset, page, count)
        return self.getPaginatedQuerySet(queryset, page)


# Fetch a list of movie metadata by multiple search criteria.
# Used in the avanced search page.
#TODO: add additional search criteria (genre, year, does it pass....)
class MovieDetailsByFilterView(ListView):
    model = MovieMetaModel
    serializer_class = MovieDetailsSerializer
    pagination_class = PageNumberPagination
    template_name = 'common/movies/movie_list.html'

    def get_queryset(self):
        # Title is a query param so we can avoid caching the result (because it's highly variable)
        title = self.request.GET.get('title', "")

        # If no filter is provided, return everything
        if not title:
            return MovieMetaModel.objects.all()

        # Otherwise do a regex search on the movies so the user doesn't need to provide an exact match.
        return MovieMetaModel.objects.filter(title__icontains=title)

# Fetch a list of movie metadata by movie title. Used in the navbar search.
# Only returns partial data and uses AJAX to speed up the query.
#TODO: only select the needed fields
#TODO: only select top 5 entries
def movies_min_by_title_view(request):
    title = request.GET.get('title', "")  # Title is a query param so we can avoid caching the result (because it's highly variable)

    movies = MovieMetaModel.objects.filter(title__icontains=title)

    html = render_to_string(
        template_name="common/movies/movie_list_min_results.html", context={"movies_min_by_title": movies}
    )
    return JsonResponse(data={"html_from_view": html}, safe=False)



# TODO: Grouping Operations on movie metadata
# Get top X grouped by year, count that pass, fail, total, percentage (provide all these so front end doesn't need to compute)
# Get top X grouped by genre, ""
# http://prepbootstrap.com/bootstrap-template/bootstrap-bar-chart

        # # Then grab the top X entries.
        # count = request.query_params.get('count', DEFAULT_PAGE_SIZE)