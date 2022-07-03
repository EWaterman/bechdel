import datetime
from django import forms

from .enums import GENRES, MOVIE_ORDERING, TEST_RESULT

def current_year():
    return datetime.date.today().year

def year_choices():
    # Initial year is 2012 because we don't have data from before then (yet)
    return [(r,r) for r in reversed(range(2012, current_year() + 1))] + [(None, "N/A")]


class MovieComplexSearchForm(forms.Form):
    title = forms.CharField(
        label='Movie Title',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search for a movie', 'type':'search'}))
    year = forms.MultipleChoiceField(
        label='Year Released',
        choices=year_choices,
        widget=forms.Select,
        initial=None,
        required=False)
    genre = forms.MultipleChoiceField(
        label='Genre',
        choices=[(x, y) for x, y in GENRES.items()],
        initial=None,
        widget=forms.Select,
        required=False)
    bResult = forms.MultipleChoiceField(
        label='Passes Bechdel Test?',
        choices=[(x, y) for x, y in TEST_RESULT.items()],
        initial=None,
        widget=forms.Select,
        required=False)
    order = forms.MultipleChoiceField(
        label='Order By',
        choices=[(x, y) for x, y in MOVIE_ORDERING.items()],
        initial='title',
        widget=forms.Select,
        required=False)
    ascending = forms.BooleanField(
        label='Sort By Ascending',
        required=False)