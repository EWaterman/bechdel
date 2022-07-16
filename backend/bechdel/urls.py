from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.urls import path
from django.contrib import admin

import django_js_reverse.views
from rest_framework.routers import DefaultRouter

from movies.routes import routes as movies_routes

router = DefaultRouter()

# Register all the routes from each of our apps (aka folders). They'll be nested under /api/
routes = movies_routes
for route in routes:
    router.register(route['regex'], route['viewset'], basename=route['basename'])

# Note that the 'name' attribute is how we'll reference the views in our html for linking internally.
urlpatterns = [
    # Add the common app, which houses the pages themselves.
    path("", include("common.urls"), name="common"),

    # Adds all the standard django admin urls and pages (such as login)
    path("admin/", admin.site.urls, name="admin"),

    # This maps all urls on the site by their "name" attribute so we don't need to hardcode the urls themselves
    # everywhere. Can access urls in js via Urls.<name>() (https://django-js-reverse.readthedocs.io/en/latest/)
    path("jsreverse/", django_js_reverse.views.urls_js, name="js_reverse"),

    # Dev endpoints for all my model views. The router ones come for free with Django rest framework.
    # These should ideally be hidden from the public in production (and the Django ones are) but
    # my apis are get only so it's fine.
    path("api/", include(router.urls), name="api"),
    path("api/custom/movies/", include("movies.urls"), name="movies"),
]

# Needed to manually serve media files (files under "mediafiles" folder) during local testing.
# Static files (which will be under "staticfiles" in prod) are handled automatically.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
