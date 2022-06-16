from django.urls import path

from . import views

app_name = 'movies'
urlpatterns = [
    # path('by-title/', views.MovieDetailsByTitleView.as_view(), name='movie_list'),
    path('by-title/', views.movies_min_by_title_view, name='movies_min_by_title'), # TODO: hide this view publicly so don't gotta support non ajax. Maybe do in the view??
]