import React, { useState } from 'react';

// Fetches the unfiltered movie list from the DB. This makes it so we can apply the filtering on
// the front end w/o re-issuing the query. This may not be performant at scale though if we have 1000+
// movies so may need to swap it to calling the get by title API (with limit 5).
// TODO: change the API so that it only returns the needed info (title, year, poster (ico version))
const App = () => {
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
