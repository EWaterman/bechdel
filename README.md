# Bechdel Tester (Unofficial)

Created by Evan Waterman

WebApp that shows whether or not a movie passes the [Bechdel Test](https://en.wikipedia.org/wiki/Bechdel_test). Mainly a movie passes iff:

1. It has at least two named women in it
2. Who talk to each other
3. About something besides a man

Initially cloned from the [Django React Boilerplate](https://github.com/vintasoftware/django-react-boilerplate) which was developed by [Vinta Software](https://www.vinta.com.br/).


### TODO:
- if I ever add users in, will need this: https://github.com/mobolic/django-session-cleanup (need to install celery again so look up what I removed in the commit after this one https://github.com/EWaterman/bechdel/commit/e86050f20b5e4358f4b1225eb361d656f392d0f3)


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
