import React from 'react';

// The searchbar itself. This will be embedded in the header.
// Results are loaded dynamically via React but if the search is submitted
// (ie they press Enter) then it takes the user to the search results page.
// Source: https://www.emgoto.com/react-search-bar/
// TODO: make the form "action" link to /search/
const SearchBar = ({ searchQuery, setSearchQuery }) => {
  return (
    <form action="/" method="get">
      <label htmlFor="movie-navbar-search">
        {/* Added for accessibility. Readers will still read this but it'll be invisible. */}
        <span className="visually-hidden">Search movie titles</span>
      </label>
      <input
        value={searchQuery}
        onInput={(e) => setSearchQuery(e.target.value)}
        type="text"
        id="movie-navbar-search"
        placeholder="Search movie titles"
        name="title"
      />
    </form>
  );
};

export default SearchBar;
