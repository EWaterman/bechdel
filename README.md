# Bechdel Tester (Unofficial)

Created by Evan Waterman

WebApp that shows whether or not a movie passes the [Bechdel Test](https://en.wikipedia.org/wiki/Bechdel_test). Mainly a movie passes iff:

1. It has at least two named women in it
2. Who talk to each other
3. About something besides a man

Initially cloned from the [Django React Boilerplate](https://github.com/vintasoftware/django-react-boilerplate) which was developed by [Vinta Software](https://www.vinta.com.br/). All the react stuff is removed though...


### Deploys

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

### Populating the data
I've added a management script to populate movie metadata from CSV files.

1. cd to backend\
2. python .\manage.py populator --year 2021


### TODO:
- if I ever add users in, will need this: https://github.com/mobolic/django-session-cleanup (need to install celery again so look up what I removed in the commit after this one https://github.com/EWaterman/bechdel/commit/e86050f20b5e4358f4b1225eb361d656f392d0f3)
- support SCSS https://www.accordbox.com/blog/how-use-scss-sass-your-django-project-python-way/
- github build failed: https://github.com/EWaterman/bechdel/runs/6541176038?check_suite_focus=true#step:12:40   see .github/workflows/main.yml
- get a postgresql dbdump from my local that I can upload straight to prod (and for prod backups).


### Future Considerations:
- add a "rating" field (G, PG...)
- pull IMDB/Rotten Tomato metadata for ratings, posters, and stuff
- Support limiting the graphs (ie fetch top 10, 100, all movies of each year...)
-- To do this it'd be better to fetch all the data ordered by gross, then loop through, grouping it manually after. That way we only have 1 trip to the db.
- Make this cards on the front page take in a count and page number so we can infinite scroll through the carousel.
- Make the by genre chart also group by year so we can see how it trends over time. Can stack each year's % passing for each genre on top of each other to get total % passing for all genres. https://www.chartjs.org/docs/latest/charts/bar.html#stacked-bar-chart


### Things I did to make it work:

Makefile
27: export PIP_REQUIRE_VIRTUALENV=true; \ -> changed to "set" because that's what windows supports

webpack.base.config.js
37: loader: ['file-loader?name=i-[hash].[ext]'], -> removed the wrapping square brackets as per: https://github.com/webpack/webpack/issues/11418. Also changed to "use:" based on: https://stackoverflow.com/questions/68356793/error-compiling-ruleset-failed-query-arguments-on-loader-has-been-removed-in

server.js
8: publicPath: config.output.publicPath, -> removed cause I think was removed? Usage instructions here: https://webpack.js.org/guides/public-path/
11: inline: true, -> removed because no longer supported as per: https://stackoverflow.com/questions/69359982/update-webpack-4-to-webpack-5-get-error-options-has-an-unknown-property-inline
17: listen -> swapped to startCallback for v4
^ migration instructions for webpack https://github.com/webpack/webpack-dev-server/blob/master/migration-v4.md

updated everything in "dependencies" block of package.json to latest versions. Also changed "node-sass" to "sass" because it was giving issues and is deprecated.
