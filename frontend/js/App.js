import React, { useState } from 'react';

import Search from './search/Search';
import { getRestCall } from './common/rest_call';

// TODO: Move this logic to the search.js file
// Consider going the router approach to support multiple pages.
// https://stackoverflow.com/questions/41956465/how-to-create-multiple-page-app-using-react
// https://www.youtube.com/watch?v=H9rHrlNTpq8&list=PLzMcBGfZo4-kCLWnGmK0jUBmGLaJxvi4j&index=7
// We can link to different inner wrapper apps for each page? Kinda shitty to have to do this but seems to be how it's implemented

// TODO: remove this and actually access the real data.

// const moviesOld = [
//   { id: '1', title: 'This first post is about React' },
//   { id: '2', title: 'This next post is about Preact' },
//   { id: '3', title: 'We have yet another React post!' },
//   { id: '4', title: 'This is the fourth and final post' },
// ];

const advancedSearch = { id: '9', title: 'Advanced Search' };

// Filters the list of movies down to those that match the given string, hiding all others.
const filterMovies = async (movies, query) => {
  // If the user hasn't typed anything yet, hide all results.
  if (!query) {
    return [];
  }

  // Otherwise filter down to just the top 5 matching results
  // TODO: limit to 5 results https://stackoverflow.com/questions/56168771/how-to-limit-for-10-results-the-array-filter
  // TODO: add link to each movie
  const filteredMovies = await movies.filter((movie) => {
    return movie.title.toLowerCase().includes(query);
  });

  // Add a link the advanced search page.
  // TODO: add actual link
  filteredMovies.push(advancedSearch);

  return filteredMovies;
};

// Fetches the unfiltered movie list from the DB. This makes it so we can apply the filtering on
// the front end w/o re-issuing the query. This may not be performant at scale though if we have 1000+
// movies so may need to swap it to calling the get by title API (with limit 5).
// TODO: change the API so that it only returns the needed info (title, year, poster (ico version))
const App = () => {
  const { search } = window.location;
  const query = new URLSearchParams(search).get('s');
  const [searchQuery, setSearchQuery] = useState(query || '');

  const movies = getRestCall('api/movies/');
  console.log('movies');
  console.log(movies);
  const filteredMovies = filterMovies(movies, searchQuery);
  console.log('filteredMovies');
  console.log(filteredMovies);

  // TODO: instead of adding the "advancedSearch" item if filteredMovies.length != 0, then add it here.
  return (
    <div className="App">
      <Search searchQuery={searchQuery} setSearchQuery={setSearchQuery} />
      <ul>
        {filteredMovies.map((movie) => (
          <li key={movie.id}>{movie.title}</li>
        ))}
      </ul>
    </div>
  );
};

export default App;
