from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.urls import path
from django.contrib import admin

import django_js_reverse.views
from rest_framework.routers import DefaultRouter

from common.routes import routes as common_routes
from movies.routes import routes as movies_routes

router = DefaultRouter()

# Register all the routes from each of our apps (aka folders). They'll be nested under /api/
routes = common_routes + movies_routes
for route in routes:
    router.register(route['regex'], route['viewset'], basename=route['basename'])

# Note that the 'name' attribute is how we'll reference the views in our html for linking internally.
urlpatterns = [
    # Adds all urls in each of our apps (aka folders).
    path("", include("common.urls"), name="common"),
    path("movies/", include("movies.urls"), name="movies"),

    # Adds all the standard django admin urls and pages (such as login)
    path("admin/", admin.site.urls, name="admin"),

    # This maps all urls on the site by their "name" attribute so we don't need to hardcode the urls themselves
    # everywhere. Can simply access in js via Urls.<name>() (https://django-js-reverse.readthedocs.io/en/latest/)
    path("jsreverse/", django_js_reverse.views.urls_js, name="js_reverse"),

    # Dev endpoints for all my model views. Comes for free with Django. Will all be nested under/api (ex: /api/movies/).
    # TODO: Hide these from the public in prod. Maybe it happens automatically idk.
    path("api/", include(router.urls), name="api"),

    # My custom internal APIs to be called from React components. Under /api so they can be hidden from the frontend users.
    # path("api/movies/", include("movies.urls"), name="movies-api"),
]

# Needed to serve media files (files under "mediafiles" folder) during local testing. Prod uses gunicorn(?)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
