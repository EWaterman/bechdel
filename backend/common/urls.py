from django.urls import path

from . import views

# The urls of the actual web pages themselves.
app_name = 'common'
urlpatterns = [
    path('', views.HomepageView.as_view(), name='home'),
    path('search/', views.AdvancedSearchView.as_view(), name='search')
]