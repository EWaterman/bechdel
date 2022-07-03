from django.views.generic import TemplateView
from movies.views import movie_details, movies_card_by_date_view, results_by_year, results_by_genre, MovieDetailsByComplexView
from movies.forms import MovieComplexSearchForm

# Views for loading individual web pages
class HomepageView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        context['movie_cards'] = movies_card_by_date_view()
        context['results_by_year'] = results_by_year()
        context['results_by_genre'] = results_by_genre()
        return context


class AdvancedSearchView(TemplateView):
    template_name = 'pages/adv_search.html'

    def get_context_data(self, **kwargs):
        context = super(AdvancedSearchView, self).get_context_data(**kwargs)
        context['movies'] = MovieDetailsByComplexView.as_view()(self.request).rendered_content
        context['form'] = MovieComplexSearchForm(self.request.GET)
        return context


class MovieDetailsView(TemplateView):
    template_name = 'pages/movie_details.html'

    def get_context_data(self, **kwargs):
        movieId = kwargs.get('movie_id')
        context = super(MovieDetailsView, self).get_context_data(**kwargs)
        context['movie_details'] = movie_details(movieId)
        return context