import React, { Component } from 'react';
import { render } from 'react-dom';

// The searchbar in the navbar.
// Results are loaded dynamically via React but if the search is submitted
// (ie they press Enter) then it takes the user to the search results page.
// Source: https://www.emgoto.com/react-search-bar/
// TODO: make the form "action" link to /search/
export default class SearchBar extends Component {
  constructor(props) {
    super(props);
  }

  render() {
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
    </form>;
  }
}

render(<SearchBar />, document.getElementById('searchbar'));
