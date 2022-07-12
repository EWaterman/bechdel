from django.urls import path

from . import views

# The urls of the actual web pages themselves.
app_name = 'common'
urlpatterns = [
    path('', views.HomepageView.as_view(), name='home'),
    path('search/', views.AdvancedSearchPageView.as_view(), name='search'),
    path('info/', views.MoreInfoPageView.as_view(), name='info'),
    path('movies/<int:movie_id>/', views.MovieDetailsPageView.as_view(), name='movie-details')
]