from django.views import generic

from movies.views import movie_details, movies_card_by_date_view, results_by_year, results_by_genre, MovieDetailsByComplexView

# Views for loading individual web pages
class HomepageView(generic.TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        context['movie_cards'] = movies_card_by_date_view()
        context['results_by_year'] = results_by_year()
        context['results_by_genre'] = results_by_genre()
        return context


class AdvancedSearchView(generic.TemplateView):
    template_name = 'pages/adv_search.html'

    def get_context_data(self, **kwargs):
        context = super(AdvancedSearchView, self).get_context_data(**kwargs)
        context['movies'] = MovieDetailsByComplexView.get_queryset(self)
        return context


class MovieDetailsView(generic.TemplateView):
    template_name = 'pages/movie_details.html'

    def get_context_data(self, **kwargs):
        movieId = kwargs.get('movie_id')
        context = super(MovieDetailsView, self).get_context_data(**kwargs)
        context['movie_details'] = movie_details(movieId)
        return context