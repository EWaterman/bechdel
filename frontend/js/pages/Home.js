// import React, { useState, useEffect } from 'react';
// import Button from 'react-bootstrap/Button';
// import { useDispatch, useSelector } from 'react-redux';

// import { creators } from '../store/rest_check';

// /**
//  * Homepage content aka the landing page.
//  * TODO: I'm guessing calling dispatch() is what actually calls the API (see fetchRestCheck())
//  * so I just need to add a few more of those for each component I want to add...
//  * How do I make it only reload that section though? I wanna add multiple
//  */
// const Home = () => {
//   const dispatch = useDispatch();
//   const restCheck = useSelector((state) => state.restCheck);
//   useEffect(() => {
//     const action = creators.fetchRestCheck();
//     dispatch(action);
//   }, [dispatch]);

//   const [showBugComponent, setShowBugComponent] = useState(false);

//   return (
//     <>
//       {/* "creators.fetchRestCheck()" in rest_check.js is an action to fetch the result of
//       GET /api/rest/rest-check/. Somehow that gets put in the "state" which we grab out
//       into its own var that we can access here. */}
//       <div>{restCheck.result}</div>

//       <Button variant="outline-dark" onClick={() => setShowBugComponent(true)}>
//         Click to test if Sentry is capturing frontend errors! (Should only work in Production)
//       </Button>
//       {showBugComponent && showBugComponent.field.notexist}
//     </>
//   );
// };

// export default Home;
