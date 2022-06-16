import React from 'react';
import { render } from 'react-dom';

import '../sass/style.scss';

import App from './App';

// The outermost wrapper on the entire React application. A page can ultimately
// only render a single component (ie div) so we need to have this one surround
// all content that contains React components. This way child components can be invoked
// from within App.js but it also means we need to nest lots of html inside it.
// render(
//   <React.StrictMode>
//     <App />
//   </React.StrictMode>,
//   document.getElementById('react-app')
// );
