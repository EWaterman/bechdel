from django.urls import path

from . import views

# The template views for making internal calls. Should not be public.
# Methods should only be added here if they specifically need to be invoked
# via REST API from within a page. If you just need to make the one call on page load,
# have the template view call the method directly and add it to its context data.
app_name = 'movies'
urlpatterns = [
    path('by-title/', views.movies_min_by_title_view, name='movies_min_by_title_api'),
]