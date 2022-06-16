from django.views import generic

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

# Views for loading individual web pages
class HomepageView(generic.TemplateView):
    template_name = 'pages/home.html'

class AdvancedSearchView(generic.TemplateView):
    template_name = 'pages/adv_search.html'

class MovieDetailsView(generic.TemplateView):
    template_name = 'pages/movie_details.html'

# TODO: remove this
class RestViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'], permission_classes=[AllowAny], url_path='rest-check',)
    def rest_check(self, request):
        return Response(
            {"result": "If you're seeing this, the REST API is working!"},
            status=status.HTTP_200_OK,
        )